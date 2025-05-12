from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

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
