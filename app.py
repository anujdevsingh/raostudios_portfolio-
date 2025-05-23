import os
import logging
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import app, mail, db

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Please install it using: pip install python-dotenv")
except Exception as e:
    print(f"Warning: Failed to load .env file: {str(e)}")

logging.basicConfig(level=logging.DEBUG)

# Configure app
app.secret_key = os.environ.get("SECRET_KEY", "development-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///raostudios.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
mail.init_app(app)
db.init_app(app)

# Import models before creating tables
from models import Contact, Booking

# Create database tables
with app.app_context():
    db.create_all()

# Import routes after app is initialized to avoid circular imports
from routes import *
from admin_routes import *

# Run the application
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
