import csv
import os
from app import app, db
from models import Contact, Booking
from datetime import datetime

def export_to_csv():
    """Export database tables to CSV files"""
    print("Starting database export...")
    
    # Create exports directory if it doesn't exist
    if not os.path.exists('exports'):
        os.makedirs('exports')
    
    # Current timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Export Contacts
    contact_filename = f'exports/contacts_{timestamp}.csv'
    with open(contact_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['ID', 'Name', 'Email', 'Message', 'Created At'])
        
        # Write data
        with app.app_context():
            contacts = Contact.query.all()
            for contact in contacts:
                writer.writerow([
                    contact.id, 
                    contact.name, 
                    contact.email, 
                    contact.message, 
                    contact.created_at
                ])
    
    print(f"Contacts exported to {contact_filename}")
    
    # Export Bookings
    booking_filename = f'exports/bookings_{timestamp}.csv'
    with open(booking_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow([
            'ID', 'Name', 'Phone', 'Event Type', 
            'Event Start Date', 'Event End Date', 
            'Address', 'Notes', 'Payment ID', 
            'Payment Status', 'Created At'
        ])
        
        # Write data
        with app.app_context():
            bookings = Booking.query.all()
            for booking in bookings:
                writer.writerow([
                    booking.id,
                    booking.name,
                    booking.phone,
                    booking.event_type,
                    booking.event_start_date,
                    booking.event_end_date,
                    booking.address,
                    booking.notes,
                    booking.payment_id,
                    booking.payment_status,
                    booking.created_at
                ])
    
    print(f"Bookings exported to {booking_filename}")
    print("Export completed successfully!")

if __name__ == "__main__":
    export_to_csv() 