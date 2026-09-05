from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.routes.auth import login_required
from app.models import ColdStorage, ColdStorageBooking
from app.extensions import db

cold_storage_bp = Blueprint('cold_storage', __name__)

@cold_storage_bp.route('/')
def index():
    district_filter = request.args.get('district', '')
    query = ColdStorage.query.filter_by(is_active=True)
    if district_filter and district_filter != 'All':
        query = query.filter(ColdStorage.district.ilike(f"%{district_filter}%"))
    
    storages = query.all()
    districts = db.session.query(ColdStorage.district).distinct().all()
    districts = [d[0] for d in districts if d[0]]

    # My bookings if logged in
    my_bookings = []
    if g.user and g.user.role == 'farmer':
        my_bookings = ColdStorageBooking.query.filter_by(farmer_id=g.user.id).order_by(ColdStorageBooking.created_at.desc()).all()

    return render_template(
        'cold_storage/index.html',
        storages=storages,
        districts=districts,
        selected_district=district_filter,
        my_bookings=my_bookings
    )


@cold_storage_bp.route('/<int:storage_id>/book', methods=['GET', 'POST'])
@login_required
def book(storage_id):
    user = g.user
    storage = ColdStorage.query.get_or_404(storage_id)

    if request.method == 'POST':
        produce_name = request.form.get('produce_name', 'Potato')
        qty = float(request.form.get('quantity_quintals', 50))
        duration = int(request.form.get('duration_months', 2))
        start_date = request.form.get('expected_storage_start', '')
        notes = request.form.get('notes', '')

        cost = round(qty * storage.approx_charge_per_month_per_quintal * duration, 2)

        booking = ColdStorageBooking(
            cold_storage_id=storage.id,
            farmer_id=user.id,
            produce_name=produce_name,
            quantity_quintals=qty,
            expected_storage_start=start_date,
            duration_months=duration,
            estimated_total_cost=cost,
            notes=notes,
            status='requested'
        )
        db.session.add(booking)
        db.session.commit()
        flash(f'Cold storage booking request sent for {qty} quintals of {produce_name} at {storage.name}!', 'success')
        return redirect(url_for('cold_storage.index'))

    return render_template('cold_storage/booking.html', storage=storage, user=user)
