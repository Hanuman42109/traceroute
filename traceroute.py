from socket import * 
import os 
import sys 
import struct 
import time 
import select 
import binascii   

ICMP_ECHO_REQUEST = 8 
MAX_HOPS = 30 
TIMEOUT  = 2.0  
TRIES    = 2 

def checksum(string):  
    csum = 0
    countTo = (int(len(string)/2))*2
    count = 0

    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += string[len(string)-1]
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer &= 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet(): 
    myChecksum = 0
    ID = os.getpid() & 0xFFFF

    # Make the header (type, code, checksum, id, sequence)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())

    # Compute the checksum
    myChecksum = checksum(header + data)

    # Repack header with checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, htons(myChecksum), ID, 1)

    packet = header + data 
    return packet  

def get_route(hostname): 

    timeLeft = TIMEOUT 

    for ttl in range(1,MAX_HOPS): 
        for tries in range(TRIES): 
            destAddr = gethostbyname(hostname) 

            #Fill in start 
            # Make a raw socket named mySocket 
            mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
            #Fill in end  

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl)) 
            mySocket.settimeout(TIMEOUT) 

            try: 
                d = build_packet() 
                mySocket.sendto(d, (hostname, 0)) 
                t = time.time() 
                startedSelect = time.time() 
                whatReady = select.select([mySocket], [], [], timeLeft) 
                howLongInSelect = (time.time() - startedSelect) 

                if whatReady[0] == []: # Timeout 
                    print("  *        *        *    Request timed out.") 
                    continue

                recvPacket, addr = mySocket.recvfrom(1024) 
                timeReceived = time.time() 
                timeLeft = timeLeft - howLongInSelect 

                if timeLeft <= 0: 
                    print("  *        *        *    Request timed out.") 
                    continue

            except timeout: 
                continue    

            else: 
                #Fill in start         
                # Fetch the ICMP type from the IP packet  
                icmpHeader = recvPacket[20:28]
                types, code, chk, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
                #Fill in end 

                if types == 11: 
                    bytes = struct.calcsize("d")  
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0] 
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - t)*1000, addr[0])) 

                elif types == 3: 
                    bytes = struct.calcsize("d")  
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0] 
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - t)*1000, addr[0])) 

                elif types == 0: 
                    bytes = struct.calcsize("d")  
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0] 
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - timeSent)*1000, addr[0])) 
                    return 

                else: 
                    print("error") 
                    break 

            finally: 
                mySocket.close() 

# Run traceroute for multiple hosts
targets = [
    "google.com",
    "amazon.com",
    "facebook.com",
    "1.1.1.1"   # Cloudflare
]

for host in targets:
    print("\n==============================")
    print("Traceroute to:", host)
    print("==============================\n")
    get_route(host)