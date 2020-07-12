import json
import csv
from datetime import datetime, timedelta, time

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def time_splitter(interval):
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
    days_list = days.split("-")
    if len(days_list) == 1:
        return [days_list[0]]
    elif len(days_list)  == 2:       
        start_day = weekdays.index( days_list[0] )
        end_day = weekdays.index(days_list[1])
        return weekdays[start_day : end_day + 1]



def unit_splitter(the_unit):
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



