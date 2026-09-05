import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from app.routes.auth import login_required
from app.models import ChatThread, Message, User, Offer, Order, Delivery
from app.extensions import db
from app.services.notification_service import NotificationService

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
@login_required
def chat_list():
    user = g.user
    if user.role == 'farmer':
        threads = ChatThread.query.filter_by(farmer_id=user.id).order_by(ChatThread.last_message_at.desc()).all()
    else:
        threads = ChatThread.query.filter_by(buyer_id=user.id).order_by(ChatThread.last_message_at.desc()).all()
    return render_template('chat/chat_list.html', threads=threads, user=user)


@chat_bp.route('/start/<int:target_user_id>')
@login_required
def start_chat(target_user_id):
    user = g.user
    target = User.query.get_or_404(target_user_id)
    
    farmer_id = user.id if user.role == 'farmer' else target.id
    buyer_id = user.id if user.role == 'buyer' else target.id

    order_id = request.args.get('order_id', type=int)
    offer_id = request.args.get('offer_id', type=int)

    thread = ChatThread.query.filter_by(farmer_id=farmer_id, buyer_id=buyer_id).first()
    if not thread:
        thread = ChatThread(
            farmer_id=farmer_id,
            buyer_id=buyer_id,
            order_id=order_id,
            offer_id=offer_id,
            subject_product="Agricultural Produce Trading"
        )
        db.session.add(thread)
        db.session.flush()
        
        # Initial greeting message
        msg = Message(
            thread_id=thread.id,
            sender_id=user.id,
            message_text=f"Hello {target.name}, I am reaching out regarding agricultural trade on Krishi Kendra.",
            message_type='text'
        )
        db.session.add(msg)
        db.session.commit()
    elif order_id:
        thread.order_id = order_id
        db.session.commit()

    return redirect(url_for('chat.view_thread', thread_id=thread.id))


@chat_bp.route('/thread/<int:thread_id>')
@login_required
def view_thread(thread_id):
    user = g.user
    thread = ChatThread.query.get_or_404(thread_id)

    if user.id not in [thread.farmer_id, thread.buyer_id] and user.role != 'admin':
        flash('Unauthorized chat access.', 'danger')
        return redirect(url_for('main.index'))

    other_user = thread.buyer if user.id == thread.farmer_id else thread.farmer
    other_profile = other_user.buyer_profile if other_user.role == 'buyer' else other_user.farmer_profile
    my_profile = user.farmer_profile if user.role == 'farmer' else user.buyer_profile

    # Mark unread messages as read
    Message.query.filter_by(thread_id=thread.id).filter(Message.sender_id != user.id).update({'is_read': True})
    db.session.commit()

    messages = Message.query.filter_by(thread_id=thread.id).order_by(Message.created_at.asc()).all()
    
    # Active order / offer context if linked
    linked_order = db.session.get(Order, thread.order_id) if thread.order_id else None
    linked_offer = db.session.get(Offer, thread.offer_id) if thread.offer_id else None

    return render_template(
        'chat/thread.html',
        thread=thread,
        messages=messages,
        other_user=other_user,
        other_profile=other_profile,
        my_profile=my_profile,
        linked_order=linked_order,
        linked_offer=linked_offer,
        user=user
    )


import os
import time
from flask import current_app
from werkzeug.utils import secure_filename

@chat_bp.route('/thread/<int:thread_id>/send', methods=['POST'])
@login_required
def send_message(thread_id):
    user = g.user
    thread = ChatThread.query.get_or_404(thread_id)

    if user.id not in [thread.farmer_id, thread.buyer_id]:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    text = request.form.get('message_text', '').strip()
    msg_type = request.form.get('message_type', 'text')
    metadata_json = request.form.get('metadata_json', '{}')

    if not text and msg_type == 'text':
        return jsonify({'success': False, 'error': 'Empty message'}), 400

    msg = Message(
        thread_id=thread.id,
        sender_id=user.id,
        message_text=text,
        message_type=msg_type,
        metadata_json=metadata_json
    )
    thread.last_message_at = datetime.utcnow()
    db.session.add(msg)
    
    recipient_id = thread.buyer_id if user.id == thread.farmer_id else thread.farmer_id
    NotificationService.send(
        user_id=recipient_id,
        title=f"New Message from {user.name}",
        message=text[:100],
        link_url=url_for('chat.view_thread', thread_id=thread.id)
    )
    db.session.commit()

    return jsonify({
        'success': True,
        'message': {
            'id': msg.id,
            'sender_id': msg.sender_id,
            'sender_name': user.name,
            'text': msg.message_text,
            'type': msg.message_type,
            'metadata': msg.get_metadata(),
            'created_at': msg.created_at.strftime('%I:%M %p')
        }
    })


@chat_bp.route('/thread/<int:thread_id>/send-voice', methods=['POST'])
@login_required
def send_voice_note(thread_id):
    user = g.user
    thread = ChatThread.query.get_or_404(thread_id)

    if user.id not in [thread.farmer_id, thread.buyer_id]:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    if 'audio' not in request.files:
        return jsonify({'success': False, 'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'success': False, 'error': 'Empty audio recording'}), 400

    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'voice_notes')
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"voice_{thread.id}_{user.id}_{int(time.time())}.webm"
    file_path = os.path.join(upload_dir, filename)
    audio_file.save(file_path)

    relative_url = f"/static/uploads/voice_notes/{filename}"
    duration = request.form.get('duration', '0:05')

    metadata = {
        'audio_url': relative_url,
        'duration': duration,
        'sender_name': user.name
    }

    msg = Message(
        thread_id=thread.id,
        sender_id=user.id,
        message_text="🎙️ Voice Note",
        message_type='voice_note',
        metadata_json=json.dumps(metadata)
    )
    thread.last_message_at = datetime.utcnow()
    db.session.add(msg)

    recipient_id = thread.buyer_id if user.id == thread.farmer_id else thread.farmer_id
    NotificationService.send(
        user_id=recipient_id,
        title=f"Voice Note from {user.name}",
        message=f"{user.name} sent a {duration} voice note.",
        link_url=url_for('chat.view_thread', thread_id=thread.id)
    )
    db.session.commit()

    return jsonify({
        'success': True,
        'message': {
            'id': msg.id,
            'sender_id': msg.sender_id,
            'sender_name': user.name,
            'text': msg.message_text,
            'type': msg.message_type,
            'metadata': metadata,
            'created_at': msg.created_at.strftime('%I:%M %p')
        }
    })


@chat_bp.route('/thread/<int:thread_id>/send-offer', methods=['POST'])
@login_required
def send_offer_card(thread_id):
    user = g.user
    thread = ChatThread.query.get_or_404(thread_id)

    if user.id not in [thread.farmer_id, thread.buyer_id]:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    product_name = request.form.get('product_name', 'Agricultural Produce').strip()
    price = float(request.form.get('price', 0))
    qty = float(request.form.get('quantity', 0))
    unit = request.form.get('unit', 'kg').strip()
    notes = request.form.get('notes', '').strip()

    if price <= 0 or qty <= 0:
        return jsonify({'success': False, 'error': 'Invalid price or quantity'}), 400

    total_amount = round(price * qty, 2)
    
    # Check if there is an existing offer linked or create new one
    offer = None
    if thread.offer_id:
        offer = db.session.get(Offer, thread.offer_id)

    if offer:
        offer.status = 'countered'
        offer.counter_price_per_unit = price
        offer.counter_quantity = qty
        offer.counter_notes = notes
        offer.last_action_by = user.role
        offer.total_amount = total_amount
    else:
        offer = Offer(
            buyer_id=thread.buyer_id,
            farmer_id=thread.farmer_id,
            product_name=product_name,
            quantity=qty,
            unit=unit,
            offered_price_per_unit=price,
            total_amount=total_amount,
            offered_by_role=user.role,
            status='countered' if user.role == 'farmer' else 'pending',
            last_action_by=user.role,
            notes=notes
        )
        db.session.add(offer)
        db.session.flush()
        thread.offer_id = offer.id

    metadata = {
        'offer_id': offer.id,
        'product_name': product_name,
        'price': price,
        'quantity': qty,
        'unit': unit,
        'total_amount': total_amount,
        'notes': notes,
        'offered_by': user.name,
        'role': user.role,
        'status': offer.status
    }

    msg = Message(
        thread_id=thread.id,
        sender_id=user.id,
        message_text=f"Formal Offer: ₹{price}/{unit} for {qty} {unit} of {product_name} (Total ₹{total_amount})",
        message_type='counter_card',
        metadata_json=json.dumps(metadata)
    )
    thread.last_message_at = datetime.utcnow()
    db.session.add(msg)

    recipient_id = thread.buyer_id if user.id == thread.farmer_id else thread.farmer_id
    NotificationService.send(
        user_id=recipient_id,
        title=f"New Counter-Offer from {user.name}",
        message=f"{user.name} proposed ₹{price}/{unit} for {qty} {unit} {product_name}.",
        link_url=url_for('chat.view_thread', thread_id=thread.id)
    )
    db.session.commit()

    return jsonify({
        'success': True,
        'message': {
            'id': msg.id,
            'sender_id': msg.sender_id,
            'sender_name': user.name,
            'text': msg.message_text,
            'type': msg.message_type,
            'metadata': metadata,
            'created_at': msg.created_at.strftime('%I:%M %p')
        }
    })


@chat_bp.route('/thread/<int:thread_id>/share-phone', methods=['POST'])
@login_required
def share_phone(thread_id):
    user = g.user
    thread = ChatThread.query.get_or_404(thread_id)
    
    # Send message with clean text (no duplicate emoji in text)
    msg = Message(
        thread_id=thread.id,
        sender_id=user.id,
        message_text=f"{user.name} shared their verified phone number: {user.phone}",
        message_type='phone_shared',
        metadata_json=json.dumps({'phone': user.phone, 'shared_by': user.name})
    )
    thread.last_message_at = datetime.utcnow()
    db.session.add(msg)
    db.session.commit()
    flash(f'Your contact number has been shared in this chat.', 'info')
    return redirect(url_for('chat.view_thread', thread_id=thread.id))


@chat_bp.route('/thread/<int:thread_id>/poll')
@login_required
def poll_messages(thread_id):
    thread = ChatThread.query.get_or_404(thread_id)
    since_id = request.args.get('since_id', 0, type=int)

    new_msgs = Message.query.filter(Message.thread_id == thread.id, Message.id > since_id).order_by(Message.created_at.asc()).all()
    results = []
    for m in new_msgs:
        results.append({
            'id': m.id,
            'sender_id': m.sender_id,
            'sender_name': m.sender.name,
            'text': m.message_text,
            'type': m.message_type,
            'metadata': m.get_metadata(),
            'created_at': m.created_at.strftime('%I:%M %p'),
            'is_me': m.sender_id == g.user.id
        })
    return jsonify({'messages': results})
