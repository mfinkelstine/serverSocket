
import pprint

pp = pprint.PrettyPrinter(indent=4)
race = [ 'racemqAd', 'racemqBd' ]

raceMQ = {}
data = '939393,3333,'


for r in race:
    if not r in raceMQ:
        raceMQ[r] = {}

    raceMQ[r].update({ 'name' : r })
    raceMQ[r].update({ 'data' : data })
    print "RaceNAME : [ %s ] raceDATA [ %s ] " %(raceMQ[r]['name'] , raceMQ[r]['data'])

pprint.pprint(raceMQ)
