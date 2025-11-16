from flask import Flask, render_template, request, redirect, url_for
from models import db, User

app = Flask(__name__)

# ------ DATABASE CONFIG -------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mzanzimarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    # Use a connection context
    with db.engine.connect() as conn:
        result = conn.execute("PRAGMA table_info(User);")
        for row in result:
            print(row)

    # Optional: test insert
    test_user = User(username="test", email="test@test.com", password="1234", classification="Customer")
    db.session.add(test_user)
    db.session.commit()
    print("Test user inserted!")


# -------- ROUTES ------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "GET":
        return render_template("register.html")
    
    # POST → create user
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Simple validation
    if not username or not email or not password:
        return "Missing required fields", 400

    # Create new user with exact column names
    new_user = User(
    username=username,
    email=email,
    password=password,
    classification="Customer"
    )
    db.session.add(new_user)
    db.session.commit()

    # Redirect to login page
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    return render_template("login.html")
