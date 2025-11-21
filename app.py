from flask import Flask, render_template, request, redirect, url_for
from models import db, User

app = Flask(__name__)

# ------ DATABASE CONFIG -------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mzanzimarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

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

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("About.html")

@app.route("/event-form")
def event_form():
    return render_template("EventForm.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/faq")
def faq():
    return render_template("FAQ.html")

@app.route("/general-policies")
def general_policies():
    return render_template("generalpolicies.html")

@app.route("/map-4way")
def map_4way():
    return render_template("Map_4way.html")

@app.route("/map-hazelwood")
def map_hazelwood():
    return render_template("map_hazelwood.html")

@app.route("/map-irene")
def map_irene():
    return render_template("map_irene.html")

@app.route("/map-montana")
def map_montana():
    return render_template("Map_montana.html")

@app.route("/map-pretorian")
def map_pretoria():
    return render_template("Map_pretoria.html")

@app.route("/map-vintage")
def map_vintage():
    return render_template("map_vintage.html")

@app.route("/market-request")
def market_request():
    return render_template("marketrequestform.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/user-page")
def user_page():
    return render_template("userpage.html")

@app.route("/vendor-request")
def vendor_request():
    return render_template("vendorrequestform.html")

@app.route("/vendors")
def vendors():
    return render_template("vendors.html")


@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)