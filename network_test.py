#! /usr/bin/env python3
import time, subprocess

count = 0
Tf = True

while Tf:
    subprocess.Popen(["ping -c 3 google.com"], shell=True)
    count += 1
    time.sleep(300)
    if count == 5:
        Tf = False
        exit
