import urllib.request
import json
import logging

logger = logging.getLogger(__name__)

# Coordinates lookup for major agricultural districts across India
DISTRICT_COORDINATES = {
    'nashik': {'lat': 19.9975, 'lon': 73.7898, 'state': 'Maharashtra'},
    'pune': {'lat': 18.5204, 'lon': 73.8567, 'state': 'Maharashtra'},
    'nagpur': {'lat': 21.1458, 'lon': 79.0882, 'state': 'Maharashtra'},
    'mumbai': {'lat': 19.0760, 'lon': 72.8777, 'state': 'Maharashtra'},
    'aurangabad': {'lat': 19.8762, 'lon': 75.3433, 'state': 'Maharashtra'},
    'chhatrapati sambhajinagar': {'lat': 19.8762, 'lon': 75.3433, 'state': 'Maharashtra'},
    'solapur': {'lat': 17.6599, 'lon': 75.9064, 'state': 'Maharashtra'},
    'kolhapur': {'lat': 16.7050, 'lon': 74.2433, 'state': 'Maharashtra'},
    'ahmednagar': {'lat': 19.0948, 'lon': 74.7480, 'state': 'Maharashtra'},
    'delhi': {'lat': 28.7041, 'lon': 77.1025, 'state': 'Delhi'},
    'jaipur': {'lat': 26.9124, 'lon': 75.7873, 'state': 'Rajasthan'},
    'ludhiana': {'lat': 30.9010, 'lon': 75.8573, 'state': 'Punjab'},
    'karnal': {'lat': 29.6857, 'lon': 76.9905, 'state': 'Haryana'},
    'bhopal': {'lat': 23.2599, 'lon': 77.4126, 'state': 'Madhya Pradesh'},
    'indore': {'lat': 22.7196, 'lon': 75.8577, 'state': 'Madhya Pradesh'},
    'lucknow': {'lat': 26.8467, 'lon': 80.9462, 'state': 'Uttar Pradesh'},
    'varanasi': {'lat': 25.3176, 'lon': 82.9739, 'state': 'Uttar Pradesh'},
    'patna': {'lat': 25.5941, 'lon': 85.1376, 'state': 'Bihar'},
    'ahmedabad': {'lat': 23.0225, 'lon': 72.5714, 'state': 'Gujarat'},
    'surat': {'lat': 21.1702, 'lon': 72.8311, 'state': 'Gujarat'},
    'rajkot': {'lat': 22.3039, 'lon': 70.8022, 'state': 'Gujarat'},
    'bengaluru': {'lat': 12.9716, 'lon': 77.5946, 'state': 'Karnataka'},
    'bangalore': {'lat': 12.9716, 'lon': 77.5946, 'state': 'Karnataka'},
    'chennai': {'lat': 13.0827, 'lon': 80.2707, 'state': 'Tamil Nadu'},
    'hyderabad': {'lat': 17.3850, 'lon': 78.4867, 'state': 'Telangana'},
    'vijayawada': {'lat': 16.5062, 'lon': 80.6480, 'state': 'Andhra Pradesh'},
    'kolkata': {'lat': 22.5726, 'lon': 88.3639, 'state': 'West Bengal'},
}

# WMO Weather Condition Codes Interpretation
WMO_CODES = {
    0: {'desc': 'Clear Sky', 'icon': '☀️', 'alert': 'Optimal for harvesting & open-field drying.'},
    1: {'desc': 'Mainly Clear', 'icon': '🌤️', 'alert': 'Good spraying and weeding conditions.'},
    2: {'desc': 'Partly Cloudy', 'icon': '⛅', 'alert': 'Favorable for general farm activities.'},
    3: {'desc': 'Overcast', 'icon': '☁️', 'alert': 'Reduced solar radiation; moderate irrigation.'},
    45: {'desc': 'Foggy', 'icon': '🌫️', 'alert': 'Check for fungal vulnerability in vegetable crops.'},
    48: {'desc': 'Depositing Rime Fog', 'icon': '🌫️', 'alert': 'High morning moisture.'},
    51: {'desc': 'Light Drizzle', 'icon': '🌦️', 'alert': 'Light moisture; avoid pesticide spray today.'},
    53: {'desc': 'Moderate Drizzle', 'icon': '🌦️', 'alert': 'Postpone pesticide spraying.'},
    55: {'desc': 'Dense Drizzle', 'icon': '🌧️', 'alert': 'Ensure field drainage.'},
    61: {'desc': 'Slight Rain', 'icon': '🌧️', 'alert': 'Keep harvested produce under tarpaulin.'},
    63: {'desc': 'Moderate Rain', 'icon': '🌧️', 'alert': 'Suspend open sowing/harvesting today.'},
    65: {'desc': 'Heavy Rain', 'icon': '⛈️', 'alert': '⚠️ Waterlogging alert. Clear farm drainage channels!'},
    71: {'desc': 'Slight Snow/Hail', 'icon': '🌨️', 'alert': 'Protect tender nurseries.'},
    80: {'desc': 'Rain Showers', 'icon': '🌦️', 'alert': 'Intermittent rain expected.'},
    81: {'desc': 'Moderate Showers', 'icon': '🌧️', 'alert': 'Cover Mandi transport loads.'},
    82: {'desc': 'Violent Showers', 'icon': '⛈️', 'alert': 'Severe weather alert.'},
    95: {'desc': 'Thunderstorm', 'icon': '⚡', 'alert': '⚠️ Lightning & thunderstorm risk. Move indoors.'},
    96: {'desc': 'Thunderstorm with Hail', 'icon': '⛈️', 'alert': '⚠️ Hail alert. Shelter livestock & equipment.'},
}


import time

_weather_cache = {}

class WeatherService:
    @staticmethod
    def get_coordinates(district_name):
        """Lookup latitude & longitude for district or fallback to Nashik."""
        if not district_name:
            return 19.9975, 73.7898, 'Nashik'
        key = district_name.strip().lower()
        if key in DISTRICT_COORDINATES:
            match = DISTRICT_COORDINATES[key]
            return match['lat'], match['lon'], district_name.title()
        
        # Partial match
        for d_key, coords in DISTRICT_COORDINATES.items():
            if d_key in key or key in d_key:
                return coords['lat'], coords['lon'], d_key.title()
        
        # Default Maharashtra farm center (Nashik)
        return 19.9975, 73.7898, district_name.title()

    @staticmethod
    def fetch_live_weather(lat=None, lon=None, district=None):
        """Fetch current weather and 5-day forecast with in-memory 15-minute caching."""
        resolved_name = district or "Nashik"
        if lat is None or lon is None:
            lat, lon, resolved_name = WeatherService.get_coordinates(district)

        cache_key = f"{round(lat, 2)}_{round(lon, 2)}"
        now = time.time()
        if cache_key in _weather_cache:
            cached_entry, cached_at = _weather_cache[cache_key]
            if now - cached_at < 900: # 15 minutes TTL
                return cached_entry

        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m"
                f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max"
                f"&timezone=auto&forecast_days=5"
            )
            
            req = urllib.request.Request(url, headers={'User-Agent': 'KrishiKendra/1.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    current = data.get('current', {})
                    code = current.get('weather_code', 0)
                    wmo_info = WMO_CODES.get(code, {'desc': 'Clear', 'icon': '☀️', 'alert': 'Favorable weather.'})

                    daily_data = data.get('daily', {})
                    forecast = []
                    dates = daily_data.get('time', [])
                    t_max = daily_data.get('temperature_2m_max', [])
                    t_min = daily_data.get('temperature_2m_min', [])
                    rain_prob = daily_data.get('precipitation_probability_max', [])
                    codes = daily_data.get('weather_code', [])

                    for i in range(min(len(dates), 5)):
                        d_code = codes[i] if i < len(codes) else 0
                        d_info = WMO_CODES.get(d_code, {'desc': 'Clear', 'icon': '☀️'})
                        forecast.append({
                            'date': dates[i],
                            'max_temp': t_max[i] if i < len(t_max) else 30,
                            'min_temp': t_min[i] if i < len(t_min) else 20,
                            'rain_prob': rain_prob[i] if i < len(rain_prob) else 0,
                            'desc': d_info['desc'],
                            'icon': d_info['icon']
                        })

                    res_payload = {
                        'success': True,
                        'location': resolved_name,
                        'latitude': lat,
                        'longitude': lon,
                        'temperature': round(current.get('temperature_2m', 28)),
                        'feels_like': round(current.get('apparent_temperature', 29)),
                        'humidity': current.get('relative_humidity_2m', 60),
                        'precipitation': current.get('precipitation', 0),
                        'wind_speed': current.get('wind_speed_10m', 10),
                        'weather_desc': wmo_info['desc'],
                        'weather_icon': wmo_info['icon'],
                        'agri_advisory': wmo_info['alert'],
                        'forecast': forecast
                    }
                    _weather_cache[cache_key] = (res_payload, now)
                    return res_payload
        except Exception as e:
            logger.warning(f"Live weather fetch error: {e}")

        # Fallback offline simulation data
        sim_payload = {
            'success': True,
            'location': resolved_name,
            'latitude': lat or 19.9975,
            'longitude': lon or 73.7898,
            'temperature': 29,
            'feels_like': 31,
            'humidity': 62,
            'precipitation': 0,
            'wind_speed': 12,
            'weather_desc': 'Partly Cloudy',
            'weather_icon': '⛅',
            'agri_advisory': 'Favorable conditions for routine agricultural activities.',
            'forecast': [
                {'date': 'Today', 'max_temp': 32, 'min_temp': 22, 'rain_prob': 10, 'desc': 'Sunny', 'icon': '☀️'},
                {'date': 'Tomorrow', 'max_temp': 31, 'min_temp': 21, 'rain_prob': 15, 'desc': 'Partly Cloudy', 'icon': '⛅'},
                {'date': 'Day 3', 'max_temp': 29, 'min_temp': 20, 'rain_prob': 40, 'desc': 'Light Rain', 'icon': '🌦️'},
                {'date': 'Day 4', 'max_temp': 30, 'min_temp': 22, 'rain_prob': 20, 'desc': 'Clear', 'icon': '🌤️'},
                {'date': 'Day 5', 'max_temp': 33, 'min_temp': 23, 'rain_prob': 5, 'desc': 'Sunny', 'icon': '☀️'}
            ]
        }
        _weather_cache[cache_key] = (sim_payload, now)
        return sim_payload
