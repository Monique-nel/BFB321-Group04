from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import base64

# --- Configuration ---
app = Flask(__name__)
app.secret_key = "my_super_secret_key_12345" 

# --- Jinja Filter for BLOB Images ---
def convert_blob_to_base64(blob_data):
    """
    Return a data-URI for a BLOB, a path for a string, 
    or an empty string if nothing supplied.
    """
    if not blob_data:                       # None or empty
        return ""
    
    if isinstance(blob_data, bytes):        # real SQLite BLOB
        return f"data:image/png;base64,{base64.b64encode(blob_data).decode('utf-8')}"
    
    if isinstance(blob_data, str):          # already a path / file name
        return blob_data                    # pass through unchanged
    
    return ""

app.jinja_env.filters['to_base64'] = convert_blob_to_base64

def get_db_connection():
    # FIX: Increased timeout to 30s and enabled WAL mode to prevent locking
    conn = sqlite3.connect('Mzanzi.db', timeout=30)
    conn.row_factory = sqlite3.Row 
    
    # Enable Write-Ahead Logging (WAL) - Huge help for concurrency
    try:
        conn.execute("PRAGMA journal_mode=WAL")
    except:
        pass # If it fails, it just ignores it, but usually it works
        
    return conn
# --- Routes ---

# DEFAULT ROUTE: Still serves the original request (MarketID = 2)
@app.route("/", methods=["GET"])
def home():
    conn = get_db_connection()
    markets = conn.execute("SELECT * FROM Market").fetchall()
    conn.close()
    return render_template("home.html", markets=markets)

@app.route("/market/<int:market_id>", methods=["GET"])
def market_details(market_id):
    conn = get_db_connection()
    market = conn.execute("SELECT * FROM Market WHERE MarketID = ?", (market_id,)).fetchone()
    conn.close()
    markets = [market] if market else []
    return render_template("home.html", markets=markets, current_id=market_id)

@app.route("/vendors", methods=["GET"])
def vendors():
    conn = get_db_connection()
    vendors = conn.execute("SELECT * FROM Vendor").fetchall()
    conn.close()
    return render_template("vendors.html", vendors=vendors)

@app.route("/events", methods=["GET"])
def events():
    conn = get_db_connection()
    events = conn.execute("SELECT * FROM Events").fetchall()
    conn.close()
    return render_template("events.html", events=events)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmpassword")

        if not username or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        user_type = "Customer"

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            existing_user = cursor.execute("SELECT * FROM User WHERE Email = ?", (email,)).fetchone()
            if existing_user:
                flash("Email address already registered.", "warning")
                conn.close()
                return redirect(url_for("register"))

            cursor.execute("""
                INSERT INTO User (Username, Email, Password, Classification)
                VALUES (?, ?, ?, ?)
            """, (username, email, hashed_password, user_type))
            
            conn.commit()
            conn.close()
            
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            print(f"Error registering user: {e}")
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return redirect(url_for("login"))
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM User WHERE Email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['Password'], password):
            session['user_id'] = user['UserID']
            session['username'] = user['Username']
            
            flash(f"Welcome back, {user['Username']}!", "success")
            return redirect(url_for('userpage')) 
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
            
    return render_template("login.html")

@app.route("/userpage")
def userpage():
    if 'user_id' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM User WHERE UserID = ?", (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template("userpage.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/vendor_request", methods=["GET", "POST"])
def vendor_request():
    if 'user_id' not in session:
        flash("Please log in to submit a vendor request.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        vendor_name = request.form.get("vendor_name")
        description = request.form.get("stall_description")
        vendor_type = request.form.get("vendor_type")
        contact = request.form.get("contact_number")
        
        try:
            conn = get_db_connection()
            
            conn.execute("UPDATE User SET Classification = ? WHERE UserID = ?", 
                         ('Vendor', session['user_id']))
            
            print(f"Promoting User {session['user_id']} to Vendor.")
            
            conn.commit()
            conn.close()
            
            flash("Congratulations! You are now a registered Vendor.", "success")
            return redirect(url_for('userpage'))
            
        except Exception as e:
            print(f"Error processing vendor request: {e}")
            flash("An error occurred (Database might be locked).", "danger")
            # FIX 2: Corrected 'vendorrequestform' to 'vendor_request'
            return redirect(url_for('vendor_request'))

    return render_template("vendorrequestform.html")

@app.route("/market_request", methods=["GET", "POST"])
def market_request():
    # 1. Security Check
    if 'user_id' not in session:
        flash("Please log in to register a market.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        # 2. Get Text Data
        market_name = request.form.get("market_name")
        description = request.form.get("description")
        location = request.form.get("location")
        location_link = request.form.get("location_link") 
        entry_fee = request.form.get("entry_fee")
        market_date = request.form.get("market_date")
        days = request.form.get("operating_days")
        instagram = request.form.get("instagram")
        facebook = request.form.get("facebook")
        
        # 3. Handle File Uploads (BLOB)
        poster_file = request.files.get("market_poster") 
        poster_blob = poster_file.read() if poster_file else None

        map_file = request.files.get("market_map")
        map_blob = map_file.read() if map_file else None

        conn = get_db_connection()
        try:
            # 4. Insert into Market Table using exact DB Schema columns
            conn.execute("""
                INSERT INTO Market (
                    MarketName, 
                    MarketDescription, 
                    MarketLocationLink,
                    MarketLocation, 
                    MarketEntryFee,
                    MarketDate,
                    MarketDays, 
                    MarketPoster,
                    MarketInstagram,
                    MarketFacebook,
                    MarketMap,
                    MarketAdministratorID
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                market_name, 
                description, 
                location_link,
                location, 
                entry_fee,
                market_date,
                days, 
                poster_blob,
                instagram,
                facebook,
                map_blob,
                session['user_id'] # Using logged-in user as the Admin ID
            ))
            
            # 5. Upgrade User Classification
            conn.execute("UPDATE User SET Classification = ? WHERE UserID = ?", 
                         ('MarketAdministrator', session['user_id']))
            
            conn.commit()
            flash("Market registered successfully!", "success")
            return redirect(url_for('home')) 
            
        except Exception as e:
            print(f"Error saving market: {e}")
            flash(f"Error saving market: {e}", "danger")
            return redirect(url_for('market_request'))
        finally:
            conn.close()

    return render_template("marketrequestform.html")

@app.route("/Eventform", methods=["GET", "POST"])
def Eventform():
    # 1. Security Check: Must be logged in
    if 'user_id' not in session:
        flash("Please log in to add an event.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        # 2. Get Text Data
        name = request.form.get("event_name")
        description = request.form.get("event_description")
        date = request.form.get("event_date") # Returns string "YYYY-MM-DDTHH:MM"
        days = request.form.get("event_days")
        link = request.form.get("booking_link")
        market_id = request.form.get("market_id")

        # 3. Handle File Upload (BLOB)
        poster_file = request.files.get("event_poster")
        # Read the file data into binary (BLOB) format if a file was selected
        poster_blob = poster_file.read() if poster_file else None

        try:
            # 4. Insert into Database
            conn.execute("""
                INSERT INTO Events (EventName, EventDescription, EventDate, EventDays, EventBookingLink, EventPoster, MarketID)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, description, date, days, link, poster_blob, market_id))
            
            conn.commit()
            flash("Event created successfully!", "success")
            return redirect(url_for('events')) # Redirect to events list after success
        except Exception as e:
            print(f"Error saving event: {e}")
            flash("Error saving event. Please try again.", "danger")
        finally:
            conn.close()

    # GET Request: Fetch markets for the dropdown so the user can select one
    markets = conn.execute("SELECT * FROM Market").fetchall()
    conn.close()
    
    return render_template("Eventform.html", markets=markets)

if __name__ == '__main__':
    print("Running Flask app. Ensure 'Mzanzi.db' exists.")
    app.run(debug=True)


# app routes for static pages 

@app.route('/general-policies')
def general_policies():
    return render_template('generalpolicies.html')

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

@app.route('/about')
def about():
    return render_template('About.html')