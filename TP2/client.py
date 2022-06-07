from socket import *
import math
import time

start_exec = time.time()

serverName = 'localhost'
serverPort = 30000

buffer_size = 40
package_size = 40

package_lost = 0
package_sent = 0
package_received = 0
percent_lost = 0

rtt = []
# rtt2 = []
num_pings = 10
dic_time = {}

#Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM) 
clientSocket.settimeout(2)  #Maximum time of waiting

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

#calculo do rtt a partir do dicionario
def rtt2(dic_time):
    rtt2 = []
    for num_seq in dic_time:
        start = dic_time[num_seq][0]
        print(start)
        end = dic_time[num_seq][1]
        print(end)
        rtt2_value = end- start
        rtt2.append(rtt2_value)
    print(rtt2)

for i in range(1,11):
    starttime = time.time()
    #Header parts
    num_seq = str(i).zfill(5)  #Putting zeros to the left
    timestamp = starttime * pow(10, 3)  #Converting to ms
    timestamp_str = str(math.trunc(timestamp % 10000))  #Conferir se ta dando 4 digitos mesmo
    #Header 
    msg_to_server =  num_seq + '0' + timestamp_str + 'Elaine'

   
    dic_time[num_seq] =  [] #Every position of the dictionary will recevif two value, one of ping and another of pong
    dic_time[num_seq].append(starttime)
  
    if(len(msg_to_server) > package_size):
        print('Invalid message!')
        continue

    else:
        #Sending message to server
        clientSocket.sendto(msg_to_server .encode(),(serverName, serverPort))
        package_sent += 1
        try:
            msg_from_server, serverAddress = clientSocket.recvfrom(buffer_size)
            msg_from_server = msg_from_server.decode()
            endtime = time.time()
            package_received += 1

            #Checking if the header received from server is valid
            if(msg_from_server[5] == 0): #It's not in the protocol format
                print('Invalid message!')
            else:
                print('Message from server: ' , msg_from_server)

            #Checking if the pong is comming from the respective ping
            index = msg_from_server[0:5]
            if(index == num_seq):
                dic_time[num_seq].append(endtime)

              

            #RTT time
            rtt.append(endtime - starttime)

        except timeout:
            package_lost += 1
            print('Unfortunately this package has been lost...')
            rtt.append(0)
            



clientSocket.close()
end_exec = time.time()

#Statistics
media = rtt_medio(rtt)  * pow(10, 3) #Converting to ms  
sd = standard_deviation(rtt, media) #mdev
rtt.sort()
rtt_min = rtt[0] * pow(10, 3) #Converting to ms
rtt_max= rtt[num_pings - 1]  * pow(10, 3) #Converting to ms
percent_lost = (package_lost / package_sent ) * 100
time_exec = (end_exec - start_exec) * pow(10, 3) #Converting to ms
time_exec = math.trunc(time_exec)


print('{} packets transmitted, {} received, {}% packet loss, time {}ms' 
.format(package_sent, package_received, percent_lost, time_exec) )

print('rtt min/avg/max/mdev = {:03f}/{:03f}/{:03f}/{:03f}'
 .format(rtt_min, media, rtt_max, sd))


print(dic_time) #ok
print('--------')
rtt2(dic_time)









