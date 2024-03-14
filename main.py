import gtfs_realtime_pb2
from datetime import datetime
import pytz
import http.client
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--stop', type=str, metavar='stop', help='The ID of the stop to query. Find it on the bus stop sign.')
parser.add_argument('-r', '--route', type=str, metavar='route',help='The route to query.')
ARGS = parser.parse_args()

# format args.
# pad all routes which are numbers to be 3 chars long (pad with 0s)
try:
	int(ARGS.route)
	if ARGS.route != None and len(ARGS.route) < 3:
		ARGS.route = '0'*(3-len(ARGS.route)) + ARGS.route
except:
	pass

print(ARGS)

# get bd file from http
conn = http.client.HTTPSConnection('gtfs.edmonton.ca', timeout=10)
conn.request('GET', '/TMGTFSRealTimeWebService/TripUpdate/TripUpdates.pb')
response = conn.getresponse()

if response.status != 200:
	print('Got invalid response from gtfs.edmonton.ca:', response.status)	
	exit(-1)
else:
	content_type = response.getheader('Content-Type')
	content_length = response.getheader('Content-Length')
	print('Got response 200 from gtfs.edmonton.ca')
	print('  Content-Type:', content_type)
	print('  Content-Length:', content_length)

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.read())

print('Parsed response')

utc_minus_7 = pytz.timezone("Canada/Mountain")

updates = []

for entity in feed.entity:	
	temp = []

	if ARGS.route != None and entity.trip_update.trip.route_id != ARGS.route:
		continue
	
	for stop in entity.trip_update.stop_time_update:
		dt1 = datetime.fromtimestamp(stop.departure.time).astimezone(utc_minus_7)
		if dt1 < datetime.now().astimezone(utc_minus_7):
			continue
		if ARGS.stop == None or stop.stop_id == ARGS.stop:
			temp.append((dt1, stop.stop_id))

	for departure_time, stop_id in temp:
		updates.append({
			'route': entity.trip_update.trip.route_id,
			'bus_label': entity.trip_update.vehicle.label,
			'stop': stop_id,
			'departure_time': departure_time
			})	
	
if len(updates) > 0:
	print('route, bus_label, stop, departure_time')
	[print(d['route'], d['bus_label'], d['stop'], d['departure_time']) for d in sorted(updates, key=lambda entry: entry['departure_time'])]

conn.close()
print('Done')

