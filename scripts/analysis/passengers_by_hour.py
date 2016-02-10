import numpy as np
import pylab as plt
import pymysql,dill,sys
import seaborn as sns

weekday_counts = [52.,53.,52.,52.,52.,52.,52.]

try:
	taxi_volume = dill.load(open('../../data/passengers_by_hour.p','rb'))
except:
	taxi_volume = np.zeros((7,24),dtype=float)
	db = pymysql.connect("localhost","taxi","","nyctaxi",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
	c = db.cursor()
	c.execute("""SELECT weekday,hour,avg(passenger_count) passengers,count(*) cnt from tripdata where passenger_count < 5 group by weekday,hour""")
	for result in c.fetchall():
		taxi_volume[int(result['weekday']),int(result['hour'])] = float(result['passengers'])

	dill.dump(taxi_volume,open('../../data/passengers_by_hour.p','wb'))


print taxi_volume


taxi_volume = np.flipud(taxi_volume)
fig, ax = plt.subplots(figsize=(24,5.5))

cax = ax.pcolor(taxi_volume,cmap='Reds')#,vmin=1.5,vmax=2)
plt.xlim((0,24))
plt.xlabel('Pickup Time')
ax.set_xticks([0,5,10,15,20])
ax.set_xticklabels(['00:00','05:00','10:00','15:00','20:00'])
ax.set_yticks(np.arange(.5,7.5,1))
ax.set_yticklabels(['Sun','Sat','Fri','Thu','Wed','Tue','Mon'])

cbar = fig.colorbar(cax)

plt.show()