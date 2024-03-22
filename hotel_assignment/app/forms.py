from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, SelectField, IntegerField, SubmitField, DateField, validators
from wtforms.validators import DataRequired, Optional, Email

class PhoneNumberForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[validators.DataRequired()])

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
class SearchRoomsForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    area = StringField('Area', validators=[Optional()])
    hotel_chain = SelectField('Hotel Chain', choices=[
        ('Luxury Resorts', 'Luxury Resorts'),
        ('Business Inn', 'Business Inn'),
        ('Budget Stays', 'Budget Stays'),
        ('Travellers Joy', 'Travellers Joy'),
        ('Comfortable Retreat', 'Comfortable Retreat')], validators=[Optional()])
    category = SelectField('Category', choices=[('1', '1 Star'), ('2', '2 Star'), ('3', '3 Star'), ('4', '4 Star'), ('5', '5 Star')])
    min_rooms = IntegerField('Minimum Number of Rooms', validators=[Optional()])
    price = IntegerField('Price Limit', validators=[Optional()])
    submit = SubmitField('Search')

class BookingForm(FlaskForm):
    customer_id = IntegerField('Existing Customer ID', validators=[Optional()])
    street_number = IntegerField('Street Number', validators=[DataRequired()])
    street_name = StringField('Street Name', validators=[DataRequired()])
    apt_number = StringField('Apartment Number', validators=[Optional()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_numbers = FieldList(FormField(PhoneNumberForm), min_entries=1)
    emails = FieldList(FormField(EmailForm), min_entries=1)
    submit = SubmitField('Confirm Booking')
    
    def validate_customer_id(form, field):
        if field.data:
            # If customer_id is provided, no need to check other fields
            return
        
        # List of required fields for a new customer
        required_fields = [form.street_number, form.street_name, form.city, 
                           form.state, form.zip_code, form.first_name, 
                           form.last_name]

        # Dynamically check if each required field is filled
        missing_fields = [f.label.text for f in required_fields if not f.data]
        
        # Check if at least one phone number and email is provided
        if not form.phone_numbers.entries[0].data.get('phone_number'):
            missing_fields.append("At least one phone number")
        if not form.emails.entries[0].data.get('email'):
            missing_fields.append("At least one email")
        
        if missing_fields:
            # Raise ValidationError with a message indicating missing fields
            raise ValidationError('Please provide an existing customer ID or fill in the fields for a new customer. Missing: ' + ', '.join(missing_fields))

