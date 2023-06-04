from flask import Flask, render_template, request, redirect, session, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from database import db, User, Booking, Customer

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost:3306/booking_web"
db.init_app(app)
migrate = Migrate(app, db)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        existing_user = User.query.filter_by(account=account).first()
        
        if existing_user:
            # Xóa tài khoản nếu đã tồn tại
            db.session.delete(existing_user)
            db.session.commit()
            flash('Tài khoản đã tồn tại và đã được xóa.')
        
        # Tạo thông tin người dùng mới
        new_user = User(account=account, password=password, name=name, email=email, phone=phone, address=address)
        
        # Thêm người dùng mới vào cơ sở dữ liệu
        db.session.add(new_user)
        db.session.commit()
        print('Tài khoản đã được tạo thành công.')
        
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/read')
def read():
    users = User.query.all()
    return render_template('read.html', users=users)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return 'Không tìm thấy người dùng.'
    
    if request.method == 'POST':
        # Cập nhật thông tin người dùng
        user.account = request.form['account']
        user.password = request.form['password']
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.address = request.form['address']

        
        db.session.commit()
        print('Thông tin người dùng đã được cập nhật.')
        
        return 'Thông tin người dùng đã được cập nhật.'
    
    return render_template('edit.html', user=user)

@app.route('/delete/<int:user_id>')
def delete(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return 'Không tìm thấy người dùng.'
    
    db.session.delete(user)
    db.session.commit()
    flash ('Người dùng đã được xóa.')
    
    return 'Người dùng đã được xóa.'


@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/booking', methods=['GET', 'POST'])
def second_booking():
    if request.method == 'POST':
        customer_id = request.form['Customer ID']
        name = request.form['Name']
        email = request.form['Email']
        table_type = request.form['Table Type']
        guest_number = int(request.form['Guest Number'])
        placement = request.form['Placement']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time = datetime.strptime(request.form['time'], '%H:%M').time()
        note = request.form['Note']

        # Kiểm tra xem customer_id đã tồn tại hay chưa
        booking_exists = Booking.query.filter_by(customer_id=customer_id).first()
        if booking_exists:
            flash('Customer ID already exists', 'error')
            return redirect('/booking')
        
        customer_exists = Customer.query.filter_by(customer_id=customer_id).first()
        if customer_exists:
            flash('Customer ID already exists', 'error')
            return redirect('/booking')
        



        customer_id = request.form['Customer ID']
        name = request.form['Name']
        email = request.form['Email']
        guest_number = int(request.form['Guest Number'])

        # Tạo đối tượng Customer mới
        customer = Customer(
            customer_id=customer_id,
            name=name,
            email=email,
            guest_number=guest_number
        )
        # Tạo đối tượng Booking mới
        table_type = request.form['Table Type']
        placement = request.form['Placement']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time = datetime.strptime(request.form['time'], '%H:%M').time()
        note = request.form['Note']

        # Tạo đối tượng Booking mới và liên kết với đối tượng Customer
        # Tạo đối tượng Booking mới và liên kết với đối tượng Customer
        new_booking = Booking(
            customer=customer,  # Sử dụng đối tượng Customer đã tạo
            table_type=table_type,
            placement=placement,
            date=date,
            time=time,
            note=note
        )



        # Thêm vào cơ sở dữ liệu
        db.session.add(new_booking)
        db.session.commit()
        print('Booking successful', 'success')
        return 'Booking successful'
    else:
        bookings = Booking.query.all()
        return render_template('booking.html', bookings=bookings)
    
@app.route('/booking/<booking_id>')
def show_booking(booking_id):
    booking = Booking.query.get(booking_id)
    customer = booking.customer
    print(customer.name)  # In ra tên khách hàng

    return render_template('booking.html', booking=booking)

@app.route('/customer/<customer_id>')
def show_customer(customer_id):
    customer = Customer.query.get(customer_id)
    bookings = customer.bookings
    for booking in bookings:
        print(booking.table_type)  # In ra loại bàn

    return render_template('booking.html', customer=customer, bookings=bookings)


@app.route('/booking/edit/<int:id>', methods=['GET', 'POST'])
def edit_booking(id):
    booking = Booking.query.get(id)
    if request.method == 'POST':
        booking.customer.customer_id = request.form['Customer ID']
        booking.customer.name = request.form['Name']
        booking.customer.email = request.form['Email']
        booking.table_type = request.form['Table Type']
        booking.guest_number = int(request.form['Guest Number'])
        booking.placement = request.form['Placement']
        booking.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        booking.time = datetime.strptime(request.form['time'], '%H:%M').time()
        booking.note = request.form['Note']


        db.session.commit()
        flash('Booking updated', 'success')
        return 'Booking updated'
    else:
        return render_template('edit_booking.html', booking=booking)

@app.route('/booking/delete/<int:id>', methods=['POST'])
def delete_booking(id):
    booking = Booking.query.get(id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted', 'success')
    return redirect(url_for('booking'))



if __name__ == '__main__':
    app.run()
