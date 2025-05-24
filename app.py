import os
import logging
import sys
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import app, mail, db

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment variables loaded from .env file")
except ImportError:
    logger.warning("python-dotenv not installed. Environment variables from system only.")
except Exception as e:
    logger.warning(f"Failed to load .env file: {str(e)}")

# Configure app
app.secret_key = os.environ.get("SECRET_KEY", "development-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

logger.info("Flask app configured")

# Configure mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

logger.info("Mail configuration set")

# Configure SQLAlchemy
database_url = os.environ.get('DATABASE_URL', 'sqlite:///raostudios.db')
# Handle postgres:// URLs (Heroku/Render legacy format)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info(f"Database URL configured: {database_url.split('@')[0]}@***")

# Initialize extensions
try:
    mail.init_app(app)
    logger.info("Mail extension initialized")
    
    db.init_app(app)
    logger.info("Database extension initialized")
    
    # Import models before creating tables
    from models import Contact, Booking
    logger.info("Models imported")
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created/verified")
        
except Exception as e:
    logger.error(f"Error during app initialization: {str(e)}")
    raise

# Import routes after app is initialized to avoid circular imports
try:
    from routes import *
    from admin_routes import *
    logger.info("Routes imported successfully")
except Exception as e:
    logger.error(f"Error importing routes: {str(e)}")
    raise

logger.info("Application startup completed successfully")

# Run the application
if __name__ == "__main__":
    # Use PORT environment variable for deployment, fallback to 8080 for local development
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') != 'production'
    logger.info(f"Starting server on port {port}, debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
