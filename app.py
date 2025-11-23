import sqlite3
import base64
from flask import Flask, render_template

# --- Configuration ---
app = Flask(__name__)

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

if __name__ == '__main__':
    # Ensure you run 'python database_setup.py' once before running this app.
    print("Running Flask app. Ensure 'Mzanzi.db' exists.")
    app.run(debug=True)