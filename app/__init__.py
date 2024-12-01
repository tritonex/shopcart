from flask import Flask
from config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    @login_manager.user_loader
    def load_user(id):
        from app.models import User
        return User.query.get(int(id))
    
    return app