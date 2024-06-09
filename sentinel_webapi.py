from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# MySQL database configuration
db_config = {
    'user': 'surge_sentinel_admin',  # Replace with your MySQL username
    'password': 'Xyru$04147MS',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'sensor_data',
}

# Connect to the MySQL database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/api/data', methods=['GET'])
def get_data():
    last_timestamp = request.args.get('lastTimestamp')
    if not last_timestamp:
        return jsonify({"error": "Missing 'lastTimestamp' parameter"}), 400

    try:
        last_timestamp_dt = datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid 'lastTimestamp' format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400

    print(last_timestamp)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT date_time, water_pressure, water_depth 
        FROM water_metrics 
        WHERE date_time > %s
    """
    cursor.execute(query, (last_timestamp_dt,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
