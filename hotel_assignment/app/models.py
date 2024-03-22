from flask_sqlalchemy import SQLAlchemy
from . import db
db = SQLAlchemy()

class HotelChain(db.Model):
    __tablename__ = 'hotel_chain'
    hotel_chainID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    street_number = db.Column(db.Integer)
    street_name = db.Column(db.String(255))
    apt_number = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(20))
    hotels = db.relationship('Hotel', backref='hotel_chain', lazy=True)
    phone_numbers = db.relationship('HotelChainPhoneNumbers', backref='hotel_chain', lazy=True)
    emails = db.relationship('HotelChainEmails', backref='hotel_chain', lazy=True)

class Hotel(db.Model):
    __tablename__ = 'hotel'
    hotelID = db.Column(db.Integer, primary_key=True)
    hotel_chainID = db.Column(db.Integer, db.ForeignKey('hotel_chain.hotel_chainID'), nullable=False)
    star_rating = db.Column(db.Integer)
    street_number = db.Column(db.Integer)
    street_name = db.Column(db.String(255))
    apt_number = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(20))
    rooms = db.relationship('Room', backref='hotel', lazy=True)
    phone_numbers = db.relationship('HotelPhoneNumbers', backref='hotel', lazy=True)
    emails = db.relationship('HotelEmails', backref='hotel', lazy=True)

class Customer(db.Model):
    __tablename__ = 'customer'
    customerID = db.Column(db.Integer, primary_key=True)
    date_of_registration = db.Column(db.Date)
    street_number = db.Column(db.Integer)
    street_name = db.Column(db.String(255))
    apt_number = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(20))
    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_numbers = db.relationship('CustomerPhoneNumbers', backref='customer', lazy=True)
    emails = db.relationship('CustomerEmails', backref='customer', lazy=True)
    bookings = db.relationship('BookingRenting', backref='customer', lazy=True)

class Room(db.Model):
    __tablename__ = 'room'
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), nullable=False)
    room_number = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10, 2))
    view_type = db.Column(db.String(255))
    is_extended = db.Column(db.Boolean)
    capacity = db.Column(db.Integer)
    amenities = db.relationship('RoomAmenities', backref='room', lazy=True)
    problems = db.relationship('RoomProblems', backref='room', lazy=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    SSN = db.Column(db.String(11), primary_key=True)
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), nullable=False)
    street_number = db.Column(db.Integer)
    street_name = db.Column(db.String(255))
    apt_number = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(20))
    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_numbers = db.relationship('EmployeePhoneNumbers', backref='employee', lazy=True)
    emails = db.relationship('EmployeeEmails', backref='employee', lazy=True)
    roles = db.relationship('EmployeeRoles', backref='employee', lazy=True)

class BookingRenting(db.Model):
    __tablename__ = 'booking_renting'
    bookingID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey('customer.customerID'), nullable=False)
    SSN = db.Column(db.String(11), db.ForeignKey('employee.SSN'), nullable=False)
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), nullable=False)
    room_number = db.Column(db.Integer, db.ForeignKey('room.room_number'), nullable=False)
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    date_booked = db.Column(db.Date)
    status = db.Column(db.String(255))
    credit_card_number = db.Column(db.String(19))
    cvv = db.Column(db.String(5))
    credit_card_expiry = db.Column(db.Date)
    billing_address = db.Column(db.String(255))

class Archives(db.Model):
    __tablename__ = 'archives'
    archiveID = db.Column(db.Integer, primary_key=True)
    bookingID = db.Column(db.Integer)
    customerID = db.Column(db.Integer)
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    date_booked = db.Column(db.Date)
    status = db.Column(db.String(255))
    room_number = db.Column(db.Integer)

class HotelChainPhoneNumbers(db.Model):
    __tablename__ = 'hotel_chain_phone_numbers'
    hotel_chainID = db.Column(db.Integer, db.ForeignKey('hotel_chain.hotel_chainID'), primary_key=True)
    phone_number = db.Column(db.String(20), primary_key=True)

class HotelPhoneNumbers(db.Model):
    __tablename__ = 'hotel_phone_numbers'
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), primary_key=True)
    phone_number = db.Column(db.String(20), primary_key=True)

class CustomerPhoneNumbers(db.Model):
    __tablename__ = 'customer_phone_numbers'
    customerID = db.Column(db.Integer, db.ForeignKey('customer.customerID'), primary_key=True)
    phone_number = db.Column(db.String(20), primary_key=True)

class EmployeePhoneNumbers(db.Model):
    __tablename__ = 'employee_phone_numbers'
    SSN = db.Column(db.String(11), db.ForeignKey('employee.SSN'), primary_key=True)
    phone_number = db.Column(db.String(20), primary_key=True)

class HotelChainEmails(db.Model):
    __tablename__ = 'hotel_chain_emails'
    hotel_chainID = db.Column(db.Integer, db.ForeignKey('hotel_chain.hotel_chainID'), primary_key=True)
    email = db.Column(db.String(255), primary_key=True)

class HotelEmails(db.Model):
    __tablename__ = 'hotel_emails'
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), primary_key=True)
    email = db.Column(db.String(255), primary_key=True)

class CustomerEmails(db.Model):
    __tablename__ = 'customer_emails'
    customerID = db.Column(db.Integer, db.ForeignKey('customer.customerID'), primary_key=True)
    email = db.Column(db.String(255), primary_key=True)

class EmployeeEmails(db.Model):
    __tablename__ = 'employee_emails'
    SSN = db.Column(db.String(11), db.ForeignKey('employee.SSN'), primary_key=True)
    email = db.Column(db.String(255), primary_key=True)

class EmployeeRoles(db.Model):
    __tablename__ = 'employee_roles'
    SSN = db.Column(db.String(11), db.ForeignKey('employee.SSN'), primary_key=True)
    role = db.Column(db.String(255), primary_key=True)

class RoomAmenities(db.Model):
    __tablename__ = 'room_amenities'
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), primary_key=True)
    room_number = db.Column(db.Integer, db.ForeignKey('room.room_number'), primary_key=True)
    amenities = db.Column(db.String(255), primary_key=True)

class RoomProblems(db.Model):
    __tablename__ = 'room_problems'
    hotelID = db.Column(db.Integer, db.ForeignKey('hotel.hotelID'), primary_key=True)
    room_number = db.Column(db.Integer, db.ForeignKey('room.room_number'), primary_key=True)
    problem = db.Column(db.String(255), primary_key=True)


