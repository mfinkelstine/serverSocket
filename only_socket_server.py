'''
    Simple udp socket server
    Silver Moon (m00n.silv3r@gmail.com)

'''

import socket
import sys
import re
import signal
import os
import sys,time
import subprocess as sub

HOST = os.uname()[1]   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

def signal_handler(signal, frame):
    print "You Pressed Ctrl+C!"
    sys.exit(0)
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created %s ' %os.uname()[1]
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit(0)


# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit(0)

while 1:
    signal.signal(signal.SIGINT, signal_handler)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data:
        break
    if re.search(r'counters', data):
        reply = 'counter...: ' + c.mainTitle
    # search if cpu were defined
    elif re.search(r'cpu', data):
        reply = 'cpu total...' + data
    else:
        reply = 'no cpu or counter were defined...' + data
        s.sendto(reply , addr)

    s.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

s.close()
