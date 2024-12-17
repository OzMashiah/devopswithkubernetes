#!/usr/bin/env python3

# Import libraries.
import time
import string
import random 

randomstring = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) # 8 length randomly generated string.

def datehash(randomstring):
    # This function gets the date and a random string and prints it.
    with open("/usr/src/app/logs/date.txt", "r") as f:
        date = f.read()
    print(date + ": " + randomstring, flush=True)

if __name__ == "__main__":
    while True:
        datehash(randomstring)
        time.sleep(5) # 5 seconds delay between executions.
