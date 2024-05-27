from matplotlib import dates as mdate
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import pandas as pd

m = pd.read_csv("data.csv")

m['Date_Time'] = pd.to_datetime(m['Date_Time'], format = '%Y-%m-%d %H:%M:%S')
m.sort_values('Date_Time', inplace = True)

cdate = m['Date_Time']
cwaterdepth = m['Water_Depth']
# cdepth = m['Depth']

fig = plt.figure()
ax1 = fig.add_subplot(111)

def animate(i):
    ax1.clear()
    ax1.plot(cdate[:i], cwaterdepth[:i], label = 'Water Depth')
    # ax1.plot(cdate[:i], cdepth[:i], label = 'Depth')
    ax1.legend(loc = 'upper left')
    ax1.set_xlim([cdate.iloc[0],
                  cdate.iloc[-1]])
    # ax1.set_ylim([min(cwaterdepth.iloc[0], cdepth.iloc[0]),
                  # max(cwaterdepth.iloc[-1], cdepth.iloc[-1])])
    ax1.xaxis.set_major_locator(mdate.SecondLocator(interval = 10))
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M:%S'))
    plt.grid()


ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.show()