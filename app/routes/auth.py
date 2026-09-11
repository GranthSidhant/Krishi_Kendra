import os
import random
import time
import base64
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g, current_app
from werkzeug.utils import secure_filename
from app.models import User, FarmerProfile, BuyerProfile
from app.extensions import db
from app.services.otp_service import OTPService
from app.services.audit_service import AuditService

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def farmer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user.role != 'farmer':
            flash('Farmer access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def buyer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user.role != 'buyer':
            flash('Buyer access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user.role != 'admin':
            flash('Authorized Admin / Officer access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def generate_unique_custom_id(role):
    prefix = 'FK' if role == 'farmer' else ('BK' if role == 'buyer' else 'ADM')
    random_num = random.randint(1000, 9999)
    custom_id = f"{prefix}-2026-{random_num}"
    while User.query.filter_by(custom_id=custom_id).first():
        random_num = random.randint(1000, 9999)
        custom_id = f"{prefix}-2026-{random_num}"
    return custom_id


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect_user_dashboard(g.user)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        role = request.form.get('role', 'farmer').lower()
        password = request.form.get('password', '')
        state = request.form.get('state', 'Maharashtra')
        district = request.form.get('district', 'Nashik')
        preferred_language = request.form.get('preferred_language', 'en')
        
        # Optional verification details
        gov_id_type = request.form.get('gov_id_type', '')
        gov_id_raw = request.form.get('gov_id_number', '').strip()
        
        if not name or not phone or not password:
            flash('Name, Mobile Number, and Password are required.', 'danger')
            return render_template('auth/register.html')
            
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            flash('This mobile number is already registered. Please log in.', 'info')
            return redirect(url_for('auth.login'))

        # Generate masked ID if provided
        gov_id_masked = None
        verification_status = 'none'
        if gov_id_raw:
            last4 = gov_id_raw[-4:] if len(gov_id_raw) >= 4 else "0000"
            gov_id_masked = f"XXXX-XXXX-{last4}"
            verification_status = 'pending'

        # Store pending registration data in session for OTP verification
        custom_id = generate_unique_custom_id(role)
        session['reg_data'] = {
            'name': name,
            'phone': phone,
            'role': role,
            'password': password,
            'custom_id': custom_id,
            'state': state,
            'district': district,
            'preferred_language': preferred_language,
            'gov_id_type': gov_id_type,
            'gov_id_masked': gov_id_masked,
            'verification_status': verification_status
        }
        
        otp = OTPService.generate_otp(phone)
        flash(f'Verification OTP sent to {phone}. (Demo Mode OTP: {otp})', 'info')
        return redirect(url_for('auth.verify_otp'))

    role_param = request.args.get('role', 'farmer')
    return render_template('auth/register.html', selected_role=role_param)


@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    reg_data = session.get('reg_data')
    if not reg_data:
        flash('Session expired. Please register again.', 'warning')
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        entered_otp = request.form.get('otp', '').strip()
        phone = reg_data['phone']

        if OTPService.verify_otp(phone, entered_otp):
            try:
                # Create user and profile
                user = User(
                    custom_id=reg_data.get('custom_id'),
                    name=reg_data.get('name'),
                    phone=reg_data.get('phone'),
                    role=reg_data.get('role', 'farmer'),
                    preferred_language=reg_data.get('preferred_language', 'en'),
                    gov_id_type=reg_data.get('gov_id_type') if reg_data.get('gov_id_type') else None,
                    gov_id_masked=reg_data.get('gov_id_masked'),
                    verification_status=reg_data.get('verification_status', 'none'),
                    is_verified=False
                )
                user.set_password(reg_data.get('password', ''))
                db.session.add(user)
                db.session.flush()

                if user.role == 'farmer':
                    farmer_profile = FarmerProfile(
                        user_id=user.id,
                        state=reg_data.get('state', 'Maharashtra'),
                        district=reg_data.get('district', 'Nashik'),
                        crops_grown='Wheat, Onion, Tomato',
                        farm_location_name=f"{user.name}'s Farm"
                    )
                    db.session.add(farmer_profile)
                elif user.role == 'buyer':
                    buyer_profile = BuyerProfile(
                        user_id=user.id,
                        business_name=f"{user.name} Trading",
                        state=reg_data.get('state', 'Maharashtra'),
                        district=reg_data.get('district', 'Nashik')
                    )
                    db.session.add(buyer_profile)

                db.session.commit()
                OTPService.clear_otp(phone)
                session.pop('reg_data', None)
                
                # Auto log-in
                session['user_id'] = user.id
                session['role'] = user.role
                session['language'] = user.preferred_language
                
                flash(f'Welcome to Krishi Kendra, {user.name}! Your Unique ID is {user.custom_id}.', 'success')
                return redirect_user_dashboard(user)
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Registration DB error: {e}")
                flash(f'Registration could not be completed. Please try again: {str(e)}', 'danger')
                return redirect(url_for('auth.register'))
        else:
            flash('Invalid OTP. Please enter the correct code (e.g. 123456).', 'danger')

    return render_template('auth/verify_otp.html', phone=reg_data['phone'])


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect_user_dashboard(g.user)

    if request.method == 'POST':
        login_id = request.form.get('login_id', '').strip() # Can be phone or custom ID
        password = request.form.get('password', '')

        try:
            user = User.query.filter((User.phone == login_id) | (User.custom_id == login_id)).first()

            if user and user.check_password(password):
                if not user.is_active:
                    flash('Your account has been suspended by the administrator.', 'danger')
                    return render_template('auth/login.html')
                    
                session['user_id'] = user.id
                session['role'] = user.role
                session['language'] = user.preferred_language
                flash(f'Logged in successfully as {user.name} ({user.role.capitalize()}).', 'success')
                
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect_user_dashboard(user)
            else:
                flash('Invalid Phone / ID or Password. Please try again.', 'danger')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Login DB error: {e}")
            flash('A database connection error occurred. Please try again.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if g.user and g.user.role == 'admin':
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        login_id = request.form.get('login_id', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter((User.phone == login_id) | (User.custom_id == login_id)).first()

        if user and user.role == 'admin' and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['language'] = user.preferred_language
            flash(f'Welcome back, Administrator {user.name}!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid Admin ID / Phone or Password. Please ensure you have administrator privileges.', 'danger')

    return render_template('auth/admin_login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))


def safe_float(val, default=0.0):
    if val is None:
        return default
    val_str = str(val).strip()
    if not val_str:
        return default
    try:
        return float(val_str)
    except (ValueError, TypeError):
        return default


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = g.user

    # Ensure profile models exist
    if user.role == 'farmer':
        if not user.farmer_profile:
            user.farmer_profile = FarmerProfile(user_id=user.id)
            db.session.add(user.farmer_profile)
            try:
                db.session.flush()
            except Exception:
                db.session.rollback()
        farmer_prof = user.farmer_profile
        buyer_prof = None
    elif user.role == 'buyer':
        if not user.buyer_profile:
            user.buyer_profile = BuyerProfile(user_id=user.id)
            db.session.add(user.buyer_profile)
            try:
                db.session.flush()
            except Exception:
                db.session.rollback()
        buyer_prof = user.buyer_profile
        farmer_prof = None
    else:
        farmer_prof = user.farmer_profile
        buyer_prof = user.buyer_profile

    if request.method == 'POST':
        try:
            name_val = request.form.get('name', '').strip()
            if name_val:
                user.name = name_val
            user.preferred_language = request.form.get('preferred_language', user.preferred_language or 'en')
            
            # Profile image upload or avatar selection
            avatar_choice = request.form.get('avatar_choice', '').strip()
            if avatar_choice:
                user.profile_image = avatar_choice

            if 'profile_image_file' in request.files:
                file = request.files['profile_image_file']
                if file and file.filename != '':
                    try:
                        file_bytes = file.read()
                        if file_bytes and len(file_bytes) > 0:
                            ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'jpeg'
                            mime = f"image/{ext}" if ext in ['png', 'webp', 'gif', 'svg'] else 'image/jpeg'
                            b64_str = base64.b64encode(file_bytes).decode('utf-8')
                            user.profile_image = f"data:{mime};base64,{b64_str}"
                            
                            # Also attempt saving to uploads/avatars/ directory if disk is writable
                            try:
                                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
                                os.makedirs(upload_dir, exist_ok=True)
                                filename = secure_filename(f"{user.custom_id}_{int(time.time())}_{file.filename}")
                                upload_path = os.path.join(upload_dir, filename)
                                with open(upload_path, 'wb') as f:
                                    f.write(file_bytes)
                            except Exception:
                                pass
                    except Exception as e:
                        current_app.logger.error(f"Error handling profile image: {e}")

            # Farmer profile updates
            if user.role == 'farmer' and farmer_prof:
                farmer_prof.farm_location_name = request.form.get('farm_location_name', farmer_prof.farm_location_name or '')
                farmer_prof.address = request.form.get('address', farmer_prof.address or '')
                farmer_prof.district = request.form.get('district', farmer_prof.district or '')
                farmer_prof.state = request.form.get('state', farmer_prof.state or '')
                farmer_prof.google_maps_link = request.form.get('google_maps_link', farmer_prof.google_maps_link or '')
                farmer_prof.crops_grown = request.form.get('crops_grown', farmer_prof.crops_grown or '')
                farmer_prof.farm_size_acres = safe_float(request.form.get('farm_size_acres'), farmer_prof.farm_size_acres or 3.0)
                farmer_prof.share_phone_consent = 'share_phone_consent' in request.form
                farmer_prof.open_to_all_quantities = 'open_to_all_quantities' in request.form
                farmer_prof.min_qty_kg = safe_float(request.form.get('min_qty_kg'), farmer_prof.min_qty_kg or 50.0)
                farmer_prof.max_qty_kg = safe_float(request.form.get('max_qty_kg'), farmer_prof.max_qty_kg or 10000.0)
                farmer_prof.bio = request.form.get('bio', farmer_prof.bio or '')

            # Buyer profile updates
            if user.role == 'buyer' and buyer_prof:
                buyer_prof.business_name = request.form.get('business_name', buyer_prof.business_name or '')
                buyer_prof.business_type = request.form.get('business_type', buyer_prof.business_type or '')
                buyer_prof.address = request.form.get('address', buyer_prof.address or '')
                buyer_prof.district = request.form.get('district', buyer_prof.district or '')
                buyer_prof.state = request.form.get('state', buyer_prof.state or '')
                buyer_prof.gst_number = request.form.get('gst_number', buyer_prof.gst_number or '')
                buyer_prof.share_phone_consent = 'share_phone_consent' in request.form
                buyer_prof.description = request.form.get('description', buyer_prof.description or '')

            # Optional Verification Document Upload
            if 'verification_doc_file' in request.files:
                doc = request.files['verification_doc_file']
                if doc and doc.filename != '':
                    doc_name = secure_filename(f"VERIF_{user.custom_id}_{int(time.time())}_{doc.filename}")
                    try:
                        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                        os.makedirs(upload_dir, exist_ok=True)
                        doc.save(os.path.join(upload_dir, doc_name))
                        user.verification_doc = doc_name
                    except Exception as e:
                        current_app.logger.warning(f"Could not save verification doc to disk: {e}")
                        user.verification_doc = doc_name

                    user.gov_id_type = request.form.get('gov_id_type', user.gov_id_type or 'Aadhaar Card')
                    raw_id = request.form.get('gov_id_number', '').strip()
                    if raw_id:
                        user.gov_id_masked = f"XXXX-XXXX-{raw_id[-4:]}"
                    user.verification_status = 'pending'
                    user.is_verified = False

            db.session.commit()
            flash('Profile and Avatar updated successfully!', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Profile update error: {e}")
            flash(f'An error occurred while saving profile: {str(e)}', 'danger')
            return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', user=user, farmer_prof=farmer_prof, buyer_prof=buyer_prof)


def redirect_user_dashboard(user):
    if user.role == 'farmer':
        return redirect(url_for('farmer.dashboard'))
    elif user.role == 'buyer':
        return redirect(url_for('buyer.dashboard'))
    elif user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('main.index'))
