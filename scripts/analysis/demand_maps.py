import pymysql,json
import csv,sys
from datetime import datetime
import shapefile
import random,dill
import numpy as np

weekday_counts = [52.,53.,52.,52.,52.,52.,52.]

try:
	taxi_volume = dill.load(open('../../data/volume_by_region.p','rb'))
except:
	taxi_volume = np.zeros((7,24,20,20),dtype=int)
	db = pymysql.connect("localhost","taxi","","nyctaxi",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
	c = db.cursor()
	c.execute("""SELECT weekday,hour,cnt,hp.id hp_id,hd.id hd_id,hp.hood_name hp_hood_name,hd.hood_name hd_hood_name from (select weekday,hour,pickup_hood,dropoff_hood,count(*) cnt from tripdata group by weekday,hour,pickup_hood,dropoff_hood) r inner join hoods as hp on hp.id=r.pickup_hood inner join hoods hd on hd.id=r.dropoff_hood order by cnt desc""")
	for result in c.fetchall():
		taxi_volume[int(result['weekday']),int(result['hour']),int(result['hp_id']),int(result['hd_id'])] = int(result['cnt'])

	dill.dump(taxi_volume,open('../../data/volume_by_region.p','wb'))


for day in range(7):
	taxi_volume[day,:,:,:] = taxi_volume[day,:,:,:]/weekday_counts[day]

print taxi_volume.shape

output = {"type":"FeatureCollection","features":[]}


sf = shapefile.Reader("../../maps/generated/neighborhoods.shp")

sall = sf.iterShapes()
hoods = [r[4].replace(' ','_') for r in sf.records()]

hood_data = []

k = 0

all_data = []

while True:
	try:
		s = sall.next()
		d = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[]}}
		d['id'] = k

		d['properties']['data'] = {}
		for di,departure_hood in enumerate(hoods):
			d['properties']['data'][departure_hood] = np.sum(taxi_volume[:5,6:,k,di])/5./18.
			all_data.append(np.sum(taxi_volume[:5,6:,k,di])/5./18.)
		d['properties']['name'] = hoods[k]
		# d['properties']['data'] = np.sum(taxi_volume[:,:,k,:])/24./7.
		for lng,lat in s.points:
			d['geometry']['coordinates'].append([lng,lat])
		d['geometry']['coordinates'] = [d['geometry']['coordinates']]
		output['features'].append(d)
		k += 1
	except:
		break

print max(all_data)
json.dump(output,open('../../app/via.json','wb'))