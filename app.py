from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import base64
import math

# --- Configuration ---
app = Flask(__name__)
app.secret_key = "my_super_secret_key_12345" 



# --- UNIVERSAL IMAGE FILTER ---
@app.template_filter('b64encode')
def b64encode_filter(data):
    if not data:
        return ""
    
    # 1. Handle SQLite 'memoryview' (common with BLOBs)
    if isinstance(data, memoryview):
        data = bytes(data)
    
    # 2. Handle Bytes (Actual Image Data) - Return base64 string
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')
    
    # 3. Handle Strings (File Paths) - Return as-is (or encode if you prefer)
    # If your DB has "logo.png", we don't want to base64 encode that text.
    if isinstance(data, str):
        return data 

    return ""

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
    
    page = request.args.get('page', 1, type=int)
    per_page = 6
    offset = (page - 1) * per_page
    
    conn = get_db_connection()

    total_markets = conn.execute("SELECT COUNT(*) FROM Market").fetchone()[0]
    total_pages = math.ceil(total_markets / per_page)
    
    markets = conn.execute("SELECT * FROM Market LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    conn.close()
    return render_template("home.html", markets=markets, page=page,total_pages=total_pages)

@app.route("/maps/<int:market_id>")
def maps(market_id):
    conn = get_db_connection()
    # Fetch the specific market
    market = conn.execute("SELECT * FROM Market WHERE MarketID = ?", (market_id,)).fetchone()
    conn.close()

    if market is None:
        return "Market not found", 404

    # Pass 'market' (singular) to the template
    return render_template("Maps.html", market=market)

@app.route("/vendors", methods=["GET"])
def vendors():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    offset = (page - 1) * per_page
    
    conn = get_db_connection()

    total_markets = conn.execute("SELECT COUNT(*) FROM Market").fetchone()[0]
    total_pages = math.ceil(total_markets / per_page)
    
    vendors = conn.execute("SELECT * FROM Vendor LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    conn.close()
    return render_template("vendors.html", vendors=vendors, page=page,total_pages=total_pages)

@app.route("/events", methods=["GET"])
def events():
    # 1. Pagination setup
    page = request.args.get('page', 1, type=int)
    per_page = 4
    offset = (page - 1) * per_page

    conn = get_db_connection()
    
    # 2. Count total events
    total_events = conn.execute("SELECT COUNT(*) FROM Events").fetchone()[0]
    total_pages = (total_events + per_page - 1) // per_page

    # 3. THE UPDATED QUERY (Joins Events with Market to get the Name)
    query = """
        SELECT Events.*, Market.MarketName 
        FROM Events 
        JOIN Market ON Events.MarketID = Market.MarketID 
        LIMIT ? OFFSET ?
    """
    events = conn.execute(query, (per_page, offset)).fetchall()
    conn.close()

    return render_template("events.html", events=events, page=page, total_pages=total_pages)

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

@app.route("/userpage", methods=['GET', 'POST'])
def userpage():
    if 'user_id' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    user_id = session['user_id']

    # Fetch User
    user = conn.execute("SELECT * FROM User WHERE UserID = ?", (user_id,)).fetchone()
    vendor = conn.execute("SELECT * FROM Vendor WHERE UserID = ?", (user_id,)).fetchone()

    vendor = None
    vendor_products = []

    # If user is vendor, load vendor + products
    if user['Classification'] == 'Vendor':
        vendor = conn.execute("SELECT * FROM Vendor WHERE UserID = ?", (user_id,)).fetchone()
        if vendor:
            vendor_products = conn.execute(
                "SELECT * FROM Product WHERE VendorID = ?",
                (vendor['VendorID'],)
            ).fetchall()

    # -------------------------
    #           POST
    # -------------------------
    if request.method == 'POST':
        action = request.form.get('action')

        try:
            if action == 'update_vendor':
                v_name = request.form.get('vendor_name')
                v_desc = request.form.get('vendor_description')
                v_type = request.form.get('vendor_type')
                v_contact = request.form.get('contact_number')
                v_loc = request.form.get('vendor_location')
                v_web = request.form.get('website')
                v_fb = request.form.get('facebook')
                v_insta = request.form.get('instagram')

                if not vendor:
                    conn.execute("""
                        INSERT INTO Vendor 
                        (UserID, VendorName, VendorStallDescription, VendorOfferingType, 
                         VendorContactNumber, VendorLocation, VendorWebsite, VendorFacebook, VendorInstagram)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, v_name, v_desc, v_type, v_contact, v_loc, v_web, v_fb, v_insta))

                else:
                    conn.execute("""
                        UPDATE Vendor 
                        SET VendorName=?, VendorStallDescription=?, VendorOfferingType=?, 
                            VendorContactNumber=?, VendorLocation=?, VendorWebsite=?, 
                            VendorFacebook=?, VendorInstagram=?
                        WHERE UserID=?
                    """, (v_name, v_desc, v_type, v_contact, v_loc, v_web, v_fb, v_insta, user_id))

                conn.commit()
                flash("Vendor profile updated!", "success")
                return redirect(url_for('userpage'))

            elif action == 'update_username':
                new_username = request.form.get('username')

                conn.execute("UPDATE User SET Username = ? WHERE UserID = ?", (new_username, user_id))
                conn.commit()

                session['username'] = new_username
                flash("Username updated successfully!", "success")
                return redirect(url_for('userpage'))

            elif action == 'update_email':
                new_email = request.form.get('email')

                conn.execute("UPDATE User SET Email = ? WHERE UserID = ?", (new_email, user_id))
                conn.commit()

                flash("Email updated successfully!", "success")
                return redirect(url_for('userpage'))

            elif action == 'update_password':
                current_pw = request.form.get('current_password')
                new_pw = request.form.get('new_password')

                db_user = conn.execute("SELECT Password FROM User WHERE UserID = ?", (user_id,)).fetchone()

                if db_user and db_user['Password'] == current_pw:
                    conn.execute("UPDATE User SET Password = ? WHERE UserID = ?", (new_pw, user_id))
                    conn.commit()
                    flash("Password changed successfully!", "success")
                else:
                    flash("Incorrect current password.", "danger")

                return redirect(url_for('userpage'))

            elif action == 'add_product':
                p_name = request.form.get('product_name')
                p_price = request.form.get('product_price')

                if vendor:
                    conn.execute("""
                        INSERT INTO Product (ProductName, ProductPrice, VendorID)
                        VALUES (?, ?, ?)
                    """, (p_name, p_price, vendor['VendorID']))
                    conn.commit()
                    flash("Product added!", "success")

                return redirect(url_for('userpage'))
            
            elif action == 'update_product':
                product_id = request.form['product_id']
                name = request.form['product_name']
                price = request.form['product_price']

                conn.execute("""
                    UPDATE Product SET ProductName=?, ProductPrice=?
                    WHERE ProductID=? AND VendorID=?
                """, (name, price, product_id, vendor['VendorID']))
                conn.commit()
                flash("Product updated!", "success")
                return redirect(url_for('userpage'))

            elif action == 'update_event':
                e_name = request.form['event_name']
                e_desc = request.form['event_description']
                e_date = request.form['event_date']
                e_days = request.form['event_days']
                e_link = request.form['event_booking_link']

                e_poster = None
                if 'event_poster' in request.files:
                    f = request.files['event_poster']
                    if f.filename:
                        e_poster = f.read()

                market_row = conn.execute(
                    "SELECT MarketID FROM Market WHERE MarketAdministratorID = ?",
                    (user_id,)
                ).fetchone()

                if market_row:
                    conn.execute("""
                        INSERT INTO Events 
                        (MarketID, EventName, EventDescription, EventDate, EventDays, EventBookingLink, EventPoster)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (market_row['MarketID'], e_name, e_desc, e_date, e_days, e_link, e_poster))

                    conn.commit()
                    flash("Event added successfully!", "success")
                else:
                    flash("Please create a market profile first.", "warning")

                return redirect(url_for('userpage'))

            elif action == 'delete_profile':
                conn.execute("DELETE FROM User WHERE UserID = ?", (user_id,))
                conn.commit()
                session.clear()
                flash("Your profile has been permanently deleted.", "info")
                return redirect(url_for('login'))

            elif action == 'update_vendor':
                # 1. Retrieve all text inputs from the form
                vendor_name = request.form.get('vendor_name')
                vendor_type = request.form.get('vendor_type')
                vendor_location = request.form.get('vendor_location')
                vendor_description = request.form.get('vendor_description')
                contact_number = request.form.get('contact_number')
                website = request.form.get('website')
                instagram = request.form.get('instagram')
                facebook = request.form.get('facebook')

                # 2. Update the Text Data
                # We update these fields regardless of whether images are changed
                conn.execute("""
                    UPDATE Vendor 
                    SET VendorName = ?, 
                        VendorOfferingType = ?, 
                        VendorLocation = ?, 
                        VendorStallDescription = ?, 
                        VendorContactNumber = ?, 
                        VendorWebsite = ?, 
                        VendorInstagram = ?, 
                        VendorFacebook = ?
                    WHERE UserID = ?
                """, (vendor_name, vendor_type, vendor_location, vendor_description, 
                    contact_number, website, instagram, facebook, user_id))

                # 3. Handle Vendor Logo (Only update if a new file is selected)
                logo_file = request.files.get('vendor_logo')
                if logo_file and logo_file.filename != '':
                    try:
                        logo_data = base64.b64encode(logo_file.read()).decode('utf-8')
                        conn.execute("UPDATE Vendor SET VendorLogo = ? WHERE UserID = ?", (logo_data, user_id))
                    except Exception as e:
                        print(f"Error uploading logo: {e}")

                # 4. Handle Description Picture (Only update if a new file is selected)
                banner_file = request.files.get('description_picture')
                if banner_file and banner_file.filename != '':
                    try:
                        banner_data = base64.b64encode(banner_file.read()).decode('utf-8')
                        conn.execute("UPDATE Vendor SET VendorDescriptionPicture = ? WHERE UserID = ?", (banner_data, user_id))
                    except Exception as e:
                        print(f"Error uploading banner: {e}")

                # 5. Commit and Redirect
                conn.commit()
                flash("Vendor profile updated successfully!", "success")
                return redirect(url_for('userpage'))
            
            elif action == 'update_market':
                # 1. Get data from the form
                market_name = request.form.get('market_name')
                market_location = request.form.get('market_location')
                entry_fee = request.form.get('entry_fee')
                
                # 2. Handle the file upload (Market Logo)
                logo_file = request.files.get('market_logo')

                try:
                    # Check if the user actually has a market to edit
                    existing_market = conn.execute("SELECT MarketID FROM Market WHERE AdminID = ?", (user_id,)).fetchone()
                    
                    if existing_market:
                        # SCENARIO A: User uploaded a NEW logo
                        if logo_file and logo_file.filename != '':
                            # Convert image to Base64 string for database storage
                            image_data = logo_file.read()
                            encoded_logo = base64.b64encode(image_data).decode('utf-8')

                            conn.execute("""
                                UPDATE Market 
                                SET MarketName = ?, MarketLocation = ?, MarketEntryFee = ?, MarketLogo = ?
                                WHERE AdminID = ?
                            """, (market_name, market_location, entry_fee, encoded_logo, user_id))

                        # SCENARIO B: User is only updating text (Keep existing logo)
                        else:
                            conn.execute("""
                                UPDATE Market 
                                SET MarketName = ?, MarketLocation = ?, MarketEntryFee = ?
                                WHERE AdminID = ?
                            """, (market_name, market_location, entry_fee, user_id))

                        conn.commit()
                        flash("Market details updated successfully!", "success")
                    
                    else:
                        # Should not happen if button is only shown to Admins, but good for safety
                        flash("No market found linked to this account.", "warning")

                except Exception as e:
                    conn.rollback()
                    flash(f"Error updating market: {e}", "danger")
                
                return redirect(url_for('user_page'))
            
            elif action == 'delete_vendor_profile':
                # 1. Delete products associated with this vendor
                vendor_entry = conn.execute("SELECT VendorID FROM Vendor WHERE UserID = ?", (user_id,)).fetchone()
                if vendor_entry:
                    conn.execute("DELETE FROM Product WHERE VendorID = ?", (vendor_entry['VendorID'],))
                
                # 2. Delete the Vendor profile
                conn.execute("DELETE FROM Vendor WHERE UserID = ?", (user_id,))
                
                # 3. FIX: Change 'User' to 'Customer' (or your database's valid default role)
                conn.execute("UPDATE User SET Classification = 'Customer' WHERE UserID = ?", (user_id,))
                
                conn.commit()
                flash("Vendor profile and products deleted. You are now a standard Customer.", "info")
                return redirect(url_for('userpage'))
        
        
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
            print("Database Error:", e)
            return redirect(url_for("userpage"))

    # -------------------------
    #      GET REQUEST
    # -------------------------
    market = None
    events = []
    vendors = []

    if user['Classification'] == 'MarketAdministrator':
        market = conn.execute(
            "SELECT * FROM Market WHERE MarketAdministratorID = ?",
            (user_id,)
        ).fetchone()

        if market:
            events = conn.execute(
                "SELECT * FROM Events WHERE MarketID = ?",
                (market['MarketID'],)
            ).fetchall()

            vendors = conn.execute("SELECT * FROM Vendor").fetchall()

    conn.close()

    return render_template(
        "userpage.html",
        user=user,
        market=market,
        events=events,
        vendors=vendors,
        vendor = vendor,
        vendor_products=vendor_products
    )

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/vendor_request", methods=["GET", "POST"])
def vendor_request():
    conn = get_db_connection()

    if 'user_id' not in session:
        conn.close()
        flash("Please log in to submit a vendor request.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        # 1. Get Text Data
        vendor_name = request.form.get("vendor_name")
        description = request.form.get("stall_description") 
        vendor_type = request.form.get("vendor_type")
        contact = request.form.get("contact_number")
        website = request.form.get("website")
        facebook = request.form.get("facebook")
        instagram = request.form.get("instagram")
        
        # Get the Market ID from the dropdown
        market_id = request.form.get("market_id")
        
        # 2. Handle File Uploads
        logo_blob = None
        if 'vendor_logo' in request.files:
            file = request.files['vendor_logo']
            if file.filename:
                logo_blob = file.read() 
        
        descriptor_blob = None
        if 'vendor_picture' in request.files:
            file = request.files['vendor_picture']
            if file.filename:
                descriptor_blob = file.read() 

        try:
            user_id = session['user_id']
            
            # 3. INSERT into the VENDOR table (Using your specific column names)
            sql = """
                INSERT INTO Vendor (
                    VendorName, 
                    VendorStallDescription, 
                    VendorOfferingType, 
                    VendorContactNumber, 
                    VendorWebsite, 
                    VendorFacebook, 
                    VendorInstagram, 
                    VendorLogo, 
                    VendorDescriptionPicture, 
                    MarketID, 
                    UserID
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                vendor_name, 
                description, 
                vendor_type, 
                contact, 
                website, 
                facebook, 
                instagram, 
                logo_blob, 
                descriptor_blob, 
                market_id, 
                user_id
            )
            
            conn.execute(sql, params)
            
            # Optional: Also update User table to say they are now a 'Vendor'
            conn.execute("UPDATE User SET Classification = 'Vendor' WHERE UserID = ?", (user_id,))
            
            conn.commit()
            flash("Congratulations! You are now a registered Vendor.", "success")
            return redirect(url_for('userpage'))
            
        except Exception as e:
            print(f"Error processing vendor request: {e}")
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for('vendor_request'))
        finally:
            conn.close()

    # --- GET REQUEST ---
    # Fetch markets for the dropdown
    markets = conn.execute("SELECT * FROM Market").fetchall()
    conn.close()
    
    return render_template("vendorrequestform.html", markets=markets)

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
    # 1. Security Check
    if 'user_id' not in session:
        flash("Please log in to add an event.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    
    # 2. AUTOMATICALLY FIND THE MARKET
    # FIX: Changed 'MarketID' to 'MarketAdministratorID' based on your userpage code
    market = conn.execute("SELECT MarketID FROM Market WHERE MarketAdministratorID = ?", (session['user_id'],)).fetchone()

    # 3. Validation: Ensure the user actually owns a market
    if not market:
        flash("You must be a Market Administrator to create an event.", "danger")
        conn.close()
        return redirect(url_for('userpage')) 

    market_id = market['MarketID'] # We now have the ID automatically

    if request.method == "POST":
        name = request.form.get("event_name")
        description = request.form.get("event_description")
        date = request.form.get("event_date") 
        days = request.form.get("event_days")
        link = request.form.get("booking_link")

        poster_file = request.files.get("event_poster")
        poster_blob = poster_file.read() if poster_file else None

        try:
            conn.execute("""
                INSERT INTO Events (EventName, EventDescription, EventDate, EventDays, EventBookingLink, EventPoster, MarketID)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, description, date, days, link, poster_blob, market_id))
            
            conn.commit()
            flash("Event created successfully!", "success")
            return redirect(url_for('events')) # Or redirect back to userpage if you prefer
        except Exception as e:
            print(f"Error saving event: {e}")
            flash("Error saving event.", "danger")
        finally:
            conn.close()
    
    conn.close()
    return render_template("Eventform.html")

@app.route('/general-policies')
def general_policies():
    return render_template('generalpolicies.html')

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    if 'user_id' not in session:
        flash("You must be logged in to do that.", "danger")
        return redirect(url_for('login'))

    try:
        user_id = session['user_id']
        conn = get_db_connection()
        
        # ---------------------------------------------------------
        # 1. Delete associated data first (Children)
        # ---------------------------------------------------------
        # NOTE: Ensure the column name in these tables matches your DB 
        # (e.g., 'UserID', 'user_id', or 'OwnerID')
        
        conn.execute('DELETE FROM Market WHERE MarketAdministratorID = ?', (user_id,))
        conn.execute('DELETE FROM Vendor WHERE UserID = ?', (user_id,))
        conn.execute('DELETE FROM Events WHERE MarketID = ?', (user_id,))
        
        # ---------------------------------------------------------
        # 2. Delete the user (Parent)
        # ---------------------------------------------------------
        conn.execute('DELETE FROM User WHERE UserID = ?', (user_id,))
        
        conn.commit()
        conn.close()

        # 3. Clear the session (Logout)
        session.clear()

        flash('Your account and all associated data have been deleted.', 'success')
        return redirect(url_for('home'))

    except Exception as e:
        print(f"Delete Error: {e}")
        flash('Error deleting account.', 'danger')
        return redirect(url_for('userpage'))
    
@app.route('/vendor_products/<int:vendor_id>')
def vendor_products(vendor_id):
    conn = get_db_connection()
    
    # 1. Get the Vendor's details (so you can display their name)
    vendor = conn.execute('SELECT * FROM Vendor WHERE VendorID = ?', (vendor_id,)).fetchone()
    
    # 2. Get the Products for this specific vendor
    products = conn.execute('SELECT * FROM Product WHERE VendorID = ?', (vendor_id,)).fetchall()
    
    conn.close()
    
    # 3. Send data to HTML
    return render_template('products.html', vendor=vendor, products=products)    
    
if __name__ == '__main__':
    print("Running Flask app. Ensure 'Mzanzi.db' exists.")
    app.run(debug=True)