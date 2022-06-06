from socket import *
from math import sqrt
import time

serverName = 'localhost'
serverPort = 30000

buffer_size = 10
package_size = 30
package_lost = 0
package_sent = 0
package_received = 0
rtt = []
num_pings = 10
#Create a UDP socket
# clientSocket = socket(AF_INET, SOCK_DGRAM) 
# clientSocket.settimeout(1)  #tempo maximo de espera por uma resposta do server

# msg_to_server = 'ping'

def rtt_medio(rtt):
    list_sum = sum(rtt)
    media = list_sum / num_pings 
    return media

#standard deviation
def standard_deviation(rtt, media):
    sum = 0
    for i in range(0,num_pings): #ta indo de 0 a 9
        sum += (rtt[i] - media ) ** 2
    sd = sum/num_pings
    sd = sqrt(sd)
    return sd


for i in range(1,11):
    clientSocket = socket(AF_INET, SOCK_DGRAM) 
    clientSocket.settimeout(1.0)  #tempo maximo de espera por uma resposta do server
    msg_to_server = 'ping'

    if(len(msg_to_server) > package_size):
        print('Invalid message!')
        exit(1)

    else:
        #Important to count RTT
        starttime = time.time()
        #Sending message to server
        clientSocket.sendto(msg_to_server .encode(),(serverName, serverPort))
        try:
            msg_from_server, serverAddress = clientSocket.recvfrom(buffer_size)
            #Important to count RTT
            endtime = time.time()
            print(msg_from_server.decode())
            #RTT time
            rtt.append(endtime - starttime)
            #print('RTT : ' , rtt[i-1])
        #except clientSocket.Timeouterror:
        except timeout:
            package_lost+= package_lost
            print('Unfortunately this package has been lost...')


    clientSocket.close()

media = rtt_medio(rtt)
rtt.sort()
print('rtt max: {:03f}'   .format(rtt[num_pings - 1]) )
print('rtt min: {:03f}'  .format(rtt[0]) )
print('RTT medio: {:03f}' .format(rtt_medio(rtt)) )

sd = standard_deviation(rtt, media)
print('sd: {:03f}'  .format(sd))

#print('number of package lost: ' , package_lost)




