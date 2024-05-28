import serial
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import os

# Serial port configuration
serial_port = 'COM3'  # Replace with your serial port
baud_rate = 115200

# Create figure for plotting
fig, (ax1, ax2) = plt.subplots(2, 1)  # Creating two subplots vertically
plt.subplots_adjust(hspace=0.5, bottom=0.2)  # Adjusting vertical spacing and bottom margin
xs_pressure = []
ys_pressure = []
xs_depth = []
ys_depth = []

# Function to read data from the serial port
def read_serial_data(ser):
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            data = line.split(',')
            if len(data) == 2:  # Assuming data format is "pressure,water depth"
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]  # Get current timestamp up to two milliseconds
                pressure = float(data[0])
                depth = float(data[1])
                
                # Write data to CSV file
                with open('data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, pressure, depth])
                
                return timestamp, pressure, depth
        except Exception as e:
            print(f"Error reading from serial port: {e}")

# This function is called periodically from FuncAnimation
def animate(i):
    global xs_pressure, ys_pressure, xs_depth, ys_depth
    data = read_serial_data(ser)
    if data:
        timestamp, pressure, depth = data
        xs_pressure.append(timestamp)
        ys_pressure.append(pressure)
        xs_pressure = xs_pressure[-20:]  # Limit lists to last 20 items
        ys_pressure = ys_pressure[-20:]
        
        xs_depth.append(timestamp)
        ys_depth.append(depth)
        xs_depth = xs_depth[-20:]  # Limit lists to last 20 items
        ys_depth = ys_depth[-20:]
    
        ax1.clear()
        ax1.plot(xs_pressure, ys_pressure)
        ax1.set_title('Water Pressure Over Time')
        ax1.set_ylabel('Pressure (hPa)')

        ax2.clear()
        ax2.plot(xs_depth, ys_depth)
        ax2.set_title('Water Depth Over Time')
        ax2.set_ylabel('Depth (cm)')
        ax2.set_xlabel('Time')

        # Rotate x-axis ticks for both plots
        ax1.tick_params(axis='x', rotation=45)
        ax2.tick_params(axis='x', rotation=45)

def main():
    global ser
    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        # time.sleep(2)  # No longer needed

        # Check if the CSV file exists, if not, create it with headers
        if not os.path.exists('data.csv'):
            with open('data.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Pressure (hPa)', 'Depth (cm)'])

        # Start the animation
        ani = animation.FuncAnimation(fig, animate, interval=250)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
