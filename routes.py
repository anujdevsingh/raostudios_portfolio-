from flask import render_template, request, redirect, url_for, flash, jsonify, session
from extensions import app, mail, db
from forms import ContactForm, BookingForm
from flask_mail import Message
from models import Booking, Contact
import os
import json
import requests
import time
import hashlib
import uuid
from datetime import datetime, timedelta

# Razorpay Configuration
import razorpay

RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')

# Initialize Razorpay client
razorpay_client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Verify Razorpay payment signature"""
    try:
        if razorpay_client:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            return True
    except Exception as e:
        print(f"Signature verification failed: {str(e)}")
        return False
    return False

@app.route('/health')
def health_check():
    """Health check endpoint for deployment services"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/test-payment')
def test_payment():
    """Test route to check Razorpay configuration"""
    config_status = {
        'RAZORPAY_KEY_ID': 'Set' if RAZORPAY_KEY_ID else 'Not Set',
        'RAZORPAY_KEY_SECRET': 'Set' if RAZORPAY_KEY_SECRET else 'Not Set',
        'RAZORPAY_CLIENT': 'Initialized' if razorpay_client else 'Not Initialized'
    }
    
    # Test order creation
    test_order = None
    if razorpay_client:
        try:
            test_order = razorpay_client.order.create({
                'amount': 100,  # Amount in paise (₹1.00)
                'currency': 'INR',
                'receipt': 'TEST_RECEIPT_123'
            })
        except Exception as e:
            test_order = f"Error: {str(e)}"
    
    return jsonify({
        'config': config_status,
        'test_order': test_order,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/', methods=['GET', 'POST'])
def index():
    """Route for home page with contact form handling"""
    form = ContactForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # Create new contact record
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        
        db.session.add(new_contact)
        db.session.commit()
        
        # Send email notification - optional
        try:
            msg = Message(
                'New Contact Form Submission',
                sender=os.environ.get('MAIL_DEFAULT_SENDER'),
                recipients=[os.environ.get('MAIL_DEFAULT_SENDER')]
            )
            msg.body = f"""
            New contact form submission:
            
            Name: {form.name.data}
            Email: {form.email.data}
            Phone: {form.phone.data}
            Event Type: {form.event_type.data}
            Message: {form.message.data}
            
            Submitted at: {datetime.now()}
            """
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email notification: {str(e)}")
        
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('index', _anchor='contact'))
    
    return render_template('index.html', form=form)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    """Route for booking page"""
    form = BookingForm()
    if request.method == 'POST':
        print("Form submitted")
        if form.validate_on_submit():
            print("Form validated successfully")
            
            # Create booking record first (without payment)
            new_booking = Booking(
                name=form.name.data,
                phone=form.phone.data,
                event_type=form.event_type.data,
                event_start_date=form.event_start_date.data,
                event_end_date=form.event_end_date.data,
                address=form.address.data,
                notes=form.notes.data,
                payment_status='pending'  # Set as pending initially
            )
            
            db.session.add(new_booking)
            db.session.commit()
            
            # Store booking ID in session for payment
            session['booking_id'] = new_booking.id
            
            # Redirect directly to payment page
            return redirect(url_for('process_payment', booking_id=new_booking.id))
        else:
            print("Form validation failed")
            print("Errors:", form.errors)
    return render_template('booking.html', form=form)

@app.route('/process_payment/<int:booking_id>', methods=['GET', 'POST'])
def process_payment(booking_id):
    """Route for processing payment with Razorpay"""
    # Get booking from database
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if payment is already completed
    if booking.payment_status == 'completed':
        flash('Payment for this booking has already been completed.', 'info')
        return redirect(url_for('index'))
    
    # Debug logging
    print(f"Razorpay Key ID: {'Set' if RAZORPAY_KEY_ID else 'Not Set'}")
    print(f"Razorpay Client: {'Initialized' if razorpay_client else 'Not Initialized'}")
    
    # Check if Razorpay is configured
    if not razorpay_client:
        flash("Payment system is not properly configured. Please contact the administrator.", "danger")
        print("ERROR: Razorpay credentials not configured")
        return redirect(url_for('index'))
    
    try:
        # Create Razorpay order
        order_amount = 100  # ₹1.00 in paise
        order_currency = 'INR'
        order_receipt = f"RAO_BOOKING_{booking_id}_{int(time.time())}"
        
        razorpay_order = razorpay_client.order.create({
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'payment_capture': 1  # Auto capture payment
        })
        
        # Store order details in session
        session['razorpay_order'] = {
            'order_id': razorpay_order['id'],
            'amount': order_amount,
            'currency': order_currency,
            'booking_id': booking_id
        }
        
        # Convert booking to dict for template
        booking_data = {
            'name': booking.name,
            'phone': booking.phone,
            'event_type': booking.event_type,
            'event_start_date': booking.event_start_date.strftime('%Y-%m-%d'),
            'event_end_date': booking.event_end_date.strftime('%Y-%m-%d'),
            'address': booking.address,
            'notes': booking.notes
        }
        
        return render_template('payment.html',
                             razorpay_key_id=RAZORPAY_KEY_ID,
                             razorpay_order=razorpay_order,
                             amount=1.00,
                             booking_data=booking_data)
        
    except Exception as e:
        print(f"Error creating Razorpay order: {str(e)}")
        flash("Error creating payment order. Please try again.", "danger")
        return redirect(url_for('index'))

@app.route('/booking/confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    """Route for booking confirmation page"""
    booking = Booking.query.get_or_404(booking_id)
    return render_template('booking_confirmation.html', booking=booking)

@app.route('/contact', methods=['POST'])
def contact():
    """Route for handling contact form submissions"""
    form = ContactForm()
    if form.validate_on_submit():
        # Create new contact record
        new_contact = Contact(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        
        db.session.add(new_contact)
        db.session.commit()
        
        # Send email notification
        try:
            msg = Message(
                'New Contact Form Submission',
                sender=os.environ.get('MAIL_DEFAULT_SENDER'),
                recipients=[os.environ.get('MAIL_DEFAULT_SENDER')]
            )
            msg.body = f"""
            New contact form submission:
            
            Name: {form.name.data}
            Email: {form.email.data}
            Phone: {form.phone.data}
            Event Type: {form.event_type.data}
            Message: {form.message.data}
            
            Submitted at: {datetime.now()}
            """
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email notification: {str(e)}")
        
        flash('Your message has been sent! We will get back to you soon.', 'success')
    else:
        flash('There was an error with your submission. Please check the form.', 'danger')
        
    return redirect(url_for('index', _anchor='contact'))

@app.route('/contact_ajax', methods=['POST'])
def contact_ajax():
    """AJAX route for handling contact form submissions"""
    form = ContactForm()
    if form.validate_on_submit():
        try:
            # Create new contact record
            new_contact = Contact(
                name=form.name.data,
                email=form.email.data,
                message=form.message.data
            )
            
            db.session.add(new_contact)
            db.session.commit()
            
            # Send email notification
            msg = Message(
                'New Contact Form Submission',
                sender=os.environ.get('MAIL_DEFAULT_SENDER'),
                recipients=[os.environ.get('MAIL_DEFAULT_SENDER')]
            )
            msg.body = f"""
            New contact form submission:
            
            Name: {form.name.data}
            Email: {form.email.data}
            Phone: {form.phone.data}
            Event Type: {form.event_type.data}
            Message: {form.message.data}
            
            Submitted at: {datetime.now()}
            """
            mail.send(msg)
            
            return jsonify({'success': True, 'message': 'Your message has been sent! We will get back to you soon.'})
            
        except Exception as e:
            print(f"Error processing contact form: {str(e)}")
            return jsonify({'success': False, 'message': 'Sorry, there was an error sending your message. Please try again.'})
    else:
        return jsonify({'success': False, 'message': 'Please check the form and try again.', 'errors': form.errors})

@app.route('/terms-and-conditions')
def terms_and_conditions():
    """Route for Terms & Conditions page"""
    return render_template('terms_and_conditions.html')

@app.route('/privacy-policy')
def privacy_policy():
    """Route for Privacy Policy page"""
    return render_template('privacy_policy.html')

@app.route('/refund-cancellation-policy')
def refund_cancellation_policy():
    """Route for Refund & Cancellation Policy page"""
    return render_template('refund_cancellation_policy.html')

@app.route('/shipping-policy')
def shipping_policy():
    """Route for shipping and delivery policy page"""
    return render_template('shipping_policy.html')

@app.route('/payment/success', methods=['POST'])
def payment_success():
    """Handle Razorpay payment success response"""
    try:
        # Get Razorpay response data
        razorpay_payment_id = request.form.get('razorpay_payment_id')
        razorpay_order_id = request.form.get('razorpay_order_id')
        razorpay_signature = request.form.get('razorpay_signature')
        test_mode = request.form.get('test_mode') == 'true'
        
        # Verify signature (skip verification for test mode)
        signature_valid = test_mode or verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature)
        
        if signature_valid:
            if 'razorpay_order' in session:
                # Get booking ID from session
                booking_id = session['razorpay_order'].get('booking_id')
                if booking_id:
                    # Update existing booking record
                    booking = Booking.query.get(booking_id)
                    if booking:
                        booking.payment_id = razorpay_payment_id
                        booking.payment_status = 'completed'
                        db.session.commit()
                
                        # Send confirmation email
                        try:
                            default_sender = os.environ.get('MAIL_DEFAULT_SENDER', 'raostudiosrgh@gmail.com')
                            
                            msg = Message(
                                'Payment Confirmation - Rao Studios',
                                sender=default_sender,
                                recipients=[default_sender]
                            )
                            msg.body = f"""
                            Dear {booking.name},
                            
                            Thank you for your payment! Your booking with Rao Studios is now confirmed.
                            
                            Booking Details:
                            - Event Type: {booking.event_type}
                            - Event Dates: From {booking.event_start_date} to {booking.event_end_date}
                            - Address: {booking.address}
                            - Payment ID: {razorpay_payment_id}
                            - Razorpay Order ID: {razorpay_order_id}
                            
                            Our team will contact you within 24 hours to discuss further details.
                            
                            Best regards,
                            Rao Studios Team
                            """
                            
                            mail.send(msg)
                        except Exception as e:
                            print(f"Email sending failed: {str(e)}")
                        
                        # Clear session data
                        session.pop('razorpay_order', None)
                        
                        # Redirect to confirmation page with success message
                        flash('Payment successful! Your booking is confirmed. We will contact you within 24 hours.', 'success')
                        return redirect(url_for('booking_confirmation', booking_id=booking.id))
                else:
                    flash('Payment was not successful. Please try again.', 'danger')
                    return redirect(url_for('process_payment', booking_id=booking_id))
        else:
            flash('Payment verification failed. Please contact support.', 'danger')
            booking_id = session.get('razorpay_order', {}).get('booking_id')
            if booking_id:
                return redirect(url_for('process_payment', booking_id=booking_id))
            else:
                return redirect(url_for('booking'))
            
    except Exception as e:
        print(f"Payment success handling error: {str(e)}")
        flash('An error occurred while processing your payment. Please contact support.', 'danger')
        booking_id = session.get('razorpay_order', {}).get('booking_id')
        if booking_id:
            return redirect(url_for('process_payment', booking_id=booking_id))
        else:
            return redirect(url_for('booking'))

@app.route('/payment/failure', methods=['POST'])
def payment_failure():
    """Handle Razorpay payment failure response"""
    try:
        error_code = request.form.get('error[code]')
        error_description = request.form.get('error[description]')
        error_source = request.form.get('error[source]')
        error_step = request.form.get('error[step]')
        error_reason = request.form.get('error[reason]')
        
        print(f"Payment failed - Code: {error_code}, Description: {error_description}, Source: {error_source}, Step: {error_step}, Reason: {error_reason}")
        
        flash(f'Payment failed: {error_description or error_reason or "Unknown error"}. Please try again.', 'danger')
        booking_id = session.get('razorpay_order', {}).get('booking_id')
        if booking_id:
            return redirect(url_for('process_payment', booking_id=booking_id))
        else:
            return redirect(url_for('booking'))
        
    except Exception as e:
        print(f"Payment failure handling error: {str(e)}")
        flash('Payment failed. Please try again.', 'danger')
        booking_id = session.get('razorpay_order', {}).get('booking_id')
        if booking_id:
            return redirect(url_for('process_payment', booking_id=booking_id))
        else:
            return redirect(url_for('booking'))
