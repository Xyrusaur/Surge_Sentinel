import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# Serial port configuration
serial_port = 'COM3'  # Replace with your serial port
baud_rate = 115200

# Create figure for plotting
fig, ax = plt.subplots()
xs = []
ys = []

# Function to read data from the serial port
def read_serial_data(ser, xs, ys):
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            data = line.split(',')
            if len(data) == 2:  # Assuming data format is "timestamp,value"
                timestamp = datetime.now()  # Get current timestamp
                value = float(data[1])
                xs.append(timestamp)  # Append current timestamp
                ys.append(value)
                xs = xs[-20:]  # Limit lists to last 20 items
                ys = ys[-20:]
        except Exception as e:
            print(f"Error reading from serial port: {e}")

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    read_serial_data(ser, xs, ys)
    ax.clear()
    ax.plot(xs, ys)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Water Depth Over Time')
    plt.ylabel('Depth (cm)')

def main():
    global ser
    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        # time.sleep(2)  # No longer needed

        # Start the animation
        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
