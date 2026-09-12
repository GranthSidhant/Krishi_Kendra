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
        print("Clearing and re-seeding Krishi Kendra database with rich Indian agricultural data...")
        try:
            db.create_all()
            AuditLog.query.delete()
            Message.query.delete()
            ChatThread.query.delete()
            Delivery.query.delete()
            Order.query.delete()
            Offer.query.delete()
            Requirement.query.delete()
            Inventory.query.delete()
            MandiRate.query.delete()
            ColdStorage.query.delete()
            MarketplaceProduct.query.delete()
            GovernmentScheme.query.delete()
            Product.query.delete()
            Category.query.delete()
            FarmerProfile.query.delete()
            BuyerProfile.query.delete()
            User.query.delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Note during clear: {e}")

        # 1. Seed Categories
        cat_cereals = Category(name='Cereals & Grains', hindi_name='अनाज एवं खाद्यान्न', icon='fa-wheat-awn', description='Wheat, Basmati Rice, Sona Masoori, Maize, Pearl Millet (Bajra), Sorghum (Jowar), Barley')
        cat_veggies = Category(name='Vegetables', hindi_name='सब्जियां', icon='fa-carrot', description='Red Onion, Tomato, Potato, Garlic, Ginger, Green Chilli, Cauliflower, Capsicum, Okra')
        cat_fruits = Category(name='Fruits & Orchards', hindi_name='फल एवं बागवानी', icon='fa-apple-whole', description='Alphonso Mango, Kesar Mango, Kashmiri Apple, Nagpur Orange, Banana, Grapes, Pomegranate, Guava')
        cat_pulses = Category(name='Pulses & Legumes', hindi_name='दालें एवं दलहन', icon='fa-seedling', description='Chana / Chickpea, Moong Dal, Toor Dal (Arhar), Urad Dal, Masoor Dal, Rajma')
        cat_cash = Category(name='Oilseeds & Cash Crops', hindi_name='तिलहन व नकदी फसलें', icon='fa-leaf', description='Soybean, Mustard, Cotton, Groundnut, Sugarcane, Sesame (Til)')
        cat_spices = Category(name='Spices & Herbs', hindi_name='मसाले एवं जड़ी-बूटियां', icon='fa-pepper-hot', description='Guntur Red Chilli, Turmeric (Haldi), Cumin (Jeera), Cardamom, Black Pepper')
        cat_organic = Category(name='Organic & Value Added', hindi_name='जैविक एवं प्रसंस्कृत उत्पाद', icon='fa-jar', description='Organic Jaggery, Desi Cow Ghee, Raw Wild Honey, Green Tea')

        db.session.add_all([cat_cereals, cat_veggies, cat_fruits, cat_pulses, cat_cash, cat_spices, cat_organic])
        db.session.flush()

        # 2. Seed Master Products (30+ diverse commodities)
        products_list = [
            # Cereals
            Product(category_id=cat_cereals.id, name='Sharbati Wheat', hindi_name='शरबती गेहूं', default_unit='kg', estimated_mandi_rate=26.50),
            Product(category_id=cat_cereals.id, name='Basmati Rice (1121)', hindi_name='बासमती चावल (1121)', default_unit='kg', estimated_mandi_rate=42.00),
            Product(category_id=cat_cereals.id, name='Sona Masoori Rice', hindi_name='सोना मसूरी चावल', default_unit='kg', estimated_mandi_rate=36.00),
            Product(category_id=cat_cereals.id, name='Yellow Maize / Corn', hindi_name='पीली मक्का', default_unit='kg', estimated_mandi_rate=19.50),
            Product(category_id=cat_cereals.id, name='Pearl Millet (Bajra)', hindi_name='बाजरा', default_unit='kg', estimated_mandi_rate=22.00),
            Product(category_id=cat_cereals.id, name='Sorghum (Jowar)', hindi_name='ज्वार', default_unit='kg', estimated_mandi_rate=28.00),
            # Vegetables
            Product(category_id=cat_veggies.id, name='Nashik Red Onion', hindi_name='नासिक लाल प्याज', default_unit='kg', estimated_mandi_rate=21.00),
            Product(category_id=cat_veggies.id, name='Hybrid Tomato', hindi_name='टमाटर', default_unit='kg', estimated_mandi_rate=16.00),
            Product(category_id=cat_veggies.id, name='Pukhraj Potato', hindi_name='आलू', default_unit='kg', estimated_mandi_rate=18.00),
            Product(category_id=cat_veggies.id, name='Garlic (Lahsun)', hindi_name='लहसुन', default_unit='kg', estimated_mandi_rate=95.00),
            Product(category_id=cat_veggies.id, name='Fresh Ginger (Adrak)', hindi_name='ताजा अदरक', default_unit='kg', estimated_mandi_rate=65.00),
            Product(category_id=cat_veggies.id, name='Green Chilli', hindi_name='हरी मिर्च', default_unit='kg', estimated_mandi_rate=45.00),
            Product(category_id=cat_veggies.id, name='Cauliflower (Phool Gobi)', hindi_name='फूलगोभी', default_unit='kg', estimated_mandi_rate=22.00),
            Product(category_id=cat_veggies.id, name='Green Capsicum', hindi_name='शिमला मिर्च', default_unit='kg', estimated_mandi_rate=38.00),
            Product(category_id=cat_veggies.id, name='Okra / Bhindi', hindi_name='भिंडी', default_unit='kg', estimated_mandi_rate=32.00),
            # Fruits
            Product(category_id=cat_fruits.id, name='Alphonso Mango (Hapus)', hindi_name='हापुस आम', default_unit='dozen', estimated_mandi_rate=450.00),
            Product(category_id=cat_fruits.id, name='Kesar Mango', hindi_name='केसर आम', default_unit='kg', estimated_mandi_rate=80.00),
            Product(category_id=cat_fruits.id, name='Royal Kashmiri Apple', hindi_name='कश्मीरी सेब', default_unit='kg', estimated_mandi_rate=110.00),
            Product(category_id=cat_fruits.id, name='Nagpur Orange (Santra)', hindi_name='नागपुर संतरा', default_unit='kg', estimated_mandi_rate=40.00),
            Product(category_id=cat_fruits.id, name='Robusta Banana', hindi_name='केला', default_unit='dozen', estimated_mandi_rate=35.00),
            Product(category_id=cat_fruits.id, name='Thompson Grapes', hindi_name='अंगूर', default_unit='kg', estimated_mandi_rate=55.00),
            Product(category_id=cat_fruits.id, name='Bhagwa Pomegranate (Anar)', hindi_name='अनार (भगवा)', default_unit='kg', estimated_mandi_rate=90.00),
            # Pulses
            Product(category_id=cat_pulses.id, name='Chana (Desi Chickpea)', hindi_name='चना', default_unit='kg', estimated_mandi_rate=58.00),
            Product(category_id=cat_pulses.id, name='Kabuli Chana (Dollar)', hindi_name='काबुली चना', default_unit='kg', estimated_mandi_rate=115.00),
            Product(category_id=cat_pulses.id, name='Toor Dal (Arhar)', hindi_name='तुअर दाल / अरहर', default_unit='kg', estimated_mandi_rate=110.00),
            Product(category_id=cat_pulses.id, name='Green Moong Dal', hindi_name='मूंग दाल', default_unit='kg', estimated_mandi_rate=88.00),
            Product(category_id=cat_pulses.id, name='Black Urad Dal', hindi_name='उड़द दाल', default_unit='kg', estimated_mandi_rate=84.00),
            # Cash Crops & Oilseeds
            Product(category_id=cat_cash.id, name='Yellow Soybean', hindi_name='सोयाबीन', default_unit='kg', estimated_mandi_rate=46.00),
            Product(category_id=cat_cash.id, name='Mustard Seed (Sarson)', hindi_name='सरसों', default_unit='kg', estimated_mandi_rate=54.00),
            Product(category_id=cat_cash.id, name='Raw Shankar Cotton', hindi_name='कपास (शंकर)', default_unit='quintal', estimated_mandi_rate=7200.00),
            Product(category_id=cat_cash.id, name='Groundnut (Peanut)', hindi_name='मूंगफली', default_unit='kg', estimated_mandi_rate=62.00),
            # Spices
            Product(category_id=cat_spices.id, name='Guntur Dry Red Chilli', hindi_name='गुंटूर सूखी लाल मिर्च', default_unit='kg', estimated_mandi_rate=185.00),
            Product(category_id=cat_spices.id, name='Salem Turmeric Finger', hindi_name='हल्दी गांठ', default_unit='kg', estimated_mandi_rate=140.00),
            Product(category_id=cat_spices.id, name='Unjha Cumin (Jeera)', hindi_name='जीरा', default_unit='kg', estimated_mandi_rate=260.00),
            Product(category_id=cat_spices.id, name='Idukki Green Cardamom', hindi_name='हरी इलायची', default_unit='kg', estimated_mandi_rate=1650.00),
            # Organic & Value-Added
            Product(category_id=cat_organic.id, name='Organic Solid Jaggery (Gur)', hindi_name='जैविक गुड़', default_unit='kg', estimated_mandi_rate=55.00),
            Product(category_id=cat_organic.id, name='Pure A2 Desi Cow Ghee', hindi_name='शुद्ध देसी गाय का घी', default_unit='liter', estimated_mandi_rate=950.00)
        ]
        db.session.add_all(products_list)
        db.session.flush()

        # 3. Seed Users & Diverse Farmer Profiles across Indian States
        farmers_data = [
            ('FK-2026-1001', '9876543210', 'Ramesh Patil', 'Village Dindori, Nashik Road', 'Nashik', 'Maharashtra', '422004', 'Patil Organic Agro Farm', 20.0063, 73.7900, 6.5, 'Sharbati Wheat, Red Onion, Hybrid Tomato, Thompson Grapes', 4.9, 34),
            ('FK-2026-1002', '9876543211', 'Gurpreet Singh', 'Khanna Tehsil, GT Road', 'Ludhiana', 'Punjab', '141401', 'Golden Harvest Farms', 30.9010, 75.8573, 14.0, 'Basmati Rice (1121), Sharbati Wheat, Mustard Seed', 4.8, 26),
            ('FK-2026-1003', '9876543212', 'Ravi Kumar Reddy', 'Tenali Road, Guntur Rural', 'Guntur', 'Andhra Pradesh', '522002', 'Reddy Spices & Cotton Estate', 16.3067, 80.4365, 9.0, 'Guntur Dry Red Chilli, Shankar Cotton, Salem Turmeric Finger', 4.9, 41),
            ('FK-2026-1004', '9876543213', 'Kailash Sharma', 'Sanwer Road, Malwa Agro Belt', 'Indore', 'Madhya Pradesh', '452001', 'Malwa Gold Farms', 22.7196, 75.8577, 8.5, 'Yellow Soybean, Garlic, Pukhraj Potato, Kabuli Chana', 4.7, 19),
            ('FK-2026-1005', '9876543214', 'Mohammad Irfan', 'Apple Valley, Sopore', 'Baramulla', 'Jammu & Kashmir', '193201', 'Kashmir Valley Orchards', 34.2986, 74.4682, 5.0, 'Royal Kashmiri Apple, Walnut, Saffron', 5.0, 52),
            ('FK-2026-1006', '9876543215', 'Rajesh Patel', 'Talala Gir, Somnath Highway', 'Junagadh', 'Gujarat', '362001', 'Gir Kesar Organic Farm', 21.5222, 70.4579, 11.0, 'Kesar Mango, Groundnut (Peanut), Unjha Cumin (Jeera)', 4.9, 38),
            ('FK-2026-1007', '9876543216', 'Devendra Verma', 'Fatehabad Road, Khandauli', 'Agra', 'Uttar Pradesh', '282001', 'Verma Agro Plantation', 27.1767, 78.0081, 7.0, 'Pukhraj Potato, Mustard Seed, Green Cauliflower', 4.6, 15),
            ('FK-2026-1008', '9876543217', 'Suresh Naidu', 'Tirthahalli Agro Belt', 'Shimoga', 'Karnataka', '577201', 'Sahyadri Organic Plantation', 13.9299, 75.5681, 6.0, 'Organic Solid Jaggery, Idukki Green Cardamom, Black Pepper', 4.9, 29)
        ]

        farmer_users = []
        for cid, phone, name, addr, dist, state, pin, farm_name, lat, lng, acres, crops, rating, revs in farmers_data:
            u = User(
                custom_id=cid, phone=phone, name=name, role='farmer', preferred_language='en',
                is_verified=True, verification_status='approved', gov_id_type='Aadhaar / KCC',
                gov_id_masked=f'XXXX-XXXX-{phone[-4:]}'
            )
            u.set_password('farmer123')
            db.session.add(u)
            db.session.flush()
            farmer_users.append(u)

            fp = FarmerProfile(
                user_id=u.id, address=addr, district=dist, state=state, pincode=pin,
                farm_location_name=farm_name, farm_latitude=lat, farm_longitude=lng,
                google_maps_link=f'https://maps.google.com/?q={lat},{lng}',
                farm_size_acres=acres, crops_grown=crops, share_phone_consent=True,
                rating=rating, total_reviews=revs
            )
            db.session.add(fp)

        # 4. Seed Buyers & Profiles
        buyers_data = [
            ('BK-2026-2001', '9876543220', 'Suresh Aggarwal', 'Aggarwal Fresh Agro Wholesale', 'Wholesale Trader', '27AABCU9603R1ZM', 'APMC Market Yard 2, Vashi', 'Mumbai', 'Maharashtra', '400703', 4.9, 45),
            ('BK-2026-2002', '9876543221', 'Anita Deshmukh', 'Sahyadri Agro Processing & Retail', 'Retail Chain & Food Processor', '27BBRTU4412Q1ZX', 'Gultekdi APMC Market', 'Pune', 'Maharashtra', '411037', 4.8, 31),
            ('BK-2026-2003', '9876543222', 'Vikramaditya Singhania', 'Global Foods Export Corp', 'Exporter / Bulk Procurer', '07AACCG8821P1ZK', 'Azadpur Mandi Commercial Block B', 'Delhi', 'Delhi', '110033', 5.0, 68),
            ('BK-2026-2004', '9876543223', 'Priya Ramanathan', 'South India Organic Supermarkets', 'Apartment Buying Club / Retail', '29AABCS1234M1ZL', 'Yeshwanthpur Wholesale Hub', 'Bengaluru', 'Karnataka', '560022', 4.9, 22),
            ('BK-2026-2005', '9876543224', 'Manish Shah', 'Gujarat Spices & Oil Millers', 'Processor & Miller', '24AAACT7721N1ZO', 'Kalupur Grain Market', 'Ahmedabad', 'Gujarat', '380001', 4.7, 18)
        ]

        buyer_users = []
        for cid, phone, name, bname, btype, gstin, addr, dist, state, pin, rating, revs in buyers_data:
            u = User(
                custom_id=cid, phone=phone, name=name, role='buyer', preferred_language='en',
                is_verified=True, verification_status='approved', gov_id_type='GSTIN',
                gov_id_masked=f'XXXX-XXXX-{phone[-4:]}'
            )
            u.set_password('buyer123')
            db.session.add(u)
            db.session.flush()
            buyer_users.append(u)

            bp = BuyerProfile(
                user_id=u.id, business_name=bname, business_type=btype, gst_number=gstin,
                address=addr, district=dist, state=state, pincode=pin, share_phone_consent=True,
                rating=rating, total_reviews=revs
            )
            db.session.add(bp)

        # Admin User
        admin1 = User(
            custom_id='ADM-2026-001', phone='9876543230', name='Dr. Ashok Mehta (District Agri Officer)',
            role='admin', preferred_language='en', is_verified=True, verification_status='approved'
        )
        admin1.set_password('admin123')
        db.session.add(admin1)
        db.session.flush()

        # 5. Seed Comprehensive Live Mandi Rates (25+ mandis across India)
        mandi_data = [
            ('Maharashtra', 'Nashik', 'Nashik APMC Mandi', 'Sharbati Wheat', 2550, 2750, 2650, 'Quintal', 'up', 1.8),
            ('Maharashtra', 'Nashik', 'Lasalgaon Mandi (Asia Largest Onion Hub)', 'Red Onion', 1900, 2300, 2100, 'Quintal', 'up', 4.2),
            ('Maharashtra', 'Nashik', 'Pimpalgaon Baswant', 'Thompson Grapes', 5000, 6200, 5600, 'Quintal', 'up', 2.5),
            ('Maharashtra', 'Nagpur', 'Nagpur Fruit Yard', 'Nagpur Orange (Santra)', 3600, 4400, 4000, 'Quintal', 'down', 1.1),
            ('Maharashtra', 'Solapur', 'Solapur Mandi', 'Bhagwa Pomegranate (Anar)', 8200, 9800, 9000, 'Quintal', 'up', 3.0),
            ('Punjab', 'Ludhiana', 'Ludhiana Grain Mandi', 'Sharbati Wheat', 2580, 2720, 2680, 'Quintal', 'stable', 0.0),
            ('Punjab', 'Karnal', 'Karnal Basmati Exchange', 'Basmati Rice (1121)', 4000, 4500, 4250, 'Quintal', 'up', 1.5),
            ('Andhra Pradesh', 'Guntur', 'Guntur Mirchi Yard', 'Guntur Dry Red Chilli', 17500, 19800, 18500, 'Quintal', 'up', 5.4),
            ('Andhra Pradesh', 'Guntur', 'Tenali Cotton Market', 'Raw Shankar Cotton', 7000, 7500, 7250, 'Quintal', 'up', 0.8),
            ('Madhya Pradesh', 'Indore', 'Indore Choithram Mandi', 'Hybrid Tomato', 1400, 1800, 1600, 'Quintal', 'down', 2.1),
            ('Madhya Pradesh', 'Indore', 'Indore Oilseed Mandi', 'Yellow Soybean', 4400, 4800, 4600, 'Quintal', 'up', 1.2),
            ('Madhya Pradesh', 'Mandsaur', 'Mandsaur Garlic Mandi', 'Garlic (Lahsun)', 9000, 10500, 9600, 'Quintal', 'up', 6.0),
            ('Jammu & Kashmir', 'Baramulla', 'Sopore Fruit Mandi', 'Royal Kashmiri Apple', 10000, 12500, 11200, 'Quintal', 'up', 2.8),
            ('Gujarat', 'Junagadh', 'Talala Gir Market', 'Kesar Mango', 7500, 9000, 8200, 'Quintal', 'up', 3.5),
            ('Gujarat', 'Unjha', 'Unjha Spices Mandi', 'Unjha Cumin (Jeera)', 24500, 27800, 26000, 'Quintal', 'up', 4.0),
            ('Gujarat', 'Rajkot', 'Rajkot Yard', 'Groundnut (Peanut)', 5900, 6500, 6200, 'Quintal', 'up', 1.0),
            ('Uttar Pradesh', 'Agra', 'Agra Veg & Potato Hub', 'Pukhraj Potato', 1650, 1950, 1800, 'Quintal', 'stable', 0.0),
            ('Uttar Pradesh', 'Mathura', 'Mathura Oilseed Mandi', 'Mustard Seed (Sarson)', 5200, 5700, 5450, 'Quintal', 'up', 1.6),
            ('Karnataka', 'Bengaluru', 'Yeshwanthpur Wholesale Yard', 'Robusta Banana', 3000, 3800, 3500, 'Quintal', 'stable', 0.0),
            ('Karnataka', 'Shimoga', 'Shimoga Arecanut & Jaggery Mandi', 'Organic Solid Jaggery', 5100, 5800, 5500, 'Quintal', 'up', 2.0),
            ('Kerala', 'Idukki', 'Spices Board Auction Centre', 'Idukki Green Cardamom', 155000, 178000, 165000, 'Quintal', 'up', 3.8),
            ('Tamil Nadu', 'Salem', 'Salem Turmeric Complex', 'Salem Turmeric Finger', 13200, 14800, 14000, 'Quintal', 'up', 2.2),
            ('Delhi', 'Delhi', 'Azadpur Mandi Asia No.1', 'Red Onion', 2000, 2400, 2200, 'Quintal', 'up', 3.0),
            ('Rajasthan', 'Bikaner', 'Bikaner Krishi Upaj Mandi', 'Pearl Millet (Bajra)', 2100, 2350, 2220, 'Quintal', 'up', 0.5)
        ]
        for st, dist, mkt, comm, min_p, max_p, mod_p, unit, trend, pct in mandi_data:
            mr = MandiRate(
                state=st, district=dist, market_name=mkt, commodity=comm,
                min_price=min_p, max_price=max_p, modal_price=mod_p,
                unit=unit, trend=trend, price_change_pct=pct
            )
            db.session.add(mr)

        # 6. Seed Diverse Farmer Active Inventories (18+ items across India)
        inventories_data = [
            # Farmer 1 (Ramesh Patil - Nashik)
            (farmer_users[0].id, 'Sharbati Wheat', 'Cereals & Grains', 6000.0, 'kg', 25.5, 'Grade A (Premium)', 'Nashik', 'Maharashtra', 'Export-grade machine-cleaned Sharbati wheat, 0% moisture, direct harvest from organic farm.'),
            (farmer_users[0].id, 'Red Onion', 'Vegetables', 8500.0, 'kg', 20.0, 'Grade A (Premium)', 'Nashik', 'Maharashtra', 'Famous Lasalgaon medium-large dark red onions, cured for 3-month shelf life.'),
            (farmer_users[0].id, 'Hybrid Tomato', 'Vegetables', 3200.0, 'kg', 15.0, 'Grade A', 'Nashik', 'Maharashtra', 'Firm, ripe red table tomatoes harvested at breaker stage for zero damage in transit.'),
            (farmer_users[0].id, 'Thompson Grapes', 'Fruits & Orchards', 2500.0, 'kg', 54.0, 'Export Quality', 'Nashik', 'Maharashtra', 'Sweet seedless table grapes with high brix sweetness index and export grading.'),

            # Farmer 2 (Gurpreet Singh - Punjab)
            (farmer_users[1].id, 'Basmati Rice (1121)', 'Cereals & Grains', 12000.0, 'kg', 41.0, 'Grade A (Premium)', 'Ludhiana', 'Punjab', 'Aged 1-year authentic 1121 Extra Long Grain Basmati, aroma certified.'),
            (farmer_users[1].id, 'Sharbati Wheat', 'Cereals & Grains', 15000.0, 'kg', 25.0, 'Grade A', 'Ludhiana', 'Punjab', 'Golden lustrous wheat grains from fertile canal-fed fields.'),
            (farmer_users[1].id, 'Mustard Seed (Sarson)', 'Oilseeds & Cash Crops', 4500.0, 'kg', 53.0, 'Grade A (High Oil)', 'Ludhiana', 'Punjab', 'Black mustard seeds with >42% natural oil content.'),

            # Farmer 3 (Ravi Kumar Reddy - Guntur, AP)
            (farmer_users[2].id, 'Guntur Dry Red Chilli', 'Spices & Herbs', 4000.0, 'kg', 180.0, 'Export Quality', 'Guntur', 'Andhra Pradesh', 'Sun-dried Teja & S17 Guntur Red Chillies with deep red colour and high pungency.'),
            (farmer_users[2].id, 'Raw Shankar Cotton', 'Oilseeds & Cash Crops', 50.0, 'quintal', 7100.0, 'Grade A (29mm staple)', 'Guntur', 'Andhra Pradesh', 'Long staple white Shankar-6 cotton with low trash content.'),
            (farmer_users[2].id, 'Salem Turmeric Finger', 'Spices & Herbs', 3500.0, 'kg', 135.0, 'Certified Organic', 'Guntur', 'Andhra Pradesh', 'High curcumin (>5.2%) double-polished turmeric fingers.'),

            # Farmer 4 (Kailash Sharma - Indore, MP)
            (farmer_users[3].id, 'Yellow Soybean', 'Oilseeds & Cash Crops', 8000.0, 'kg', 45.0, 'Grade A', 'Indore', 'Madhya Pradesh', 'Cleaned non-GMO yellow soybean with high protein yield.'),
            (farmer_users[3].id, 'Garlic (Lahsun)', 'Vegetables', 2800.0, 'kg', 92.0, 'Grade A (Bold Cloves)', 'Indore', 'Madhya Pradesh', 'Bold white cloves, cured and packed in breathable net bags.'),
            (farmer_users[3].id, 'Pukhraj Potato', 'Vegetables', 10000.0, 'kg', 17.5, 'Grade A', 'Indore', 'Madhya Pradesh', 'Freshly dug large table potatoes suitable for retail and chips making.'),

            # Farmer 5 (Mohammad Irfan - Kashmir)
            (farmer_users[4].id, 'Royal Kashmiri Apple', 'Fruits & Orchards', 5000.0, 'kg', 105.0, 'Premium Orchard Grade', 'Baramulla', 'Jammu & Kashmir', 'Crisp, crimson red Delicious apples from Sopore valley orchards.'),

            # Farmer 6 (Rajesh Patel - Junagadh, Gujarat)
            (farmer_users[5].id, 'Kesar Mango', 'Fruits & Orchards', 3000.0, 'kg', 78.0, 'GI Tagged Organic', 'Junagadh', 'Gujarat', 'Naturally ripened sweet Gir Kesar mangoes with authentic GI tag.'),
            (farmer_users[5].id, 'Groundnut (Peanut)', 'Oilseeds & Cash Crops', 6000.0, 'kg', 60.0, 'Grade A (Bold)', 'Junagadh', 'Gujarat', 'Cleaned bold shell groundnuts from Saurashtra.'),
            (farmer_users[5].id, 'Unjha Cumin (Jeera)', 'Spices & Herbs', 2000.0, 'kg', 255.0, 'Machine Cleaned 99.5%', 'Junagadh', 'Gujarat', 'Aromatic machine cleaned cumin seeds ready for direct packaging.'),

            # Farmer 7 (Devendra Verma - Agra, UP)
            (farmer_users[6].id, 'Green Capsicum', 'Vegetables', 1500.0, 'kg', 36.0, 'Grade A', 'Agra', 'Uttar Pradesh', 'Crisp polyhouse green bell peppers, zero pest blemish.'),

            # Farmer 8 (Suresh Naidu - Shimoga, Karnataka)
            (farmer_users[7].id, 'Organic Solid Jaggery', 'Organic & Value Added', 3000.0, 'kg', 52.0, 'Chemical-Free Natural', 'Shimoga', 'Karnataka', 'Pure natural sugarcane jaggery prepared without chemical clarifiers.'),
            (farmer_users[7].id, 'Idukki Green Cardamom', 'Spices & Herbs', 600.0, 'kg', 1600.0, '8mm Bold Green', 'Shimoga', 'Karnataka', 'Sun-cured 8mm bold green cardamom pods with intense aroma.')
        ]

        inv_objects = []
        for fid, pname, cat, qty, unit, price, grade, dist, st, desc in inventories_data:
            inv = Inventory(
                farmer_id=fid, product_name=pname, category_name=cat, available_quantity=qty,
                unit=unit, expected_price_per_unit=price, quality_grade=grade,
                location_district=dist, location_state=st, description=desc, status='available'
            )
            db.session.add(inv)
            inv_objects.append(inv)
        db.session.flush()

        # 7. Seed Active Buyer Requirements (Spot & Pre-Orders)
        reqs_data = [
            (buyer_users[0].id, 'Red Onion', 5000.0, 'kg', 'Grade A (Premium)', 19.5, 'APMC Market Yard 2, Vashi', 'Mumbai', 'Maharashtra', False, '', 'Standard 50kg gunny bag packaging required for wholesale yard distribution.'),
            (buyer_users[0].id, 'Sharbati Wheat', 4000.0, 'kg', 'Grade A', 25.0, 'APMC Market Yard 2, Vashi', 'Mumbai', 'Maharashtra', False, '', 'Requirement for retail packaging mill.'),
            (buyer_users[1].id, 'Hybrid Tomato', 3000.0, 'kg', 'Grade A', 14.5, 'Gultekdi APMC Market', 'Pune', 'Maharashtra', False, '', 'Looking for daily supply of 3 MT firm tomatoes for supermarket delivery.'),
            (buyer_users[2].id, 'Basmati Rice (1121)', 10000.0, 'kg', 'Export Quality', 40.0, 'Azadpur Mandi Commercial Block B', 'Delhi', 'Delhi', True, 'Nov 2026 Harvest Season', 'Pre-order contract for Gulf export consignment. 25% Advance on sowing confirmation.'),
            (buyer_users[2].id, 'Guntur Dry Red Chilli', 2500.0, 'kg', 'Export Quality', 182.0, 'Azadpur Mandi Block B', 'Delhi', 'Delhi', False, '', 'Export grade Teja chillies needed with lab moisture certificate.'),
            (buyer_users[3].id, 'Alphonso Mango', 200.0, 'dozen', 'Grade A (Organic)', 420.0, 'Yeshwanthpur Wholesale Hub', 'Bengaluru', 'Karnataka', True, 'April 2026 Harvest Season', 'Pre-order for apartment consumer club in Bangalore.'),
            (buyer_users[4].id, 'Yellow Soybean', 15000.0, 'kg', 'Grade A', 44.5, 'Kalupur Grain Market', 'Ahmedabad', 'Gujarat', False, '', 'Bulk supply for solvent extraction oil plant.')
        ]

        req_objects = []
        for bid, pname, qty, unit, qual, price, loc, dist, st, is_pre, timeline, notes in reqs_data:
            req = Requirement(
                buyer_id=bid, product_name=pname, required_quantity=qty, unit=unit,
                required_quality=qual, target_price_per_unit=price, delivery_location=loc,
                delivery_district=dist, delivery_state=st, is_pre_order=is_pre,
                target_harvest_timeline=timeline, additional_notes=notes, status='open'
            )
            db.session.add(req)
            req_objects.append(req)
        db.session.flush()

        # 8. Seed Negotiation Offers, Counter-Offers, and Deals
        # Offer 1: Countered offer awaiting buyer review
        offer1 = Offer(
            requirement_id=req_objects[0].id,
            inventory_id=inv_objects[1].id,
            buyer_id=buyer_users[0].id,
            farmer_id=farmer_users[0].id,
            product_name='Red Onion',
            quantity=3000.0,
            unit='kg',
            offered_price_per_unit=19.5,
            total_amount=60000.0,
            offered_by_role='farmer',
            status='countered',
            counter_price_per_unit=20.0,
            counter_quantity=3000.0,
            counter_notes='Offered ₹20.00/kg for top-tier cured Lasalgaon Red Onions.',
            last_action_by='farmer'
        )

        # Offer 2: Confirmed and converted to Order
        offer2 = Offer(
            requirement_id=req_objects[1].id,
            inventory_id=inv_objects[0].id,
            buyer_id=buyer_users[0].id,
            farmer_id=farmer_users[0].id,
            product_name='Sharbati Wheat',
            quantity=2500.0,
            unit='kg',
            offered_price_per_unit=25.5,
            total_amount=63750.0,
            offered_by_role='buyer',
            status='accepted',
            last_action_by='farmer'
        )

        db.session.add_all([offer1, offer2])
        db.session.flush()

        # 9. Seed Confirmed Order with Active Delivery & Escrow
        order1 = Order(
            order_code='ORD-2026-8801',
            offer_id=offer2.id,
            inventory_id=inv_objects[0].id,
            buyer_id=buyer_users[0].id,
            farmer_id=farmer_users[0].id,
            product_name='Sharbati Wheat',
            quantity=2500.0,
            unit='kg',
            agreed_price_per_unit=25.5,
            total_amount=63750.0,
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
            vehicle_type='Mini Truck (Tata Ace 2 Ton)',
            transport_partner_name='Kisan Express Green Logistics',
            driver_name='Ramesh Shinde',
            driver_phone='+91 98231 44556',
            vehicle_number='MH-15-EG-4402',
            pickup_otp='4819',
            delivery_otp='7294',
            estimated_cost=2100.0,
            current_status='in_transit',
            current_location='Igatpuri Ghat Tollway Checkpoint',
            estimated_arrival='Tomorrow by 09:30 AM',
            tracking_notes='Produce loaded with temperature and moisture sensor active.'
        )
        db.session.add(deliv1)

        # 10. Seed Negotiation Chat Thread & Messages
        chat1 = ChatThread(
            farmer_id=farmer_users[0].id,
            buyer_id=buyer_users[0].id,
            order_id=order1.id,
            offer_id=offer2.id,
            subject_product='Sharbati Wheat & Red Onion Trade'
        )
        db.session.add(chat1)
        db.session.flush()

        msg1 = Message(thread_id=chat1.id, sender_id=buyer_users[0].id, message_text="Namaste Ramesh ji! We need 2,500 kg Sharbati Wheat for our Vashi wholesale distribution. Can you dispatch by tomorrow?")
        msg2 = Message(thread_id=chat1.id, sender_id=farmer_users[0].id, message_text="Namaste Suresh ji. Yes, our wheat is machine-cleaned with 0% moisture. Mandi benchmark is ₹26.50, I will supply direct at ₹25.50/kg.")
        msg3 = Message(thread_id=chat1.id, sender_id=buyer_users[0].id, message_text="Deal agreed at ₹25.50/kg! Confirmed order created with escrow security.")
        msg4 = Message(
            thread_id=chat1.id, sender_id=farmer_users[0].id,
            message_text="📞 Ramesh Patil shared their direct contact: +91 9876543210",
            message_type='phone_shared',
            metadata_json='{"phone": "+91 9876543210", "shared_by": "Ramesh Patil"}'
        )
        db.session.add_all([msg1, msg2, msg3, msg4])

        # 11. Seed Cold Storage Facilities (6+ across states)
        cold_storages = [
            ColdStorage(
                name='Kisan Shetkari Sahakari Cold Storage', operator_name='Nashik District Farmers Cooperative',
                contact_phone='+91 94220 11223', address='Pimpalgaon Baswant Road', district='Nashik', state='Maharashtra',
                total_capacity_mt=5000.0, available_capacity_mt=1850.0, approx_charge_per_month_per_quintal=65.0,
                temp_range_celsius='0°C to 4°C (Controlled Humidity)', supported_produce='Potato, Onion, Grapes, Apples, Carrots',
                facilities='Solar Cold Backup, Automated Pre-cooling, 24/7 CCTV, Loading Ramp', is_verified=True, is_active=True
            ),
            ColdStorage(
                name='Punjab Agro Logistics & Cold Chain', operator_name='Punjab State Cooperative',
                contact_phone='+91 98140 22334', address='GT Road, Khanna', district='Ludhiana', state='Punjab',
                total_capacity_mt=8000.0, available_capacity_mt=3200.0, approx_charge_per_month_per_quintal=58.0,
                temp_range_celsius='-2°C to 2°C (Preservation Grade)', supported_produce='Potato, Peas, Cauliflower, Apple',
                facilities='Multi-chamber temperature zones, Generator backup', is_verified=True, is_active=True
            ),
            ColdStorage(
                name='Malwa Krishi Cold Storage', operator_name='Malwa Agri Traders',
                contact_phone='+91 98260 33445', address='Sanwer Road Industrial Area', district='Indore', state='Madhya Pradesh',
                total_capacity_mt=6000.0, available_capacity_mt=2100.0, approx_charge_per_month_per_quintal=60.0,
                temp_range_celsius='1°C to 4°C', supported_produce='Potato, Garlic, Onion, Ginger',
                facilities='Air-conditioned sorting hall, CCTV', is_verified=True, is_active=True
            ),
            ColdStorage(
                name='Kashmir Valley CA Atmosphere Storage', operator_name='J&K Horticultural Produce Marketing',
                contact_phone='+91 94190 55667', address='Industrial Growth Centre, Lassipora', district='Baramulla', state='Jammu & Kashmir',
                total_capacity_mt=10000.0, available_capacity_mt=4500.0, approx_charge_per_month_per_quintal=85.0,
                temp_range_celsius='-0.5°C to 1°C (Controlled Atmosphere)', supported_produce='Apple, Pear, Walnut, Cherry',
                facilities='CA Nitrogen flush chambers, Automatic grading lines', is_verified=True, is_active=True
            ),
            ColdStorage(
                name='Guntur Spices & Agro Cold Depot', operator_name='Guntur Agro Logistics',
                contact_phone='+91 98480 77889', address='Autonagar Spices Yard', district='Guntur', state='Andhra Pradesh',
                total_capacity_mt=7000.0, available_capacity_mt=2800.0, approx_charge_per_month_per_quintal=70.0,
                temp_range_celsius='4°C to 8°C (Dehumidified)', supported_produce='Dry Red Chilli, Turmeric, Tamarind',
                facilities='Anti-fungal fumigation, High stack forklifts', is_verified=True, is_active=True
            )
        ]
        db.session.add_all(cold_storages)

        # 12. Seed Marketplace Farm Supplies & Inputs
        market_products = [
            MarketplaceProduct(category='Seeds', title='Certified Hybrid Sharbati Wheat Seeds (PBW 550)', brand='National Seeds Corp', description='Disease resistant high-yield wheat seeds with 95% certified germination rate.', price=1250.0, unit='bag / 40kg', is_available=True),
            MarketplaceProduct(category='Seeds', title='Certified 1121 Pusa Basmati Paddy Seed', brand='IARI Pusa', description='High aroma, disease-tolerant long grain certified paddy seeds.', price=1650.0, unit='bag / 30kg', is_available=True),
            MarketplaceProduct(category='Fertilizers', title='Organic Neem Coated Urea & Bio-NPK (19:19:19)', brand='IFFCO Agro', description='Water soluble balanced plant nutrition for healthy vegetative growth and soil health.', price=850.0, unit='bag / 50kg', is_available=True),
            MarketplaceProduct(category='Fertilizers', title='Granulated Organic Vermicompost Fertilizer', brand='Krishi Bio Compost', description='100% pure cow dung vermicompost enriched with beneficial microbes.', price=450.0, unit='bag / 50kg', is_available=True),
            MarketplaceProduct(category='Equipment', title='Battery Powered 16L Backpack Knapsack Sprayer', brand='Krishi Power', description='Rechargeable 12V lithium-ion battery sprayer with adjustable brass nozzles.', price=2400.0, unit='piece', is_available=True),
            MarketplaceProduct(category='Equipment', title='Digital Soil NPK & Moisture Testing Meter', brand='AgroSense Labs', description='Handheld 4-in-1 digital sensor for instant soil pH, moisture, temperature and NPK reading.', price=1850.0, unit='piece', is_available=True),
            MarketplaceProduct(category='Irrigation', title='Automatic Inline Drip Irrigation Kit (1 Acre)', brand='Jain Farm Fresh', description='Complete precision drip irrigation kit with pressure-compensating drippers and filter unit.', price=6500.0, unit='kit / 1 acre', is_available=True),
            MarketplaceProduct(category='Solar & Eco', title='Solar Powered Insect Pest Trap (LED Attraction)', brand='Surya Agro Green', description='Automatic dusk-to-dawn solar insect trap reducing pesticide expenditure by 70%.', price=1450.0, unit='unit', is_available=True)
        ]
        db.session.add_all(market_products)

        # 13. Seed Government Schemes
        schemes = [
            GovernmentScheme(
                title='Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
                hindi_title='प्रधानमंत्री किसान सम्मान निधि योजना',
                category='Subsidy & Financial Assistance',
                description='Direct income support of ₹6,000 per year transferred into the bank accounts of all landholding farmer families across India.',
                eligibility_summary='All small and marginal landholding farmer families with bank-linked Aadhaar.',
                benefits_summary='₹6,000 annually paid in 3 equal four-monthly installments of ₹2,000 directly via DBT.',
                application_link='https://pmkisan.gov.in/', launch_year='2019', is_featured=True
            ),
            GovernmentScheme(
                title='Pradhan Mantri Fasal Bima Yojana (PMFBY)',
                hindi_title='प्रधानमंत्री फसल बीमा योजना',
                category='Insurance',
                description='Comprehensive crop insurance providing financial support to farmers suffering crop loss/damage arising out of unforeseen weather events.',
                eligibility_summary='All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.',
                benefits_summary='Low premium rates (2% for Kharif, 1.5% for Rabi crops) with full sum insured coverage.',
                application_link='https://pmfby.gov.in/', launch_year='2016', is_featured=True
            ),
            GovernmentScheme(
                title='PM-KUSUM Solar Agriculture Pump Scheme',
                hindi_title='पीएम कुसुम सौर कृषि पंप योजना',
                category='Solar & Irrigation',
                description='Subsidies for standalone solar agriculture pumps and solarisation of existing grid-connected agriculture pumps.',
                eligibility_summary='Individual farmers, water user associations, and FPOs.',
                benefits_summary='Up to 60% capital subsidy from Central and State Governments for solar pumps.',
                application_link='https://pmkusum.mnre.gov.in/', launch_year='2019', is_featured=True
            ),
            GovernmentScheme(
                title='Agriculture Infrastructure Fund (AIF)',
                hindi_title='कृषि अवसंरचना कोष (AIF)',
                category='Credit & Infrastructure',
                description='Medium-long term debt financing facility for investment in viable projects for post-harvest management infrastructure and community farming assets.',
                eligibility_summary='FPOs, PACS, Agri-entrepreneurs, Startups, and Central/State agencies.',
                benefits_summary='3% per annum interest subvention up to a limit of ₹2 Crore with CGTMSE credit guarantee.',
                application_link='https://agriinfra.dac.gov.in/', launch_year='2020', is_featured=True
            ),
            GovernmentScheme(
                title='Paramparagat Krishi Vikas Yojana (PKVY)',
                hindi_title='परम्परागत कृषि विकास योजना',
                category='Organic Farming',
                description='Promotion of commercial organic farming through certified PGS (Participatory Guarantee System) cluster approach.',
                eligibility_summary='Farmers adopting certified organic cultivation practices in 50-acre clusters.',
                benefits_summary='₹50,000 per hectare financial assistance for organic inputs, certification, and direct marketing.',
                application_link='https://pgsindia-ncof.gov.in/', launch_year='2015', is_featured=True
            )
        ]
        db.session.add_all(schemes)

        # 14. Seed Audit Log
        log1 = AuditLog(
            action='SYSTEM_INITIALIZED',
            details='Krishi Kendra SIH 2026 database initialized with master data, 8 farmers across 8 states, 5 buyers, and 25 live mandi benchmarks.'
        )
        db.session.add(log1)

        db.session.commit()
        print("Seeding completed successfully! 30+ products, 18+ active inventories, 8 farmers, 5 buyers, and 25 mandi benchmarks populated.")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    seed_all_sample_data(app)
