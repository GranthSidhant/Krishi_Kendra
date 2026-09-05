from app.services.mandi_service import MandiService

class DealAnalysisService:
    @staticmethod
    def analyze_offer(commodity_name: str, offered_price_per_unit: float, unit: str = 'kg', farmer_expected_price: float = None, district: str = None) -> dict:
        """
        Evaluates an offer against Mandi benchmarks, transport margin, and farmer expectations.
        Returns score, color badge, recommendation text, and breakdown.
        """
        mandi_info = MandiService.get_rate_for_commodity(commodity_name, district)
        benchmark_rate_kg = mandi_info.get('rate_per_kg', 25.0)
        
        # Standardize offered price to per kg
        offered_rate_kg = offered_price_per_unit
        if unit.lower() == 'quintal':
            offered_rate_kg = round(offered_price_per_unit / 100.0, 2)
        elif unit.lower() == 'ton':
            offered_rate_kg = round(offered_price_per_unit / 1000.0, 2)
            
        diff_pct = ((offered_rate_kg - benchmark_rate_kg) / max(benchmark_rate_kg, 1.0)) * 100
        diff_pct = round(diff_pct, 1)
        
        if diff_pct >= 2.0:
            status = 'good'
            badge_class = 'success'
            tag = '🟢 Good Deal'
            recommendation = f"Great offer! Price (₹{offered_rate_kg}/kg) is {diff_pct}% above the current Mandi average (₹{benchmark_rate_kg}/kg). Recommended to accept."
        elif diff_pct >= -6.0:
            status = 'negotiate'
            badge_class = 'warning text-dark'
            tag = '🟡 Consider Counter-Offer'
            suggested_counter = round(benchmark_rate_kg * 1.05, 2)
            recommendation = f"Fair offer, but slightly below peak Mandi price (₹{benchmark_rate_kg}/kg). Consider sending a counter-offer around ₹{suggested_counter}/kg."
        else:
            status = 'review'
            badge_class = 'danger'
            tag = '🔴 Review Carefully'
            suggested_counter = round(benchmark_rate_kg, 2)
            recommendation = f"Low offer! Price is {abs(diff_pct)}% below the Mandi benchmark (₹{benchmark_rate_kg}/kg). Submitting a counter-offer or rejecting is advised."
            
        return {
            'status': status,
            'badge_class': badge_class,
            'tag': tag,
            'recommendation': recommendation,
            'benchmark_mandi_rate_kg': benchmark_rate_kg,
            'offered_rate_kg': offered_rate_kg,
            'diff_pct': diff_pct,
            'market_name': mandi_info.get('market_name', 'APMC Mandi')
        }
