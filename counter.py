import sys,time
from datetime import datetime, timedelta


incCounter = 0
countTil = 10


while 1:

    print "starting script"
    next_hour = datetime.now() + timedelta(minute = 60)
    next_hour = int(next_hour.strftime('%M'))
    print "next hour is [ %s ] " %next_hour

    while 1:
        print "dd [ %s ] ss [ %s ]" %(datetime.now(), datetime.now().replace(minute=next_hour, minute=10) )
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
