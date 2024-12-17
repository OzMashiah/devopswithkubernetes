#!/usr/bin/env python3

# Import libraries.
import time
import datetime

def datefile():
    # This function gets the date and a random string and prints it.
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # current date formatted to string.
    with open("/usr/src/app/logs/date.txt", "w") as f:
        f.write(date)

if __name__ == "__main__":
    while True:
        datefile()
        time.sleep(5) # 5 seconds delay between executions.
