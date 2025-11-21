from flask import Flask, render_template
import os

app = Flask(__name__)

TEMPLATE_DIR = os.path.join(app.root_path, "templates")

# Automatically generate routes for every .html file
for filename in os.listdir(TEMPLATE_DIR):
    if filename.endswith(".html"):
        # Clean route (e.g., /faq)
        route_clean = "/" + filename.replace(".html", "").lower()

        # Raw .html route (e.g., /FAQ.html)
        route_html = "/" + filename

        # Use a factory to bind filename correctly
        def make_view(f):
            return lambda: render_template(f)

        # Register clean URL
        app.add_url_rule(route_clean, route_clean, make_view(filename))

        # Register .html URL
        app.add_url_rule(route_html, route_html, make_view(filename))

        print(f"Registered route: {route_clean}  -> {filename}")
        print(f"Registered route: {route_html} -> {filename}")


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)