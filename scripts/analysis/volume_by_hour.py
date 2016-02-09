import numpy as np
import pylab as plt
import pymysql,dill,sys
import seaborn as sns

weekday_counts = [52.,53.,52.,52.,52.,52.,52.]

try:
	taxi_volume = dill.load(open('../../data/volume_by_hour.p','rb'))
except:
	taxi_volume = np.zeros((7,24),dtype=int)
	db = pymysql.connect("localhost","taxi","","nyctaxi",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
	c = db.cursor()
	c.execute("""SELECT weekday,hour,count(*) cnt from tripdata group by weekday,hour""")
	for result in c.fetchall():
		taxi_volume[int(result['weekday']),int(result['hour'])] = int(result['cnt'])

	dill.dump(taxi_volume,open('../../data/volume_by_hour.p','wb'))


for day in range(7):
	taxi_volume[day,:] = taxi_volume[day,:]/weekday_counts[day]

# print taxi_volume
via = np.sum(np.sum(taxi_volume[:5,6:24],axis=1)/18.)/5.
M_Thu_night = np.sum(np.sum(taxi_volume[1:5,:2],axis=1)/2.)/4.
weekends_6_00 = np.sum(np.sum(taxi_volume[5:,6:24],axis=1)/18.)/2.
weekends_00_2 = np.sum(np.sum(taxi_volume[5:7,:2],axis=1)/2.)/2.
weekends_10_00 = np.sum(np.sum(taxi_volume[5:,10:24],axis=1)/14.)/2.

groups = [via,M_Thu_night,weekends_00_2,weekends_6_00,weekends_10_00]

print np.array(groups)/groups[0]

fig, ax = plt.subplots()
plt.bar(range(len(groups)),groups,align='center')
ax.set_xticks([0,1,2,3,4])
ax.set_xticklabels(['Via','Late Weekdays', 'Late Weekend','Weekend 06-00','Weekend 10-00'])
plt.xlabel('Rides per hour')
plt.title('Demand for NYC taxis by expansion option')
# plt.figure()
# plt.bar(range(7),latenight)

# plt.plot()



taxi_volume = np.flipud(taxi_volume)
fig, ax = plt.subplots(figsize=(24,5.5))
# plt.xticks(range(24))
# plt.yticks(np.array(range(7)) + .5)
# plt.grid()
cax = ax.pcolor(taxi_volume,cmap='Blues')#,vmin=0,vmax=.12)
plt.xlim((0,24))
plt.xlabel('Pickup Time')
ax.set_xticks([0,5,10,15,20])
ax.set_xticklabels(['00:00','05:00','10:00','15:00','20:00'])
ax.set_yticks(np.arange(.5,7.5,1))
ax.set_yticklabels(['Sun','Sat','Fri','Thu','Wed','Tue','Mon'])
cbar = fig.colorbar(cax,ticks=[5e3,10e3,15e3,20e3,25e3])
# cbar = fig.colorbar(cax)
cbar.ax.set_yticklabels(['5k', '10k', '15k','20k','25k'])# vertically oriented colorbar
# plt.savefig('plots/heatmap_all.png')
# plt.colorbar()
plt.show()