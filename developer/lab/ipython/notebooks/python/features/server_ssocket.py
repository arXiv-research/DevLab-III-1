'''
Create a server on the local machine
Server has the below methods:
 bind(): It binds the server to a specific ip and port so that it can listen to incoming requests on that ip and port.
 listen(): It puts the server into listen mode. This allows the server to listen to incoming connections. 
 accept(): It initiates a connection with the client
 close(): It closes the connection with the client.
'''
import socket                
  
# next create a socket object 
s = socket.socket()          # it will take the default parameters 
print "Socket successfully created"
  
# reserve a port on the computer example 12345
port = 12345                
  
# Next bind to the port, by setting an empty string we are allowing the server listen to reuests coming from other computer  
s.bind(('', port))         
print "socket binded to %s" %(port) 
  
# put the socket into listening mode 
# 5 refers that 5 connections are kept waiting if the server is busy and 
# if 6th server tries to connect then the connection is refused
s.listen(5)      
print "socket is listening"            
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
   # Establish connection with client. 
   c, addr = s.accept()      
   print 'Got connection from', addr 
  
   # send a thank you message to the client.  
   c.send('Thank you for connecting') 
  
   # Close the connection with the client 
   c.close() 
