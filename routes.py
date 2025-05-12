from flask import render_template, request, redirect, url_for, flash
from extensions import app, mail
from forms import ContactForm
from flask_mail import Message

@app.route('/')
def index():
    """Route for home page"""
    return render_template('index.html')

# No contact form route needed anymore
