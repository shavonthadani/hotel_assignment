from flask import render_template, request, redirect, url_for
from . import db
from sqlalchemy import text
from .models import Hotel, Room
from .forms import SearchRoomsForm, BookingForm
from flask import current_app as app 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book_room/<int:hotel_id>/<room_number>', methods=['GET', 'POST'])
def book_room(hotel_id, room_number):
    form = BookingForm()
    if form.validate_on_submit():
        # Process the booking using form data and the room_id
        # For example, create a booking record in the database
        
        return redirect(url_for('booking_success'))  # Redirect to a booking success page
    # If GET request or form not valid, render the booking form template
    return render_template('booking.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search_rooms():
    form = SearchRoomsForm()
    if form.validate_on_submit():
        # Retrieve form data
        start_date = form.start_date.data
        end_date = form.end_date.data
        capacity = form.capacity.data
        category = form.category.data
        
        # Optional fields
        area = form.area.data
        hotel_chain = form.hotel_chain.data
        price = form.price.data
        min_rooms = form.min_rooms.data if form.min_rooms.data else 0
        # Base SQL query incorporating mandatory fields and excluding booked rooms
        sql_query = """
            SELECT room.*, hotel_chain.name, hotel.city 
            FROM room
            JOIN hotel ON room.hotelID = hotel.hotelID
            JOIN hotel_chain ON hotel.hotel_chainID = hotel_chain.hotel_chainID
            WHERE hotel.hotelID IN (
                SELECT hotelID 
                FROM room
                GROUP BY hotelID
                HAVING COUNT(room_number) >= :min_rooms
            )
            AND room.capacity >= :capacity
            AND hotel.star_rating = :category
            AND NOT EXISTS (
                SELECT 1 FROM booking_renting br
                WHERE br.hotelID = room.hotelID
                AND br.room_number = room.room_number
                AND br.check_in_date <= :end_date
                AND br.check_out_date >= :start_date
            )

        """

        # Parameters dictionary
        params = {'capacity': capacity, 'category': category, 'start_date': start_date, 'end_date': end_date, 'min_rooms': min_rooms}

        # Append conditions for optional fields
        if area:
            sql_query += " AND hotel.city ILIKE :area"
            params['area'] = f"%{area}%"
        
        if hotel_chain:
            sql_query += " AND hotel.hotel_chainID IN (SELECT hotel_chainID FROM hotel_chain WHERE name = :hotel_chain)"
            params['hotel_chain'] = hotel_chain
        
        if price is not None:  # Check if price is provided (it could be 0)
            sql_query += " AND room.price <= :price"
            params['price'] = price

        # Execute the constructed query
        query = text(sql_query)
        available_rooms = db.engine.execute(query, **params).fetchall()

        # Render the template with available rooms
        return render_template('search_results.html', rooms=available_rooms)
    return render_template('search.html', form=form)