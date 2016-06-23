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

HOST = os.uname()[1]   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port


class CollectCpu(object):
    def __init__(self,debug=True):
        self.topCommand = "top -bn2 > /tmp/top; grep Tasks: /tmp/top |tail -n 1 | xargs -I {} grep -n {} /tmp/top| tail -n 1|  cut -f1 -d: | xargs -I {} sed -n {},+22p /tmp/top| grep Cpu"
        self.debug = debug
        self.server = HOST

    def cpu_top_collect(self):
        lines = []
        process  = sub.Popen(self.topCommand, stdin=sub.PIPE,stdout=sub.PIPE,stderr=sub.PIPE, shell=True)
        if self.debug:
            print "topCommand "+self.topCommand
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
                print "output line [%s]"%line
            print line
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


cpu = CollectCpu()
cpuResults = cpu.cpu_top_collect()
print cpuResults
