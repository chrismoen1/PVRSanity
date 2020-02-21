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

import re  # Regex expression

global c
global db

import re
# setup.py
from distutils.core import setup

counter = 0
path = "D:\\scripts\\output\\hourly_C"

def get_token(type_cert, _env, _proxyurl):
    # This is courtesy of James Owen c. April 2019
    # open token file and check expiry
    basePath = 'C:/Tools/scripts/'
    token_filename = ""
    token_uri = ""
    cert = ""
    cert_pass = ""

    if _env == 'proda':
        instance = 'proda.bce'

        if type_cert == 'OSS':
            cert = basePath + 'credentials/ossbssTools-proda-sts.pfx'
        elif type_cert == 'DVRPROXY':
            cert = basePath + 'credentials/ndvrTools-proda-sts.pfx'
        cert_pass = 'Medi@F1rst'
        token_uri = 'https://appgw-operatorstsssl.' + instance + '.tv3cloud.com/certactive'
        token_filename = './' + instance + '_token.json'


    elif _env == 'prodc':
        instance = 'prodc.bce'
        cert = basePath + 'credentials/ucpusher-ssl.pfx'
        cert_pass = ''
        token_uri = 'https://appgw-operatorstsssl.' + instance + '.tv3cloud.com/certactive'
        token_filename = './' + instance + '_token.json'
    elif _env == 'prodb':
        instance = 'prodb.bce'

        if type_cert == 'OSS':
            cert = basePath + 'credentials/ossbssTools-prodb-sts.pfx'
        elif type_cert == 'DVRPROXY':
            cert = basePath + 'credentials/ndvrTools-prodb-sts.pfx'

        cert_pass = 'Medi@F1rst'
        token_uri = 'https://appgw-operatorstsssl.' + instance + '.tv3cloud.com/certactive'
        token_filename = './' + instance + '_token.json'

    token_valid = 0
    try:
        with open(token_filename, 'r') as token_file_in:
            try:
                token = json.load(token_file_in)
                if ((datetime.datetime.timestamp(dateutil.parser.parse(token['RefreshTime'])) - time.time()) > 0):
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
        response = get(token_uri, headers={'Content-Type': 'application/json'}, verify=True, pkcs12_filename=cert,
                       pkcs12_password=cert_pass, proxies=_proxyurl)
        if (response.status_code == 200):
            token = response.json()  # load token from repsonse.get()
            with open(token_filename, 'w', encoding="utf-8", newline='\n') as token_file:
                try:
                    json.dump(response.json(), token_file, indent=4, sort_keys=True, ensure_ascii=False)
                    token_file.write('\n')
                    token_file.close()
                    # print (bcolors.OKGREEN + 'token saved ok. proceeding...\n' + bcolors.ENDC)
                except OSError:
                    print(bcolors.WARNING + 'can\'t create files.  bailing...' + bcolors.ENDC + '\n')
                    sys.exit('barf!')
        else:
            print('token request response: ', response.json()['ErrorDescription'], '\n')
            sys.exit('invalid cert or wrong password\n')

    try:
        auth_header = {'Authorization': 'OAUTH2 access_token="' + (token['AccessToken']) + '"',
                       'Content-Type': 'application/json'}
        return auth_header
    except:
        return None


def splitNumbers(eachList):
    # Then we know that there is a match for this particular file type
    pathList = eachList.split('_')
    recordedL = pathList[2]
    scheduledL = pathList[3]
    pastScheduledL = pathList[4]
    recordingL = pathList[5]

    recordedCount = recordedL.split('-')[1]  # Total amount of recordings on the STB
    scheduledCount = scheduledL.split('-')[1]  # ...
    pastScheduledCount = pastScheduledL.split('-')[1]  # ...
    pastRecordingCount = recordingL.split('-')[1]
    return (recordedCount, scheduledCount, pastScheduledCount, pastRecordingCount)


def getPastNumbers(path, account, currentPathName):
    # Use this path to gather all of the file output
    dir_list = os.listdir(path)

    totalPast = []
    for eachList in dir_list:
        reg = re.match(account, eachList)
        if reg != None:
            pastNums = splitNumbers(eachList)
            totalPast.append(pastNums)

    totalPast.append(splitNumbers(currentPathName))
    return totalPast  # Return the total past


def appendPastDefs_total(total, pastDefs):
    pastDefs_trans = list(map(list, zip(*pastDefs)))  # Here we are just transposing the original matrix

    i = 0

    current = ""
    for row in pastDefs_trans:
        # We will append this to the output
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

    annotations = ["Valid Dates (" + percentageOfValidDatesString + "%)",
                   "Invalid Dates (" + percentageOfInvalidDatesString + "%)"]

    data = [numberOfValidDates, numberOfInvalidDates]

    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(annotations[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                    horizontalalignment=horizontalalignment, **kw)

    # ax.set_title("Valid and Invalid Dates")

    plt.show()
    # plt.savefig("TimestampAnalyser.png")


def output_file(account, individualRecs, recSummary, showName, recCount, schedCount, recordingCount, pastScheduled):
    t = path + "\\" + showName + ".txt"
    pastDefinitions = getPastNumbers('C:\\Report_ORT\\', account, showName)

    file1 = open(t, "a")

    total = ""
    total += '-------------------------------------------Account Recording Breakdown Over Time-------------------------------------------\n'

    total += appendPastDefs_total(total, pastDefinitions)

    for eachRecs in individualRecs:
        row = ""
        for key, value in eachRecs.items():
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
        total += '|Show: ' + eachT[0] + '|Recorded Count: ' + eachT[1] + '|Scheduled Count: ' + eachT[
            2] + '|Recording Count: ' + eachT[3] + '|Past Scheduled: ' + eachT[4] + '|Series Obj State: ' + eachT[
                     5] + '|Channel Number: ' + eachT[6]
        total += '\n'

    file1.write(total)
    file1.close()


def timeDelta(time1, time2):  # time stamp

    time1_st = datetime.datetime.strptime(time1, "%Y-%m-%dT%H:%M:%SZ")
    time2_st = datetime.datetime.strptime(time2, "%Y-%m-%dT%H:%M:%SZ")

    delta = time2_st - time1_st
    delta_seconds = delta.total_seconds()
    # If the delta time is negative, then we know that it was scheduled in the past
    return delta_seconds / (24 * 60 * 60)


def organizeOutputFile(file):
    # Organize the output file name
    dir_list = os.listdir(file)  # Output file name of all of the files in the directory
    theName = 'allAccountList.txt'
    outputFile = file + theName  # A place where we can output all of the files
    file1 = open(outputFile, 'w')

    total = ""
    total += "Account, Name, Recorded Count, Scheduled Count, Past Scheduled, Recording, Time Stamp\n"

    for eachD in dir_list:
        # Each File name, we will check to see
        # eachD = eachD.split('_')
        eachD = eachD.replace('_', ',')
        if eachD != theName:
            total += eachD + '\n'

    file1.write(total)
    return


def getRecCount(totalTable):
    # Get the recording counts for the tables
    recordingCount = 0
    recordedCount = 0
    scheduledCount = 0
    pastScheduledCount = 0
    unmatchedCount = 0
    # str(recCount), str(schedCount),str(recordingCount),str(pastScheduled),str(conflictCount),str(cancelledCount), str(unmatchedProgramCount)
    # row = showName,str(recCount), str(schedCount),str(recordingCount),str(pastScheduledCount), str(seriesObjState), str(channelNumber)
    for eachRow in totalTable:
        recordedCount += int(eachRow[1])
        scheduledCount += int(eachRow[2])
        recordingCount += int(eachRow[3])
        pastScheduledCount += int(eachRow[4])

        unmatchedCount += int(eachRow[7])
    return (recordedCount, scheduledCount, pastScheduledCount, recordingCount, unmatchedCount)


def validationCheckFakeIds(individualRecordings, accountName):
    # Check the fake IDS of the recordings to ensure that there is no episodes that are incorrectly matched
    for eachRec in individualRecordings:
        # Check to see whether or not the
        programDetailsGeneric = eachRec['isGeneric']
        fake = eachRec['seriesExtID']
        programID = eachRec['programDetailsGLF']
        if fake.find('fake') != -1 and programDetailsGeneric == False:
            print(
                "This ID should have switched back: " + eachRec['Show'] + " for " + programID + " with " + accountName)

            # Then we have disciov


def checkResponseType(response):
    # responseCode = respone.
    code = response.status_code
    if str(code) == "503":
        print("Error code present")

   # sanityData.errorResponseCode(code)


def getUpgradeGroup(eachAccount, env):
    accountSettings = 'https://appgw-boss.' + env + '.bce.tv3cloud.com/oss/v1/accounts/' + eachAccount
    tok = get_token('OSS', env, list())

    session = requests.Session()
    session.headers = tok

    response = session.get(accountSettings)
    rj = response.json()


def mf_getRecordings(typeCALL, accountName, env, DVRVersion,file_scriptOutput):
    skipToken = ""
    totalRec = 0
    pastScheduled = 0
    seriesDetailObj = []
    totalTable = []
    individualRecordings = []
    totalSched = 0
    totalRecordingCount = 0
    seriesObjState = ""

    tok = get_token(typeCALL, env, list())

    session = requests.Session()
    session.headers = tok

    while (skipToken != None):

        top = str(100)

        if typeCALL == 'OSS':
            url = 'https://appgw-boss.' + env + '.bce.tv3cloud.com/oss/v1/accounts/' + accountName + '/recording-definitions/?$top=' + top + '&$skipToken=' + skipToken

        try:
            response = session.get(url)
            if str(response.status_code) == "503":
                print("503 Error on this account ", accountName)
            # checkResponseType(response)
        except:
            return

        # testSkipToken(url)
        rj = response.json()
        if rj == None:
            return  # Then there is nothing in this json (i.e empty )
        try:
            code = rj['code']
            if code == 'NotFound':
                return
        except:
            pass

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
                glfStationId = eachRec['stationId']
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
                try:  # if the series object has no recording object, parsing the array will fail - catching this exception.
                    progDetail = recGroup[0]['programDetails']
                    seriesNameValue = "* " + progDetail['name']

                except:
                    seriesNameValue = "* ERROR * NULL Recordings Object"

            showName = seriesNameValue
            channelNumber = eachRec['channelNumber']
            seriesObjType = eachRec['type']

            if (recGroup != None):
                for eachRecGroup in recGroup:
                    innerRow = {}
                    try:
                        seriesID = str(eachRecGroup['id'])
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



                    # checkValidation(seriesDetailObj,accountName)
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
                    print (startUTC[0:4] + "|" + showName)
                    txtOutput = startUTC[0:4] + "|" + showName + "\n"
                    file_scriptOutput.write(txtOutput)
                    innerRow['originalAirDate'] = originalAirDate
                    innerRow['recordingID'] = eachRecGroup['id']
                    innerRow['glfStationID'] = glfStationId
                    # print(glfStationId)

                    # print(originalAirDate)
                    if seriesObjState == "Scheduled":
                        schedCount += 1
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


            #totalTable.append(row)

            # individualRecordings = []
            recCount = 0
            schedCount = 0
            recordingCount = 0
            pastScheduled = 0
            conflictCount = 0
            cancelledCount = 0

        if skipToken == None or skipToken == "":
            break
    # checkCatalogue(individualRecordings,tok,env,accountName)
    # print(len(individualRecordings))
    return individualRecordings  # return the Total Table of all recordings


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size * 1e-9  # Return in GB


def printTestCase(sentence, number):
    if number == 0:
        # Then the test case has passed
        failed = colored("Passed", "green")
        print(sentence + " COUNT: " + str(number) + " " + failed)
    elif number == None:
        passed = colored("Passed", "green")
        print(sentence + " " + passed)
    else:
        # Then the tets case has failed
        passed = colored("Failed", "red")
        print(sentence + " COUNT: " + str(number) + " " + passed)



def getAccounts_FeatureGroup(_feature_group, env):
    tok = get_token('OSS', env, list())

    session = requests.Session()
    session.headers = tok

    allAccounts = []
    skip = ""

    while True:
        url = 'https://appgw-boss.' + env + '.bce.tv3cloud.com/oss/v1/feature-groups/' + _feature_group + '/accounts?$top=10'

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


def checkOSSRecsPastDate(timeStamp, ossRecordings):
    # Goal of this function is to check whether there are any recordings that have been scheduled greater than a certain timeframe
    count = 0
    try:
        recordingLength = len(ossRecordings)
    except:
        return
        pass

    for eachOSS in ossRecordings:
        ossTimeStamp = eachOSS['Time']
        if timeDelta(timeStamp, ossTimeStamp) > 0:
            count += 1
    if count > 0:
        print("This account has " + str(recordingLength) + " but has recordings that are not past the 18th")

        return


def main():
    testResults = []
    file_scriptOutput = open("C://Users//Me//Downloads//recordingsaudit_date_bucket.txt",'a')
    envs = ['proda']

    for env in envs:

        if env == 'proda':
            DVRVersion = "S96"
        elif env == 'prodb':
            DVRVersion = "S108"
        elif env == 'prodc':
            DVRVersion = "S116"

        print("Running test cases for", env)

        _feature_group = "NAPA_TRIAL"

        accountsInFeatureGroup = getAccounts_FeatureGroup(_feature_group, env)

        featureGroupLen = len(accountsInFeatureGroup)

        for eachAccount in accountsInFeatureGroup:

            #try:
            OSSRecs = mf_getRecordings('OSS', eachAccount, env, DVRVersion,file_scriptOutput)
            #except:
                #print("Empty OSS")


main()  # Return the Test Results