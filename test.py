from datetime import time, datetime
import json

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
input1 = "Mon-Thu 11 am - 10:30 pm  / Fri  / Sat 11:30 am - 11 pm  / Sun 4:30 pm - 10:30 pm"
input2 = "Mon-Thu, Sun 11:30 am - 10 pm  / Fri-Sat 11:30 am - 11 pm"

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
    times_list = the_unit.split("/")
    for unit in times_list:
        if unit.find(",") > 0:
            
            extra_unit = unit.split(",")[1]
            times_list.insert( times_list.index(unit) +1 ,  extra_unit)
            corrected_unit = unit.split(",")[0]
            #print( day_splitter( corrected_unit.split()[0] ) )
            days_list = day_splitter( corrected_unit.split()[0] ) 
            interval = extra_unit.split(maxsplit=1)[1]
        else:
            #print( day_splitter( unit.split()[0]) )
            days_list = day_splitter( unit.split()[0])
            interval = unit.split(maxsplit=1)[1]
        for day in days_list:
            #print(day + " -- " +interval)
            timetable.update( { day : time_splitter(interval) } )

    return timetable


    
#rez = unit_splitter(input2)
#print(json.dumps(rez, indent=4  ) )

print(time_splitter("11 am-10:30 pm"))