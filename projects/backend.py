from flask import Flask,render_template
from projects.models import db, Market

def create_app():

    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET","POST"])
    def home():
        markets = Market.query.all()
        return render_template("home.html", markets=markets)
    
    @app.route("/events", methods=["GET","POST"])
    def events():
        return render_template("events.html")
    
    @app.route("/login", methods=["GET","POST"])
    def login():
        return render_template("login.html")
    
    @app.route("/map", methods=["GET","POST"])
    def map():
        return render_template("map.html")
    
    @app.route("/userpage", methods=["GET","POST"])
    def userpage():
        return render_template("userpage.html")
    
    @app.route("/vendors", methods=["GET","POST"])
    def vendors():
        return render_template("vendors.html")

    return app