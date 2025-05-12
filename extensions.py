from flask import Flask
from flask_mail import Mail

app = Flask(__name__, template_folder='templates', static_folder='static')
mail = Mail() 