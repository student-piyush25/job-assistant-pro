import razorpay
import os
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_required, current_user
from models import User
from extensions import db
from dotenv import load_dotenv

load_dotenv()

# Global Razorpay Client initialized with environment variables
client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_SECRET")))

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_key_123")
    app.config['RAZORPAY_KEY_ID'] = os.getenv("RAZORPAY_KEY_ID")
    app.config['RAZORPAY_SECRET'] = os.getenv("RAZORPAY_SECRET")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Plugins
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Import Blueprints inside the function to prevent circular imports
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp, main_bp
    from routes.resume import resume_bp
    from routes.interview import interview_bp

    # Registering all your project modules
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(main_bp) 

    # SINGLE Payment Success Route (Defined here to avoid blueprint conflicts)
    @app.route('/payment_success', methods=['POST'])
    @login_required
    def payment_success():
        data = request.json
        params_dict = {
            'razorpay_order_id': data.get('razorpay_order_id'),
            'razorpay_payment_id': data.get('razorpay_payment_id'),
            'razorpay_signature': data.get('razorpay_signature')
        }
        try:
            # Verify the payment cryptographically
            client.utility.verify_payment_signature(params_dict)
            
            # Update the user status in the database
            user = db.session.get(User, current_user.id)
            user.is_premium = True
            db.session.commit()
            
            return jsonify({"status": "success"})
        except Exception as e:
            print(f"❌ Payment Verification Error: {e}")
            return jsonify({"status": "failed", "error": str(e)}), 400

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

# Initialize the app instance
app = create_app()

if __name__ == '__main__':
    # Using 0.0.0.0 so it's accessible on your local network/mobile testing
    app.run(debug=True, host='0.0.0.0', port=5000)