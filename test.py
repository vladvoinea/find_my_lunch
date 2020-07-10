import datetime

obj = {
		"Mon": {
			"open": datetime.time(10,00),
			"close": datetime.time(20, 00)
		},
		"Tue": {
			"open": datetime.time(8, 00),
			"close": datetime.time(22, 00)
		}
	}


print(obj.keys())
