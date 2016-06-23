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
from datetime import datetime, timedelta
import subprocess as sub
import pprint
pp = pprint.PrettyPrinter(depth=6)

HOST = os.uname()[1]   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

global raceMQ
debug = True
class Counters(object):

    def __init__(self,race,server,debug=False):
        print "Counter init"
        self.race       = race
        #self.raceStatus = status
        self.server     = server
        self.debug      = debug

    def getRaceType(self):
        self.race = "none"

    def maintitle(self):
        return self.mainTitle+' Main Title'

    def CollectNode(self):
        for race in self.race:
            print "race [ %s ]" %race
            if self.race[race]["raceStatus"]:
                print "Collecting counters from [ %s ] status [ %s ] " %(race,self.race[race]['raceStatus'])
                results = self._node_get_counters(race)
                print results

    #def _node_get_counters(self,race):
    def CollectNodeCounters(self,race):

        if str(race) == "racemqAd":
            race = "racemqA"
        elif str(race) == "racemqBd":
            race = "racemqB"
        dumpCounters="echo ctr_dump /tmp/ctrl > /data/%scli; sleep 1; grep \"^RACE: \" /tmp/ctrl| awk '{print $4\" \"$5}'| sort -g | tail -n 2| sed -n 1p |xargs -I {} grep -n {} /tmp/ctrl| cut -f1 -d: | xargs -I {} sed -n {},+75p /tmp/ctrl "% race
        if self.debug:
            print "DEBUG [%s] Counters command %s"%( self.server,dumpCounters )

        output=runCommand(dumpCounters)

        output=output.strip().split("\n")
        lines = []
        now = int( time.time() )
        rx = re.compile('[\[\]{},):]+')
        rx_clean = re.compile('[(%]+')
        rx_drop = re.compile('[=]')
        rx_special = re.compile('>=')
        prefix = ""
        for line in output:
            if self.debug:
                print "DEBUG [ %s ] " %line

            if line and line[0] != "R":
                res = rx.sub(' ', line).strip()
                data=res.split()
                if len(data) > 1:
                    if data[0] == "PipesIn":
                        break
                    if data[0] == "AlgInternals":
                        continue
                    l = -1
                    for i in data:
                        header = data[0].split("=")
                        if len(header) == 1 and not data[0].isdigit():
                            prefix = data[0]
                        if i[0] == "(":
                            name = data[l].split("=")
                            i=rx_clean.sub('', i)
                            lines.append("%s %d" % (self.server+"."+race+"."+prefix+"."+name[0]+name[0]+" "+i,now))
                        else:
                            i=rx_special.sub('>', i)
                            i=rx_clean.sub('', i)
                            i=rx_drop.sub(' ', i)
                            if len(i.split(" ")) > 1:
                                lines.append("%s %d" % (self.server+"."+race+"."+prefix+"."+i,now))
                        l +=1
                else:
                    prefix = data[0]

        message = '\n'.join(lines) + '\n' #all lines must end in a newline
        return message

    def returnCounter(self):
        return self.sideTitle

class CollectCpu(object):
    def __init__(self,debug=True):
        self.topCommand = "top -bn2 > /tmp/top; grep Tasks: /tmp/top |tail -n 1 | xargs -I {} grep -n {} /tmp/top| tail -n 1|  cut -f1 -d: | xargs -I {} sed -n {},+22p /tmp/top| grep Cpu "
        self.debug = debug
        self.server = HOST
    def cpu_top_collect(self):

        lines = []
        process  = sub.Popen(self.topCommand, stdin=sub.PIPE,stdout=sub.PIPE,stderr=sub.PIPE, shell=True)
        if self.debug:
            print "DEBUG command [ %s ] " %self.topCommand
        os.waitpid(process.pid, 0)
        output = process.stdout.read().strip().split("\n")
        now = int( time.time() )
        rx = re.compile('[\[\]{},):%]+')
        rx_drop = re.compile('k ')
        prefix = ""
        counter = 0
        name = ""
        for line in output:
            if self.debug:
                print "DEBUG line [ %s ]" %line
            flag = 0
            if line:
                line = rx_drop.sub(' ', line)
                res = rx.sub(' ', line).strip()
                data=res.split()
                if len(data) > 1:
                    if data[0] == "PipesIn":
                        break
                    if data[0] == "AlgInternals":
                        continue
                    header = data[0]
                    for i in data:
                        try:
                            i = float(i)
                            counter = i
                            flag = 1
                            continue
                        except:
                            name = i
                        if flag == 1:
                            lines.append("%s %d %d" % (self.server+"."+header+"."+name,counter,now))
        message = '\n'.join(lines) + '\n' #all lines must end in a newline
        return message

class CollectThrouput(object):
    def __init__(self):
        self.throuput = throuput


class CollectIOps(object):
    def __init__(self,IOPS):
        self.IOPS = IOPS



def signal_handler(signal, frame):
    print "You Pressed Ctrl+C!"
    sys.exit(0)

def readSVCxmlFile():
    svcConfigFile = "/data/svc_config.xml"
    print "Checking xml file [ %s ]" % svcConfigFile
    if not os.path.isfile(svcConfigFile):
        print "File [ %s ] does not exits " %svcConfigFile
        sys.exit(0)

    from xml.dom import minidom
    xml = minidom.parse(svcConfigFile)

    elmentName = xml.getElementsByTagName("service")
    #print "element %s " %elName.firstChild.data
    for name in elmentName:
        processName = name.getElementsByTagName("process_name")[0].firstChild.data
        if re.match("racemq|rtc_racemqd", processName ):
            print "Process Name is : [ %s ] " %processName
            raceName[processName] = processName

    #for k,v in raceName.iteritems():
    #    print "Finihsed k [ %s ] v [ %s ]" %(k,v)
    print "Finihsed processing xml file"


def runCommand(exe,shell=True):

    proc     = sub.Popen(exe, shell=True,stdout=sub.PIPE)
    dataout = proc.communicate()[0]
    return dataout

def raceMQActive():
    for r in raceName:
        processID = 'ps -efL | grep -i '+r+'| grep -v grep | awk "'"{print \$2}"'" | uniq'
        processCount = 'ps -efL | grep -c -i '+r+' | grep -v grep'
        procid=runCommand(processID)
        rep = procid.replace("\n",",").rstrip(',')
        if not r in raceMQ:
            raceMQ[r] = {}
            raceMQ[r].update({'race' : r })

        raceMQ[r].update(   { 'raceProcessID' : rep})
        raceMQ[r].update({'raceProcessCount' : runCommand(processCount).rstrip('\n')})
        raceMQ[r].update({ 'racePIPEcount'    : 'None' })
        for pid in raceMQ[r]['raceProcessID'].split(','):
            #print "pid is [ %s ]"%pid
            processPipeCount = 'ls -l /proc/'+pid+'/fd | grep -c pipe'
            if pid == "":
                print "no process id were found"
            else:
                if raceMQ[r]['racePIPEcount'] == "None":
                    raceMQ[r].update({ 'racePIPEcount'    : runCommand(processPipeCount).rstrip('\n') })
                else:
                    raceMQ[r].update({ 'racePIPEcount'    : ( raceMQ[r]['racePIPEcount'] + runCommand(processPipeCount).rstrip('\n')) })
        if debug:
            print "len [ %s ] pcount [ %s ] " %(raceMQ[r]['racePIPEcount'], raceMQ[r]['raceProcessCount'])
        if ( int(raceMQ[r]['racePIPEcount']) > 2 ) and ( int(raceMQ[r]['raceProcessCount']) > 4 ) :
            raceMQ[r].update({'raceStatus' : True })
        else:
            raceMQ[r].update({'raceStatus' : False })
    if debug:
        pp.pprint(raceMQ)
        for k in raceMQ:
            print "race name = [ %s ] v "%raceMQ[k]['raceProcessID']

def epocTimeConvert(time):
    system_epoc_time =  datetime.now().strftime('%s')
    conveted_epoc_min = time * 60
    total_epoc_time = int(system_epoc_time) + int(conveted_epoc_min)
    return  datetime.fromtimestamp(int(total_epoc_time)).strftime('%Y-%m-%d %H:%M:%S')

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created %s ' %os.uname()[1]
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    if msg[0] == '-3':
        try:
            s.bind((IP, PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()



timeCountInMinuts = 0.5
nextTime = epocTimeConvert(timeCountInMinuts)

#now keep talking with the client
raceName = {}
raceMQ = {}
readSVCxmlFile()
raceMQActive()
intPeriedTime = 36
intPeriedTimeCount = 0


print 'Socket bind complete to [ %s ]'%os.uname()[1]

while 1:
    signal.signal(signal.SIGINT, signal_handler)
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data:
        break
    #searchObj = re.search(
    if re.search(r'counters', data):
        print "GET COUNTERS "
        count = Counters(raceMQ,HOST)
        for race in raceMQ:
            if raceMQ[race]["raceStatus"]:
                msg = count.CollectNodeCounters(race)
                size_of_package = sys.getsizeof(msg)
                #print "msg size [ %s ] "%size_of_package
                print "%s results %s [ %s ] %s \n%s"%(10*"=",race,size_of_package,20*"=",msg)
                if race == "racemqAd":
                    racemqA = msg
                if race == "racemqBd":
                    print "string not empty"
                    msg += str(racemqA)

        print "%s results %s \n %s"%(10*"=",20*"=",msg)
        s.sendto(msg, addr)
    # search if cpu were defined
    elif re.search(r'cpu', data):
        cpu = CollectCpu()
        cpuResults = cpu.cpu_top_collect()
        s.sendto(cpuResults , addr)
        #reply = 'cpu total...' + data
    else:
        reply = 'no cpu or counter were defined...' + data
        s.sendto(reply , addr)

    #s.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

s.close()
