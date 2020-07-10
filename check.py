import json
import csv
from datetime import datetime, timedelta, time


def time_splitter(times):
	return {
		"Mon": {
			"open": time(10,00),
			"close": time(20, 00)
		},
		"Tue": {
			"open": time(8, 00),
			"close": time(22, 00)
		}
	}


def checker( rest_obj, date_time):
	lunch_day = date_time.strftime("%a")
	lunch_time = date_time + timedelta(hours=1)
	if lunch_day in rest_obj["timetable"].keys() :
		print(lunch_time)
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
			print(row["restaurant"] +" ==> "+row['times'])
			rest_obj = { "name": row['restaurant'], 
						 "timetable": time_splitter( row['times'] )
			}
			print(rest_obj)
			if checker(rest_obj, the_time):
				print(rest_obj["name"] +  " is open")
			else:
				print(rest_obj["name"] +  " IS CLOSED")
		

	print("selected time is: "+ the_time.strftime("%a %I %M %p")) 



lunchtime = datetime(2020, 7, 6, 19, 1) 
find_my_lunch("restaurants.csv", lunchtime)



