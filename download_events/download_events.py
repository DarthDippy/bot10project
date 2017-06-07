# Simple python script to download event information from Meetup and Eventbrite and load to Postgres

import urllib2
import json
import psycopg2
import datetime


# Define where to geographically grab events
EVENT_LAT = '33.7751'
EVENT_LON = '-84.3908'
EVENT_RADIUS = '50'

# Meetup API Info
MEETUP_API_KEY = '87872f624223d394a56593b7b2738'
MEETUP_API_LINK = 'https://api.meetup.com/2/open_events'
MEETUP_API_PARAMS = 'key=' + MEETUP_API_KEY + '&sign=true&radius=' + EVENT_RADIUS + '&lat=' + EVENT_LAT + '&lon=' + EVENT_LON

#Eventbrite API Info
EVENTBRITE_API_KEY = '57WTPIE4PAOHTQVGQWWU'
EVENTBRITE_API_LINK = 'https://www.eventbriteapi.com/v3/events/search/'
EVENTBRITE_API_PARAMS = ('start_date.range_start=2017-06-06T00:00:00&start_date.range_end=2017-06-09T00:00:00' + '&location.latitude=' + EVENT_LAT + '&location.longitude=' + EVENT_LON + '&location.within=' 
	+ EVENT_RADIUS + 'mi&token=' + EVENTBRITE_API_KEY)

# Postgres DB Info
POSTGRES_DB_HOST = 'postgresql-group10.postgres.database.azure.com'
POSTGRES_DB_PORT = '5432'
POSTGRES_DB_USER = 'group10@postgresql-group10'
POSTGRES_DB_PASS = 'connectTHEawesomeness10'
POSTGRES_DB_NAME = 'postgres'
POSTGRES_DB_TABLE = 'decode.events'


# Download and return Meetup JSON Events
def downloadMeetup():
	meetup_json = json.loads(urllib2.urlopen(MEETUP_API_LINK + '?' + MEETUP_API_PARAMS).read())
	return meetup_json

# Download and return Eventbrite JSON Events
def downloadEventbrite():
	result = json.loads(urllib2.urlopen(EVENTBRITE_API_LINK + '?' + EVENTBRITE_API_PARAMS).read())
	result_page_count = int(result['pagination']['page_count'])

	for i in range(1, result_page_count):
		#try:
		result = json.loads(urllib2.urlopen(EVENTBRITE_API_LINK + '?' + EVENTBRITE_API_PARAMS + '&page=' + str(i)).read())
		parseEventbrite(result)
		#except HTTPError:
		#	print "Rate limit reached!"
		#	sleep(60)


# Parse and Store Meetup JSON Events
def parseMeetup(meetup_json):
	# Connect to DB
	conn = psycopg2.connect(dbname=POSTGRES_DB_NAME,user=POSTGRES_DB_USER,password=POSTGRES_DB_PASS,host=POSTGRES_DB_HOST,port=POSTGRES_DB_PORT)
	cur = conn.cursor()

	insert_error_count = 0
	key_error_count = 0

	for result in meetup_json['results']:
		try:
			event_id = str(result['id'])
			source = 'Meetup'
			event_name = result['name']
			event_description = result['description']
			event_url = result['event_url']
			if 'fee' not in result:
				event_free = True
				event_cost = 0
				event_cost_currency = 'USD'
			else:
				event_free = False
				event_cost = result['fee']['amount']
				event_currency = result['fee']['currency']
			yes_rsvp_count = result['yes_rsvp_count']
			maybe_rsvp_count = result['maybe_rsvp_count']
			if 'rsvp_limit' in result:
				capacity = result['rsvp_limit']
			else:
				capacity = -1
			waitlist = result['waitlist_count']
			venue_name = result['venue']['name']
			venue_address = result['venue']['address_1']
			if 'zip' in result['venue']:
				venue_zip = result['venue']['zip']
			else:
				venue_zip = -1
			venue_city = result['venue']['city']
			if 'state' in result:
				venue_state = result['venue']['state']
			else:
				venue_state = ''
			venue_lat = result['venue']['lat']
			venue_lon = result['venue']['lon']
			group_name = result['group']['name']
			created = int(result['created']) / 1000
			updated = int(result['updated']) / 1000
			start_time = int(result['time']) / 1000
			if 'duration' in result:
				end_time = (int(result['time']) + int(result['duration'])) / 1000
			else:
				end_time = (int(result['time']) + 10800000) / 1000

			#try:
			cur.execute("INSERT INTO " + POSTGRES_DB_TABLE + " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (event_id, source,
				event_name, event_description, event_url, event_free, event_cost, event_cost_currency, yes_rsvp_count, maybe_rsvp_count, capacity, waitlist,
				venue_name, venue_address, venue_zip, venue_city, venue_state, venue_lat, venue_lon, group_name, datetime.datetime.fromtimestamp(created),
				datetime.datetime.fromtimestamp(updated), datetime.datetime.fromtimestamp(start_time), datetime.datetime.fromtimestamp(end_time)))
			#except UnicodeEncodeError:
			#	insert_error_count += 1
		except KeyError:
			key_error_count += 1

		

	print "Insert errors: " + str(insert_error_count)
	print "Key errors: " + str(key_error_count)
	conn.commit()
	cur.close()
	conn.close()



# Parse and Store Eventbrite JSON Events
def parseEventbrite(eventbrite_json):
	# Connect to DB
	conn = psycopg2.connect(dbname=POSTGRES_DB_NAME,user=POSTGRES_DB_USER,password=POSTGRES_DB_PASS,host=POSTGRES_DB_HOST,port=POSTGRES_DB_PORT)
	cur = conn.cursor()

	insert_error_count = 0
	key_error_count = 0

	for event in eventbrite_json['events']:
		try:
			venue = json.loads(urllib2.urlopen('https://www.eventbriteapi.com/v3/venues/' + event['venue_id'] + '/?token=' + EVENTBRITE_API_KEY).read())
			organizer = json.loads(urllib2.urlopen('https://www.eventbriteapi.com/v3/organizers/' + event['organizer_id'] + '/?token=' + EVENTBRITE_API_KEY).read())
			event_id = str(event['id'])
			source = 'Eventbrite'
			event_name = event['name']['text']
			event_description = event['description']['text']
			event_url = event['url']
			event_free = event['is_free']
			event_cost = -1
			event_cost_currency = event['currency']
			yes_rsvp_count = -1
			maybe_rsvp_count = -1
			capacity = event['capacity']
			waitlist = -1
			venue_name = venue['name']
			venue_address = venue['address']['address_1']
			venue_zip = venue['address']['postal_code']
			venue_city = venue['address']['city']
			venue_state = venue['address']['region']
			venue_lat = venue['latitude']
			venue_lon = venue['longitude']
			group_name = organizer['name']
			created = str(event['created']).replace('Z', 'UTC')
			updated = str(event['changed']).replace('Z', 'UTC')
			start_time = str(event['start']['utc']).replace('Z', 'UTC')
			end_time = str(event['end']['utc']).replace('Z', 'UTC')

			try:
				cur.execute("INSERT INTO " + POSTGRES_DB_TABLE + " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (event_id, source,
					event_name, event_description, event_url, event_free, event_cost, event_cost_currency, yes_rsvp_count, maybe_rsvp_count, capacity, waitlist,
					venue_name, venue_address, venue_zip, venue_city, venue_state, venue_lat, venue_lon, group_name, datetime.datetime.strptime(created, '%Y-%m-%dT%H:%M:%S%Z'),
					datetime.datetime.strptime(updated, '%Y-%m-%dT%H:%M:%S%Z'), datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%Z'),
					datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%Z')))
			except:
				insert_error_count += 1
		except:
			key_error_count += 1
		#except HTTPError:
		#	perint "Rate limit reached!"
		#	sleep(60)

		

	print "Insert errors: " + str(insert_error_count)
	print "Key errors: " + str(key_error_count)
	conn.commit()
	cur.close()



# Main
if __name__ == "__main__":
	meetup_json = downloadMeetup()
	parseMeetup(meetup_json)

	downloadEventbrite()
