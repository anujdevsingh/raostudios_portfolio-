from flask import render_template, jsonify, request, redirect, url_for, flash, session
from extensions import app, db
from models import Contact, Booking
from functools import wraps
import os

# Simple Admin Authentication
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated in session
        if not session.get('admin_authenticated'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login')
def admin_login():
    """Admin login page"""
    # If already authenticated, redirect to dashboard
    if session.get('admin_authenticated'):
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin_login.html')

@app.route('/admin/verify', methods=['POST'])
def admin_verify():
    """Verify admin password"""
    # Get admin password from environment or use default
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    # Get password from form
    password = request.form.get('password')
    
    if password == admin_password:
        # Set admin as authenticated in session
        session['admin_authenticated'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid password. Please try again.', 'danger')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    # Remove admin authentication from session
    session.pop('admin_authenticated', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard showing database entries"""
    # Get latest contacts
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    
    # Get latest bookings
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    
    return render_template('admin_dashboard.html', 
                          contacts=contacts, 
                          bookings=bookings)

@app.route('/admin/export', methods=['GET'])
@admin_required
def admin_export():
    """Admin export data as JSON"""
    data_type = request.args.get('type', 'all')
    
    if data_type == 'contacts' or data_type == 'all':
        contacts = Contact.query.all()
        contacts_data = [{
            'id': c.id,
            'name': c.name,
            'email': c.email,
            'message': c.message,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in contacts]
    else:
        contacts_data = []
        
    if data_type == 'bookings' or data_type == 'all':
        bookings = Booking.query.all()
        bookings_data = [{
            'id': b.id,
            'name': b.name,
            'phone': b.phone,
            'event_type': b.event_type,
            'event_start_date': b.event_start_date.isoformat() if b.event_start_date else None,
            'event_end_date': b.event_end_date.isoformat() if b.event_end_date else None,
            'address': b.address,
            'notes': b.notes,
            'payment_id': b.payment_id,
            'payment_status': b.payment_status,
            'created_at': b.created_at.isoformat() if b.created_at else None
        } for b in bookings]
    else:
        bookings_data = []
    
    # Return data as JSON
    return jsonify({
        'contacts': contacts_data,
        'bookings': bookings_data
    }) 