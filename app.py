from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, session, flash
import os
import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'Mzanzi_secret_key_2025'  # Required for flash messages

# Database configuration
DATABASE = 'Mzanzi.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def init_db():
    """Initialize database if it doesn't exist"""
    if not os.path.exists(DATABASE):
        print(f"Database {DATABASE} not found. Please run init_db.py first.")
        return False
    return True

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET"])
def home():
    conn = get_db_connection()
    markets = conn.execute("SELECT * FROM Market ORDER BY MarketID").fetchall()
    conn.close()
    print(markets)
    return render_template("home.html", markets=markets)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM User WHERE email_address = ?', (email,)
    ).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        # Login successful
        session['user_id'] = user['student_id']
        session['user_email'] = user['email_address']
        session['user_fullname'] = user['full_name']
        flash(f'Welcome back, {user["full_name"]}!', 'success')
        return redirect(url_for('userpage'))
    else:
        # Login failed
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('home'))

@app.route("/eventform", methods=["GET", "POST"])
def eventform():
    return render_template("EventForm.html")

@app.route("/events", methods=["GET", "POST"])
def events():
    return render_template("events.html")

@app.route("/faq", methods=["GET", "POST"])
def faq():
    return render_template("FAQ.html")

@app.route("/generalpolicies", methods=["GET", "POST"])
def generalpolicies():
    return render_template("generalpolicies.html")

@app.route("/maps/<int:market_id>", methods=["GET", "POST"])
def market_details(market_id):
    conn = get_db_connection()
    market = conn.execute("SELECT * FROM Market WHERE MarketID = ?", (market_id,)).fetchone()
    conn.close()
    return render_template("Maps.html", market=market)

@app.route("/marketrequestform", methods=["GET", "POST"])
def marketrequestform():
    return render_template("marketrequestfrom.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/userpage", methods=["GET", "POST"])
def userpage():
    return render_template("userpage.html")

@app.route("/vendorrequestform", methods=["GET", "POST"])
def vendorrequestform():
    return render_template("vendorrequestform.html")

@app.route("/vendors", methods=["GET", "POST"])
def vendors():
    return render_template("vendors.html")

# Run the application
if __name__ == "__main__":
    app.run(debug=True)