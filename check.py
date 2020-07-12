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
	opening = intervals[0].strip()
	closing = intervals[1].strip()
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
		return [days_list[0]]
	elif len(days_list)  == 2:       
		start_day = weekdays.index( days_list[0] )
		end_day = weekdays.index(days_list[1])
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
            
            first_days = day_splitter( unit.split(",")[0] )
            second_unit = unit.split(",")[1]
            second_days = day_splitter( second_unit.split()[0] )
            days_list.extend(first_days)
            days_list.extend(second_days)
            interval = second_unit.split(maxsplit=1)[1]

        else:
            
            days_list = day_splitter( unit.split()[0] )
            interval = unit.split(maxsplit=1)[1]
        for day in days_list:
            
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
	lunch_day = date_time.strftime("%a")
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

	with open(the_file, newline='') as csvfile:
		fieldnames = ["restaurant" , "times"]
		reader = csv.DictReader(csvfile, fieldnames = fieldnames)
		for row in reader:
			#print(row["restaurant"] +" ==> "+row['times'])
			rest_obj = { "name": row['restaurant'], 
						 "timetable": unit_splitter( row['times'] )
			}
			
			if checker(rest_obj, the_time):
				print(rest_obj["name"] +  " is open")
			else:
				print(rest_obj["name"] +  " IS CLOSED")
		

	



lunchtime = datetime(2020, 7, 6, 17, 0) 
find_my_lunch("restaurants.csv", lunchtime)



