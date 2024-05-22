import serial
import csv
import pandas as pd  # Optional, used for comments
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.animation as animation

# Serial port configuration
port = 'COM3'  # Replace with your actual serial port
baudrate = 115200  # Adjust baudrate if needed

# Open serial connection
ser = serial.Serial(port, baudrate)

# Variables to store data for animation
water_pressures = []  # Assuming water pressure is the first column
depths = []

# Open CSV file for writing (append mode) - Moved outside the loop
with open('data.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)

    # Check if the file is empty (has no lines)
    csvfile.seek(0, 2)
    empty_file = csvfile.tell() == 0  # Check if file size is 0 bytes

    # Write headers if the file is empty
    if empty_file:
        writer.writerow(["Water Pressure", "Depth"])  # Adjust header if pressure is named differently


def get_data():
    """
    Reads data from the serial port and updates the global lists water_pressures and depths.
    Handles potential errors during data parsing.
    """
    # Read incoming line
    data_line = ser.readline().decode('utf-8').strip()

    # Check if data is available
    if data_line:
        # Split data into a list (optional)
        try:
            data_list = data_line.split(',')
        except ValueError:
            print(f"Error splitting data line: {data_line}")
            return

        # Extract water pressure (assuming pressure is the first element)
        try:
            water_pressure = float(data_list[0])
        except ValueError:
            print(f"Error converting water pressure to float: {data_line}")
            return

        water_pressures.append(water_pressure)

        # Extract depth (assuming depth is the last element)
        try:
            depth = float(data_list[-1])
        except ValueError:
            print(f"Error converting depth to float: {data_line}")
            return

        return water_pressure, depth  # Return extracted values

    # Initialize empty lists if no data received yet (optional)
    return [], []  # Or any other initialization logic


def animate(i):
    """
    This function is called for each frame of the animation.
    Updates the line plot with the latest data (up to a certain limit).
    Sets labels, title, and grid.
    """
    # Get new data (if available)
    try:
        water_pressure, depth = get_data()  # Get data and handle potential errors
    except Exception as e:
        print(f"Error getting data: {e}")
        return line,  # Return the line object even on error (to avoid animation stopping)

    # Update line data only if there's data (and handle empty depths)
    if water_pressures:
        max_data_points = 100
        if not depths:  # Check if depths is empty
            print("No depth data received yet.")
            return line  # Avoid plotting with empty depths
        valid_pressures = water_pressures[-max_data_points:]
        valid_depths = depths[-max_data_points:]
        line.set_data(valid_pressures, valid_depths)
    else:
        print("No data received yet.")

    # Set labels, title, and grid (can be done outside animate if they don't change)
    ax.set_xlabel('Water Pressure')  # Update label based on actual pressure name
    ax.set_ylabel('Depth (CM)')
    ax.set_title('Water Pressure vs Depth')
    ax.grid(True)

    return line,


fig, ax = plt.subplots()
line, = ax.plot([], [], label='Depth')  # Initialize empty line object

# Create animation object
anim = animation.FuncAnimation(fig, animate, frames=1000, interval=200)  # Adjust frames and interval

plt.show()
