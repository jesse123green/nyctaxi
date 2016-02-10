import numpy as np
import pylab as plt
import pymysql,dill,sys
import seaborn as sns


## Number of weekdays in dataset
weekday_counts = [52.,53.,52.,52.,52.,52.,52.]


####### Load Data
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

### Normalize by number of weekdays
for day in range(7):
	taxi_volume[day,:] = taxi_volume[day,:]/weekday_counts[day]



###### Expansion option bar chart

via = np.sum(np.sum(taxi_volume[:5,6:24],axis=1)/18.)/5.
M_Thu_night = np.sum(np.sum(taxi_volume[1:5,:2],axis=1)/2.)/4.
weekends_6_00 = np.sum(np.sum(taxi_volume[5:,6:24],axis=1)/18.)/2.
weekends_00_2 = np.sum(np.sum(taxi_volume[5:7,:2],axis=1)/2.)/2.
weekends_10_00 = np.sum(np.sum(taxi_volume[5:,10:24],axis=1)/14.)/2.

groups = [via,M_Thu_night,weekends_00_2,weekends_6_00,weekends_10_00]

print np.array(groups)/groups[0]


##### Heatmap

fig, ax = plt.subplots()
plt.bar(range(len(groups)),groups,align='center')
plt.bar([2],[13934],align='center',color='red') ##  SELECT count(*)/52/4 from tripdata where pickup_hood not in (18,19,7,15,14,0,6) and dropoff_hood not in (18,19,7,15,14,0,6) and hour < 2 and weekday > 4
ax.set_xticks([0,1,2,3,4])
ax.set_xticklabels(['Via','Late Weekdays', 'Late Weekend','Weekend 06-00','Weekend 10-00'])
plt.xlabel('Rides per hour')
plt.title('Demand for NYC taxis by expansion option')
# plt.figure()
# plt.bar(range(7),latenight)

plt.show()



taxi_volume = np.flipud(taxi_volume)
fig, ax = plt.subplots(figsize=(8,5.5))
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
# plt.savefig('plots/total_volume_heatmap.png')
# plt.colorbar()
plt.show()