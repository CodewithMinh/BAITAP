from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost:3306/booking_web"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, account='{self.account}', password='{self.password}', name='{self.name}', email='{self.email}', phone='{self.phone}', address='{self.address}')>"
    
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    guest_number = db.Column(db.Integer, nullable=False)

    bookings = db.relationship('Booking', backref='customer')

    def __repr__(self):
        return f"Customer(id={self.id}, customer_id='{self.customer_id}', name='{self.name}', email='{self.email}', guest_number='{self.guest_number}')"


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    table_type = db.Column(db.String(50), nullable=False)
    placement = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Booking(id={self.id}, table_type='{self.table_type}', placement='{self.placement}', date='{self.date}', time='{self.time}', note='{self.note}')"
