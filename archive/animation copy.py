from matplotlib import dates as mdate
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import pandas as pd

m = pd.read_csv("covid-data.csv")

m['date'] = pd.to_datetime(m['date'], format = '%d-%m-%Y')
m.sort_values('date', inplace = True)

cdate = m['date']
ccase = m['total_cases']
cdeath = m['total_deaths']

fig = plt.figure()
ax1 = fig.add_subplot(111)

def animate(i):
    ax1.clear()
    ax1.plot(cdate[:i], ccase[:i], label = 'cases')
    ax1.plot(cdate[:i], cdeath[:i], label = 'deaths')
    ax1.legend(loc = 'upper left')
    ax1.set_xlim([cdate.iloc[0],
                  cdate.iloc[-1]])
    ax1.set_ylim([min(ccase.iloc[0], cdeath.iloc[0]),
                  max(ccase.iloc[-1], cdeath.iloc[-1])])
    ax1.xaxis.set_major_locator(mdate.DayLocator(interval = 5))
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%d-%m-%Y'))


ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.show()