from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:manu123@localhost/hotel_project'
    app.config['SECRET_KEY'] = '9b2de1a123d80b1eeb6d5c6f47aec25b'

    db.init_app(app)

    with app.app_context():
        from . import routes

    return app
