from flask import Flask, render_template, request, redirect, url_for
from models import db, User

app = Flask(__name__)

# ------ DATABASE CONFIG -------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mzanzimarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# -------- ROUTES ------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register_user():

    # If GET → show register page
    if request.method == "GET":
        return render_template("register.html")

    # POST → create user
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Simple validation
    if not username or not email or not password:
        return "Missing required fields", 400

    # CHECK IF USER ALREADY EXISTS
    existing = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing:
        return "User already exists", 409

    # Create new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    # Send user to login page
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    return render_template("login.html")
