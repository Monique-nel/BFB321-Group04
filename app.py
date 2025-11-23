from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import base64

# --- Configuration ---
app = Flask(__name__)

app = Flask(__name__)
app.secret_key = "my_super_secret_key_12345" 

# --- Jinja Filter for BLOB Images ---
def convert_blob_to_base64(blob_data):
    """Converts raw BLOB data (e.g., image poster) to a Base64 string for HTML display."""
    if blob_data:
        # Assuming the poster is a PNG image. Adjust 'image/png' if needed.
        return f"data:image/png;base64,{base64.b64encode(blob_data).decode('utf-8')}"
    return None

# Register the filter with Jinja environment
app.jinja_env.filters['to_base64'] = convert_blob_to_base64

# --- Database Helper Function ---

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect('Mzanzi.db')
    conn.row_factory = sqlite3.Row 
    return conn

# --- Routes ---

# NEW ROUTE: Displays a specific market detail by ID passed in the URL
@app.route("/market/<int:market_id>", methods=["GET"])
def market_details(market_id):
    conn = get_db_connection()
    # Fetch the specific market using the ID from the URL
    market = conn.execute(
        "SELECT * FROM Market WHERE MarketID = ?", 
        (market_id,)
    ).fetchone() # Use fetchone() since we expect at most one row
    conn.close()

    # Pass a list containing the single market (or empty list if None) for the template loop compatibility
    markets = [market] if market else []
    
    # The home.html template is flexible enough to handle this single item/empty list
    # We pass 'current_id' to dynamically update the page title and heading.
    return render_template("home.html", markets=markets, current_id=market_id)

# DEFAULT ROUTE: Still serves the original request (MarketID = 2)
@app.route("/", methods=["GET"])
def home():
    conn = get_db_connection()
    
    # Fetch all rows
    markets = conn.execute("SELECT * FROM Market").fetchall()
    conn.close()
    print(f"Fetched {len(markets)} markets for home listing.")
    
    # Passes all markets to the template
    return render_template("home.html", markets=markets)

@app.route("/vendors", methods=["GET"])
def vendors():
    conn = get_db_connection()
    
    # Fetch all rows
    vendors = conn.execute("SELECT * FROM Vendor").fetchall()
    conn.close()
    print(f"Fetched {len(vendors)} vendors for home listing.")
    
    # Passes all vendors to the template
    return render_template("vendors.html", vendors=vendors)

@app.route("/events", methods=["GET"])
def events():
    conn = get_db_connection()
    
    # Fetch all rows
    events = conn.execute("SELECT * FROM Events").fetchall()
    conn.close()
    print(f"Fetched {len(events)} events for home listing.")
    
    # Passes all events to the template
    return render_template("events.html", events=events)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 1. Get data from the form
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmpassword")

        # 2. Basic Validation
        if not username or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        # 3. Hash the password
        hashed_password = generate_password_hash(password)
        user_type = "Customer"

        try:
            # Ensure you have this function defined elsewhere in app.py
            conn = get_db_connection()
            cursor = conn.cursor()

            # 5. Check if email already exists
            existing_user = cursor.execute("SELECT * FROM User WHERE Email = ?", (email,)).fetchone()
            if existing_user:
                flash("Email address already registered.", "warning")
                conn.close()
                return redirect(url_for("register"))

            # 6. Insert new user
            cursor.execute("""
                INSERT INTO User (Username, Email, Password, Classification)
                VALUES (?, ?, ?, ?)
            """, (username, email, hashed_password, user_type))
            
            conn.commit()
            print(f"User successfully added to database: {username} ({email})")
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

        # FIX: Validate input to ensure 'password' is a string (not None)
        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return redirect(url_for("login"))
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM User WHERE Email = ?", (email,)).fetchone()
        conn.close()

        # Verify user exists and password matches hash
        if user and check_password_hash(user['Password'], password):
            # In a real app, you would store the user in a session here
            flash(f"Welcome back, {user['Username']}!", "success")
            return redirect(url_for('userpage')) # Redirect to userpage page
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
            
    return render_template("login.html")

@app.route("/userpage", methods=["GET"])
def userpage():
    conn = get_db_connection()
    
    # Fetch all rows
    userpage = conn.execute("SELECT * FROM Events").fetchall()
    conn.close()
    print(f"Fetched {len(userpage)} userpage for home listing.")
    
    # Passes all userpage to the template
    return render_template("userpage.html", userpage=userpage)


if __name__ == '__main__':
    # Ensure you run 'python database_setup.py' once before running this app.
    print("Running Flask app. Ensure 'Mzanzi.db' exists.")
    app.run(debug=True)