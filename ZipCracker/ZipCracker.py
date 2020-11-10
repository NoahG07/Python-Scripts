#! /usr/bin/env python3
""" Dictionary attack on password protected zipfiles """

# Add main() and extract() functions
# main() - opening zipfile and dictionary
# extract() - extract zipfile

import argparse
import zipfile
from time import sleep
import sys

parser = argparse.ArgumentParser(description="Breaking into zipfiles")
parser.add_argument("-z", "--zipfile", help="input, which is the zipfile")
parser.add_argument("-d", "--dictionary", help="dictionary file")
args = parser.parse_args()

# args.zipfile is the argument containing the zipfile
with zipfile.ZipFile(args.zipfile) as myzip:
    # args.dictionary is the argument containing the dictionary file
    with open(args.dictionary) as passwords:
        for line in passwords.readlines():
            # strips the line of all spaces and newlines '\n'
            newline = line.strip()
            try:
                password = bytes(newline.encode("utf-8"))
                myzip.extractall(pwd=password)
                print("Cracking...")
                sleep(2)
                print(f"\n[*] Extracted: {myzip.filename}")
                print(f"[*] Password: {newline}")
                sys.exit()
            # if there is an error with the password continue the loop
            except:
                continue
