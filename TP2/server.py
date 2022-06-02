from socket import *

serverHost = '127.0.0.1'
serverPort = 30000

buffer_size = 10

serverSocket = socket(AF_INET, SOCK_DGRAM)  #Create a UDP socket
serverSocket.bind((serverHost, serverPort)) 

print ('The server is ready to receive!')

msg_to_client = 'pong'
while True:

  msg_from_client, clientAddress = serverSocket.recvfrom(buffer_size)
  modifiedMessage = msg_from_client.decode().upper()
  print('Recieved:' ,  modifiedMessage)


  serverSocket.sendto(msg_to_client.encode(), clientAddress)