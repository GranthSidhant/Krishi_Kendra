import os
import json
import logging
import datetime
from app.services.mandi_service import MandiService

logger = logging.getLogger(__name__)

# In-memory forecast cache (15-minute TTL)
_forecast_cache = {}

COMMODITY_VOLATILITY_PROFILES = {
    'onion': {'volatility': 0.035, 'perishability': 'medium', 'storage_gain_potential': True, 'storage_rate_day': 0.85},
    'tomato': {'volatility': 0.055, 'perishability': 'high', 'storage_gain_potential': True, 'storage_rate_day': 1.20},
    'potato': {'volatility': 0.025, 'perishability': 'low', 'storage_gain_potential': True, 'storage_rate_day': 0.65},
    'wheat': {'volatility': 0.012, 'perishability': 'none', 'storage_gain_potential': False, 'storage_rate_day': 0.45},
    'rice': {'volatility': 0.010, 'perishability': 'none', 'storage_gain_potential': False, 'storage_rate_day': 0.45},
    'soybean': {'volatility': 0.020, 'perishability': 'none', 'storage_gain_potential': False, 'storage_rate_day': 0.50},
    'cotton': {'volatility': 0.018, 'perishability': 'none', 'storage_gain_potential': False, 'storage_rate_day': 0.50},
    'garlic': {'volatility': 0.040, 'perishability': 'medium', 'storage_gain_potential': True, 'storage_rate_day': 0.90},
    'mustard': {'volatility': 0.015, 'perishability': 'none', 'storage_gain_potential': False, 'storage_rate_day': 0.50}
}

class PriceForecastService:
    @staticmethod
    def get_forecast(commodity: str, district: str = None) -> dict:
        """
        Generates 7-day APMC Mandi price trajectory and cold storage decision ROI analysis.
        """
        commodity_clean = (commodity or 'Wheat').strip().title()
        district_clean = (district or 'Nashik').strip().title()
        cache_key = f"{commodity_clean.lower()}:{district_clean.lower()}"

        if cache_key in _forecast_cache:
            entry = _forecast_cache[cache_key]
            if (datetime.datetime.utcnow() - entry['cached_at']).total_seconds() < 900:
                return entry['data']

        # 1. Fetch current benchmark rate
        mandi_info = MandiService.get_rate_for_commodity(commodity_clean, district_clean)
        current_rate_kg = mandi_info.get('rate_per_kg', 24.0)
        current_price_qtl = round(current_rate_kg * 100.0, 2)
        market_name = mandi_info.get('market_name', f"{district_clean} Mandi")

        # 2. Get Commodity Profile
        prof_key = commodity_clean.lower()
        matched_profile = None
        for k, p in COMMODITY_VOLATILITY_PROFILES.items():
            if k in prof_key:
                matched_profile = p
                break
        if not matched_profile:
            matched_profile = {'volatility': 0.02, 'perishability': 'medium', 'storage_gain_potential': False, 'storage_rate_day': 0.75}

        # 3. Build 7-Day Baseline Trajectory Curve
        today = datetime.datetime.utcnow()
        days_labels = []
        forecast_modal = []
        forecast_min = []
        forecast_max = []

        # Directional trend factor
        base_trend = mandi_info.get('trend', 'stable')
        if base_trend == 'up':
            daily_factor = 1.018 # +1.8% daily
        elif base_trend == 'down':
            daily_factor = 0.985 # -1.5% daily
        else:
            daily_factor = 1.008 # mild positive drift

        current_sim_price = current_price_qtl

        for i in range(7):
            d = today + datetime.timedelta(days=i)
            day_name = d.strftime('%a, %d %b')
            days_labels.append(day_name)

            if i == 0:
                p_modal = current_price_qtl
            else:
                current_sim_price = current_sim_price * (daily_factor + (0.003 if i % 2 == 0 else -0.002))
                p_modal = round(current_sim_price, 1)

            p_min = round(p_modal * (1.0 - matched_profile['volatility']), 1)
            p_max = round(p_modal * (1.0 + matched_profile['volatility']), 1)

            forecast_modal.append(p_modal)
            forecast_min.append(p_min)
            forecast_max.append(p_max)

        day7_price = forecast_modal[-1]
        price_change_pct = round(((day7_price - current_price_qtl) / max(current_price_qtl, 1.0)) * 100, 1)

        # 4. Compute Cold Storage Strategy & Net Financial ROI
        storage_gain_potential = matched_profile.get('storage_gain_potential', False)
        storage_fee_day = matched_profile.get('storage_rate_day', 0.80)
        recommended_storage_days = 10
        total_storage_cost_qtl = round(storage_fee_day * recommended_storage_days, 1)

        # Projected 10-day price
        projected_10day_price = round(current_price_qtl * (1.0 + (price_change_pct * 1.3 / 100.0)), 1)
        gross_gain_qtl = round(projected_10day_price - current_price_qtl, 1)
        net_gain_qtl = round(gross_gain_qtl - total_storage_cost_qtl, 1)

        if price_change_pct >= 5.0 and storage_gain_potential:
            recommendation_code = 'store'
            recommendation_title = '🟢 Hold Produce & Store in Cold Storage'
            recommendation_title_hi = '🟢 फसल को रोकें और कोल्ड स्टोरेज में रखें'
            action_badge = 'HOLD & STORE'
            badge_class = 'success'
            advisory = (
                f"Market supply is projected to tighten over the next 7-10 days, lifting {commodity_clean} prices "
                f"by +{price_change_pct}%. Storing in cold storage (at approx ₹{storage_fee_day}/day/Qtl) will yield an "
                f"estimated Net Extra Profit of +₹{net_gain_qtl}/Quintal after deducting all storage fees."
            )
            advisory_hi = (
                f"अगले 7-10 दिनों में {commodity_clean} के भाव में +{price_change_pct}% की तेजी आने का अनुमान है। "
                f"कोल्ड स्टोरेज (लगभग ₹{storage_fee_day}/दिन/क्विंटल) में रखने पर सारा किराया काटकर प्रति क्विंटल "
                f"+₹{net_gain_qtl} का शुद्ध अतिरिक्त लाभ प्राप्त होगा।"
            )
        elif price_change_pct <= -3.0:
            recommendation_code = 'sell'
            recommendation_title = '🔴 Sell Immediately at Spot Mandi Rate'
            recommendation_title_hi = '🔴 वर्तमान मंडी भाव पर तुरंत बेचें'
            action_badge = 'SELL NOW'
            badge_class = 'danger'
            advisory = (
                f"Upcoming harvest arrivals are projected to create supply pressure, dropping prices by {price_change_pct}%. "
                f"It is recommended to liquidate existing inventory at the current spot benchmark (₹{current_price_qtl}/Qtl) "
                f"rather than incurring holding and perishability depreciation."
            )
            advisory_hi = (
                f"आगामी दिनों में नई फसल की आवक बढ़ने से भाव में {price_change_pct}% की गिरावट का अनुमान है। "
                f"वर्तमान भाव (₹{current_price_qtl}/क्विंटल) पर अपनी उपज तुरंत बेचना अधिक लाभदायक रहेगा।"
            )
        else:
            recommendation_code = 'stable'
            recommendation_title = '🟡 Stable Market: Spot Sell or Direct Contract'
            recommendation_title_hi = '🟡 स्थिर बाजार: सामान्य विक्रय या अग्रिम सौदा'
            action_badge = 'STABLE SPOT'
            badge_class = 'warning text-dark'
            advisory = (
                f"Prices for {commodity_clean} are projected to remain steady around ₹{current_price_qtl}/Qtl with low volatility (±{abs(price_change_pct)}%). "
                f"Direct farm-gate pickup or spot APMC mandi sales are advised."
            )
            advisory_hi = (
                f"{commodity_clean} के भाव ₹{current_price_qtl}/क्विंटल के आसपास स्थिर रहने की संभावना है। "
                f"मंडी या सीधे खरीदार को बेचना सुरक्षित विकल्प है।"
            )

        result = {
            'success': True,
            'commodity': commodity_clean,
            'district': district_clean,
            'market_name': market_name,
            'current_price_qtl': current_price_qtl,
            'current_rate_kg': current_rate_kg,
            'price_change_pct': price_change_pct,
            'trend_direction': 'up' if price_change_pct > 0 else ('down' if price_change_pct < 0 else 'flat'),
            'days_labels': days_labels,
            'forecast_modal': forecast_modal,
            'forecast_min': forecast_min,
            'forecast_max': forecast_max,
            'recommendation_code': recommendation_code,
            'recommendation_title': recommendation_title,
            'recommendation_title_hi': recommendation_title_hi,
            'action_badge': action_badge,
            'badge_class': badge_class,
            'advisory': advisory,
            'advisory_hi': advisory_hi,
            'roi_breakdown': {
                'current_price_qtl': current_price_qtl,
                'projected_10day_price': projected_10day_price,
                'gross_gain_qtl': gross_gain_qtl,
                'storage_fee_day': storage_fee_day,
                'storage_days': recommended_storage_days,
                'total_storage_cost_qtl': total_storage_cost_qtl,
                'net_gain_qtl': net_gain_qtl,
                'storage_recommended': (recommendation_code == 'store')
            }
        }

        _forecast_cache[cache_key] = {
            'cached_at': datetime.datetime.utcnow(),
            'data': result
        }

        return result
