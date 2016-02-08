import shapefile,sys,time
import pymysql

db = pymysql.connect("localhost","taxi","","nyctaxi",charset="utf8",cursorclass=pymysql.cursors.DictCursor)

sf = shapefile.Reader("../maps/nyc_via_ll_simple.shp")

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



for s in sf.iterShapes():
    try:
        # via_bb = ['%.3f' % coord for coord in s.bbox]
        via_bb = [[s.bbox[0],s.bbox[1]],[s.bbox[0],s.bbox[3]],[s.bbox[2],s.bbox[3]],[s.bbox[2],s.bbox[1]]]
        print via_bb
        via = list(s.points)
    except:
        pass



c = db.cursor()
c2 = db.cursor()
t = time.time()
k = 0



while k < 168e6:
    c.execute("""SELECT medallion,pickup_datetime,pickup_latitude,pickup_longitude,dropoff_latitude,dropoff_longitude from tripdata WHERE trip_distance < 25 limit 500000 OFFSET %s""",(k,))
    print 'fresh new round...'
    flag = 0
    for result in c.fetchall():
        flag = 1
        if result['pickup_longitude'] > -74.01934254624476 and result['pickup_longitude'] < -73.93505300005577 and result['pickup_latitude'] > 40.69977416538266 and result['pickup_latitude'] < 40.80335618764529:
            if result['dropoff_longitude'] > -74.01934254624476 and result['dropoff_longitude'] < -73.93505300005577 and result['dropoff_latitude'] > 40.69977416538266 and result['dropoff_latitude'] < 40.80335618764529:
                if point_in_poly(result['pickup_longitude'],result['pickup_latitude'],via):
                    if point_in_poly(result['dropoff_longitude'],result['dropoff_latitude'],via):
                        c2.execute("""UPDATE tripdata set isvia=1 WHERE medallion=%s and pickup_datetime=%s""",(result['medallion'],result['pickup_datetime']))
        if k % 100000 == 0:
            db.commit()
            print k
        k += 1
    print 'Running for %.2f hrs'%((time.time()-t)/60./60.)
    if flag == 0:
        break

    # break
# print point_in_poly(-73.992325,40.728855,via_bb)

# print 170e6*(time.time()-t)/60./60./100000.
# shapeRecs = sf.shapeRecord(0)
# print shapeRecs.shape