import random
import datetime
import logging
from app.extensions import db
from app.models import Delivery, Order
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

VEHICLE_PROFILES = {
    'mini_truck': {
        'name': 'Mini Truck (Tata Ace / Mahindra Bolero Maxx)',
        'capacity_mt': 1.5,
        'rate_per_km': 22.0,
        'base_fare': 350.0,
        'temp_controlled': False,
        'recommended_for': ['Vegetables', 'Fruits', 'Grains under 15 Qtl']
    },
    'medium_truck': {
        'name': 'Medium Commercial Truck (Eicher 14ft Pro 2049)',
        'capacity_mt': 4.5,
        'rate_per_km': 38.0,
        'base_fare': 650.0,
        'temp_controlled': False,
        'recommended_for': ['Bulk Wheat', 'Rice', 'Soybean', 'Cotton', 'Potatoes']
    },
    'tractor': {
        'name': 'Tractor Trolley with High-Rise Tarpaulin',
        'capacity_mt': 3.0,
        'rate_per_km': 28.0,
        'base_fare': 400.0,
        'temp_controlled': False,
        'recommended_for': ['Sugarcane', 'Raw Grains', 'Local Mandi Distance']
    },
    'cold_reefer': {
        'name': 'Refrigerated Cold-Chain Reefer Truck (2°C - 8°C)',
        'capacity_mt': 3.5,
        'rate_per_km': 55.0,
        'base_fare': 1200.0,
        'temp_controlled': True,
        'recommended_for': ['Tomatoes', 'Strawberries', 'Exotics', 'Dairy', 'Grapes']
    },
    'self_pickup': {
        'name': 'Buyer Self-Arranged Farm-Gate Mandi Pickup',
        'capacity_mt': 10.0,
        'rate_per_km': 0.0,
        'base_fare': 0.0,
        'temp_controlled': False,
        'recommended_for': ['Direct Buyer Transport']
    }
}

class LogisticsService:
    @staticmethod
    def calculate_freight(vehicle_category: str, distance_km: float = 45.0) -> dict:
        """
        Calculates realistic logistics cost based on vehicle type and mileage.
        """
        profile = VEHICLE_PROFILES.get(vehicle_category, VEHICLE_PROFILES['mini_truck'])
        distance = max(5.0, float(distance_km or 45.0))
        estimated_freight = round(profile['base_fare'] + (distance * profile['rate_per_km']), 2)
        
        return {
            'vehicle_category': vehicle_category,
            'vehicle_name': profile['name'],
            'capacity_mt': profile['capacity_mt'],
            'distance_km': distance,
            'estimated_freight': estimated_freight,
            'temp_controlled': profile['temp_controlled']
        }

    @staticmethod
    def generate_handover_otps() -> tuple:
        """
        Generates 6-digit pickup OTP (for farmer) and delivery OTP (for buyer).
        """
        pickup_otp = f"{random.randint(100000, 999999)}"
        delivery_otp = f"{random.randint(100000, 999999)}"
        return pickup_otp, delivery_otp

    @staticmethod
    def verify_pickup_otp(order_id: int, entered_otp: str) -> dict:
        """
        Validates pickup OTP at the farmer's farm gate and moves delivery to 'in_transit'.
        """
        order = Order.query.get(order_id)
        if not order or not order.delivery:
            return {'success': False, 'error': 'Delivery record not found.'}

        delivery = order.delivery
        entered_clean = str(entered_otp or '').strip()

        if delivery.pickup_otp and delivery.pickup_otp != entered_clean:
            return {'success': False, 'error': 'Invalid Pickup OTP. Please check with the Farmer.'}

        now = datetime.datetime.utcnow()
        delivery.pickup_verified_at = now
        delivery.current_status = 'in_transit'
        delivery.tracking_notes = f"Farm-gate loading verified and dispatched on {now.strftime('%d %b, %I:%M %p')}."
        order.status = 'in_transit'

        NotificationService.send(
            user_id=order.buyer_id,
            title='Produce Picked Up & In Transit!',
            message=f"Order #{order.order_code} was loaded onto {delivery.vehicle_type} and is on its way to your destination.",
            link_url=f"/orders/{order.id}"
        )

        db.session.commit()
        return {'success': True, 'message': 'Pickup verified! Order is now In Transit.'}

    @staticmethod
    def verify_delivery_otp(order_id: int, entered_otp: str) -> dict:
        """
        Validates buyer's delivery OTP after physical weighment & inspection.
        Marks order as 'delivered' and triggers escrow release.
        """
        from app.services.escrow_service import EscrowService

        order = Order.query.get(order_id)
        if not order or not order.delivery:
            return {'success': False, 'error': 'Delivery record not found.'}

        delivery = order.delivery
        entered_clean = str(entered_otp or '').strip()

        if delivery.delivery_otp and delivery.delivery_otp != entered_clean:
            return {'success': False, 'error': 'Invalid Delivery OTP. Please check the OTP sent to the Buyer.'}

        # Release escrow funds to farmer
        payout_res = EscrowService.release_escrow_payout(order_id)
        return {
            'success': True,
            'message': 'Delivery inspected and confirmed! Escrow funds released to Farmer.',
            'payout': payout_res
        }
