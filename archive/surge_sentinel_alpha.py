import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
from datetime import datetime
import matplotlib.animation as animation
import csv
import os

# Serial port configuration
serial_port = 'COM3'  # Replace with your serial port
baud_rate = 115200

# Create figure for plotting
fig = Figure(figsize=(8, 6))
ax1 = fig.add_subplot(211)  # Creating two subplots vertically
ax2 = fig.add_subplot(212)
ax1.set_title('Water Pressure Over Time')
ax1.set_ylabel('Pressure (hPa)')
ax2.set_title('Water Depth Over Time')
ax2.set_ylabel('Depth (cm)')
ax2.set_xlabel('Time')
ax2.tick_params(axis='x', rotation=45)
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
                if os.path.getsize('data.csv') == 0:
                    # File is empty, write headers along with data
                    with open('data.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Time', 'Pressure (hPa)', 'Depth (Cm)'])  # Writing headers
                        writer.writerow([timestamp, pressure, depth])  # Writing data
                else:
                    # File is not empty, directly append data
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
        ax1.set_xticklabels([])

        ax2.clear()
        ax2.plot(xs_depth, ys_depth)
        ax2.set_title('Water Depth Over Time')
        ax2.set_ylabel('Depth (cm)')
        ax2.set_xlabel('Time')
        ax2.tick_params(axis='x', rotation=45)

def main():
    global ser
    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        
        # Check if the CSV file exists, if not, create it with headers
        if not os.path.exists('data.csv'):
            with open('data.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Pressure (hPa)', 'Depth (cm)'])

        # Create Tkinter GUI
        root = tk.Tk()
        root.title("Surge Sentinel")
        root.geometry("800x600")

        # Create a canvas
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Start the animation
        ani = animation.FuncAnimation(fig, animate, interval=250)

        root.mainloop()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
