from flask_login import LoginManager
import os
from flask import Flask
from dotenv import load_dotenv 
from app.models import db, mail

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Create instance folder if it doesn't exist
    os.makedirs(app.instance_path, exist_ok=True)

    from app.models.user import User
    
    db_path = os.path.join(app.instance_path, 'models.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
 
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login_page"

    
   
    # App configs
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
    mail.init_app(app)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "changeme")
    app.config["CHECKMK_BASE_URL"] = os.getenv("CHECKMK_BASE_URL")
    app.config["CHECKMK_SITE_ID"] = os.getenv("CHECKMK_SITE_ID")
    app.config["CHECKMK_USERNAME"] = os.getenv("CHECKMK_USERNAME")
    app.config["CHECKMK_PASSWORD"] = os.getenv("CHECKMK_PASSWORD")
    app.config["CHECKMK_VERIFY_SSL"] = os.getenv("VERIFY_SSL", "false").lower() == "true"

    app.config["SESSION_COOKIE_SECURE"] = True
    # app.config["PERMANENT_SESSION_LIFETIME"] = 1800

    # Function config 
    from app.auth.routes import auth_bp
    from app.hosts.routes import hosts_bp
    from app.host_services.routes import host_services_bp
    from app.monitoring.routes import monitor_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(hosts_bp)
    app.register_blueprint(host_services_bp)
    app.register_blueprint(monitor_bp)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login_page"

    
    from app.errors.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    with app.app_context():
        db.create_all()

    return app