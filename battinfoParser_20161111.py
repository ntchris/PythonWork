##
## <Description>
##

from __future__ import print_function
import datetime
import re
import sys
import time
import json
import string
from sets import Set

 
#Oct 28 21:19:14.961    5   500   300 battery low voltage:7.Oct 28 21:34:03.655    5   500   300 
#  alarm: {"recorded_on":1477690339503,"alarms":{"alarm":"interval","travel_mode":"battery_transit","state":0,"stop_time":0,
# "geo_location":{"lat":43.516735,"lon":-80.51476559999999},"altitude":349,"temperature":23.95,"humid":25.9248046875,"pressure":98176,
#"battery_info":{"vendor_id":3,"id_voltage":1.961,"state":[{"time":1477689554,"voltage":7.037500000000001,"temperature":24.18},
# {"time":0,"voltage":0,"temperature":0},{"time":1477689556,"voltage":6.8825,"temperature":24.18}]}}}

# "recorded_on":1477690339503,"alarms":{"alarm":"interval","travel_mode":"battery_transit","state":0,"stop_time":0,"geo_location":{"lat":43.516735,"lon":-80.51476559999999},"altitude":349,"temperature":23.95,"humid":25.9248046875,"pressure":98176,"battery_info":{"vendor_id":3,"id_voltage":1.961,"state":[{"time":1477689554,"voltage":7.037500000000001,"temperature":24.18},{"time":0,"voltage":0,"temperature":0},{"time":1477689556,"voltage":6.8825,"temperature":24.18}]}}}

#### to do, check missing events to report potential changed keyword ####

# json.dumps([1,2,3,{'4': 5, '6': 7}], separators=(',',':')) '[1,2,3,{"4":5,"6":7}]'


#test data batInfoJson=json.loads('{"vendor_id":3,"id_voltage":1.961,"state":[{"time":1477689554,"voltage":7.037500000000001,"temperature":24.18}, {"time":0,"voltage":0,"temperature":0},{"time":1477689556,"voltage":6.8825,"temperature":24.18}]}')
   
   
   
class BattInfoParserClass:

   # put important event keywords here.  only include event contents, do not add prefix space or code like 300 500 ...
   vendor_id = "vendor_id"
   id_voltage="id_voltage"
   state="state"
   time="time"
   voltage="voltage"
   temperature="temperature"    
   excel_Seperator=";"
   # there are 3 set of voltage data in the battery info state
   batteryStateCount=3
   
   # input one line of Json data, not junk chars.
   @staticmethod
   def parseOneBattInfo(jsonDataString):
      #           '["foo         ", {"bar":["baz", null, 1.0, 2]}]'
      #batInfoJson=json.loads('{"vendor_id":3,"id_voltage":1.961,"state":[{"time":1477689554,"voltage":7.037500000000001,"temperature":24.18}, {"time":0,"voltage":0,"temperature":0},{"time":1477689556,"voltage":6.8825,"temperature":24.18}]}')
   
      alarmJson = json.loads(jsonDataString)
      batteryInfoData=alarmJson["alarms"]["battery_info"]

      return batteryInfoData 
  
   @staticmethod
   def preparLine(logline):
      alarmKeyword="alarm: {"
   
      #battery_info":

      #if( alarmKeyword in logline ):
      # search from the end, because sometimes the first report is corrupted, so we have to use the 2nd one
      alarmIndex=string.rfind(logline, alarmKeyword)
      # get everthing else after the alarm: {   keyword
      if(alarmIndex<0) :
         return ""
      subStringIndex=alarmIndex+len(alarmKeyword)-1
      alarmJsonString= logline[subStringIndex:]

      return alarmJsonString
   
   @staticmethod
   def writeCSVFileHeader(outputCSVfile):
   
      volState=BattInfoParserClass.excel_Seperator+BattInfoParserClass.time+BattInfoParserClass.excel_Seperator+BattInfoParserClass.voltage+BattInfoParserClass.excel_Seperator+BattInfoParserClass.temperature

      # write the excel file headers 
      outputCSVfile.write(BattInfoParserClass.vendor_id+BattInfoParserClass.excel_Seperator+BattInfoParserClass.id_voltage+volState+volState+volState+"\n" )
      #test data batInfoJson=json.loads('{"vendor_id":3,"id_voltage":1.961,"state":[{"time":1477689554,"voltage":7.037500000000001,"temperature":24.18}, {"time":0,"voltage":0,"temperature":0},{"time":1477689556,"voltage":6.8825,"temperature":24.18}]}')

   
   @staticmethod
   def writeBatteryInfoToCSV(outputCSVfile, batteryData):

      #state="state"
      #time="time"
      #voltage="voltage"
      #temperature="temperature"    
   
      stateString=""
      #we have 3 members in the state
      for voltageStateData in batteryData[BattInfoParserClass.state]:     
         stateString=stateString+ str(voltageStateData[BattInfoParserClass.time])+BattInfoParserClass.excel_Seperator+ str(voltageStateData[BattInfoParserClass.voltage])+BattInfoParserClass.excel_Seperator+ str(voltageStateData[BattInfoParserClass.temperature])+BattInfoParserClass.excel_Seperator
      
      csvdata = str(batteryData[BattInfoParserClass.vendor_id])+ BattInfoParserClass.excel_Seperator+ str(batteryData[BattInfoParserClass.id_voltage])+ BattInfoParserClass.excel_Seperator + stateString
      
      outputCSVfile.write(csvdata+"\n")      

      return  
    
  
#test data batInfoJson=json.loads('{"vendor_id":3,"id_voltage":1.961,"state":[{"time":1477689554,"voltage":7.037500000000001,"temperature":24.18}, {"time":0,"voltage":0,"temperature":0},{"time":1477689556,"voltage":6.8825,"temperature":24.18}]}')

def printLine():
   print ("====================================================================\n")

 

def main():

   errorLineList = list()
   parsedCount=0
   
   if len(sys.argv) < 2:
      print("Usage: python " + sys.argv[0] + " <battery info log file>")
      sys.exit(0)

   origBattInfoLogFile = sys.argv[1]   

   output_battInfoCSV_filename = origBattInfoLogFile+"_parsed.csv"

   origlogfile = open(origBattInfoLogFile, "r")
   outputBattCSVfile = open(output_battInfoCSV_filename, "w")
   BattInfoParserClass.writeCSVFileHeader(outputBattCSVfile)

   i=0
   for origline in origlogfile:
     i=i+1   
     origline=origline.strip()
     if(len(origline)==0):
        continue
     try:
        #we only process the 2nd alarm data even there are two of them, so the first one is skipped(if there are two in one line)
        preparedLine= BattInfoParserClass.preparLine(origline)
        if(len(preparedLine)==0):
           continue
        batteryData=BattInfoParserClass.parseOneBattInfo(preparedLine)        
        BattInfoParserClass.writeBatteryInfoToCSV(outputBattCSVfile, batteryData)
        parsedCount=parsedCount+1
        
     except ValueError:
       print("corrupted data line can not prase json data in line:#" + str(i))
       errorLine.append("original line number : "+str(i) + "  " +origline)
     
     try:     
        # test corrupted line.  Do we have two more alarm: { in one line ?  if yes, report this corrupted line so someone may manually process
        dontcare,alarmpart=origline.split("alarm: {")
     except ValueError:
        print("Error two alarm data in one line! #" + str(i))
        errorLineList.append("original line number : "+str(i) + "  " +origline)
       
   outputBattCSVfile.close()
   origlogfile.close()
   printLine()
   
   print("BatteryInfo parsed: "+str(parsedCount ))
   
   print("\n\n Battery Info log parsed, new CSV file generated: " + output_battInfoCSV_filename+"\n")
   print("If using Office365, new an empty doc, choose Data->From Text -> choose semicolon as seperator")
   
   print ("corrupted lines :" + str(len(errorLineList)))
   print ("You can manually analyze those lines")

   printLine()

main()

