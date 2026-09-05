import sys
from pathlib import Path
from datetime import datetime, timedelta

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.extensions import db
from app.models import (
    User, FarmerProfile, BuyerProfile, Category, Product, Inventory,
    Requirement, Offer, Order, Delivery, ChatThread, Message, MandiRate,
    ColdStorage, MarketplaceProduct, GovernmentScheme, Dispute, AuditLog
)

def seed_all_sample_data(app):
    with app.app_context():
        # Clear existing data if any
        db.drop_all()
        db.create_all()

        print("Seeding Krishi Kendra database with rich Indian agricultural data...")

        # 1. Seed Categories
        cat_cereals = Category(name='Cereals & Grains', hindi_name='अनाज एवं खाद्यान्न', icon='fa-wheat-awn', description='Wheat, Rice, Maize, Bajra, Jowar')
        cat_veggies = Category(name='Vegetables', hindi_name='सब्जियां', icon='fa-carrot', description='Onion, Tomato, Potato, Garlic, Ginger')
        cat_fruits = Category(name='Fruits', hindi_name='फल', icon='fa-apple-whole', description='Apples, Grapes, Pomegranate, Banana')
        cat_pulses = Category(name='Pulses & Legumes', hindi_name='दालें एवं दलहन', icon='fa-seedling', description='Chana, Moong, Toor, Urad')
        cat_cash = Category(name='Oilseeds & Cash Crops', hindi_name='तिलहन व नकदी फसलें', icon='fa-leaf', description='Soybean, Mustard, Cotton, Sugarcane')

        db.session.add_all([cat_cereals, cat_veggies, cat_fruits, cat_pulses, cat_cash])
        db.session.flush()

        # 2. Seed Master Products
        prod_wheat = Product(category_id=cat_cereals.id, name='Wheat', hindi_name='गेहूं', default_unit='kg', estimated_mandi_rate=23.50)
        prod_rice = Product(category_id=cat_cereals.id, name='Basmati Rice', hindi_name='बासमती चावल', default_unit='kg', estimated_mandi_rate=38.00)
        prod_onion = Product(category_id=cat_veggies.id, name='Red Onion', hindi_name='लाल प्याज', default_unit='kg', estimated_mandi_rate=18.50)
        prod_tomato = Product(category_id=cat_veggies.id, name='Tomato', hindi_name='टमाटर', default_unit='kg', estimated_mandi_rate=14.00)
        prod_potato = Product(category_id=cat_veggies.id, name='Potato', hindi_name='आलू', default_unit='kg', estimated_mandi_rate=16.50)
        prod_soybean = Product(category_id=cat_cash.id, name='Soybean', hindi_name='सोयाबीन', default_unit='kg', estimated_mandi_rate=42.00)
        prod_garlic = Product(category_id=cat_veggies.id, name='Garlic', hindi_name='लहसुन', default_unit='kg', estimated_mandi_rate=85.00)
        prod_cotton = Product(category_id=cat_cash.id, name='Cotton', hindi_name='कपास', default_unit='quintal', estimated_mandi_rate=6800.00)

        db.session.add_all([prod_wheat, prod_rice, prod_onion, prod_tomato, prod_potato, prod_soybean, prod_garlic, prod_cotton])
        db.session.flush()

        # 3. Seed Users & Profiles
        # Farmer 1 (Nashik)
        farmer1 = User(
            custom_id='FK-2026-1001',
            phone='9876543210',
            name='Ramesh Patil',
            role='farmer',
            preferred_language='en',
            is_verified=True,
            verification_status='approved',
            gov_id_type='Aadhaar Card',
            gov_id_masked='XXXX-XXXX-4819'
        )
        farmer1.set_password('farmer123')
        db.session.add(farmer1)
        db.session.flush()

        farmer1_prof = FarmerProfile(
            user_id=farmer1.id,
            address='Village Dindori, Nashik Road',
            district='Nashik',
            state='Maharashtra',
            pincode='422004',
            farm_location_name='Patil Organic Agro Farm',
            farm_latitude=20.0063,
            farm_longitude=73.7900,
            google_maps_link='https://maps.google.com/?q=20.0063,73.7900',
            farm_size_acres=5.5,
            crops_grown='Wheat, Red Onion, Tomato',
            share_phone_consent=True, # Explicit consent to test phone call
            rating=4.9,
            total_reviews=28
        )
        db.session.add(farmer1_prof)

        # Farmer 2 (Ludhiana)
        farmer2 = User(
            custom_id='FK-2026-1002',
            phone='9876543211',
            name='Gurpreet Singh',
            role='farmer',
            preferred_language='en',
            is_verified=True,
            verification_status='approved',
            gov_id_type='Kisan Credit Card',
            gov_id_masked='XXXX-XXXX-9122'
        )
        farmer2.set_password('farmer123')
        db.session.add(farmer2)
        db.session.flush()

        farmer2_prof = FarmerProfile(
            user_id=farmer2.id,
            address='Khanna Tehsil, GT Road',
            district='Ludhiana',
            state='Punjab',
            pincode='141401',
            farm_location_name='Golden Harvest Farms',
            farm_latitude=30.9010,
            farm_longitude=75.8573,
            farm_size_acres=12.0,
            crops_grown='Wheat, Basmati Rice',
            share_phone_consent=False, # Phone private by default
            rating=4.8,
            total_reviews=19
        )
        db.session.add(farmer2_prof)

        # Buyer 1 (Mumbai Wholesale)
        buyer1 = User(
            custom_id='BK-2026-2001',
            phone='9876543220',
            name='Suresh Aggarwal',
            role='buyer',
            preferred_language='en',
            is_verified=True,
            verification_status='approved',
            gov_id_type='GSTIN',
            gov_id_masked='XXXX-XXXX-8821'
        )
        buyer1.set_password('buyer123')
        db.session.add(buyer1)
        db.session.flush()

        buyer1_prof = BuyerProfile(
            user_id=buyer1.id,
            business_name='Aggarwal Fresh Agro Wholesale',
            business_type='Wholesale Trader',
            gst_number='27AABCU9603R1ZM',
            address='APMC Market Yard 2, Vashi',
            district='Mumbai',
            state='Maharashtra',
            pincode='400703',
            share_phone_consent=True,
            rating=4.9,
            total_reviews=42
        )
        db.session.add(buyer1_prof)

        # Admin / Agriculture Officer
        admin1 = User(
            custom_id='ADM-2026-001',
            phone='9876543230',
            name='Dr. Ashok Mehta (District Agri Officer)',
            role='admin',
            preferred_language='en',
            is_verified=True,
            verification_status='approved'
        )
        admin1.set_password('admin123')
        db.session.add(admin1)
        db.session.flush()

        # 4. Seed Live Mandi Rates
        mandi_data = [
            ('Maharashtra', 'Nashik', 'Nashik APMC Mandi', 'Wheat', 2250, 2450, 2350, 'Quintal', 'up', 1.8),
            ('Maharashtra', 'Nashik', 'Lasalgaon Mandi', 'Red Onion', 1700, 2000, 1850, 'Quintal', 'up', 3.2),
            ('Madhya Pradesh', 'Indore', 'Indore APMC Market', 'Tomato', 1200, 1550, 1400, 'Quintal', 'down', 0.8),
            ('Uttar Pradesh', 'Agra', 'Agra Fruit & Veg Market', 'Potato', 1500, 1750, 1650, 'Quintal', 'up', 2.0),
            ('Punjab', 'Karnal', 'Karnal Grain Mandi', 'Basmati Rice', 3600, 4000, 3800, 'Quintal', 'up', 0.5),
            ('Maharashtra', 'Nagpur', 'Nagpur Grain Yard', 'Soybean', 4000, 4400, 4200, 'Quintal', 'up', 1.2),
            ('Gujarat', 'Ahmedabad', 'Ahmedabad APMC', 'Garlic', 8000, 9200, 8500, 'Quintal', 'up', 4.5),
            ('Punjab', 'Ludhiana', 'Ludhiana Mandi', 'Wheat', 2280, 2420, 2380, 'Quintal', 'stable', 0.0),
        ]
        for st, dist, mkt, comm, min_p, max_p, mod_p, unit, trend, pct in mandi_data:
            mr = MandiRate(
                state=st, district=dist, market_name=mkt, commodity=comm,
                min_price=min_p, max_price=max_p, modal_price=mod_p,
                unit=unit, trend=trend, price_change_pct=pct
            )
            db.session.add(mr)

        # 5. Seed Farmer Inventories
        inv1 = Inventory(
            farmer_id=farmer1.id,
            product_name='Wheat',
            category_name='Cereals & Grains',
            available_quantity=5000.0,
            unit='kg',
            expected_price_per_unit=24.0,
            quality_grade='Grade A (Premium)',
            location_district='Nashik',
            location_state='Maharashtra',
            description='Premium Sharbati Wheat, machine-cleaned, 0% moisture.',
            status='available'
        )
        inv2 = Inventory(
            farmer_id=farmer1.id,
            product_name='Red Onion',
            category_name='Vegetables',
            available_quantity=3500.0,
            unit='kg',
            expected_price_per_unit=19.0,
            quality_grade='Grade A (Premium)',
            location_district='Nashik',
            location_state='Maharashtra',
            description='Export grade Nasik Red Onions, medium to big size.',
            status='available'
        )
        inv3 = Inventory(
            farmer_id=farmer2.id,
            product_name='Basmati Rice',
            category_name='Cereals & Grains',
            available_quantity=8000.0,
            unit='kg',
            expected_price_per_unit=38.0,
            quality_grade='Grade A (Premium)',
            location_district='Ludhiana',
            location_state='Punjab',
            description='1121 Extra Long Grain Basmati Rice, aged 1 year.',
            status='available'
        )
        db.session.add_all([inv1, inv2, inv3])
        db.session.flush()

        # 6. Seed Buyer Requirement & Match
        req1 = Requirement(
            buyer_id=buyer1.id,
            product_name='Wheat',
            required_quantity=2000.0,
            unit='kg',
            required_quality='Grade A (Premium)',
            target_price_per_unit=23.5,
            delivery_location='APMC Market Yard 2, Vashi, Navi Mumbai',
            delivery_district='Mumbai',
            delivery_state='Maharashtra',
            required_by_date=(datetime.utcnow() + timedelta(days=5)).strftime('%Y-%m-%d'),
            additional_notes='Immediate procurement for wholesale retail distribution.',
            status='open'
        )
        db.session.add(req1)
        db.session.flush()

        # 7. Seed Active Offer & Negotiation
        offer1 = Offer(
            requirement_id=req1.id,
            inventory_id=inv1.id,
            buyer_id=buyer1.id,
            farmer_id=farmer1.id,
            product_name='Wheat',
            quantity=2000.0,
            unit='kg',
            offered_price_per_unit=24.0,
            total_amount=48000.0,
            offered_by_role='farmer',
            status='countered',
            counter_price_per_unit=24.0,
            counter_quantity=2000.0,
            counter_notes='Offered ₹24/kg for premium Grade A Sharbati Wheat.',
            last_action_by='farmer'
        )
        db.session.add(offer1)
        db.session.flush()

        # 8. Seed Confirmed Order with Logistics
        order1 = Order(
            order_code='ORD-2026-8801',
            offer_id=offer1.id,
            buyer_id=buyer1.id,
            farmer_id=farmer1.id,
            product_name='Red Onion',
            quantity=1500.0,
            unit='kg',
            agreed_price_per_unit=19.0,
            total_amount=28500.0,
            delivery_address='APMC Market Yard 2, Vashi, Navi Mumbai',
            status='in_transit',
            payment_status='in_escrow'
        )
        db.session.add(order1)
        db.session.flush()

        deliv1 = Delivery(
            order_id=order1.id,
            pickup_address='Patil Organic Agro Farm, Dindori, Nashik',
            drop_address='APMC Market Yard 2, Vashi, Navi Mumbai',
            vehicle_type='Mini Truck (Tata Ace)',
            transport_partner_name='Kisan Express Freight',
            driver_name='Ramesh Shinde',
            driver_phone='+91 98231 44556',
            vehicle_number='MH-15-EG-4402',
            estimated_cost=1450.0,
            current_status='in_transit',
            current_location='Igatpuri Highway Checkpoint',
            estimated_arrival='Tomorrow by 09:30 AM',
            tracking_notes='Produce loaded with temperature monitoring active.'
        )
        db.session.add(deliv1)

        # 9. Seed Chat Thread & Messages
        chat1 = ChatThread(
            farmer_id=farmer1.id,
            buyer_id=buyer1.id,
            order_id=order1.id,
            offer_id=offer1.id,
            subject_product='Wheat & Onion Trade Negotiation'
        )
        db.session.add(chat1)
        db.session.flush()

        msg1 = Message(thread_id=chat1.id, sender_id=buyer1.id, message_text="Namaste Ramesh ji, I saw your 5,000 kg Wheat listing. What is the best price for 2,000 kg?")
        msg2 = Message(thread_id=chat1.id, sender_id=farmer1.id, message_text="Namaste Suresh ji. This is premium Sharbati Wheat. Current Mandi is ₹23.50. I can supply Grade A at ₹24/kg with direct farm dispatch.")
        msg3 = Message(
            thread_id=chat1.id,
            sender_id=farmer1.id,
            message_text="📞 Ramesh Patil shared their phone number: +91 9876543210",
            message_type='phone_shared',
            metadata_json='{"phone": "+91 9876543210", "shared_by": "Ramesh Patil"}'
        )
        db.session.add_all([msg1, msg2, msg3])

        # 10. Seed Cold Storage Facilities
        cs1 = ColdStorage(
            name='Kisan Shetkari Sahakari Cold Storage',
            operator_name='Nashik District Farmers Cooperative',
            contact_phone='+91 94220 11223',
            address='Pimpalgaon Baswant Road',
            district='Nashik',
            state='Maharashtra',
            total_capacity_mt=5000.0,
            available_capacity_mt=1850.0,
            approx_charge_per_month_per_quintal=65.0,
            temp_range_celsius='0°C to 4°C (Controlled Humidity)',
            supported_produce='Potato, Onion, Grapes, Apples, Carrots',
            facilities='Solar Cold Backup, Automated Pre-cooling, 24/7 CCTV, Loading Ramp',
            is_verified=True,
            is_active=True
        )
        cs2 = ColdStorage(
            name='Punjab Agro Logistics & Cold Chain',
            operator_name='Punjab State Cooperative',
            contact_phone='+91 98140 22334',
            address='GT Road, Khanna',
            district='Ludhiana',
            state='Punjab',
            total_capacity_mt=8000.0,
            available_capacity_mt=3200.0,
            approx_charge_per_month_per_quintal=58.0,
            temp_range_celsius='-2°C to 2°C (Preservation Grade)',
            supported_produce='Potato, Peas, Cauliflower, Apple',
            facilities='Multi-chamber temperature zones, Generator backup',
            is_verified=True,
            is_active=True
        )
        cs3 = ColdStorage(
            name='Malwa Krishi Cold Storage',
            operator_name='Malwa Agri Traders',
            contact_phone='+91 98260 33445',
            address='Sanwer Road Industrial Area',
            district='Indore',
            state='Madhya Pradesh',
            total_capacity_mt=6000.0,
            available_capacity_mt=2100.0,
            approx_charge_per_month_per_quintal=60.0,
            temp_range_celsius='1°C to 4°C',
            supported_produce='Potato, Garlic, Onion, Ginger',
            facilities='Air-conditioned sorting hall, CCTV',
            is_verified=True,
            is_active=True
        )
        db.session.add_all([cs1, cs2, cs3])

        # 11. Seed Marketplace Products
        mp1 = MarketplaceProduct(category='Seeds', title='Certified High-Yield Hybrid Wheat Seeds (PBW 550)', brand='National Seeds Corp', description='Disease resistant high-yield wheat seeds with 95% germination rate.', price=1250.0, unit='bag / 40kg', is_available=True)
        mp2 = MarketplaceProduct(category='Fertilizers', title='Organic Neem Coated Urea & Bio-NPK (19:19:19)', brand='IFFCO Agro', description='Water soluble balanced plant nutrition for healthy vegetative growth.', price=850.0, unit='bag / 50kg', is_available=True)
        mp3 = MarketplaceProduct(category='Equipment', title='Battery Powered 16L Backpack Knapsack Sprayer', brand='Krishi Power', description='Rechargeable lithium-ion battery sprayer with adjustable brass nozzles.', price=2400.0, unit='piece', is_available=True)
        mp4 = MarketplaceProduct(category='Irrigation', title='Automatic Inline Drip Irrigation Kit (1 Acre)', brand='Jain Farm Fresh', description='Complete drip irrigation kit with inline drippers and filter unit.', price=6500.0, unit='kit / 1 acre', is_available=True)
        db.session.add_all([mp1, mp2, mp3, mp4])

        # 12. Seed Government Schemes
        gs1 = GovernmentScheme(
            title='Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
            hindi_title='प्रधानमंत्री किसान सम्मान निधि योजना',
            category='Subsidy & Financial Assistance',
            description='Direct income support of ₹6,000 per year transferred into the bank accounts of all landholding farmer families across India.',
            eligibility_summary='All small and marginal landholding farmer families with bank-linked Aadhaar.',
            benefits_summary='₹6,000 annually paid in 3 equal four-monthly installments of ₹2,000 directly via DBT.',
            application_link='https://pmkisan.gov.in/',
            launch_year='2019',
            is_featured=True
        )
        gs2 = GovernmentScheme(
            title='Pradhan Mantri Fasal Bima Yojana (PMFBY)',
            hindi_title='प्रधानमंत्री फसल बीमा योजना',
            category='Insurance',
            description='Comprehensive crop insurance providing financial support to farmers suffering crop loss/damage arising out of unforeseen weather events.',
            eligibility_summary='All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.',
            benefits_summary='Low premium rates (2% for Kharif, 1.5% for Rabi crops) with full sum insured coverage.',
            application_link='https://pmfby.gov.in/',
            launch_year='2016',
            is_featured=True
        )
        gs3 = GovernmentScheme(
            title='PM-KUSUM Solar Agriculture Pump Scheme',
            hindi_title='पीएम कुसुम सौर कृषि पंप योजना',
            category='Solar & Irrigation',
            description='Subsidies for standalone solar agriculture pumps and solarisation of existing grid-connected agriculture pumps.',
            eligibility_summary='Individual farmers, water user associations, and FPOs.',
            benefits_summary='Up to 60% capital subsidy from Central and State Governments for solar pumps.',
            application_link='https://pmkusum.mnre.gov.in/',
            launch_year='2019',
            is_featured=True
        )
        db.session.add_all([gs1, gs2, gs3])

        # 13. Seed Audit Log
        log1 = AuditLog(
            action='SYSTEM_INITIALIZED',
            details='Krishi Kendra SIH 2026 database initialized with master data and verified users.'
        )
        db.session.add(log1)

        db.session.commit()
        print("Seeding completed successfully! All sample data, users, and market benchmarks ready.")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    seed_all_sample_data(app)
