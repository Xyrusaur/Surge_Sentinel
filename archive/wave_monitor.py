import serial
import csv
import pandas as pd
from datetime import datetime
# import matplotlib.pyplot as plt

# Serial port configuration
port = 'COM3'  # Replace with your actual serial port
baudrate = 115200  # Adjust baudrate if needed

# Open serial connection
ser = serial.Serial(port, baudrate)

# Open CSV file for writing (append mode) - Moved outside the loop
with open('data.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    
    # Check if the file is empty (has no lines)
    csvfile.seek(0, 2)  # Move file pointer to the end
    empty_file = csvfile.tell() == 0  # Check if file size is 0 bytes

  # Write headers if the file is empty
    if empty_file:
      csvfile.write("Date_Time,Water_Pressure,Water_Depth\n")

    # Read data from serial monitor in a loop
    while True:
        # Read incoming line
        data_line = ser.readline().decode('utf-8').strip()

        # Check if data is available
        if data_line:
            # Split data into list if needed (optional)
            data_list = data_line.split(',')

            # Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_list.insert(0,timestamp)
            csv_string = ",".join(data_list)

            # Write data to CSV file
            csvfile.write(f"{csv_string}\n")
            csvfile.flush() # Force data write to disk

            data = pd.read_csv('data.csv', encoding='utf-8', skipinitialspace=True, delimiter=',', quoting=csv.QUOTE_NONE)