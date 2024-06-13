import serial
import mysql.connector
from datetime import datetime
import pytz

# Serial port configuration
port = 'COM3'  # Replace with your actual serial port
baudrate = 115200  # Adjust baudrate if needed

# Open serial connection
ser = serial.Serial(port, baudrate)

# MySQL database configuration
db_config = {
    'user': 'surge_sentinel_admin',  # Replace with your MySQL username
    'password': 'Xyru$04147MS',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'sensor_data',
}

# Connect to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Insert data into MySQL database
def insert_data(timestamp, water_pressure, water_depth):
    insert_query = (
        "INSERT INTO water_metrics (date_time, water_pressure, water_depth) "
        "VALUES (%s, %s, %s)"
    )
    data = (timestamp, water_pressure, water_depth)
    cursor.execute(insert_query, data)
    conn.commit()

# Read data from serial monitor in a loop
while True:
    # Read incoming line
    data_line = ser.readline().decode('utf-8').strip()

    # Check if data is available
    if data_line:
        # Split data into list if needed (optional)
        data_list = data_line.split(',')

        # Get current timestamp with timezone information
        local_tz = pytz.timezone('Pacific/Auckland')
        timestamp = datetime.now(local_tz)
        
        # Ensure the data list has the correct number of elements
        if len(data_list) == 2:
            try:
                water_pressure = float(data_list[0])
                water_depth = float(data_list[1])

                # Insert data into MySQL database
                insert_data(timestamp, water_pressure, water_depth)
            except ValueError:
                print("Error: Invalid data format")

# Close the database connection
cursor.close()
conn.close()
