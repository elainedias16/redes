from socket import *

serverName = 'localhost'
serverPort = 30000

buffer_size = 10
package_size = 30
package_lost = 0

#Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM) 
clientSocket.settimeout(1)  #tempo maximo de espera por uma resposta do server

msg_to_server = 'ping'
for i in range(1,11):
    if(len(msg_to_server) > package_size):
        print('Invalid message!')
        exit(1)

    else:
        #Sending message to server
        clientSocket.sendto(msg_to_server .encode(),(serverName, serverPort))
        try:
            msg_from_server, serverAddress = clientSocket.recvfrom(buffer_size)
            print(msg_from_server.decode())
        except clientSocket.Timeouterror:
            package_lost+= package_lost
            print('Unfortunately the package has been lost...')


print('number of package lost: ' ,package_lost)
clientSocket.close()