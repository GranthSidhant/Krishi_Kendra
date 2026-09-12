import os
import random
import datetime
import logging
from app.extensions import db
from app.models import Order, Inventory
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

class EscrowService:
    @staticmethod
    def process_escrow_payment(order_id: int, payment_method: str = 'UPI_ESCROW', upi_id: str = None) -> dict:
        """
        Simulates atomic Escrow Funding by the Buyer.
        Locks funds in Krishi Kendra Trust Escrow, deducts farmer's available inventory stock,
        and updates Order status to 'confirmed' with an Escrow Certificate ID.
        """
        order = Order.query.get(order_id)
        if not order:
            return {'success': False, 'error': 'Order not found'}

        now = datetime.datetime.utcnow()
        escrow_txn = f"ESC-TXN-2026-{random.randint(10000, 99999)}"
        order.escrow_txn_id = escrow_txn
        order.payment_method = payment_method or 'UPI_ESCROW'
        order.payment_status = 'in_escrow'
        order.status = 'confirmed'
        order.paid_at = now

        # Auto-deduct Farmer inventory stock if inventory is linked
        stock_deducted = 0
        inv_item = None
        if order.offer and order.offer.inventory_id:
            inv_item = Inventory.query.get(order.offer.inventory_id)
        elif order.inventory_id:
            inv_item = Inventory.query.get(order.inventory_id)
        else:
            # Match by farmer_id and product_name
            inv_item = Inventory.query.filter_by(farmer_id=order.farmer_id, product_name=order.product_name).first()

        if inv_item:
            order.inventory_id = inv_item.id
            if inv_item.available_quantity >= order.quantity:
                inv_item.available_quantity = round(inv_item.available_quantity - order.quantity, 2)
                stock_deducted = order.quantity
                if inv_item.available_quantity <= 0:
                    inv_item.available_quantity = 0
                    inv_item.status = 'sold_out'
            else:
                stock_deducted = inv_item.available_quantity
                inv_item.available_quantity = 0
                inv_item.status = 'sold_out'

        # Notify Farmer that escrow is safely locked
        NotificationService.send(
            user_id=order.farmer_id,
            title='Escrow Payment Locked (₹' + f"{order.total_amount:,.2f})",
            message=f"Buyer {order.buyer.name} funded the Smart Escrow ({escrow_txn}) for Order #{order.order_code}. You can safely prepare harvest for dispatch.",
            link_url=f"/orders/{order.id}"
        )

        db.session.commit()

        return {
            'success': True,
            'escrow_txn_id': escrow_txn,
            'total_amount': order.total_amount,
            'payment_status': 'in_escrow',
            'stock_deducted': stock_deducted,
            'paid_at': now.strftime('%d %b %Y, %I:%M %p')
        }

    @staticmethod
    def release_escrow_payout(order_id: int) -> dict:
        """
        Releases locked escrow funds directly to the Farmer's Bank Account / UPI VPA
        after buyer verifies produce quality & weighment.
        """
        order = Order.query.get(order_id)
        if not order:
            return {'success': False, 'error': 'Order not found'}

        now = datetime.datetime.utcnow()
        payout_txn = f"PAYOUT-HDFC-2026-{random.randint(100000, 999999)}"
        order.payout_txn_id = payout_txn
        order.payout_released_at = now
        order.payment_status = 'released'
        order.status = 'delivered'

        if order.delivery:
            order.delivery.current_status = 'delivered'
            order.delivery.delivery_verified_at = now

        # Notify Farmer of instant settlement
        NotificationService.send(
            user_id=order.farmer_id,
            title='Payment Released to Bank Account!',
            message=f"₹{order.total_amount:,.2f} for Order #{order.order_code} was credited directly to your bank account ({payout_txn}).",
            link_url=f"/orders/{order.id}"
        )

        db.session.commit()

        return {
            'success': True,
            'payout_txn_id': payout_txn,
            'amount_released': order.total_amount,
            'released_at': now.strftime('%d %b %Y, %I:%M %p')
        }
