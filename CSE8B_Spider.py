#https://docs.google.com/spreadsheets/u/0/d/1VUBQIkxmuH_q_FRB_lry7Y-WyGSJ3wLj-BfMQA4slh0/htmlembed/sheet?headers=false&gid=0
#(([abcdefghijklmnopqrstuvwxyz, ])*)

import re
import urllib2
import datetime
import uuid
import requests
from firebase import firebase

firebase = firebase.FirebaseApplication('https://dopeaf1-f4532.firebaseio.com/',None)

def read_task_info_CSE8B(x):

    url = 'https://docs.google.com/spreadsheets/u/0/d/1VUBQIkxmuH_q_FRB_lry7Y-WyGSJ3wLj-BfMQA4slh0/htmlembed/sheet?headers=false&gid=0'
    request = urllib2.Request(url)

    response = urllib2.urlopen(request)

    data=response.read().replace('\n',"")    

    #Ten Weeks Task in total

    task_Regex = re.compile(r'<tbody>.*</tbody>')

    all_Task_Table = re.findall(task_Regex,data)

    task_Spliter = re.compile(r'<tr.*?</tr>')

    lines = re.findall(task_Spliter,all_Task_Table[0])

    regex_spilt_Single_Line = re.compile(r'<td.*?</td>')
    regex_extractContents = re.compile(r'>.*[^</td>]')


    for index in range(2,len(lines)):


        #5td is task name #6 is due day

        single_Lines = re.findall(regex_spilt_Single_Line,lines[index])

        num_of_slots = len(single_Lines)

        if(num_of_slots >= 8):
            if(num_of_slots >= 9):

                Week = re.findall(regex_extractContents, single_Lines[0])[0][1:]

            Date = re.findall(regex_extractContents,single_Lines[num_of_slots - 8])[0][1:]

            RA = re.findall(regex_extractContents,single_Lines[num_of_slots - 4])

            RQ = re.findall(regex_extractContents,single_Lines[num_of_slots - 3])

            PSA = re.findall(regex_extractContents,single_Lines[num_of_slots - 2])

            Stepik = re.findall(regex_extractContents,single_Lines[num_of_slots - 1])

            if(Date != "Date"):

                if(len(RA) > 0):

                    RA = RA[0][1:]

                    if(RA != "No reading") :

                        print("Due Date: Week", Week, Date)

                        print("Reading Assignment:", RA)

                        print("\n")

                        putDataToFirebase(Date, 'Reading Assignment', RA)

                if(len(RQ) > 0):

                    RQ = RQ[0][1:]

                    if(RQ[:2] != "No"):

                        if(RQ[:2] == "RQ" or RQ[:2] == "Vi"):

                            print("Due Date: Week", Week, Date, "9AM")

                            print("Reading Quiz:", RQ)

                            print("\n")

                            putDataToFirebase(Date, 'Reading Quiz', RQ)

                        else:

                            RQ = re.findall(re.compile(r'>.*[^</a]'), RQ)[0][1:]

                            print("Due Date: Week", Week, Date, "9AM")

                            print("Reading Quiz:", RQ)

                            print("\n")

                            putDataToFirebase(Date, 'Reading Quiz', RQ)

                if(len(PSA) > 0):

                    PSA = PSA[0][1:]

                    if(PSA[5:] == "due") :

                        print("Due Date: Week", Week, Date)

                        print("PSA:", PSA)

                        print("\n")

                        putDataToFirebase(Date, 'PSA', PSA)

                if(len(Stepik) > 0):

                    Stepik = re.findall(re.compile(r'>.*[^</a]'), Stepik[0][1:])[0][1:]

                    if(Stepik[0] != "<"):

                        print("Due Date: Week", Week, Date)

                        print("Stepik:", Stepik)

                        print("\n")

                        putDataToFirebase(Date, 'Stepik', Stepik)


                    else:

                        Stepik = re.findall(re.compile(r'>.*[^</a></div]'), Stepik)[0][1:]

                        print("Due Date: Week", Week, Date)

                        print("Stepik:", Stepik)

                        print("\n")

                        putDataToFirebase(Date, 'Stepik', Stepik)

def putDataToFirebase(date, taskName, detail):
    #'Thu, Mar 16'
    finalDate = ''

    if 'Jan' in date:
        date.replace('Jan ','')
        dayString = date[len(date)-2:len(date)]
        dayVal = int(date[len(date)-2:len(date)])
        if dayVal < 10:
            dayString = '0'+date[len(date)-1:len(date)]
        finalDate = '01/'+dayString+'/2017 09:00'
    if 'Feb' in date:
        date.replace('Feb ','')
        dayString = date[len(date)-2:len(date)]
        dayVal = int(date[len(date)-2:len(date)])
        if dayVal < 10:
            dayString = '0'+date[len(date)-1:len(date)]
        finalDate = '02/'+dayString+'/2017 09:00'
    if 'Mar' in date:
        date.replace('Mar ','')
        dayString = date[len(date)-2:len(date)]
        dayVal = int(date[len(date)-2:len(date)])
        if dayVal < 10:
            dayString = '0'+date[len(date)-1:len(date)]
        finalDate = '03/'+dayString+'/2017 09:00'

    UUID_Gen = uuid.uuid3(uuid.NAMESPACE_DNS, detail)

    postToVerifiedTaskList = firebase.put('','/verified_Tasks/CSE8B/'+str(UUID_Gen),
            {
                'courseID':'CSE8B',
                'taskName':taskName,
                'taskDescription':detail,
                'dueDate':finalDate,
                'priority':5,
                'taskID':str(UUID_Gen),
                'verified':True
            })
    postToVerifiedTaskList = firebase.put('','/tasks/'+str(UUID_Gen),
            {
                'courseID':'CSE8B',
                'taskName':taskName,
                'taskDescription':detail,
                'dueDate':finalDate,
                'priority':5,
                'taskID':str(UUID_Gen),
                'verified':True
            })





read_task_info_CSE8B(1)

