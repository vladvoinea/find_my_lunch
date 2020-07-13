# Find my lunch Challenge

## Requirement

Given the attached CSV file, write a function find_my_lunch(csv_file, open_datetime) which takes as parameters a filename and a Python datetime object and returns a list of restaurant names which are open on that date and time.
Comment your code as if it were being checked-in to your team's shared source control system, and note any limitations of your **complete solution** (the previous term should be avoided).

Correct solutions are more important than optimized solutions.

Assumptions:

* If a day of the week is not listed, the restaurant is closed on that day

* All times are local (don’t attempt timezone awareness)

* The CSV input file has no formatting errors


## Calling the function

Can be simply done by using the specified arguments:
'''python
find_my_lunch( "restaurants.csv", datetime.datetime(2020, 7, 6, 17, 0) ) 
'''

## Identified wrinkles 

* The input lunch time could be "funny" like 12:55 and a specific restaurant could be closing at 13:00. Hence the need to have a lunch duration that will be added to the innitial lunch time in order to perform the comparison.
* Some restaurants schedules have a day interval and a solitary day like: "Mon-Thu, Sun 11 am - 10 pm  / Fri-Sat 11 am - 12 am". So we need to correctly handle this scenario.


## Limitations

If the CSV input adheres to the rules that can be inferred from this sample csv, there should be no limitations

