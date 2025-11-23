from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('Mzanzi.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.template_filter("b64encode")
def b64encode_filter(data):
    if data is None:
        return None
    return base64.b64encode(data).decode("utf-8")

@app.route("/", methods=["GET"])
def home():
    conn = get_db_connection()
    markets = conn.execute("SELECT * FROM Market ORDER BY MarketID").fetchall()
    conn.close()
    print(markets)
    return render_template("home.html", markets=markets)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

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