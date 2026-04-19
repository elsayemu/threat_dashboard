from flask import Flask, render_template, jsonify  # Flask framework components
import sqlite3  # SQLite database interaction

# Initialize Flask application
app = Flask(__name__)

DB = "database.db"

# Establish database connection
def get_db():
    return sqlite3.connect(DB)

# Route for dashboard page
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint to retrieve threat data
@app.route("/api/threats")
def get_threats():
    # Connect to database
    conn = get_db()
    cursor = conn.cursor()

    # Execute SQL query:
    # - Select relevant fields
    # - Order by most recent entries first
    # - Limit to 50 records for performance
    cursor.execute("""
        SELECT ip, score, country, timestamp 
        FROM threats 
        ORDER BY timestamp DESC 
        LIMIT 50
    """)

    # Fetch all results from query
    rows = cursor.fetchall()

    # Close database connection
    conn.close()

    # Convert raw database rows into structured JSON format
    # Each row is mapped to a dictionary
    data = [
        {
            "ip": r[0],         # IP address
            "score": r[1],      # Threat score
            "country": r[2],    # Country of origin
            "timestamp": r[3]   # Time of data collection
        }
        for r in rows
    ]

    # Return data as JSON response to frontend
    return jsonify(data)


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)