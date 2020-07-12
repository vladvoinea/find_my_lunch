import json
import csv
from datetime import datetime, timedelta, time

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def time_splitter(interval):
	"""Splits the time interval into opening and closing datetime times

	Args:
	-----
	An string that has the following interval pattern:
	'11 am - 10:30 pm'

	Returns:
	--------
	A dict like:
	{
	 "open": datetime.time,
	 "close": datetime.time
	}
	"""


	intervals = interval.split("-")

	# removing leading and trailing spaces
	opening = intervals[0].strip()
	closing = intervals[1].strip()

	#Trying to match a format of '10:30 pm' or '11 am'
	try:
		opening_datetine = datetime.strptime(opening, "%I:%M %p" )
	except ValueError:
		opening_datetine = datetime.strptime(opening, "%I %p" )

	try:
		closing_datetime = datetime.strptime(closing, "%I:%M %p" )
	except ValueError:
		closing_datetime = datetime.strptime(closing, "%I %p" )


	return {
			"open": opening_datetine.time(),
			"close": closing_datetime.time()
		}

def day_splitter(days):
	'''
	Generates a list of days from a weekday interval

	Args:
	-----
	A string interval of the following patterns:
	'Mon-Tue'
	'Tue'

	Returns:
	--------
	A list of all the weekdays contained in the passed interval
	['Mon', 'Tue', 'Wed', 'Thu']
	['Tue']
	'''
	days_list = days.split("-")
	if len(days_list) == 1:
		# in case we only have one day
		return [days_list[0]]
	elif len(days_list)  == 2:      
		# in case we have an in terval
		# getting the index of where the start and end day are located within the week 
		start_day = weekdays.index( days_list[0] )
		end_day = weekdays.index(days_list[1])

		# then using them to slice the weekdays list
		return weekdays[start_day : end_day + 1]



def unit_splitter(the_unit):
	""" 
	Splits series of weekday and time intervals and build a dict that will contain the structured timetable
	for each restaurant

	Args:
	-----
	A time table series of units like:
	'Mon-Thu, Sun 11:30 am - 10 pm  / Fri-Sat 11:30 am - 11 pm'

	Returns:
	--------
	A dict with structured data:
	{
		"Mon": {
			"open":datetime.time,
			"close":datetime.time
		},
		"Tue": {
			"open":datetime.time,
			"close":datetime.time
		}
	}


	"""
	timetable = {}
	days_list = []
	times_list = the_unit.split("/")
	for unit in times_list:
		if unit.find(",") > 0:

			# dealing with the tricky scenario when the opening hours match 2 different intervals like 'Mon-Thu, Sun 9 am - 10 pm'
			first_days = day_splitter( unit.split(",")[0] )
			second_unit = unit.split(",")[1]
			second_days = day_splitter( second_unit.split()[0] )
			days_list.extend(first_days)
			days_list.extend(second_days)

			# we need to get the time interval so just split after the first space to get '9 am - 10 pm'
			interval = second_unit.split(maxsplit=1)[1]

		else:
			
			# the simple scenario 'Mon-Thu 9 am - 10 p'
			days_list = day_splitter( unit.split()[0] )
			interval = unit.split(maxsplit=1)[1]
		for day in days_list:
			
			# adding a key value pair to the dict using the .update() method
			timetable.update( { day : time_splitter(interval) } )

	return timetable



def checker( rest_obj, date_time):
	""" 
	Checks the object containg all the restaurant timetables against our specific lunch time

	Args:
	-----
	rest_obj is a dict a restaurant timetable:
	
		"timetable": {
			"Mon": {
				"open":datetime.time,
				"close":datetime.time
			},
			"Tue": {
				"open":datetime.time,
				"close":datetime.time
			}
		}
	

	Returns:
	--------
	TRUE if the timetable shows that the restaurant is open for us to have a 59min lunch
	FALSE if the restaurant is closed or closes by the time we want to have a 59min lunch

	"""

	# get the day of our intended lunch
	lunch_day = date_time.strftime("%a")
	# calculate the start time of the lunch + an estimated 59 minutes in order to have time to eat when you want to start your lunch at 12:55 and the restaurant closes at 13:00
	lunch_time = date_time + timedelta(minutes=59)
	if lunch_day in rest_obj["timetable"].keys() :
		
		if rest_obj["timetable"][lunch_day]["open"] < lunch_time.time() and rest_obj["timetable"][lunch_day]["close"] >= lunch_time.time() :
			return True
		else:
			return False
	else:
		return False



def find_my_lunch(the_file, the_time):
	"""
	Opens the file, and iterates over the restaurants to check which is open

	Args:
	-----
	the name of a csv file structured like:
	"Herbivore","Mon-Thu, Sun 9 am - 10 pm  / Fri-Sat 9 am - 11 pm"


	"""

	open_list = []
	with open(the_file, newline='') as csvfile:
		# put our own headers to the file since it doesn't have any
		fieldnames = ["restaurant" , "times"]
		reader = csv.DictReader(csvfile, fieldnames = fieldnames)
		for row in reader:

			rest_obj = { "name": row['restaurant'], 
						 "timetable": unit_splitter( row['times'] )
			}
			
			if checker(rest_obj, the_time):
				print(rest_obj["name"] +  " is open")
				open_list.append( rest_obj["name"] )
			else:
				print(rest_obj["name"] +  " IS CLOSED")
		return open_list
		

	



lunchtime = datetime(2020, 7, 6, 17, 0) 
print( find_my_lunch("restaurants.csv", lunchtime) )



