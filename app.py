
import os
from flask import Flask, render_template
from models import db, User
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    # existing config and blueprints ....

    # Configuration
    app.config['SECRET_KEY'] = "careerboost_secure_key_v1"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    os.makedirs(app.instance_path, exist_ok=True)
    # Initialize Plugins
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.resume import resume_bp
    from routes.dashboard import main_bp
    from routes.interview import interview_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(interview_bp)

    # 404 Error Handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('500.html'), 500

    # Create database within app context
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')