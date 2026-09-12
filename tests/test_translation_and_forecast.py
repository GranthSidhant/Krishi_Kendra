import pytest
from app import create_app
from config import Config
from app.extensions import db
from app.services.translation_service import TranslationService
from app.services.price_forecast_service import PriceForecastService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_translation_service_direct():
    """Test the translation service heuristic and translation methods directly."""
    # Test translating English to Hindi
    res = TranslationService.translate_text("Hello, what is the best price for your wheat?", target_lang="hi")
    assert res is not None
    assert "translated_text" in res
    assert res["target_lang"] == "hi"
    assert len(res["translated_text"]) > 0

    # Test translating to Marathi
    res_mr = TranslationService.translate_text("Fresh organic tomatoes ready for pickup", target_lang="mr")
    assert res_mr is not None
    assert res_mr["target_lang"] == "mr"
    assert len(res_mr["translated_text"]) > 0

def test_chat_translation_api(client):
    """Test the POST /api/chat/translate endpoint."""
    payload = {
        "text": "Can you deliver 50 quintals by tomorrow evening?",
        "target_lang": "hi"
    }
    response = client.post("/api/chat/translate", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "translated_text" in data
    assert data["target_lang"] == "hi"
    assert len(data["translated_text"]) > 0

def test_chat_translation_api_missing_data(client):
    """Test the POST /api/chat/translate endpoint with missing text."""
    response = client.post("/api/chat/translate", json={"target_lang": "hi"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "No text provided" in data["error"]

def test_price_forecast_service_direct(app):
    """Test price forecasting and cold storage advisory logic with app context."""
    with app.app_context():
        forecast = PriceForecastService.get_forecast("Onion", "Nashik")
        assert forecast is not None
        assert forecast["success"] is True
        assert forecast["commodity"] == "Onion"
        assert len(forecast["days_labels"]) == 7
        assert len(forecast["forecast_modal"]) == 7
        assert len(forecast["forecast_min"]) == 7
        assert len(forecast["forecast_max"]) == 7
        assert "recommendation_code" in forecast
        assert "roi_breakdown" in forecast
        assert "advisory" in forecast
        assert "advisory_hi" in forecast

        # Verify min <= modal <= max
        for min_p, mod_p, max_p in zip(forecast["forecast_min"], forecast["forecast_modal"], forecast["forecast_max"]):
            assert min_p <= mod_p <= max_p

def test_mandi_forecast_api(client):
    """Test the GET /api/mandi/forecast endpoint."""
    response = client.get("/api/mandi/forecast?commodity=Tomato&district=Pune")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["commodity"] == "Tomato"
    assert len(data["days_labels"]) == 7
    assert len(data["forecast_modal"]) == 7
    assert "recommendation_code" in data
    assert "roi_breakdown" in data
    assert "advisory" in data
