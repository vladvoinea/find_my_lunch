from datetime import datetime

timps =[ "3 pm", "4:30 pm"]

for timp in timps:
    try:
        tm = datetime.strptime(timp, "%I:%M %p" )
    except ValueError:
        tm = datetime.strptime(timp, "%I %p" )

    print(tm.time())
