#Elaine Dias Pires
from socket import *
import math
import time

start_exec = time.time()

serverName = '168.227.188.22'
serverPort = 30000

buffer_size = 40
package_size = 40

package_lost = 0
package_sent = 0
package_received = 0
percent_lost = 0

num_pings = 10

#Every position of the dictionary bellow will receive two values, one related to ping 
# and another related to pong, if there isn't any loss of packages.
#  The key is the number of the package.
dic_time = {}
#List that will receive rtt's times
rtt = []

#Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM) 
clientSocket.settimeout(1)  #Maximum time of waiting

def rtt_medio(rtt, size):
    rtt_sum = sum(rtt)
    media = rtt_sum / size
    return media

def standard_deviation(rtt, media, size):
    sum = 0
    for i in range(0, size): 
        sum += (rtt[i] - media ) ** 2
    sd = sum/ size
    sd = math.sqrt(sd)
    return sd

def rtt_calc(dic_time, rtt):
    for num_seq in dic_time:
        if(len(dic_time[num_seq])==2): #if there is time of ping and pong
            start = dic_time[num_seq][0]
            end = dic_time[num_seq][1]
            rtt_value = end - start
            rtt.append(rtt_value)


for i in range(1,11):
    starttime = time.time()
    #Header parts
    num_seq = str(i).zfill(5)  #Putting zeros to the left
    timestamp = starttime * pow(10, 3)  #Converting to ms
    timestamp_str = str(math.trunc(timestamp % 10000))  
    #Header 
    msg_to_server =  num_seq + '0' + timestamp_str + 'Elaine'

    dic_time[num_seq] =  [] 
    dic_time[num_seq].append(starttime)
  
    if(len(msg_to_server) > package_size):
        print('Package size error!')
        package_lost += 1
        continue

    else:
        #Sending message to server
        clientSocket.sendto(msg_to_server .encode(),(serverName, serverPort))
        print('Message to server:   ' , msg_to_server)
        package_sent += 1
        try:
            msg_from_server, serverAddress = clientSocket.recvfrom(buffer_size)
            msg_from_server = msg_from_server.decode()
            endtime = time.time()

            #Checking if the header received from server is valid
            index_int = int(msg_from_server[0:5])
            m3= int(len(msg_from_server[6:10]))
            if(index_int > 10):
                print('Sequence number error!')
                package_lost += 1
                continue
            elif(msg_from_server[5] != '1'):
                print('Ping/Pong error!')
                package_lost += 1
                continue
            elif(m3 != 4 ):
                print('Timestamp error!')
                package_lost += 1
                continue
            elif(len(msg_from_server[10:]) > 30):
                print('Message size error!')
                package_lost += 1
                continue
            else:
                package_received += 1
                print('Message from server: ' , msg_from_server)

            #Checking if the pong is comming from the respective ping
            index = msg_from_server[0:5]
            if(index == num_seq):
                dic_time[num_seq].append(endtime)
                if(endtime - starttime > 1):
                    package_lost -= 1
            

        except timeout:
            package_lost += 1
            print('Timeout...')
           
            

clientSocket.close()
end_exec = time.time()
rtt_calc(dic_time, rtt) #It will calculate rtt's times and put in rtt list
size = len(rtt) #Not necessarily will be the number of pings, because some package maybe has been lost.

if(size > 0):
    #Statistics
    media = rtt_medio(rtt, size)  * pow(10, 3) #Converting to ms  
    sd = standard_deviation(rtt, media, size) #mdev
    rtt.sort()

    rtt_min = rtt[0] * pow(10, 3) #Converting to ms
    rtt_max= rtt[size - 1]  * pow(10, 3) #Converting to ms
    percent_lost = (package_lost  / 10 ) * 100
    time_exec = (end_exec - start_exec) * pow(10, 3) #Converting to ms
    time_exec = math.trunc(time_exec)

    print('{} packets transmitted, {} received, {}% packet loss, time {}ms' 
    .format(package_sent, package_received, percent_lost, time_exec) )

    print('rtt min/avg/max/mdev = {:03f}/{:03f}/{:03f}/{:03f}'
    .format(rtt_min, media, rtt_max, sd))
elif(size==0):
    print("All pagkages has been lost, it's not possible to calculate statistics this way.")











