#! /usr/bin/python3

from sys import argv

try: 
    script, filename = argv 
except ValueError: 
    print("You forgot the filename. (Don't forget file extension)")

print ("")
print ("[*] Welcome User!") 
print ("[*] This is a simple note taking application.")
print ("[*] Working File: " + filename)
print ("-----------------------------------------------") 
print ("") 

f = open(filename, 'a')

while True:
    name = input()

# 'if' what I input is not equal to 'quit', the program will continue to write
# to the file.
    if name != 'quit':
        f.write(str(name) + '\n') 
# 'else' if quit was entered, the loop will break and close the file.
    else: 
        break 
        f.close() 
