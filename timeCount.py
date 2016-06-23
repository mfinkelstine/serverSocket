import sys,time
from datetime import datetime, timedelta


timeCountInMinuts = 0.5


next_hour = datetime.now() + timedelta(hours = 1)
print next_hour
def epocTimeConvert(time):
    system_epoc_time =  datetime.now().strftime('%s')
    conveted_epoc_min = time * 60
    total_epoc_time = int(system_epoc_time) + int(conveted_epoc_min)
    return  datetime.fromtimestamp(int(total_epoc_time)).strftime('%Y-%m-%d %H:%M:%S')

nextTime = epocTimeConvert(timeCountInMinuts)
print "system time [ %s ] next time [ %s ] " %( datetime.now(),nextTime)
while 1:

    print "system time [ %s ] next time [ %s ] " %( datetime.now(),nextTime)
    if str(datetime.now()) > nextTime:
        print "yes"
        break

sys.exit(0)

#next_minute = int(next_minute.strftime('%M'))
#next_hour = int(next_hour.strftime('%H'))

#next_minute = datetime.now() + timedelta(minutes = timeCountInMinuts)
#next_minute = int(next_minute.strftime('%M'))
#next_hour = datetime.now() + timedelta(minute = 60)
#next_hour = int(next_hour.strftime('%H'))
#print "timenow [ %s ] nexttime [ %s ] next hour [ %s ] next minutes [ %s ] " %(datetime.now(),datetime.now().replace(minute=next_minute), next_hour , next_minute)

#sys.exit(0)

#nexttime=datetime.now().replace(minute=next_minute)

while 1:
    print "deltatime [ %s ] netxtime [ %s ]" %(datetime.now(), nextTime)

    if datetime.now() >= nextTime:
        print "time is to restart service "
        #next_minute = datetime.now() + timedelta(minutes = timeCountInMinuts)
        #next_minute = int(next_minute.strftime('%M'))
        #nexttime=datetime.now().replace(minute=next_minute)
        break
    time.sleep(1)


sys.exit(0)
while 1:

    print "starting script"
    next_hour = datetime.now() + timedelta(minute = 60)
    next_hour = int(next_hour.strftime('%M'))
    print "next hour is [ %s ] " %next_hour

    while 1:
        print "dd [ %s ] ss [ %s ]" %(datetime.now(), datetime.now().replace(hour=next_hour, minute=10) )
        if datetime.now() > datetime.now().replace(hour=next_hour, minute=1):
            break


#while 1:
#    if ( int(incCounter) > int(countTil) ):
#        print "[%s] [%s]"%(int(incCounter) ,int(countTil))
#        print "need to restart service"
#        incCounter = 0
#    else:
#        print "[%s] [%s]"%(int(incCounter) ,int(countTil))
#        incCounter += 1
#    time.sleep(1)
