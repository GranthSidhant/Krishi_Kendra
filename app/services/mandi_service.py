from app.models import MandiRate, Product
from app.extensions import db

class MandiService:
    @staticmethod
    def get_latest_rates(district=None, commodity=None, limit=20):
        """
        Fetches latest mandi market rates with optional filters.
        """
        query = MandiRate.query
        if district and district.lower() != 'all':
            query = query.filter(MandiRate.district.ilike(f"%{district}%"))
        if commodity and commodity.lower() != 'all':
            query = query.filter(MandiRate.commodity.ilike(f"%{commodity}%"))
            
        return query.order_by(MandiRate.updated_at.desc()).limit(limit).all()

    @staticmethod
    def get_rate_for_commodity(commodity_name: str, district: str = None) -> dict:
        """
        Finds benchmark rate for a commodity to display next to offer inputs.
        Returns modal_price in ₹/kg (standardized from quintal if needed).
        """
        query = MandiRate.query.filter(MandiRate.commodity.ilike(f"%{commodity_name}%"))
        if district:
            specific = query.filter(MandiRate.district.ilike(f"%{district}%")).first()
            if specific:
                rate_per_kg = round(specific.modal_price / 100.0, 2) if specific.unit.lower() == 'quintal' else round(specific.modal_price, 2)
                return {
                    'found': True,
                    'market_name': specific.market_name,
                    'district': specific.district,
                    'rate_per_kg': rate_per_kg,
                    'raw_modal_price': specific.modal_price,
                    'unit': specific.unit,
                    'trend': specific.trend,
                    'date': specific.price_date
                }
        
        # General match
        item = query.first()
        if item:
            rate_per_kg = round(item.modal_price / 100.0, 2) if item.unit.lower() == 'quintal' else round(item.modal_price, 2)
            return {
                'found': True,
                'market_name': item.market_name,
                'district': item.district,
                'rate_per_kg': rate_per_kg,
                'raw_modal_price': item.modal_price,
                'unit': item.unit,
                'trend': item.trend,
                'date': item.price_date
            }
            
        # Fallback default estimate if not in Mandi table yet
        prod = Product.query.filter(Product.name.ilike(f"%{commodity_name}%")).first()
        fallback_rate = prod.estimated_mandi_rate if prod else 25.0
        return {
            'found': False,
            'market_name': 'District APMC Benchmark',
            'district': district or 'State Average',
            'rate_per_kg': fallback_rate,
            'raw_modal_price': fallback_rate * 100,
            'unit': 'Quintal',
            'trend': 'stable',
            'date': 'Today'
        }
