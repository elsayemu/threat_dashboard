import sqlite3              # For interacting with SQLite database
import requests             # For making HTTP requests to external API
import os                   # For accessing environment variables
from datetime import datetime  # For timestamping records
from dotenv import load_dotenv # For loading variables from .env file

load_dotenv()

# Retrieve API key from environment
API_KEY = os.getenv("ABUSEIPDB_API_KEY")

DB = "database.db"

# Initialize the database and create table if it does not exist
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Create table to store threat data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique ID for each record
            ip TEXT,                               # IP address flagged as malicious
            score INTEGER,                         # Abuse confidence score from API
            country TEXT,                          # Country code of IP origin
            timestamp TEXT                         # Time when data was collected
        )
    """)

    # Save changes and close connection
    conn.commit()
    conn.close()

# Fetch threat data from AbuseIPDB API
def fetch_data():
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    
    # Headers required for authentication and response format
    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    # Query parameters to filter results
    params = {
        "confidenceMinimum": 75  # Only return high-confidence threats
    }

    # Send GET request to API
    response = requests.get(url, headers=headers, params=params)

    # Handle API error response
    if response.status_code != 200:
        print("Error fetching data:", response.text)
        return []

    # Extract relevant data from JSON response
    data = response.json()["data"]

    results = []

    # Process only first 20 entries to limit database size and API usage
    for entry in data[:20]:
        results.append({
            "ip": entry["ipAddress"],                    # Extract IP address
            "score": entry["abuseConfidenceScore"],      # Extract threat score
            "country": entry["countryCode"],             # Extract country code
            "timestamp": datetime.now().isoformat()      # Record current timestamp
        })

    return results


# Insert fetched data into database
def insert_data(entries):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Loop through each entry and insert into table
    for entry in entries:
        cursor.execute(
            "INSERT INTO threats (ip, score, country, timestamp) VALUES (?, ?, ?, ?)",
            (entry["ip"], entry["score"], entry["country"], entry["timestamp"])
        )

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Entry point of script
if __name__ == "__main__":
    # Ensure database and table exist
    init_db()

    # Fetch threat data from API
    data = fetch_data()

    # Insert fetched data into database
    insert_data(data)

    # Output number of records inserted
    print(f"Inserted {len(data)} records.")