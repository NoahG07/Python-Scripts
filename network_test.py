#! /usr/bin/env python3
# This script was made to test a network connection 
# every 3 minutes, if there are connectivity issues.
import time, subprocess

count = 0
Tf = True

while Tf:
    subprocess.Popen(["ping -c 2 google.com"], shell=True)
    count += 1
    time.sleep(300)
    if count == 5:
        Tf = False
        exit
