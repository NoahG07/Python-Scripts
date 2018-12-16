#! /usr/bin/python3 

import socket
from requests import get

public_ip = get('https://api.ipify.org').text 
local_ip = socket.gethostbyname(socket.gethostname()) 

print('\nGetting public and local IP... ') 
#print('Public IP: ' + public_ip\n'Local IP: ' + local_ip)
print('Public IP: ' + public_ip) 
print('Local IP: ' + local_ip + '\n') 
