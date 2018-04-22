import urllib
from xml.etree.ElementTree import ElementTree
import webbrowser
new = 2 # open in a new tab, if possible
data_file = './rt22.xml'

#hit the public ctabustracker api for some bus data
u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data = u.read()
f = open(data_file, 'wb')
f.write(data)
f.close()

office_latitude = 41.98062
# find_bus_id = 4366
find_bus_id = 4120
north_bound_buses = []
south_bound_buses = []

#follow that bus
fb_direction = None
fb_lat = None
fb_lon = None
follow_bus = None

tree = ElementTree()
doc = tree.parse(data_file)

for bus in doc.findall('bus'):
    bus_id = int(bus.findtext('id'))
    print 'bus_id: {}'.format(bus_id)
    direction = bus.findtext('dd')
    lat = float(bus.findtext('lat'))
    lon = float(bus.findtext('lon'))
    if bus_id == find_bus_id:
        print bus
        follow_bus = bus
        fb_direction = direction
        fb_lat = lat
        fb_lon = lon

    if lat > office_latitude and direction.startswith('North'):
        north_bound_buses.append(bus)
    elif lat < office_latitude and direction == 'Southbound':
        south_bound_buses.append(bus)


print '%f %f' % (fb_lat, fb_lon)
print len(north_bound_buses)
print len(south_bound_buses)
for bus in north_bound_buses:
    print '%s %f' % (bus.findtext('dd'), float(bus.findtext('lat')))

for bus in south_bound_buses:
    print '%s %f' % (bus.findtext('dd'), float(bus.findtext('lat')))

map_url = "https://maps.googleapis.com/maps/api/staticmap?center=41.878674,-87.640333&zoom=14&size=400x400\
&markers=color:blue%7Clabel:Bus%7C{:f},{:f}&key=AIzaSyACIfog8ROa7QUniCL5c1gg72VS_6TYa24".format(fb_lat, fb_lon)

# map_url = "https://google.com"

webbrowser.open_new(map_url)
