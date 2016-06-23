'''
    udp socket client
    Silver Moon
'''

import socket   # for sockets
import signal
import sys      # for exit
import csv      # for reading configuration file


global storage

configFile="storagelist.cfg"

def signal_handler(signal, frame):
    print "You Pressed Ctrl+C!"
    sys.exit(0)
# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

#host = 'rtcsvc18';
#host = 'rtcsvc03n1';
host = 'rtcsvc18n2';
port = 8888;
def checkHostDeamon():
    hostname = meir
def readConfigFile(filename):
    storagecfg = filename
    with open(storagecfg) as csvfile:
        line = csv.reader(csvfile, delimiter=',')
        d = dict(filter(None,csv.reader(csvfile,delimiter=',')))
        for row in line:
            print row

readConfigFile(configFile)
print "csv to dict \n %s" %d
sys.exit(0)

while(1) :
    signal.signal(signal.SIGINT, signal_handler)
    msg = raw_input('Enter message to send : ')

    try :
        #Set the whole string
        s.sendto(msg, (host, port))

        # receive data from client (data, addr)
        d = s.recvfrom(28700)
        reply = d[0]
        addr = d[1]

        print 'Server reply : ' + reply

    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
