from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    custom_id = db.Column(db.String(32), unique=True, nullable=False, index=True) # e.g. FK-2026-1001, BK-2026-2001, ADM-001
    phone = db.Column(db.String(15), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='farmer') # farmer, buyer, admin
    name = db.Column(db.String(120), nullable=False)
    profile_image = db.Column(db.String(255), default='default_avatar.png')
    preferred_language = db.Column(db.String(10), default='en') # en, hi, mr, ta, te
    
    # Verification details (optional Govt ID - Aadhaar/Voter ID)
    is_verified = db.Column(db.Boolean, default=False)
    verification_status = db.Column(db.String(20), default='none') # none, pending, approved, rejected
    gov_id_type = db.Column(db.String(50), nullable=True) # Aadhaar, Voter Card, Kisan Credit Card
    gov_id_masked = db.Column(db.String(50), nullable=True) # e.g. "XXXX-XXXX-1234" (Never store full plaintext)
    verification_doc = db.Column(db.String(255), nullable=True)
    verification_rejection_reason = db.Column(db.String(255), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farmer_profile = db.relationship('FarmerProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    buyer_profile = db.relationship('BuyerProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    inventories = db.relationship('Inventory', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    requirements = db.relationship('Requirement', backref='buyer', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_private=False):
        data = {
            'id': self.id,
            'custom_id': self.custom_id,
            'name': self.name,
            'role': self.role,
            'profile_image': self.profile_image,
            'is_verified': self.is_verified,
            'verification_status': self.verification_status,
            'preferred_language': self.preferred_language
        }
        if include_private:
            data['phone'] = self.phone
            data['is_active'] = self.is_active
        return data


class FarmerProfile(db.Model):
    __tablename__ = 'farmer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    address = db.Column(db.String(255), default='')
    district = db.Column(db.String(100), default='Nashik')
    state = db.Column(db.String(100), default='Maharashtra')
    pincode = db.Column(db.String(10), default='422001')
    
    farm_location_name = db.Column(db.String(150), default='Family Farm')
    farm_latitude = db.Column(db.Float, nullable=True, default=19.9975)
    farm_longitude = db.Column(db.Float, nullable=True, default=73.7898)
    google_maps_link = db.Column(db.String(300), default='')
    
    farm_size_acres = db.Column(db.Float, default=3.5)
    crops_grown = db.Column(db.String(255), default='Wheat, Onion, Tomato')
    bio = db.Column(db.Text, default='Dedicated organic farmer cultivating natural crops.')
    
    # Quantity Preferences
    min_qty_kg = db.Column(db.Float, default=50.0)
    max_qty_kg = db.Column(db.Float, default=10000.0)
    open_to_all_quantities = db.Column(db.Boolean, default=True)
    
    # Strict Privacy: phone number shared ONLY if explicit consent is true
    share_phone_consent = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=4.8)
    total_reviews = db.Column(db.Integer, default=12)


class BuyerProfile(db.Model):
    __tablename__ = 'buyer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    business_name = db.Column(db.String(150), default='Fresh Harvest Traders')
    business_type = db.Column(db.String(80), default='Wholesale Trader') # Wholesale Trader, Retailer, Apartment Buying Club, Consumer, Processor
    gst_number = db.Column(db.String(30), nullable=True)
    
    address = db.Column(db.String(255), default='')
    district = db.Column(db.String(100), default='Mumbai')
    state = db.Column(db.String(100), default='Maharashtra')
    pincode = db.Column(db.String(10), default='400001')
    latitude = db.Column(db.Float, nullable=True, default=19.0760)
    longitude = db.Column(db.Float, nullable=True, default=72.8777)
    
    description = db.Column(db.Text, default='Procuring direct-from-farm produce at transparent fair prices.')
    share_phone_consent = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=4.9)
    total_reviews = db.Column(db.Integer, default=8)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    hindi_name = db.Column(db.String(80), default='')
    icon = db.Column(db.String(50), default='fa-seedling')
    description = db.Column(db.String(255), default='')
    is_active = db.Column(db.Boolean, default=True)
    products = db.relationship('Product', backref='category', lazy='dynamic', cascade='all, delete-orphan')


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    hindi_name = db.Column(db.String(100), default='')
    default_unit = db.Column(db.String(20), default='kg') # kg, quintal, ton
    estimated_mandi_rate = db.Column(db.Float, default=25.0) # benchmark ₹/kg
    image_url = db.Column(db.String(255), default='default_crop.jpg')
    is_active = db.Column(db.Boolean, default=True)


class Inventory(db.Model):
    __tablename__ = 'inventories'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    
    product_name = db.Column(db.String(100), nullable=False)
    category_name = db.Column(db.String(80), default='Vegetables')
    available_quantity = db.Column(db.Float, nullable=False, default=100.0)
    unit = db.Column(db.String(20), default='kg') # kg, quintal, ton
    expected_price_per_unit = db.Column(db.Float, nullable=False) # in ₹
    quality_grade = db.Column(db.String(20), default='Grade A') # Grade A, Grade B, Grade C, Premium Organic
    harvest_date = db.Column(db.String(30), default=datetime.utcnow().strftime('%Y-%m-%d'))
    location_district = db.Column(db.String(100), default='Nashik')
    location_state = db.Column(db.String(100), default='Maharashtra')
    
    image_url = db.Column(db.String(255), default='crop_default.jpg')
    status = db.Column(db.String(30), default='available') # available, low_stock, sold_out
    description = db.Column(db.Text, default='Freshly harvested high quality farm produce.')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Requirement(db.Model):
    __tablename__ = 'requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    
    product_name = db.Column(db.String(100), nullable=False)
    required_quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='kg')
    required_quality = db.Column(db.String(30), default='Grade A')
    target_price_per_unit = db.Column(db.Float, nullable=True)
    
    delivery_location = db.Column(db.String(255), default='Mumbai Central Wholesale Market')
    delivery_district = db.Column(db.String(100), default='Mumbai')
    delivery_state = db.Column(db.String(100), default='Maharashtra')
    delivery_pincode = db.Column(db.String(10), default='400001')
    required_by_date = db.Column(db.String(30), default='')
    additional_notes = db.Column(db.Text, default='')
    
    status = db.Column(db.String(30), default='open') # open, responded, matched, completed, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    offers = db.relationship('Offer', backref='requirement', lazy='dynamic', cascade='all, delete-orphan')


class Offer(db.Model):
    __tablename__ = 'offers'
    
    id = db.Column(db.Integer, primary_key=True)
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirements.id', ondelete='SET NULL'), nullable=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventories.id', ondelete='SET NULL'), nullable=True)
    
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='kg')
    offered_price_per_unit = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    offered_by_role = db.Column(db.String(20), default='buyer') # 'buyer' (direct request) or 'farmer' (response to requirement)
    
    status = db.Column(db.String(30), default='pending') # pending, countered, accepted, rejected, ordered
    
    # Counter-offer parameters
    counter_price_per_unit = db.Column(db.Float, nullable=True)
    counter_quantity = db.Column(db.Float, nullable=True)
    counter_notes = db.Column(db.Text, nullable=True)
    last_action_by = db.Column(db.String(20), default='buyer')
    
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='buyer_offers')
    farmer = db.relationship('User', foreign_keys=[farmer_id], backref='farmer_offers')


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_code = db.Column(db.String(32), unique=True, nullable=False, index=True) # e.g. ORD-2026-8801
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id', ondelete='SET NULL'), nullable=True)
    
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='kg')
    agreed_price_per_unit = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    delivery_address = db.Column(db.String(255), nullable=False)
    delivery_date = db.Column(db.String(30), default='')
    
    # Flow: confirmed -> processing -> transport_assigned -> in_transit -> delivered -> completed
    status = db.Column(db.String(30), default='confirmed')
    payment_status = db.Column(db.String(30), default='in_escrow') # pending, in_escrow, released, completed
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='buyer_orders')
    farmer = db.relationship('User', foreign_keys=[farmer_id], backref='farmer_orders')
    delivery = db.relationship('Delivery', backref='order', uselist=False, cascade='all, delete-orphan')


class Delivery(db.Model):
    __tablename__ = 'deliveries'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    pickup_address = db.Column(db.String(255), default='')
    drop_address = db.Column(db.String(255), default='')
    vehicle_type = db.Column(db.String(50), default='Mini Truck (Tata Ace)') # Mini Truck, Pickup, Medium Truck, Refrigerated
    transport_partner_name = db.Column(db.String(100), default='Gramin Express Logistics')
    driver_name = db.Column(db.String(80), default='Ramesh Shinde')
    driver_phone = db.Column(db.String(20), default='+91 98231 44556')
    vehicle_number = db.Column(db.String(30), default='MH-15-EG-4402')
    estimated_cost = db.Column(db.Float, default=1250.0)
    
    current_status = db.Column(db.String(30), default='assigned') # requested, assigned, picked_up, in_transit, delivered
    current_location = db.Column(db.String(150), default='Nashik Highway Hub')
    estimated_arrival = db.Column(db.String(50), default='Tomorrow by 11:00 AM')
    tracking_notes = db.Column(db.Text, default='Produce loaded carefully with temperature check passed.')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatThread(db.Model):
    __tablename__ = 'chat_threads'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='SET NULL'), nullable=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id', ondelete='SET NULL'), nullable=True)
    
    subject_product = db.Column(db.String(100), default='Produce Negotiation')
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    farmer = db.relationship('User', foreign_keys=[farmer_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    messages = db.relationship('Message', backref='thread', lazy='dynamic', cascade='all, delete-orphan')


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('chat_threads.id', ondelete='CASCADE'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    message_text = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(30), default='text') # text, offer_card, counter_card, status_update, phone_shared
    metadata_json = db.Column(db.Text, default='{}') # contains price, quantity, status JSON
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id])

    def get_metadata(self):
        try:
            return json.loads(self.metadata_json or '{}')
        except:
            return {}


class MandiRate(db.Model):
    __tablename__ = 'mandi_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False, index=True)
    district = db.Column(db.String(100), nullable=False, index=True)
    market_name = db.Column(db.String(150), nullable=False) # e.g. Nashik APMC Mandi, Lasalgaon
    commodity = db.Column(db.String(100), nullable=False, index=True) # e.g. Wheat, Onion, Tomato
    variety = db.Column(db.String(100), default='Local / Hybrid')
    grade = db.Column(db.String(30), default='FAQ (Fair Average Quality)')
    
    min_price = db.Column(db.Float, nullable=False) # ₹ per quintal (or kg standard)
    max_price = db.Column(db.Float, nullable=False)
    modal_price = db.Column(db.Float, nullable=False) # Average/Current trading price
    unit = db.Column(db.String(20), default='Quintal')
    
    trend = db.Column(db.String(10), default='up') # up, down, stable
    price_change_pct = db.Column(db.Float, default=1.8)
    price_date = db.Column(db.String(30), default=datetime.utcnow().strftime('%Y-%m-%d'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class ColdStorage(db.Model):
    __tablename__ = 'cold_storages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    operator_name = db.Column(db.String(120), default='Kisan Shetkari Sahakari')
    contact_phone = db.Column(db.String(20), default='+91 94220 11223')
    email = db.Column(db.String(120), default='contact@kisanstorage.org')
    
    address = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(100), nullable=False, default='Nashik')
    state = db.Column(db.String(100), nullable=False, default='Maharashtra')
    pincode = db.Column(db.String(10), default='422003')
    latitude = db.Column(db.Float, default=20.005)
    longitude = db.Column(db.Float, default=73.810)
    
    total_capacity_mt = db.Column(db.Float, default=5000.0) # Metric Tonnes
    available_capacity_mt = db.Column(db.Float, default=1850.0)
    approx_charge_per_month_per_quintal = db.Column(db.Float, default=65.0) # ₹ / quintal / month
    temp_range_celsius = db.Column(db.String(50), default='0°C to 4°C (Controlled Humidity)')
    supported_produce = db.Column(db.String(255), default='Potato, Onion, Apples, Grapes, Carrots')
    facilities = db.Column(db.String(255), default='Solar Cold Backup, Automated Pre-cooling, 24/7 CCTV')
    
    is_verified = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('ColdStorageBooking', backref='facility', lazy='dynamic', cascade='all, delete-orphan')


class ColdStorageBooking(db.Model):
    __tablename__ = 'cold_storage_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    cold_storage_id = db.Column(db.Integer, db.ForeignKey('cold_storages.id', ondelete='CASCADE'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    produce_name = db.Column(db.String(100), nullable=False)
    quantity_quintals = db.Column(db.Float, nullable=False)
    expected_storage_start = db.Column(db.String(30), default='')
    duration_months = db.Column(db.Integer, default=2)
    estimated_total_cost = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(30), default='requested') # requested, confirmed, in_storage, released, cancelled
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    farmer = db.relationship('User', foreign_keys=[farmer_id])


class MarketplaceProduct(db.Model):
    __tablename__ = 'marketplace_products'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False) # Seeds, Fertilizers, Equipment, Irrigation, Crop Protection
    title = db.Column(db.String(150), nullable=False)
    brand = db.Column(db.String(100), default='Krishi Brand')
    description = db.Column(db.Text, default='')
    price = db.Column(db.Float, nullable=False) # in ₹
    unit = db.Column(db.String(30), default='bag / 50kg')
    image_url = db.Column(db.String(255), default='input_product.jpg')
    stock_quantity = db.Column(db.Integer, default=100)
    is_available = db.Column(db.Boolean, default=True)


class MarketplaceOrder(db.Model):
    __tablename__ = 'marketplace_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('marketplace_products.id'), nullable=False)
    
    product_title = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(255), default='')
    status = db.Column(db.String(30), default='confirmed') # confirmed, dispatched, delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    farmer = db.relationship('User', foreign_keys=[farmer_id])
    product = db.relationship('MarketplaceProduct', foreign_keys=[product_id])


class GovernmentScheme(db.Model):
    __tablename__ = 'government_schemes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    hindi_title = db.Column(db.String(200), default='')
    category = db.Column(db.String(80), default='Subsidy & Financial Assistance') # Subsidy, Insurance, Credit/Loan, Solar, Irrigation
    description = db.Column(db.Text, nullable=False)
    eligibility_summary = db.Column(db.Text, default='All small and marginal landholding farmer families.')
    benefits_summary = db.Column(db.Text, default='Financial benefit of ₹6,000 per year in three equal installments.')
    application_link = db.Column(db.String(300), default='https://pmkisan.gov.in/')
    launch_year = db.Column(db.String(20), default='2019')
    is_featured = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Dispute(db.Model):
    __tablename__ = 'disputes'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='SET NULL'), nullable=True)
    raised_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    against_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    reason = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='open') # open, under_review, resolved, dismissed
    resolution_notes = db.Column(db.Text, default='')
    resolved_by_admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    raised_by = db.relationship('User', foreign_keys=[raised_by_id])
    against_user = db.relationship('User', foreign_keys=[against_user_id])
    order = db.relationship('Order', foreign_keys=[order_id])


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False) # e.g. "USER_VERIFIED", "CATEGORY_ADDED", "DISPUTE_RESOLVED"
    target_entity = db.Column(db.String(80), default='')
    target_id = db.Column(db.String(50), default='')
    details = db.Column(db.Text, default='')
    ip_address = db.Column(db.String(50), default='127.0.0.1')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    admin = db.relationship('User', foreign_keys=[admin_id])


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link_url = db.Column(db.String(255), default='#')
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
