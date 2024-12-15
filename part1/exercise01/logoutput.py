#!/usr/bin/env python3

# Import libraries.
import time
import datetime
import string
import random 

def datehash(randomstring):
    # This function gets the date and a random string and prints it.
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # current date formatted to string.
    print(date + ": " + randomstring)

if __name__ == "__main__":
    randomstring = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) # 8 length randomly generated string.
    while True:
        datehash(randomstring)
        time.sleep(5) # 5 seconds delay between executions.
