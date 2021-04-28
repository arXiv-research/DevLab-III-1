# socket program starts by importing the socket library
import socket
import sys

# Make  socket instance with two parameters
# The first parameter is AF_INET : refers to the address family ipv4
# The second one is SOCK_STREAM which means connection oriented TCP protocol. socket.SOCK_DGRAM can be used to use the UDP protocol
# NOTE: if any error occurs during the creation of a socket then a socket.error
try: 
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Socket successfully created"
    print socket_instance
except socket.error as err: 
    print "socket creation failed with error %s" %(err)


# Findign the IP of the server using the socket library
try:
    host_ip = socket.gethostbyname('www.google.com')
    print "IP of the www.google.com : "
    print host_ip
except socket.gaierror: 
    # this means could not resolve the host 
    print "there was an error resolving the host"
    sys.exit() 
 
port = 80 
  
#connecting to the server# connecting to the server 
socket_instance.connect((host_ip, port)) 
  
print "the socket has successfully connected to google ip %s on port == %s" %(host_ip,port)
