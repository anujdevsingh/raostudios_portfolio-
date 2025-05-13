from flask import render_template, request, redirect, url_for, flash, jsonify, session
from extensions import app, mail, db
from forms import ContactForm, BookingForm
from flask_mail import Message
from models import Booking
import os
import json
from datetime import datetime

@app.route('/')
def index():
    """Route for home page"""
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    """Route for booking page"""
    form = BookingForm()
    if request.method == 'POST':
        print("Form submitted")
        if form.validate_on_submit():
            print("Form validated successfully")
            # Store form data in session to use after payment
            session['booking_data'] = {
                'name': form.name.data,
                'phone': form.phone.data,
                'event_type': form.event_type.data,
                'event_start_date': form.event_start_date.data.strftime('%Y-%m-%d'),
                'event_end_date': form.event_end_date.data.strftime('%Y-%m-%d'),
                'address': form.address.data,
                'notes': form.notes.data
            }
            # Redirect to payment page
            return redirect(url_for('process_payment'))
        else:
            print("Form validation failed")
            print("Errors:", form.errors)
    return render_template('booking.html', form=form)

@app.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    """Route for processing payment"""
    if 'booking_data' not in session:
        flash('Please complete the booking form first', 'warning')
        return redirect(url_for('booking'))
    
    if request.method == 'POST':
        # Get payment details from Razorpay
        payment_id = request.form.get('razorpay_payment_id')
        
        if payment_id:
            # Create booking record
            booking_data = session['booking_data']
            new_booking = Booking(
                name=booking_data['name'],
                phone=booking_data['phone'],
                event_type=booking_data['event_type'],
                event_start_date=datetime.strptime(booking_data['event_start_date'], '%Y-%m-%d').date(),
                event_end_date=datetime.strptime(booking_data['event_end_date'], '%Y-%m-%d').date(),
                address=booking_data['address'],
                notes=booking_data['notes'],
                payment_id=payment_id,
                payment_status='completed'
            )
            
            db.session.add(new_booking)
            db.session.commit()
            
            # Clear the session
            session.pop('booking_data', None)
            
            # Get default sender email or use a fallback
            default_sender = os.environ.get('MAIL_DEFAULT_SENDER', 'raostudiossrgh@gmail.com')
            
            # Send confirmation email
            msg = Message(
                'Booking Confirmation - Rao Studios',
                sender=default_sender,
                recipients=[booking_data.get('email', 'info@raostudios.com')]
            )
            msg.body = f"""
            Dear {booking_data['name']},
            
            Thank you for booking with Rao Studios!
            
            Booking Details:
            - Event Type: {booking_data['event_type']}
            - Event Dates: From {booking_data['event_start_date']} to {booking_data['event_end_date']}
            - Address: {booking_data['address']}
            
            Our team will contact you within 24 hours to discuss further details.
            
            Best regards,
            Rao Studios Team
            """
            
            try:
                mail.send(msg)
            except Exception as e:
                # Log the error but continue with the booking process
                print(f"Email sending failed: {str(e)}")
            
            return redirect(url_for('booking_confirmation', booking_id=new_booking.id))
    
    # For GET request, show payment page with Razorpay integration
    razorpay_key_id = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_12345')
    return render_template('payment.html', 
                           key_id=razorpay_key_id, 
                           amount=500, # ₹500 token amount
                           booking_data=session['booking_data'])

@app.route('/booking/confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    """Route for booking confirmation page"""
    booking = Booking.query.get_or_404(booking_id)
    return render_template('booking_confirmation.html', booking=booking)
