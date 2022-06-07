from socket import *
import math
import time
#from string import slipt

serverName = 'localhost'
serverPort = 30000

buffer_size = 10
package_size = 40

package_lost = 0
package_sent = 0
package_received = 0
percent_lost = 0

rtt = []
num_pings = 10
#dicionario chave index e content lista de tempo

#Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM) 
clientSocket.settimeout(1)  #Maximum time of waiting

def rtt_medio(rtt):
    list_sum = sum(rtt)
    media = list_sum / num_pings 
    return media

def standard_deviation(rtt, media):
    sum = 0
    for i in range(0,num_pings): 
        sum += (rtt[i] - media ) ** 2
    sd = sum/num_pings
    sd = math.sqrt(sd)
    return sd

#Checking if the header is valid
def valid_message(message):
    str = message
    print(str[0:5])  # num seq , 5 digitos , pega do 0 ao 4
    print(str[5])  # 0  , 1 digito , pega o 5
    print(str[6:10])  #pegar 4 digitos, pega do 6 ao 9
    print(str[10:])  #pega do 10 ate o final
    print('--------')
    # if(len(str[0:5])== 5 and len(str[5]== 1) and len(str[6:10]==4) and len(str[10:] <= 30)) :
    #     return True
    # else:
    #     return False


for i in range(1,11):
    starttime = time.time()
    #Header parts
    num_seq = str(i).zfill(5)  #Putting zeros to the left
    timestamp = starttime * pow(10, 3)  #Converting to ms
    timestamp_str = str(math.trunc(timestamp % 10000))  #Conferir se ta dando 4 digitos mesmo
    #Header 
    msg_to_server =  num_seq + '0' + timestamp_str + 'Elaine'
    print(msg_to_server)
    # str = msg_to_server.slipt()
    valid_message(msg_to_server)
    # print(str[0])
    # print(str[1])
    # print(str[2])
    # print(str[3])

 
  
    if(len(msg_to_server) > package_size):
        print('Invalid message!')
        exit(1)

    else:
        #Sending message to server
        clientSocket.sendto(msg_to_server .encode(),(serverName, serverPort))
        package_sent += 1
        try:
            msg_from_server, serverAddress = clientSocket.recvfrom(buffer_size)
            #sliptar a mensagem e ver o index
            endtime = time.time()
            package_received += 1

            #Checking if the header received from server is valid
            # if(valid_message(msg_from_server.decode()) == False):
            #     print('Invalid message!')
            # else:
            #     print(msg_from_server.decode())

            #RTT time
            rtt.append(endtime - starttime)

        except timeout:
            package_lost += 1
            print('Unfortunately this package has been lost...')



clientSocket.close()

#Statistics
media = rtt_medio(rtt) #avg
sd = standard_deviation(rtt, media) #mdev
rtt.sort()
rtt_min = rtt[0]
rtt_max= rtt[num_pings - 1]
percent_lost = (package_lost / package_sent ) * 100


print('{} packets transmitted, {} received, {}% packet loss, time' 
.format(package_sent, package_received, percent_lost) )

print('rtt min/avg/max/mdev = {:03f}/{:03f}/{:03f}/{:03f}'
 .format(rtt_min, media, rtt_max, sd))










