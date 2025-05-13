from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from datetime import date

class ContactForm(FlaskForm):
    """Form for contact page"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    event_type = SelectField('Event Type', 
                            choices=[
                                ('wedding', 'Wedding'),
                                ('engagement', 'Engagement'),
                                ('birthday', 'Birthday'),
                                ('anniversary', 'Anniversary'),
                                ('corporate', 'Corporate Event'),
                                ('other', 'Other')
                            ],
                            validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=5, max=1000)])
    submit = SubmitField('Send Message')

class BookingForm(FlaskForm):
    """Form for booking page"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    event_type = SelectField('Event Type', 
                            choices=[
                                ('wedding', 'Wedding'),
                                ('pre-wedding', 'Pre-Wedding'),
                                ('haldi', 'Haldi'),
                                ('engagement', 'Engagement'),
                                ('birthday', 'Birthday'),
                                ('anniversary', 'Anniversary'),
                                ('corporate', 'Corporate Event'),
                                ('other', 'Other')
                            ],
                            validators=[DataRequired()])
    event_start_date = DateField('Event Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    event_end_date = DateField('Event End Date', validators=[DataRequired()], format='%Y-%m-%d')
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=5, max=500)])
    notes = TextAreaField('Additional Notes', validators=[Length(max=1000)])
    submit = SubmitField('Proceed to Payment')
    
    def validate_event_start_date(self, field):
        if field.data < date.today():
            raise ValidationError('Event date cannot be in the past')
    
    def validate_event_end_date(self, field):
        if field.data < self.event_start_date.data:
            raise ValidationError('End date must be after start date')
