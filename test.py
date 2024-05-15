import csv
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv', encoding='utf-8', skipinitialspace=True, delimiter=',', quotechar='"')

# pressure = data['Pressure']
time = data['Time']
depth = data['Depth']

plt.plot(time, depth)
plt.xlabel('Time')
plt.ylabel('Depth (CM)')
plt.title('Time vs Depth')
plt.grid(True)
plt.show()

print(time)
print(depth)