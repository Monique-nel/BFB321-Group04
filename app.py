from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

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

@app.route("/maps", methods=["GET", "POST"])
def maps():
    return render_template("Maps.html")

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