from flask import Flask, render_template, redirect, url_for, request, flash as msg, session, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime
import os
import requests
import serial 


from flash import make_conf, flasher
from models import *
from dotenv import load_dotenv
from monitor import generate_frames, generate_serial_data
# from buttons import *


# Load enviroment variables
load_dotenv()

# Init Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)
login_manager = LoginManager(app)

conf_path = os.getenv('CONFIG_PATH')  # Init paths for firmwares

# Init additional functions for lab completing
# init_buttons()

# Create relations
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



def delete_expired_records():
    expired_records = Reservation.query.filter(
        (Reservation.date + datetime.timedelta(minutes=15)) < datetime.datetime.utcnow()
    ).all()
    for record in expired_records:
        db.session.delete(record)
    db.session.commit()

    
@app.route('/', methods=['GET'])
def index():
    delete_expired_records()
    return render_template('login.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('reserve'))
        else:
            msg('Login or password is incorrect')
            return redirect(url_for('signin'))
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if confirm_password != password:
            msg('Passwords don`t match')
            return redirect(url_for('signup'))
        user = User.query.filter_by(email=email).first()
        if user:
            msg('Email already exists')
            return redirect(url_for('signup'))
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        msg('Registration successful')
        return redirect(url_for('signin'))
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        datetime_str = date + ' ' + time
        datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        reservation_prev = datetime_obj - datetime.timedelta(minutes=15)
        reservation_next = datetime_obj + datetime.timedelta(minutes=15) 
        reservations = Reservation.query.filter(Reservation.date >= reservation_prev, Reservation.date <= reservation_next).all()
        if reservations:
            msg('Date and time already reserved')
            return redirect(url_for('reserve'))
        else:
            new_reservation = Reservation(date=datetime_obj, user_id=current_user.id)
            db.session.add(new_reservation)
            db.session.commit()
            msg('Reservation successful')
            return redirect(url_for('reserve'))
    return render_template('reserve.html')


@app.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    reservation = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.date).first()
    if reservation and reservation.date <= datetime.datetime.now():
        if request.method == 'POST':
            firmware = request.files['firmware']
            filename = firmware.filename
            firmware.save(fr'../firmwares/{filename}')
            username = current_user.id
            created_conf_path = make_conf(conf_path, filename, username)
            return redirect(url_for('monitor', ccp=created_conf_path))
        return render_template('send.html', ccp=None)
    else:
        msg('You have no reservation or your reservation time has not come yet')
        return redirect(url_for('reserve'))


@app.route('/stream')
def stream():    
    return Response(generate_serial_data(), mimetype='text/event-stream')


@app.route('/monitor', methods=['GET', 'POST'])
@login_required
def monitor():
    ccp = request.args.get('ccp')
    if not ccp:
        msg('You have to upload binary file')
        return redirect(url_for('send'))
    if Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.date).first():
        return render_template('monitor.html', case_2_logs=[x for x in range(100)])
    msg('You have no reservation or your reservation time has not come yet')
    return redirect(url_for('reserve'))


@app.route('/simulate_button', methods=['POST'])
def simulate_button():
    button = request.form['button']
    press_button(button)
    return redirect('/monitor')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/flash', methods=['POST'])
def flash():
    if request.method == "POST":
        return redirect(url_for('monitor'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', reservations=reservations)


@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
@login_required
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.user_id == current_user.id:
        db.session.delete(reservation)
        db.session.commit()
        msg('Reservation deleted successfully')
    else:
        msg('You are not authorized to delete this reservation')
    return redirect(url_for('profile'))
