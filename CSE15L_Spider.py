#http://ieng6.ucsd.edu/~cs15x/calendar.html

#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
import urllib2
import datetime
import uuid
import requests
from firebase import firebase

firebase = firebase.FirebaseApplication('https://dopeaf1-f4532.firebaseio.com/',None)

def read_task_info_CSE15L(x):
    url = 'http://ieng6.ucsd.edu/~cs15x/calendar.html'
    request = urllib2.Request(url)

    response = urllib2.urlopen(request)

    data=response.read().replace('\n',"")  

    regex_extractContents = re.compile(r'<.*?>')

    #Ten Weeks Task in total
    task_Regex = re.compile(r'<p>.*?</p>')
    ps = re.findall(task_Regex,data)

    for i in range(len(ps)):
        p = ps[i]
        if p.find("Midterm") != -1:
            while (regex_extractContents.search(p)):
                p = re.sub(regex_extractContents, "", p)
            print(p)
        elif p.find("Final") != -1:
            while (regex_extractContents.search(p)):
                p = re.sub(regex_extractContents, "", p)
            print(p)

    UUID_Gen = uuid.uuid3(uuid.NAMESPACE_DNS, "CSE15Lmidterm")

    postToVerifiedTaskList = firebase.put('','/verified_Tasks/CSE15L/'+str(UUID_Gen),
    {
        'courseID':'CSE15L',
        'taskName':'Midterm',
        'taskDescription':"In Class Midterm",
        'dueDate':"22/02/2017 15:00",
        'priority':5,
        'taskID':str(UUID_Gen),
        'verified':True
    })
    postToVerifiedTaskList = firebase.put('','/tasks/'+str(UUID_Gen),
    {
        'courseID':'CSE15L',
        'taskName':'Midterm',
        'taskDescription':"In Class Midterm",
        'dueDate':"22/02/2017 15:00",
        'priority':5,
        'taskID':str(UUID_Gen),
        'verified':True
    })


    UUID_Gen = uuid.uuid3(uuid.NAMESPACE_DNS, "CSE15Lfinal")

    postToVerifiedTaskList = firebase.put('','/verified_Tasks/CSE15L/'+str(UUID_Gen),
    {
        'courseID':'CSE15L',
        'taskName':'Final',
        'taskDescription':"A00 Final: Mon,  March 20th, 2017, 3:00pm-5:00pm\nB00 Final: Wed,  March 22nd, 2017, 3:00pm-5:00pm\nC00 Final: Fri,  March 24th, 2017, 3:00pm-5:00pm",
        'dueDate':'24/03/2017 15:00',
        'priority':5,
        'taskID':str(UUID_Gen),
        'verified':True
    })
    postToVerifiedTaskList = firebase.put('','/tasks/'+str(UUID_Gen),
    {
        'courseID':'CSE15L',
        'taskName':'Final',
        'taskDescription':"A00 Final: Mon,  March 20th, 2017, 3:00pm-5:00pm\nB00 Final: Wed,  March 22nd, 2017, 3:00pm-5:00pm\nC00 Final: Fri,  March 24th, 2017, 3:00pm-5:00pm",
        'dueDate':'24/03/2017 15:00',
        'priority':5,
        'taskID':str(UUID_Gen),
        'verified':True
    })






read_task_info_CSE15L(1)

