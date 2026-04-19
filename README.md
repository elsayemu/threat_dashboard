The scope of this project involved designing and implementing a rudimentary lightweight threat monitoring system that takes in public threat intelligence and presents it through a web-based dashboard.

**Tools Used**

**Backend**:	I chose Python for this project as it’s really good for scripting and automation. I chose Flask as it’s a lightweight web framework that’s very easy to get up and running, especially for smaller projects such as this one. The project was organized and written in Visual Studio Code.
**API Integration**:	AbuseIPDB gives out real threat intelligence data including malicious IP addresses, geographic information, and confidence scores. I chose their API as it’s easy to obtain, real, and relevant to the field.
**Database**:	SQLite was used primarily for its simplicity. It offers database functions such as persistence, and querying, while also being perfect for small scale apps.
**Frontend**:	The frontend was done in HTML and JavaScript to stay minimal while also being functional.

Here’s the pipeline:
Threat API -> Data Collection Script -> Database -> Flask API -> Web Dashboard

To run this app, you must store your own AbuseIPDB API key in an .env file.
Next, run fetch_data.py, and finally, app.py.
