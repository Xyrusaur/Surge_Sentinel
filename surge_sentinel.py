import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

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
                timestamp = datetime.now()  # Get current timestamp
                pressure = float(data[0])
                depth = float(data[1])
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
        ax1.set_ylabel('Pressure (Pa)')

        ax2.clear()
        ax2.plot(xs_depth, ys_depth)
        ax2.set_title('Water Depth Over Time')
        ax2.set_ylabel('Depth (cm)')
        ax2.set_xlabel('Time')

        plt.xticks(rotation=45, ha='right')

def main():
    global ser
    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        # time.sleep(2)  # No longer needed

        # Start the animation
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
