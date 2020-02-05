
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:14:00 2019

@author: Chris Moen
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 16:37:39 2019

@author: Chris Moen
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:15:49 2019

@author: Chris Moen
"""
import datetime
import time
import json

from colorama import init, Fore, Back, Style
from termcolor import colored
from requests_pkcs12 import get
import requests
import os 
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import re #Regex expression 
global c
global db

import re 
# setup.py
from distutils.core import setup
counter = 0

path = "D:\\scripts\\output\\hourly_C"

class SanityData:
    def __init__(self):
        self.valMissingIDs_program = 0
        self.valIndRecs_program = 0
        self.valImages_program = 0
        self.valDVRIds_program = 0
        self.accountConfigurationVal_program = 0
        self.progDetails = 0
        self.outOfSync = 0
        self.fake_generic = 0
        self.originalAirDate = []
        self.errorCodes = []
        self.enableConfiguration = 0
        self.devices = 0
        self.skipTokenError = 0
        self.DVREmptyData = 0
        self.dvrStationOutOfSync = 0
        self.dvr_s96 = 0
        self.dvr_s108 = 0
        self.dvr_s116 = 0
        self.oss = 0
    def getOriginalAirDate(self):
        return self.originalAirDate
    def getEnableConfiguration(self):
        return self.enableConfiguration
    def getMissingIDS(self):
        return self.valMissingIDs_program
    def getValIndRecs(self):
        return self.valIndRecs_program
    def valImages(self):
        return self.valImages_program
    def valDVRIds(self):
        return self.valDVRIds_program
    def getAccountConfigurationVal(self):
        return self.accountConfigurationVal_program
    def getProgDetails(self):
        return self.progDetails
    def getDVROutOfSync(self):
        return self.outOfSync
    def getFake_generic(self):
        return self.fake_generic
    def getDevices(self):
        return self.devices
    def getDVREmptyData(self):
        return self.DVREmptyData
    def getSkipTokenError(self):
        return self.skipTokenError
    def setSkipTokenError(self,skipToken):
        self.skipTokenError += skipToken
    def setDevices(self,devices):
        self.devices += devices
    def errorResponseCode(self,code):
        self.errorCodes.append(code)
    def getErrorResponseCode(self,code):
        return self.errorCodes
    def setEnableConfiguration(self,enableConfiguration):
        if enableConfiguration != None:
            self.enableConfiguration += enableConfiguration
    def setOriginalAirDate(self,originalAirDate):
        if originalAirDate != None:
            self.originalAirDate.append(originalAirDate)
    def setValMissingIDS(self, valMissingIDs):
        if valMissingIDs != None:
            self.valMissingIDs_program += valMissingIDs
    def setValIndRecs(self,valIndRecs):
        if valIndRecs != None:
            self.valIndRecs_program += valIndRecs
    def setValImages(self,valImages):
        if valImages != None:
            self.valImages_program += valImages
    def setValDVRIds(self,valDVRIds):
        if valDVRIds != None:
            self.valDVRIds_program += valDVRIds
    def setAccountConfigurationVal(self, accountConfigurationVal):
        if accountConfigurationVal != None:
            self.accountConfigurationVal_program += accountConfigurationVal
    def setProgDetails(self,progDetails):
        if progDetails != None:
            self.progDetails += progDetails
    def setDVROutOfSync(self,outOfSync):
        if outOfSync != None:
            self.outOfSync += outOfSync
    def setfake_generic(self,fake_generic):
        if fake_generic != None:
            self.fake_generic += fake_generic
    def setDVREmptyData(self,dvrData):
        if dvrData != None:
            self.DVREmptyData += dvrData
    def setAPIResponse(self,dvr_s96,dvr_s108,dvr_s116,oss):
        self.dvr_s96 += dvr_s96
        self.dvr_s108 += dvr_s108
        self.dvr_s116 += dvr_s116
        self.oss += oss

    def setdvrStationOutOfSync(self,dvrStationOutOfSync):
        self.dvrStationOutOfSync += dvrStationOutOfSync
    def getdvrStationOutOfSync(self):
        return self.dvrStationOutOfSync

    def getDVR_S96(self):
        return self.dvr_s96
    def getDVR_S108(self):
        return self.dvr_s108
    def getDVR_s116(self):
        return self.dvr_s116
    def getOSS(self):
        return self.oss
def get_token(type_cert,_env,_proxyurl):
    #This is courtesy of James Owen c. April 2019 
    # open token file and check expiry
    basePath = 'C:/Tools/scripts/'
    token_filename = "" 
    token_uri = "" 
    cert = "" 
    cert_pass = ""
    
    if _env =='proda':
        instance = 'proda.bce'
        
        if type_cert == 'OSS': 
            cert = basePath + 'credentials/ossbssTools-proda-sts.pfx'
        elif type_cert == 'DVRPROXY': 
            cert = basePath + 'credentials/ndvrTools-proda-sts.pfx'
        cert_pass = 'Medi@F1rst'
        token_uri = 'https://appgw-operatorstsssl.'+instance+'.tv3cloud.com/certactive'
        token_filename = './'+instance+'_token.json'


    elif _env == 'prodc':
        instance = 'prodc.bce'
        cert = basePath + 'credentials/ucpusher-ssl.pfx'
        cert_pass = ''
        token_uri = 'https://appgw-operatorstsssl.'+instance+'.tv3cloud.com/certactive'
        token_filename = './'+instance+'_token.json'
    elif _env == 'prodb':
        instance = 'prodb.bce'
        
        if type_cert == 'OSS': 
            cert = basePath + 'credentials/ossbssTools-prodb-sts.pfx'
        elif type_cert == 'DVRPROXY': 
            cert = basePath + 'credentials/ndvrTools-prodb-sts.pfx'
            
        cert_pass = 'Medi@F1rst'
        token_uri = 'https://appgw-operatorstsssl.'+instance+'.tv3cloud.com/certactive'
        token_filename = './'+instance+'_token.json'
        
    token_valid = 0
    try:
        with open(token_filename, 'r') as token_file_in:
            try:
                token = json.load(token_file_in)
                if ((datetime.datetime.timestamp(dateutil.parser.parse(token['RefreshTime'])) - time.time()) > 0 ):
                    token_valid = 1
                    # print(bcolors.OKGREEN + 'token loaded ok. proceeding...\n' + bcolors.ENDC)
                else:
                    print('token expired. getting new token...\n')
            except:
                pass
    except OSError:
        print('no token file. getting new token...\n')

    if (token_valid):
        pass
    else:
        response = get(token_uri, headers={'Content-Type': 'application/json'}, verify=True, pkcs12_filename=cert, pkcs12_password=cert_pass, proxies=_proxyurl)
        if (response.status_code == 200 ):
            token = response.json() # load token from repsonse.get()
            with open(token_filename, 'w', encoding="utf-8", newline='\n') as token_file:
                try:
                    json.dump(response.json(),token_file, indent=4, sort_keys=True, ensure_ascii=False)
                    token_file.write('\n')
                    token_file.close()
                    # print (bcolors.OKGREEN + 'token saved ok. proceeding...\n' + bcolors.ENDC)
                except OSError:
                    print(bcolors.WARNING + 'can\'t create files.  bailing...' + bcolors.ENDC + '\n')
                    sys.exit('barf!')
        else:
            print ('token request response: ', response.json()['ErrorDescription'],'\n')
            sys.exit ('invalid cert or wrong password\n')

    try:
        auth_header = { 'Authorization': 'OAUTH2 access_token="'+(token['AccessToken'])+'"', 'Content-Type': 'application/json' }
        return auth_header
    except:
        return None

def splitNumbers(eachList): 
    #Then we know that there is a match for this particular file type 
    pathList = eachList.split('_') 
    recordedL = pathList[2] 
    scheduledL = pathList[3] 
    pastScheduledL = pathList[4] 
    recordingL = pathList[5] 
            
    recordedCount = recordedL.split('-')[1] #Total amount of recordings on the STB 
    scheduledCount = scheduledL.split('-')[1] #...
    pastScheduledCount = pastScheduledL.split('-')[1]  #... 
    pastRecordingCount = recordingL.split('-')[1] 
    return (recordedCount, scheduledCount, pastScheduledCount,pastRecordingCount)

def getPastNumbers(path,account,currentPathName): 
    #Use this path to gather all of the file output     
    dir_list = os.listdir(path)
    
    totalPast = [] 
    for eachList in dir_list: 
        reg = re.match(account, eachList)
        if reg != None: 
            
            pastNums = splitNumbers(eachList) 
            totalPast.append(pastNums) 
            
    totalPast.append(splitNumbers(currentPathName)) 
    return totalPast #Return the total past 
    
def appendPastDefs_total(total, pastDefs): 
    
    pastDefs_trans = list(map(list, zip(*pastDefs))) #Here we are just transposing the original matrix 

    i = 0 
    
    current = "" 
    for row in pastDefs_trans: 
        #We will append this to the output 
        if i == 0: 
            current += "| Recorded Count Over Time |"
        elif i == 1: 
            current += "| Scheduled Count Over Time |" 
        elif i == 2: 
            current += "| Past Scheduled Count Over Time |" 
        elif i == 3: 
            current += "| Recording Count Over Time |" 
    
        for ind in row: 
            current += ind + ', ' 
            
        current += '\n'
        i += 1
    return current 
def TimestampAnalyser(timestamps):
    
    results = []
    
    referenceDatetime = datetime.datetime.strptime('1900-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
    
    # Looping through timestamps
    for dateString in timestamps:
        dateString = dateString.replace("T", " ")
        try:
            # Turning timestamp string into a datetime object
            datetimeObject = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
            if datetimeObject > referenceDatetime:
                results.append(1)
                print(datetimeObject)
            else:
                results.append(0)
        except:
            results.append(0)
        
    return results


def DonutChartOfResults(results):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    numberOfValidDates = 0
    numberOfInvalidDates = 0
    for result in results:
        if result == 1:
            numberOfValidDates += 1
        else:
            numberOfInvalidDates += 1

    percentageOfValidDates = (numberOfValidDates / (numberOfValidDates + numberOfInvalidDates)) * 100
    percentageOfValidDatesString = "{:.2f}".format(percentageOfValidDates)
    
    percentageOfInvalidDates = (numberOfInvalidDates / (numberOfValidDates + numberOfInvalidDates)) * 100
    percentageOfInvalidDatesString = "{:.2f}".format(percentageOfInvalidDates)
    
    annotations = ["Valid Dates (" + percentageOfValidDatesString + "%)", "Invalid Dates (" + percentageOfInvalidDatesString + "%)"]
    
    data = [numberOfValidDates, numberOfInvalidDates]
    
    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
    
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(annotations[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)
    
    #ax.set_title("Valid and Invalid Dates")
    
    plt.show()
    #plt.savefig("TimestampAnalyser.png")
 
def output_file(account,individualRecs, recSummary,showName,recCount, schedCount, recordingCount, pastScheduled): 

    t = path + "\\" + showName + ".txt"
    pastDefinitions = getPastNumbers('C:\\Report_ORT\\',account,showName) 
    
    file1 = open(t,"a") 
    
    total = "" 
    total += '-------------------------------------------Account Recording Breakdown Over Time-------------------------------------------\n'
    
    total += appendPastDefs_total(total,pastDefinitions)  
   
    for eachRecs in individualRecs: 
        row = "" 
        for key,value in eachRecs.items():
         
            row += '|' + key + ':' + str(value) + '|'
        total += '\n' + row
        
    total += '\n'
    total += '\n' 
    total += '\n'
    total += '\n'
    
    total += '-------------------------------------------Show Summary -------------------------------------------'
    total += '\n'
    
    for eachT in recSummary: 
        row = "" 
        total += '|Show: ' + eachT[0] + '|Recorded Count: ' + eachT[1] + '|Scheduled Count: ' + eachT[2]  + '|Recording Count: ' + eachT[3] + '|Past Scheduled: ' + eachT[4] + '|Series Obj State: ' + eachT[5] + '|Channel Number: ' + eachT[6]       
        total += '\n'
    
    file1.write(total)
    file1.close()

def timeDelta(time1,time2): #time stamp 
   
    time1_st = datetime.datetime.strptime(time1,"%Y-%m-%dT%H:%M:%SZ")
    time2_st = datetime.datetime.strptime(time2,"%Y-%m-%dT%H:%M:%SZ")
    
    delta = time2_st - time1_st  
    delta_seconds = delta.total_seconds()
    #If the delta time is negative, then we know that it was scheduled in the past 
    return delta_seconds/(24*60*60) 
    

def organizeOutputFile(file): 
    
    #Organize the output file name 
    dir_list = os.listdir(file) #Output file name of all of the files in the directory 
    theName = 'allAccountList.txt' 
    outputFile = file + theName #A place where we can output all of the files 
    file1 = open(outputFile,'w') 
    
    total = "" 
    total += "Account, Name, Recorded Count, Scheduled Count, Past Scheduled, Recording, Time Stamp\n"
    
    for eachD in dir_list:
        #Each File name, we will check to see 
        #eachD = eachD.split('_') 
        eachD = eachD.replace('_',',')
        if eachD != theName:    
            total += eachD + '\n'
        
    file1.write(total)
    return 

def getRecCount(totalTable): 
    #Get the recording counts for the tables
    recordingCount =0 
    recordedCount = 0 
    scheduledCount = 0  
    pastScheduledCount = 0 
    unmatchedCount = 0 
    #str(recCount), str(schedCount),str(recordingCount),str(pastScheduled),str(conflictCount),str(cancelledCount), str(unmatchedProgramCount)
    #row = showName,str(recCount), str(schedCount),str(recordingCount),str(pastScheduledCount), str(seriesObjState), str(channelNumber)
    for eachRow in totalTable: 
        recordedCount += int(eachRow[1]) 
        scheduledCount += int(eachRow[2]) 
        recordingCount += int(eachRow[3])
        pastScheduledCount += int(eachRow[4])
        
        unmatchedCount += int(eachRow[7]) 
    return (recordedCount,scheduledCount,pastScheduledCount,recordingCount,unmatchedCount)

            #THen we know that it is correctly matched
def validationCheckIndividualRecs(individualRecordings,accountName): 
    #we can check the individual recordings within 
    flagged_recorded = []
    flagged_scheduled = []
    for arec in individualRecordings:

        glfProgramID_a = arec['programDetailsGLF']
        seriesID_a = arec['seriesExtID'] 
        season_a = arec['Season Number'] 
        ep_a = arec['Ep'] 
        show_a = arec['Show'] 
        time_a = arec['Time'] 
        state_a = arec['Series State'] 
        seriesID_a = arec['seriesID']
        isSeries_a = arec['seriesObjType']
        originalAir_a = arec['originalAirDate']
        #innerRow['Season Number'] = seasonNumber 
        #innerRow['Ep'] = epNumber

        for brec in individualRecordings: 
            
            glfProgramID_b = brec['programDetailsGLF']
            seriesID_b = brec['seriesExtID'] 
            season_b = brec['Season Number'] 
            ep_b = brec['Ep'] 
            state_b = brec['Series State'] 
            show_b = brec['Show']
            originalAir_b = brec['originalAirDate']
            isSeries_b = brec['seriesObjType']

            time_b = brec['Time'] 
            #seriesID_b = brec['seriesID']
            
            if seriesID_a == seriesID_b and glfProgramID_b == glfProgramID_a and glfProgramID_b != "None" and glfProgramID_a != "None":    
                if state_b == "Scheduled" and state_a == "Cancelled" and timeDelta(time_b,time_a) > 0:  
                        #And the time_a was greater than time_b
                        print("Show was scheduled and then cancelled")
                        return 1

            if ep_a != 'NULL' and ep_a != 'None' and ep_b != 'None' and season_a != 'None' and season_b != 'None' and ep_b != 'NULL' and season_a != 'NULL' and season_b != 'NULL' and ep_a == ep_b and season_a == season_b and time_b != time_a and show_a == show_b and state_b ==  state_a and seriesID_b == seriesID_a: 
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', 'T') + 'Z'
                if timeDelta(time_a,time_now) < 0 and timeDelta(time_b,time_now) < 0: 
                    print("Second Recording should not have happened on this account with show " + show_a + " at  " + time_a + " vs "  + time_b + " for " + accountName) 
                    
                return 1

            if glfProgramID_b != None and glfProgramID_b != "NULL" and glfProgramID_a == glfProgramID_b and state_a == "Recorded" and state_b == "Recorded" and time_a != time_b and isSeries_b == 'Series' and isSeries_a == 'Series':
                print("The Show " + show_a + " at " + time_a + " vs " + time_b + " for " + accountName +" was duplicated as being recorded!! with GLF " + glfProgramID_b)
                flagged_recorded.append(glfProgramID_a)
                return 1
            #if seriesID_a == seriesID_b and glfProgramID_a != glfProgramID_a and originalAir_b != originalAir_a: 
                #THen we have an example of a show that has an invalid program configuration xdx
                #print("Original Air date is not set properly")
                #return 1
     
    return 0  
def valCheckIndRecordings_GLF(individualRecordings): 
    #Check to see if there were any recordings that were cancelled and scheduled with the same series but had a different 
    '''
    If there are any issues with the individual recordings ta
    
    '''
def validationCheckFakeIds(individualRecordings,accountName): 
    #Check the fake IDS of the recordings to ensure that there is no episodes that are incorrectly matched 
    for eachRec in individualRecordings:

        #Check to see whether or not the 
        programDetailsGeneric = eachRec['isGeneric']
        fake = eachRec['seriesExtID'] 
        programID = eachRec['programDetailsGLF'] 
        if fake.find('fake') != -1 and programDetailsGeneric == False:
            print("This ID should have switched back: " + eachRec['Show'] + " for " + programID + " with " + accountName)   
            
            #Then we have disciov
def checkSeriesValidation(recs,individualRecordings,seriesDetailObj,accountName,sanityData,_type):
    #This function will perform the basic series validation tests as part of the sanity 
    #accounts_Test is the account that is used for tracking the outcomes in each of the test 
    valMissingIDs = 0 
    valIndRecs = 0
    valImages = 0
    valDVRIds = 0
    
    valMissingIDs = validationCheckMissingIDS(recs) 

    valImages = validationCheckImages(_type,seriesDetailObj)
    valDVRIds = validationCheckDVRIds(_type,seriesDetailObj)
    #valFakeMatch = validationCheckFakeIds(individualRecordings,accountName) 
    #valCheckIndRecordings_GLF(individualRecordings)
    
   # sanityData.setAll(valMissingIDs, valIndRecs,valImages,valDVRIds) 
   
    sanityData.setValMissingIDS(valMissingIDs)

    sanityData.setValImages(valImages) 
    sanityData.setValDVRIds(valDVRIds) 
    
    '''
    js = {
          "Missing Ids": valMissingIDs, 
          "Missed Recordings": valIndRecs,
          "Missing Images": valImages, 
          "Unmatched Programs": valDVRIds
          }

    tot['data'].append(js) 
    '''
def validationCheckMissingIDS(recs):

    recs_string = str(recs) 
    count = 0 
    #Converting the recs to a string value 
    if 'description' not in recs_string:
        count += 1  
    if 'images' not in recs_string: 
        count += 1    
    if 'name' not in recs_string: 
        count += 1  
    if 'roles' not in recs_string: 
        count += 1  
    if 'sortName' not in recs_string: 
        count += 1  
    if 'startYear' not in recs_string: 
        count += 1  
    if 'endYear' not in recs_string: 
        count += 1   
    if 'externalAccountId' not in recs_string: 
        count += 1  
    if count == 8: 
        return 1 
    else: 
        return 0 

def validationCheckDVRIds(_type,seriesDetailObj): 
    if len(seriesDetailObj) == 0: 
        return 0
    
    if _type == "OSS": 
        dvrID = seriesDetailObj['id']#FOR THE OSS 
    elif _type == "DVRPROXY": 
        try: 
            dvrID = seriesDetailObj['glfSeriesId'] #For the DVR Proxy 
        except: 
            dvrID = "" 
            pass
    if dvrID != None: 
        if dvrID.find('dvr-unmatched') == 0:
            return 1 
        else: 
            return 0 
  
def validationCheckImages(_type,seriesDetailObj):
    if len(seriesDetailObj) == 0: 
        return 0
    try: 
        images = seriesDetailObj['images'] 
    except: 
        images = None 
    try: 
        startYear = seriesDetailObj['startYear'] 
    except: 
        startYear = None
    try: 
        endYear = seriesDetailObj['endYear'] 
    except: 
        endYear = None  
    
    if startYear == None and endYear == None and images == None: 
        #print("Empty Start Year + End Year + Image") 
        return 1 
    else: 
        return 0 
def convertToString(seriesExtID,programGeneric,accountName,showName,programDetailsID): 
    #Convert to the series EXT ID. 
    try: 
        hexValue = seriesExtID.split('y')[1]
    except: 
        return 0
    hexx = bytearray.fromhex(hexValue).decode()
    if hexx.find('EP0') == 0 and programGeneric == True: #Then we have found that hte ID matches EP 
        print(hexx + " That should have been programGeneric, but isn't " + accountName + " for " + showName + " " + programDetailsID)
        return 1 
    if hexx.find('SH0') == 0 and programGeneric == False: 
        print(hexx + " That should have been programGeneric, but isn't " + accountName+ " for " + showName + " " + programDetailsID)
        return 1 
    
    return 0 #Then there is nothing wrong with this         

def testSkipToken(typeCALL,accountName,env,sanityData,DVRVersion): 
    toek = get_token(typeCALL,env, list())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    session = requests.Session()
    session.headers = toek
    if typeCALL == 'OSS': 
        url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/' + accountName + '/recording-definitions/?$top=1&$skipToken='
    elif typeCALL == 'DVRPROXY': 
        #url = 'https://appgw-client.'+env+'.bce.tv3cloud.com/S96/dvrproxy/v1/tenants/default/accounts/' + accountName + '/recording-definitions/?$top='+top+'&$skipToken=' + skipToken
        url= 'https://appgw-client.'+env+'.bce.tv3cloud.com/'+DVRVersion+'/dvrproxy/v1/tenants/default/accounts/' + accountName + '/recording-definitions/?orderby=startdate&$top=1&$skipToken='
        
    try:
        response = session.get(url)
    except:     
        return 
    if str(response.status_code) == '503': 
        return 
    else:
        rj = response.json()
        if len(rj) == 1: 
            return 
        else: 
            try: 
                skipToken = rj['skipToken'] 
                return 
                
            except: 
                #Otherwise, this is an error and we have an error with this account 
                sanityData.setSkipTokenError(1)
                print("Invalid Skip Token "  + accountName)  
                return 
def checkResponseType(response): 
    #responseCode = respone.
    code = response.status_code 
    if str(code) == "503":
        print("Error code present") 
    
    sanityData.errorResponseCode(code) 
def getUpgradeGroup(eachAccount,env): 
    accountSettings = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/' + eachAccount
    tok = get_token('OSS',env, list())
    
    session = requests.Session()
    session.headers = tok
    
    response = session.get(accountSettings) 
    rj = response.json() 
def checkCatalogue(recs, tok, _env,accountName):
    session = requests.Session()
    session.headers = tok
    for eachRec in recs: 
        try: 
            uid = str(eachRec['externalID'])
        except: 
            return
        env = str(_env)
        # print('==> Getting title: ' + str(uid) +'\n')
        url = "https://appgw-client-a." + env + ".bce.tv3cloud.com/S96/discovery/v3/programs/" + uid
        # print("URL: " + url)
        # try:
        # augmented_data = mf_get_op_data(uid)
        # popularity = augmented_data['popularity']
        # mf_imagestatus = augmented_data['mf_imagestatus']
        # try:
        # mf_matchstatus = augmented_data['mf_matchstatus']
        # except:
        # mf_matchstatus = "Err"
        # except:
        # popularity = -1
        # try:
        response = session.get(url)  # , headers=token
        if str(response.status_code) != '404': 
            try:
                rj = response.json()
                # print(rj)
                try:
                    description = rj['Description']
                except:
                    description = ""
                try:
                    seriesid = rj['SeriesId']
                except:
                    seriesid = "Error"
                try:
                    title = rj['Name']
                except:
                    title = "Error"
                try:
                    inferred_oad = rj['OriginalAirDate']
                except:
                    inferred_oad = "Error"
                try:
                    inferred_language = rj['Locale']
                except:
                    inferred_language = "Error"
                try:
                    inferred_rating = rj['Ratings'][0]['Value']
                except:
                    inferred_rating = "Error"
                try:
                    episode_title = rj['EpisodeName']
                except:
                    episode_title = ""
                try:
                    images = rj['Images']
                except:
                    images = []
                try:
                    supported_images = rj['SupportedImages']
                except:
                    supported_images = []
                try:
                    showName = rj['Name']
                except:
                    showName = "test"

                currShow = eachRec['Show']
                if showName != currShow and eachRec['Series State'] != "Recorded":
                    print("The OSS Show Name: "  + currShow + " and the Catalogue Show Name: " + showName)
                    print("State: ", eachRec['Series State'] + " on " + accountName)
            except:
                return

def mf_getRecordings(typeCALL,accountName,env,sanityData,DVRVersion):
                         
    skipToken = ""
    totalRec = 0                                                                                                                                                                                                                                                                                                                               
    pastScheduled = 0 
    seriesDetailObj = [] 
    totalTable = []
    individualRecordings = [] 
    totalSched = 0 
    totalRecordingCount =0 
    seriesObjState = ""
    
    tok = get_token(typeCALL,env, list())
    
    session = requests.Session()
    session.headers = tok
    
    while(skipToken != None):
        
        top = str(100)
        
        if typeCALL == 'OSS': 
            url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/' + accountName + '/recording-definitions/?$top='+top+'&$skipToken=' + skipToken
            
        elif typeCALL == 'DVRPROXY':
            #url = 'https://appgw-client.'+env+'.bce.tv3cloud.com/S96/dvrproxy/v1/tenants/default/accounts/' + accountName + '/recording-definitions/?$top='+top+'&$skipToken=' + skipToken
            url= 'https://appgw-client.'+env+'.bce.tv3cloud.com/'+DVRVersion+'/dvrproxy/v1/tenants/default/accounts/' + accountName + '/recording-definitions/?orderby=startdate&$top='+top+'&$skipToken='+skipToken
          
        try:
            response = session.get(url)
            if str(response.status_code) == "503": 
                print("503 Error on this account ", accountName)
            #checkResponseType(response) 
        except: 
            return

        #testSkipToken(url)
        rj = response.json()
        if rj == None: 
            return #Then there is nothing in this json (i.e empty )
        try: 
            code  = rj['code']  
            if code == 'NotFound':
                return 
        except: 
            pass
        
        #upgradeGroup = getUpgradeGroup(accountName,env) 
        
        testSkipToken(typeCALL, accountName,env,sanityData,DVRVersion) 
    
        try: 
            skipToken = rj['skipToken']
        except: 
            
            skipToken = None
        try: 
            recs = rj['recordingDefinitions']
        except: 
            return 
        recCount = 0 
        schedCount = 0
        recordingCount = 0
        pastScheduled = 0
        conflictCount = 0
        cancelledCount = 0 
        unmatchedProgramCount = 0 
        
        for eachRec in recs: 

            recGroup = eachRec['recordings']
            try: 
                seriesDetails = eachRec['seriesDetails'] 
            except: 
                seriesDetails = None 
                
            if seriesDetails != None: 
                seriesDetailObj = eachRec['seriesDetails']
            try: 
                seriesNameObj = seriesDetailObj['name']
            except: 
                seriesNameObj = None 
            try: 
                glfStationId  = eachRec['stationId']
            except: 
                glfStationId = ""
            
            try: 
                seriesExtID = seriesDetailObj['id'] 
            except: 
                seriesExtID = "NULL" 
                
            try: 
                seriesNameValue = seriesNameObj[0]['value']
            except: 
                seriesNameValue = None
            
                
            if seriesNameValue == None or seriesNameValue == "": 
                seriesNameValue = "NULL"
                # i am getting the show name from the 1st recObj in the resulting array of json objects.
                try: # if the series object has no recording object, parsing the array will fail - catching this exception. 
                    progDetail = recGroup[0]['programDetails']
                    seriesNameValue = "* "+ progDetail['name']
                
                except:
                    sanityData.setProgDetails(1) #Means we have a null recordings object so we 
                    seriesNameValue = "* ERROR * NULL Recordings Object"
    
            showName = seriesNameValue 
            channelNumber = eachRec['channelNumber']
            seriesObjType = eachRec['type']
  
            if (recGroup != None): 
                for eachRecGroup in recGroup:
                    innerRow = {}  
                    try: 
                        seriesID =str(eachRecGroup['id'])
                    except: 
                        seriesID = "NULL" 
                    try: 
                        seriesObjState = str(eachRecGroup['state'])
                    except: 
                        seriesObjState = "NULL"
                    try: 
                        seasonNumber = str(eachRecGroup['programDetails']['seasonNumber'])
                    except: 
                        seasonNumber = "NULL"
                    try: 
                        epNumber = str(eachRecGroup['programDetails']['episodeNumber'])
                    except: 
                        epNumber = "NULL" 
                    try: 
                        startUTC = str(eachRecGroup['scheduledStartUtc'])
                    except: 
                        startUTC = "NULL" 
                    try: 
                        programDetailsGLF = programDetailsGLF = str(eachRecGroup['programDetails']['glfProgramId'])
                    except: 
                        programDetailsGLF = "NULL" 
                    try: 
                        programDetailsID = str(eachRecGroup['programDetails']['id']) 
                    except:
                        programDetailsID = "NULL" 
                    try: 
                        originalAirDate = eachRecGroup['programDetails']['originalAirDateTime'] 
                    except: 
                        originalAirDate = "NULL" 
                    try: 
                        programDetailsGeneric = eachRecGroup['programDetails']['isGeneric']
                    except:
                        programDetailsGeneric = "NULL"
                    try: 
                        externalId = eachRecGroup['programDetails']['id']
                    except: 
                        externalId = "NULL" 
                        
                    sanityData.setOriginalAirDate(originalAirDate) 
                    #checkValidation(seriesDetailObj,accountName)
                    innerRow['Time'] = startUTC
                    innerRow['Show'] = showName
                    innerRow['Season Number'] = seasonNumber 
                    innerRow['Ep'] = epNumber
                    innerRow['externalID'] = externalId
                    innerRow['Channel Number'] = channelNumber
                    innerRow['Series State'] = seriesObjState 
                    innerRow['seriesObjType'] = seriesObjType
                    innerRow['programDetailsGLF'] = programDetailsGLF
                    innerRow['isGeneric'] = programDetailsGeneric
                    innerRow['glfProgramId'] = programDetailsID
                    innerRow['seriesID'] = seriesID
                    innerRow['seriesExtID'] = seriesExtID
                    innerRow['originalAirDate'] = originalAirDate 
                    innerRow['recordingID'] = eachRecGroup['id']
                    innerRow['glfStationID'] = glfStationId
                    #print(glfStationId)
                    
                    #print(originalAirDate)
                    if seriesObjState == "Scheduled": 
                        schedCount += 1
                        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', 'T') + 'Z'
                        if timeDelta(startUTC,time_now) < 0: 
                            try: 
                                sanityData.setfake_generic(convertToString(programDetailsID,programDetailsGeneric,accountName,showName,programDetailsGLF))
                            except: 
                                pass 
                        totalSched += schedCount
                    elif seriesObjState == "Recorded": 
                        recCount += 1 
                        totalRec += recCount 
                    elif seriesObjState == "Recording": 
                        recordingCount += 1
                        totalRecordingCount += recordingCount
                    elif seriesObjState == "Conflicts": 
                        conflictCount += 1
                    elif seriesObjState == "Canceled": 
                        cancelledCount += 1
                     
                    #if showName == 'General Hospital' or showName == 'Family Feud': 
                        #print(showName + ' ' + str(channelNumber
                        #print(programDetailsGLF)))
                    #if isPastScheduled(startUTC) and seriesObjState == "Scheduled": 
                        #pastScheduled += 1
                        
                    individualRecordings.append(innerRow) 

            row = {
                "Show Name": showName,
                "recCount": recCount,
                "schedCount": schedCount, 
                "recordingCount": recordingCount, 
                "pastScheduled": pastScheduled, 
                "conflictCount": conflictCount, 
                "cancelledCount": cancelledCount, 
                "seriesObjstate": seriesObjState, 
                "channelNumber": channelNumber,
                "seriesExtID": seriesExtID 
                }
            
            #row = showName,str(recCount), str(schedCount),str(recordingCount),str(pastScheduled),str(conflictCount),str(cancelledCount),str(seriesObjState), str(channelNumber), str(seriesExtID) 
            #print("TYPECALL", typeCALL) 
            #print(row) 
        
            totalTable.append(row)
            checkSeriesValidation(recs,individualRecordings,seriesDetailObj,accountName,sanityData,typeCALL)
            
            #individualRecordings = [] 
            recCount = 0 
            schedCount = 0 
            recordingCount = 0 
            pastScheduled = 0 
            conflictCount = 0 
            cancelledCount = 0
            
        if skipToken == None or skipToken == "": 
            break
    #checkCatalogue(individualRecordings,tok,env,accountName)
    #print(len(individualRecordings))
    valIndRecs = 0
    valIndRecs = validationCheckIndividualRecs(individualRecordings, accountName)

    sanityData.setValIndRecs(valIndRecs)
    return individualRecordings #return the Total Table of all recordings

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size * 1e-9 #Return in GB 

def printTestCase(sentence, number): 
    if number == 0: 
        #Then the test case has passed 
        failed = colored("Passed", "green") 
        print(sentence + " COUNT: " + str(number) + " " + failed ) 
    elif number == None: 
        passed = colored("Passed", "green") 
        print(sentence + " " + passed) 
    else: 
        #Then the tets case has failed  
        passed = colored("Failed", "red") 
        print(sentence + " COUNT: " + str(number) + " " + passed ) 

def processResults(sanityData,featureGroupLen,TOTALSHOWS):
    #Process the accounts 
    js = []
    '''
    valMissingIDs_program = 0 
    valIndRecs_program = 0
    valImages_program = 0
    valDVRIds_program = 0
    
    
    js = {"account": accountName, 
          "Missing Ids":valMissingIDS, 
          "Missed Recordings": valIndRecs,
          "Missing Images": valImage, ,,
          "Unmatched Programs": valDVRIds
          }

    
    for eachRow in accounts_Test: 
        
        for eachDat in eachRow['data']: 
            if eachDat['Missing Ids'] == True: 
                #Then it means that this account has failed the test case 
                valMissingIDs_program += 1
            if eachDat['Missed Recordings'] == True: 
                valIndRecs_program += 1
            if eachDat['Missing Images'] == True: 
                valImages_program += 1
            if eachDat['Unmatched Programs'] == True: 
                valDVRIds_program += 1
    '''
    
    valMissingIDs_program = sanityData.getMissingIDS()
    valIndRecs_program = sanityData.getValIndRecs() 
    valImages_program =  sanityData.valImages()
    valDVRIds_program = sanityData.valDVRIds()
    valAccountConfiguration_program = sanityData.getAccountConfigurationVal() 
    progDetails = sanityData.getProgDetails()
    outOfSync = sanityData.getDVROutOfSync() 
    fake_gen = sanityData.getFake_generic()
    enableConfig = sanityData.getEnableConfiguration()
    devices = sanityData.getDevices() 
    
    skipTokenError = sanityData.getSkipTokenError() 
    perc_devices = 100 * devices/featureGroupLen 
    perc_enableConfig= 100 *enableConfig/featureGroupLen
    list_originalAir = sanityData.getOriginalAirDate() 
    outOfSyncDVRData = sanityData.getdvrStationOutOfSync() 
    
    try: 
        results = TimestampAnalyser(list_originalAir)
        DonutChartOfResults(results)
    except: 
        results = 0
    
    print("Summary of Results")
    print("Total Shows Counted: ",TOTALSHOWS)
    print("--------------------------------------------------------------------------------")
    printTestCase("Test Case 1: Number of Occurences of missing sections in JSON [MFR-8980]", valMissingIDs_program)
    js.append({"Test Case 1: Number of Occurences of missing sections in JSON [MFR-8980]": valMissingIDs_program})
    
    printTestCase("Test Case 2: Number of Occurences of recordings that were scheduled and duplicated with the same episode [MFR-4380]",  valIndRecs_program)
    js.append({"Test Case 2: Number of Occurences of recordings that were scheduled and duplicated with the same episode [MFR-4380]": valIndRecs_program})
    
    #printTestCase("Test Case 3: Number of Occurences of missing image data ", valImages_program)
    printTestCase("Test Case 3: Number of Occurences of unmatched series IDs [MFR-9116] ", valDVRIds_program)
    js.append({"Test Case 3: Number of Occurences of unmatched series IDs [MFR-9116]": valDVRIds_program})
    
    printTestCase("Test Case 4: Number of Occurences of invalid account profile configurations (Ingress or Egress is not set) [MFR-9409]", valAccountConfiguration_program) 
    js.append({"Test Case 4: Number of Occurences of invalid account profile configurations (Ingress or Egress is not set) [MFR-9409]": valAccountConfiguration_program})
    
    printTestCase("Test Case 5: Number of Occurences of empty program details data [MFR-8192]",progDetails)
    js.append({"Test Case 5: Number of Occurences of empty program details data [MFR-8192]": progDetails})
    
    printTestCase("Test Case 6: Number of Occurences of out-of-sync accounts between DVR Proxy and OSS definitions [MFR-8249]", outOfSync)
    js.append({"Test Case 6: Number of Occurences of out-of-sync accounts between DVR Proxy and OSS definitions [MFR-8249]": progDetails})
    
    
    printTestCase("Test Case 7: Number of Occurences of fake but labelled as generic for EP0 and SH0 IDS", fake_gen)
    if perc_enableConfig > 2: 
        #Then 
        printTestCase("Test Case 8: Accounts that have been accidently disabled",enableConfig)
        js.append({"Test Case 8: Accounts that have been accidently disabled": enableConfig})
        
    else: 
        printTestCase("Test Case 8: Accounts that have been accidently disabled",number = None) 
        js.append({"Test Case 8: Accounts that have been accidently disabled": 0})
        
    if perc_devices > 2: 
        printTestCase("Test Case 9: Accounts that have accidently had their devices their removed", devices)
        js.append({"Test Case 9: Accounts that have accidently had their devices their removed": devices})
    else: 
        printTestCase("Test Case 9: Accounts that have accidently had their devices their removed", number = None) 
        js.append({"Test Case 9: Accounts that have accidently had their devices their removed": 0})
    try: 
        printTestCase("Test Case 10: Number of occurences of invalid original air dates [MFR-9472]", results.count(0))
        js.append({"Test Case 10: Number of occurences of invalid original air dates [MFR-9472]": results.count(0)})
    except: 
        printTestCase("Test Case 10: Number of occurences of invalid original air dates[MFR-9472]", 0) 
        js.append({"Test Case 10: Number of occurences of invalid original air dates [MFR-9472]": 0})
        
    printTestCase("Test Case 11: Number of occurences of invalid skip tokens [MFR-6261]",  skipTokenError)
    js.append({"Test Case 11: Number of occurences of invalid skip tokens [MFR-6261]": skipTokenError})
    printTestCase("Test Case 12: Number of occurences of empty DVR Data ", sanityData.getDVREmptyData())
    js.append({"Test Case 12: Number of occurences of empty DVR Data": sanityData.getDVREmptyData()})
    
    printTestCase("Test Case 13: Number of occurences where DVR station ID did not match OSS station ID",outOfSyncDVRData)
    js.append({"Test Case 13: Number of occurences where DVR station ID did not match OSS station ID": outOfSyncDVRData})
    return js
    
    #print("Test Case 5: Total Number of Unmatched Program IDS", unmatchedProgramCount)
    #def checkRecordedStates(OSSRecs, DVRRECS): 

def checkDVREmpty(DVRRECS,OSSRecs,sanityData,accountName):
    for eachDVR in DVRRECS:

        dvrProgId = eachDVR['programDetailsGLF']
        dvr_id = eachDVR['recordingID']
        dvr_time = eachDVR['Time']
        dvrShowName = eachDVR['Show']

        if dvrShowName == "NULL" or dvrShowName == None or dvrShowName == "" or dvrShowName ==  "* ERROR * NULL Recordings Object" and re.match('8455',accountName):
            print("This show has empty program detail information (DVR) " + accountName)
            sanityData.setDVREmptyData(1)
        if dvrProgId == None or dvrProgId == "NULL" or dvrProgId == "" or dvrProgId == 'None' and re.match('8455',accountName):
            print("This show has an empty program ID on account (DVR) ", accountName)
            sanityData.setDVREmptyData(1)

            for eachOSS in OSSRecs:
                if dvr_id == eachOSS['recordingID']:

                    showName = eachOSS['Show']
                    startTime = eachOSS['Time']
                    channelNumber = eachOSS['Channel Number']
                    break
            try:
                print("This Show is Empty "+ showName + " " + startTime + " on channel " + str(channelNumber) + " on " + accountName)
            except:
                pass
def performDVRProxySanity(eachAccount, OSSRecs,env,sanityData,dvrVersion): 
    #Perform a sanity based on the recordings of the OSS Definitions
    DVRRECS = mf_getRecordings('DVRPROXY',eachAccount,env,sanityData,dvrVersion)
    checkDVREmpty(DVRRECS,OSSRecs,sanityData,eachAccount)
    #compareRecs(DVRRECS,OSSRecs) 
    try:
        DVRLength = len(DVRRECS)
    except:
        DVRLength = 0 
    try:
        OSSLength = len(OSSRecs) 
    except:
        OSSLength = 0 
    
    if DVRLength != OSSLength: 
        for eachOSS in OSSRecs: 
            ossProgId = eachOSS['programDetailsGLF'] 
            ossState = eachOSS['Series State'] 
            startTime = eachOSS['Time'] 
            OSS_id = eachOSS['recordingID'] 
            
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', 'T') + 'Z'
            delta = timeDelta(startTime, time_now)
            
            flag = False  
            for eachDVR in DVRRECS: 
                dvrProgId = eachDVR['programDetailsGLF'] 
                dvrState = eachDVR['Series State']
                dvr_id = eachDVR['recordingID'] 
                #print(dvrProgId) 
                
                if dvr_id == OSS_id:
                    #Found that there is a match 
                    flag = True
                    if eachDVR['glfStationID'] != eachOSS['glfStationID'] and eachDVR['glfStationID'] != ''and eachOSS['glfStationID'] != '': 
                        print("Mismatch between GLF station IDs " + eachDVR['glfStationID'] + " " + eachOSS['glfStationID']) 
                        sanityData.setdvrStationOutOfSync(1)
                    
            if flag == False and ossState == 'Recorded': 
                #Then there is something wrong 
                if abs(delta)< 90 and abs(delta) > 0.06: 
                    sanityData.setDVROutOfSync(1) 
                    print("Out of Sync!!! " + eachAccount + " " + ossProgId)  
                    
        #checkRecordedStates(OSSRecs, DVRRECS)  #Now we check to see that the recorded counts for the assets matches each other  
        #print(strr) 
        '''
    #Now we want to compare the recordings of the OSS and the DVR 
    for eachDVRRec in DVRRECS: 
        for eachOSSRec in OSSRecs: 
            #Now we just want to make sure that the show name is sam
            show_OSS = eachOSSRec["Show Name"]
            show_DVR = eachDVRRec["Show Name"]
            
            recCount_OSS = eachOSSRec["recCount"] 
            recCount_DVR = eachDVRRec["recCount"] 
            
            channelNumber_OSS = eachOSSRec["shedCount"]
            channelNumber_DVR = eachDVRRec["shedCount"]
            
            if '* ERROR * NULL Recordings Object' in show_DVR == True and recCount_OSS == recCount_DVR and channelNumber_OSS == channelNumber_DVR: 
                #Then we know that this is a valid run through 
      '''      
            
def getAccounts_FeatureGroup(_feature_group,env):
    tok = get_token('OSS',env, list())
    
    session = requests.Session()
    session.headers = tok
    
    allAccounts = [] 
    skip = "" 

    while True:
        url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/feature-groups/' + _feature_group +'/accounts?$top=10'
        
        if len(skip) > 0: 
            url += '&$skipToken=' + skip 

        resp = session.get(url) 
        rj = resp.json() 
        try: 
            accounts = rj['accountIds']
        except: 
            pass
        
        try: 
            allAccounts.extend(accounts)
        except: 
            pass 
        try: 
            skip = rj['skipToken'] 
        except: 
            break 
        if skip == None: 
            break 

    return allAccounts
def checkAccountSettings(accountName,env,sanityData):
    #Now we want to check the account's settings to make sure that there is no potential discrepancy with the ingress bandwidths
    url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts' + accountName

    skip = ""
    count_band = 0
    tok = get_token('OSS',env, list())

    session = requests.Session()
    session.headers = tok
    while True:
        url = url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/' + accountName
        if len(skip) > 0:
            url += '&$skipToken=' + skip

        try:
            resp = session.get(url)
            rj = resp.json()
        except:
            pass
        if accountName.find('84') == -1:
           return

        wanProfile = rj['wanProfile']['maxBitRate']
        enable = rj['enabled']
        ingressBandwidth = rj['streamProfile']['maxIngressBandwidth']
        egressBandwidth = rj['streamProfile']['maxEgressBandwidth']
        ingressStreamCount = rj['streamProfile']['maxIngressStreamCount']
        egressStreamCount = rj['streamProfile']['maxEgressStreamCount']

        wanProfile = rj['wanProfile']['maxBitRate']

        if enable == True:
            #Then we can do some checks
            if ingressBandwidth == None and egressBandwidth != None:
                #print("Account profile has not been set properly for Egress Bandwidth and Ingress Bandwidth for " + accountName)
                count_band += 1
            if ingressBandwidth != None and egressBandwidth == None:
                #print("Account profile has not been set properly for Egress Bandwidth and Ingress Bandwidth for " + accountName)
                count_band += 1
            if egressStreamCount == None and ingressStreamCount != None:
                #print("Account profile has not been set properly for Egress Stream Count and Ingress Stream Count for " + accountName)
                count_band += 1
            #if ingressBandwidth != None and wanProfile != None:
                #if ingressBandwidth > int(wanProfile):
                    #print("Account profile has not been set properly for Ingress Bandwdith and Wan Profile for " + accountName)
                    #count_band += 1
            if wanProfile == None:
                count_band += 1
        elif enable == False:
            sanityData.setEnableConfiguration(1)
        try:
            skip = rj['skipToken']
        except:
            skip = None

        if skip == None:
            break

    if count_band != 0:
        #THen we have a case that there is an account mismatch
        print(accountName + " Is not configured correctly ")
        sanityData.setAccountConfigurationVal(1)

def checkDeviceSettings(accountName,env,sanityData):
    #Now we want to check the account's settings to make sure that there is no potential discrepancy with the ingress bandwidths

    skip = ""
    count_band = 0
    tok = get_token('OSS',env, list())

    session = requests.Session()
    session.headers = tok
    while True:
        url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/' + accountName + '/devices'
        if len(skip) > 0:
            url += '&$skipToken=' + skip

        try:
            resp = session.get(url)
            rj = resp.json()
        except:
            pass

        if re.match('84',accountName) == None:
            return
        try:
            deviceIDs = len(rj['deviceIds'])
        except:
            deviceIDs = 0
        if deviceIDs == 0:
            sanityData.setDevices(1)

        try:
            skip = rj['skipToken']
        except:
            skip = None

        if skip == None:
            break

def testAPICall(accountName,env,sanityData):
    #Run API call testing
    dvrVersion = ['S96','S108','S116']
    skipToken = ""
    top = '100'

    #Token for the DVR Proxy API
    tok_dvr = get_token('DVRPROXY',env, list())
    session_dvr = requests.Session()
    session_dvr.headers = tok_dvr

    tok_oss = get_token("OSS", env,list())
    session_oss = requests.Session()
    session_oss.headers = tok_oss

    for eachdvr in dvrVersion:
        url_recordingDefinitionsDVR= 'https://appgw-client.'+env+'.bce.tv3cloud.com/'+eachdvr+'/dvrproxy/v1/tenants/default/accounts/' + accountName + '/recording-definitions/?orderby=startdate&$top='+top+'&$skipToken='+skipToken

        #url_devices = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/' + accountName + '/devices'
        recordingDefinitionsDVR = session_dvr.get(url_recordingDefinitionsDVR)
        #time.sleep(10)

        #sanityData.setAPIResponse()

        #url_recordingDefinitionsOSS = session.get(url_recordingDefinitionsOSS)
        #resp_url_devices = session.get(url_devices)

        print("DVR Recording Definitions ", recordingDefinitionsDVR)

    url_recordingDefinitionsOSS = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/' + accountName + '/recording-definitions/?$top='+top+'&$skipToken=' + skipToken
    recordingDefinitionsOSS = session_oss.get(url_recordingDefinitionsOSS)
    print("OSS Recording Definitions", recordingDefinitionsOSS)

def checkOSSRecsPastDate(timeStamp,ossRecordings):
    #Goal of this function is to check whether there are any recordings that have been scheduled greater than a certain timeframe
    count = 0
    try:
        recordingLength = len(ossRecordings)
    except:
        return
        pass

    for eachOSS in ossRecordings:
        ossTimeStamp = eachOSS['Time']
        if timeDelta(timeStamp,ossTimeStamp) > 0:
            count += 1
    if count > 0:

        print("This account has " + str(recordingLength) + " but has recordings that are not past the 18th")

        return
def main(): 
    testResults = [] 
    envs = ['proda']
    
    sanityData = SanityData() #Class to hold    all of the sanity data 
    TOTALSHOWS = 0
    for env in envs:
        
        if env == 'proda': 
            DVRVersion = "S96"
        elif env == 'prodb': 
            DVRVersion = "S108" 
        elif env == 'prodc': 
            DVRVersion = "S116" 
            

        
        print("Running test cases for", env)
        
        _feature_group = "NAPA_TRIAL"
    
        accountsInFeatureGroup = getAccounts_FeatureGroup(_feature_group,env)

        #accountsInFeatureGroup = ['8452000000000003']
        #accountsInFeatureGroup = ['ucclient20']

        featureGroupLen = len(accountsInFeatureGroup)
        
        for eachAccount in accountsInFeatureGroup:

            #try:
                #testAPICall(eachAccount, env, sanityData)
            #except:
                #pass

            try:
                OSSRecs = mf_getRecordings('OSS',eachAccount,env,sanityData,DVRVersion)
                TOTALSHOWS += len(OSSRecs)
            except:
                OSSRecs = None
            #   pass
            try:
                accountConfigurationVal = checkAccountSettings(eachAccount,env,sanityData)#Query the account settings where something could potentially be problematic
            except:
                pass
            try:
                checkDeviceSettings(eachAccount,env,sanityData)
            except:
                pass

            #Check to see if any of the DVR PRoxy Definitions are okay
            try:
                if OSSRecs != None:
                    performDVRProxySanity(eachAccount, OSSRecs,env,sanityData,DVRVersion)
            except:
                pass

        innerRow = {}

        results_p = processResults(sanityData,featureGroupLen,TOTALSHOWS)
        innerRow['Environment'] = results_p
        testResults.append(results_p)

        print(testResults)
        print("\n")
    return testResults

main() #Return the Test Results 