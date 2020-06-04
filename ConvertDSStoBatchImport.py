from hec.script import *
from hec.heclib.dss import *
from hec.io import TimeSeriesContainer
from hec.heclib.util import HecTime
import java
import csv
import array 

#This script was developed 8/2019 by Brennan B Beam at USACE HEC. It's intended purpose was unloading a large dss file into a formatted csv file acceptble to the nature conservancy software IHA
#It iterates through every path in a dss file and writes all the location, date, and flow data to a csv file in three columns. 

##############    DEFINING SOURCE DATA , OUTPUT LOCATION, HEADERS ################
fileName = r"D:\Brennan\Johns_IHA_Dam_Analysis\IHA\For Grace\Inflows and Outflows for Grace - 2018-07-02.dss"
#open the dss file
dssFile = HecDss.open(fileName)
# Create List of pathnames in dss file 
pathnames = dssFile.getPathnameList()
outFile = open(r'D:\Brennan\Johns_IHA_Dam_Analysis\BatchImportUSACEDams.csv', 'wb')
#creating headers
header1 = ['batch']
header2 = ['Dam_Name','Date','Flow']
#writing headers
writer = csv.writer(outFile)
writer.writerow(header1)
writer.writerow(header2)
#Initializing HecTime Object
myTime = HecTime()

################      DEFINING OFFSET FOR OUTFLOWS     #################
listStartTimes = []
listEndTimes = []
#build list of start times
for eachPath in pathnames:
	firstTSC = dssFile.get(eachPath)
	firstTime = firstTSC.startTime
	myTime.set(firstTime)
	foo = myTime.date(firstTime)
	listStartTimes.append(foo)
#build list of end times
for eachPath in pathnames:
	firstTSC = dssFile.get(eachPath)
	finalTime = firstTSC.endTime
	myTime.set(finalTime)
	foo = myTime.date(finalTime)
	listEndTimes.append(foo)

#print the largest and smallest start times
print "earliest and latest start times"
print listStartTimes[0]
finalValue =( len(listStartTimes)-1)
print listStartTimes[finalValue]

#print the largest and smallest start times
print "earliest and latest end times"
print listEndTimes[0]
finalValue = (len(listEndTimes)-1)
print listEndTimes[finalValue]

for eachPathname in pathnames:
#############   TEEING UP  LIST CREATION ###################################
	myTSC = dssFile.get(eachPathname)
##############   CREATING VALUES LIST ####################################
	valuesList = myTSC.values
##############   CREATING TIMES LIST    ####################################
	timeList = myTSC.times
	dateList = []
	for each in timeList:
		myTime.set(each)
		day = myTime.date(each) 
		dateList.append(day)
##############   CREATING NAME LIST  ###################################
#Getting Dam Name 
	damName = myTSC.location
#Initializing blank list
	damNameList = []
#Filling list with correct number of names
	for eachEntry in timeList:
		damNameList.append(damName)
##################     COMBINING LISTS    #################################
	rows = zip(damNameList, dateList, valuesList)
#################         WRITING        ####################################
	for eachRow in rows:
		writer.writerow(eachRow)
outFile.close()