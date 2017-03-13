#http://cseweb.ucsd.edu/classes/wi17/cse20-ab/
#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
import datetime
import uuid
import requests
from firebase import firebase

firebase = firebase.FirebaseApplication('https://dopeaf1-f4532.firebaseio.com/',None)

def read_task_info_CSE20(x):

	r = requests.get('http://cseweb.ucsd.edu/classes/wi17/cse20-ab/', allow_redirects=True)
	data=r.text.encode('utf-8').replace('\n',"")

	task_num_counter = 0

	now = datetime.datetime.now()

	#Ten Weeks Task in total
	task_Regex = re.compile(r'<!-- HW -->.*?<br>')
	all_HW = re.findall(task_Regex,data)


	dueDay_regex = re.compile(r'\d+/\d+')
	taskName_regex = re.compile(r'[A-Z]+\s\d')


	for index in range(0,len(all_HW)):

	    #5td is task name #6 is due day
	    single_Due_Day = re.findall(dueDay_regex,all_HW[index])
	    single_task	   = re.findall(taskName_regex,all_HW[index])

	    print("Task:")
	    print(single_task[0])
	    print("")
	    print("Due at ")
	    print(single_Due_Day[0]+" "+str(now.year))
	    print("")

	    day_regex = re.compile(r'\d+')

		day = re.findall(day_regex,single_Due_Day[0])[0]

		month_regex_1 = re.compile(r'/\d+')
		month_regex_1_val = re.findall(month_regex_1,single_Due_Day[0])[0]
		month_regex_2 = re.compile(r'\d+')
		month_regex_2_val = re.findall(month_regex_2,month_regex_1_val)[0] 

	    dayString = day
		if int(day) < 10:
			dayString = '0'+dayString

		monthString = month_regex_2_val
		if int(month_regex_2_val) < 10:
			monthString = '0'+monthString

	    UUID_Gen = uuid.uuid3(uuid.NAMESPACE_DNS, single_task[0])
	    postToVerifiedTaskList = firebase.put('','/verified_Tasks/CSE20/'+str(UUID_Gen),
				{
					'courseID':'CSE20',
					'taskName':single_task[0],
					'taskDescription':'Task from course schedule',
					'dueDate':dayString+"/"+monthString+"/"+str(now.year)+' 12:00',
					'taskID':str(UUID_Gen),
					'priority':5,
					'verified':True
				})
	    postToVerifiedTaskList = firebase.put('','/tasks/'+str(UUID_Gen),
            {
                'courseID':'CSE20',
					'taskName':single_task[0],
					'taskDescription':'Task from course schedule',
					'dueDate':dayString+"/"+monthString+"/"+str(now.year)+' 12:00',
					'taskID':str(UUID_Gen),
					'priority':5,
					'verified':True
            })


read_task_info_CSE20(1)

