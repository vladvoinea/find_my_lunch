from datetime import time, datetime
import json

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
input1 = "Mon-Thu 11 am - 10:30 pm  / Fri  / Sat 11:30 am - 11 pm  / Sun 4:30 pm - 10:30 pm"
input2 = "Mon-Thu, Sun 11:30 am - 10 pm  / Fri-Sat 11:30 am - 11 pm"

def time_splitter(interval):
    	"""Splits the time interval into opening and closing datetime times

	Args:
	An string that has the following interval pattern:
	'11 am - 10:30 pm'

	Returns:
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
		A string interval of the following patterns:
		'Mon-Tue'
		'Tue'
		Returns:
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
	A time table series of units like:
	'Mon-Thu, Sun 11:30 am - 10 pm  / Fri-Sat 11:30 am - 11 pm'

	Returns:
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



#rez = unit_splitter(input2)
#print(json.dumps(rez, indent=4  ) )

#print(time_splitter("11 am-10:30 pm"))

print(day_splitter("Mon-Thu"))


""" 
	Checks the object containg all the restaurant timetables against our specific lunch time

	Args:
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
	TRUE if the timetable shows that the restaurant is open for us to have a 59min lunch
	FALSE if the restaurant is closed or closes by the time we want to have a 59min lunch

	"""