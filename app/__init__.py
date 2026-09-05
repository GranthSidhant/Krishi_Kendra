import os
from flask import Flask, session, g
from config import Config
from app.extensions import db, jwt, cors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # User loader & context processor
    from app.models import User, Notification

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = db.session.get(User, user_id)

    @app.context_processor
    def inject_globals():
        current_lang = session.get('language', app.config.get('DEFAULT_LANGUAGE', 'en'))
        unread_notifs = 0
        if g.user:
            unread_notifs = Notification.query.filter_by(user_id=g.user.id, is_read=False).count()
        return {
            'current_user': g.user,
            'current_lang': current_lang,
            'available_languages': app.config.get('LANGUAGES', {}),
            'unread_notifications_count': unread_notifs,
            'dev_otp_mode': app.config.get('DEV_OTP_MODE', True)
        }

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.farmer import farmer_bp
    from app.routes.buyer import buyer_bp
    from app.routes.admin import admin_bp
    from app.routes.chat import chat_bp
    from app.routes.orders import orders_bp
    from app.routes.cold_storage import cold_storage_bp
    from app.routes.marketplace import marketplace_bp
    from app.routes.schemes import schemes_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(farmer_bp, url_prefix='/farmer')
    app.register_blueprint(buyer_bp, url_prefix='/buyer')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(cold_storage_bp, url_prefix='/cold-storage')
    app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
    app.register_blueprint(schemes_bp, url_prefix='/schemes')
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app
