from flask import Flask,render_template

def create_app():

    app = Flask(__name__)
    
    app = create_app()
    
    if __name__ == "__main__":
        app.run(debug=True)

    @app.route("/", methods=["GET","POST"])
    def home():
        return render_template("home.html")
    
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