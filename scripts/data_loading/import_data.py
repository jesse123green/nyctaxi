from glob import glob
import pymysql
import csv,sys
from datetime import datetime
import shapefile

sf = shapefile.Reader("../maps/neighborhoods.shp")

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


sall = sf.iterShapes()
hoods = [r[4] for r in sf.records()]

hood_borders = []
print hoods
while True:
    try:
        s = sall.next()
        # via_bb = ['%.3f' % coord for coord in s.bbox]
        via_bb = [[s.bbox[0],s.bbox[1]],[s.bbox[0],s.bbox[3]],[s.bbox[2],s.bbox[3]],[s.bbox[2],s.bbox[1]]]
        # print via_bb
        hood_borders.append(list(s.points))
    except:
        # print 'no'
        break

n_hoods = len(hoods)

db = pymysql.connect("localhost","taxi","","nyctaxi",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
k = 0
for f in glob('/Volumes/GLYPH-500 GB/taxi/taxidata_via/trip_data*'):
	with open(f,'rb') as c:
		print f
		creader = csv.reader(c)
		creader.next()
		for row in creader:

			if row[10] == '0' or row[11] == '0' or row[12] == '0' or row[13] == '0':
				continue

			try:
				pickup_lng = float(row[10])
				pickup_lat = float(row[11])
				dropoff_lng = float(row[12])
				dropoff_lat = float(row[13])
			except:
				continue
			flag = 0

			if dropoff_lng > -74.01934254624476 and dropoff_lng < -73.93505300005577 and dropoff_lat > 40.69977416538266 and dropoff_lat < 40.80335618764529:
				if pickup_lng > -74.01934254624476 and pickup_lng < -73.93505300005577 and pickup_lat > 40.69977416538266 and pickup_lat < 40.80335618764529:

					for n_p in range(n_hoods):
						if point_in_poly(pickup_lng,pickup_lat,hood_borders[n_p]):
							flag = 1
							for n_d in range(n_hoods):
								if point_in_poly(dropoff_lng,dropoff_lat,hood_borders[n_d]):
									y,mo,d = map(int,row[5].split()[0].split('-'))
									h,m,s = map(int,row[5].split()[1].split(':'))
									weekday = datetime(y,mo,d,h,m,s).weekday()									
									cursor.execute("""INSERT INTO tripdata VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(row[0],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],y,mo,d,h,m,weekday,n_p,n_d))
									break
						if flag == 1:
							break
			# data = list(row)
			# data.extend([y,mo,d,h,m,weekday])



		db.commit()
		