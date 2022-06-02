from socket import *

serverName = 'localhost'
serverPort = 30000
buffer_size = 10

#Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)  

message = input("Input what you want to send to the server: ")

clientSocket.sendto(message.encode(),(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(buffer_size)

print(modifiedMessage.decode())

clientSocket.close()

