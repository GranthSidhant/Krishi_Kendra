import os
from flask import Flask, session, g
from config import Config
from app.extensions import db, jwt, cors

def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    # Ensure uploads and instance directories exist
    try:
        os.makedirs(flask_app.config['UPLOAD_FOLDER'], exist_ok=True)
        if not os.environ.get('VERCEL'):
            os.makedirs(os.path.join(flask_app.root_path, '..', 'instance'), exist_ok=True)
    except Exception as e:
        flask_app.logger.warning(f"Directory creation note: {e}")

    # Configure connection pooling for PostgreSQL (prevents serverless cold start socket hangs)
    db_uri = str(flask_app.config.get('SQLALCHEMY_DATABASE_URI', ''))
    if 'postgresql' in db_uri:
        flask_app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 120,
            'pool_size': 10,
            'max_overflow': 15,
            'pool_timeout': 15,
            'connect_args': {
                'connect_timeout': 10,
                'keepalives': 1,
                'keepalives_idle': 30,
                'keepalives_interval': 10,
                'keepalives_count': 5
            }
        }

    # Initialize extensions
    db.init_app(flask_app)
    jwt.init_app(flask_app)
    cors.init_app(flask_app)

    @flask_app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # User loader & context processor
    from app.models import User, Notification

    @flask_app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = db.session.get(User, user_id)

    @flask_app.context_processor
    def inject_globals():
        current_lang = session.get('language', flask_app.config.get('DEFAULT_LANGUAGE', 'en'))
        unread_notifs = 0
        if g.user:
            unread_notifs = Notification.query.filter_by(user_id=g.user.id, is_read=False).count()
        return {
            'current_user': g.user,
            'current_lang': current_lang,
            'available_languages': flask_app.config.get('LANGUAGES', {}),
            'unread_notifications_count': unread_notifs,
            'dev_otp_mode': flask_app.config.get('DEV_OTP_MODE', True)
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
    from app.routes.requests import requests_bp

    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    flask_app.register_blueprint(farmer_bp, url_prefix='/farmer')
    flask_app.register_blueprint(buyer_bp, url_prefix='/buyer')
    flask_app.register_blueprint(admin_bp, url_prefix='/admin')
    flask_app.register_blueprint(chat_bp, url_prefix='/chat')
    flask_app.register_blueprint(orders_bp, url_prefix='/orders')
    flask_app.register_blueprint(cold_storage_bp, url_prefix='/cold-storage')
    flask_app.register_blueprint(marketplace_bp, url_prefix='/marketplace')
    flask_app.register_blueprint(schemes_bp, url_prefix='/schemes')
    flask_app.register_blueprint(api_bp, url_prefix='/api')
    flask_app.register_blueprint(requests_bp, url_prefix='/requests')

    with flask_app.app_context():
        try:
            db.create_all()
            try:
                with db.engine.connect() as conn:
                    # PostgreSQL column type migrations
                    if db.engine.name == 'postgresql':
                        try:
                            conn.execute(db.text("ALTER TABLE users ALTER COLUMN profile_image TYPE TEXT;"))
                            conn.execute(db.text("ALTER TABLE users ALTER COLUMN verification_doc TYPE TEXT;"))
                            conn.execute(db.text("ALTER TABLE messages ALTER COLUMN metadata_json TYPE TEXT;"))
                            conn.commit()
                        except Exception:
                            pass

                    # General column migrations for requirements, transport_bookings, orders, deliveries, etc.
                    migration_sqls = [
                        "ALTER TABLE requirements ADD COLUMN is_pre_order BOOLEAN DEFAULT 0;",
                        "ALTER TABLE requirements ADD COLUMN target_harvest_timeline VARCHAR(100);",
                        "ALTER TABLE requirements ADD COLUMN advance_payment_terms VARCHAR(255);",
                        "ALTER TABLE transport_bookings ADD COLUMN is_shared_pooling BOOLEAN DEFAULT 0;",
                        "ALTER TABLE transport_bookings ADD COLUMN pool_code VARCHAR(50);",
                        "ALTER TABLE transport_bookings ADD COLUMN pickup_latitude FLOAT;",
                        "ALTER TABLE transport_bookings ADD COLUMN pickup_longitude FLOAT;",
                        "ALTER TABLE orders ADD COLUMN escrow_txn_id VARCHAR(50);",
                        "ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50) DEFAULT 'UPI_ESCROW';",
                        "ALTER TABLE orders ADD COLUMN paid_at TIMESTAMP;",
                        "ALTER TABLE orders ADD COLUMN payout_txn_id VARCHAR(50);",
                        "ALTER TABLE orders ADD COLUMN payout_released_at TIMESTAMP;",
                        "ALTER TABLE orders ADD COLUMN inventory_id INTEGER;",
                        "ALTER TABLE orders ADD COLUMN buyer_rating INTEGER;",
                        "ALTER TABLE orders ADD COLUMN buyer_review TEXT;",
                        "ALTER TABLE orders ADD COLUMN farmer_rating INTEGER;",
                        "ALTER TABLE orders ADD COLUMN farmer_review TEXT;",
                        "ALTER TABLE deliveries ADD COLUMN pickup_otp VARCHAR(10);",
                        "ALTER TABLE deliveries ADD COLUMN delivery_otp VARCHAR(10);",
                        "ALTER TABLE deliveries ADD COLUMN pickup_verified_at TIMESTAMP;",
                        "ALTER TABLE deliveries ADD COLUMN delivery_verified_at TIMESTAMP;",
                        "ALTER TABLE deliveries ADD COLUMN vehicle_category VARCHAR(30) DEFAULT 'mini_truck';",
                        "ALTER TABLE deliveries ADD COLUMN distance_km FLOAT DEFAULT 0.0;",
                    ]
                    for stmt in migration_sqls:
                        try:
                            conn.execute(db.text(stmt))
                            conn.commit()
                        except Exception:
                            pass
            except Exception as e_mig:
                flask_app.logger.warning(f"Schema migration note: {e_mig}")
        except Exception as e:
            flask_app.logger.error(f"Error initializing database tables: {e}")

    return flask_app
