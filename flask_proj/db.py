import os
from sqlite3 import connect
from dotenv import load_dotenv

load_dotenv()


def init_db():
    conn = connect(os.getenv('DB_ID'))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id integer NOT NULL PRIMARY KEY, email TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS reservations
                 (id integer NOT NULL PRIMARY KEY, date DATE, time TIME)''')
    conn.commit()
    conn.close()


def auth(email, password):
    conn = connect(os.getenv('DB_ID'))
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user


def make_reserve(date, time):
    return

def delete_expired():
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    expired_reservations = Reservation.query.filter(Reservation.date < ten_minutes_ago).all()
    
    for reservation in expired_reservations:
        db.session.delete(reservation)
    
    db.session.commit()