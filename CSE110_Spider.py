#http://ieng6.ucsd.edu/~cs110x/static/logistics_a00/
#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
import datetime
import uuid
import requests
from firebase import firebase

firebase = firebase.FirebaseApplication('https://dopeaf1-f4532.firebaseio.com/',None)

def read_task_info_CSE110(x):

	r = requests.get('http://ieng6.ucsd.edu/~cs110x/static/logistics_a00/', allow_redirects=True)
	data=r.text.encode('utf-8').replace('\n',"")

	task_num_counter = 0

	now = datetime.datetime.now()

	#Ten Weeks Task in total
	task_Regex = re.compile(r'<table>.*</table>')
	all_Task_Table = re.findall(task_Regex,data)
	task_Spliter = re.compile(r'<tr>.*?</tr>')
	spilitted_Tasks = re.findall(task_Spliter,all_Task_Table[0])
	regex_getOff = re.compile(r'[^td<>].*[^</td>]')


	for index in range(1,len(spilitted_Tasks)):

		#5td is task name #6 is due day
		regex_spilt_Single_Line = re.compile(r'<td>.*?</td>')
		single_Lines = re.findall(regex_spilt_Single_Line,spilitted_Tasks[index])
		spilitted_Tasks_Name = re.findall(regex_getOff,single_Lines[4])

		task_in_one = spilitted_Tasks_Name[0]

		spilitted_Tasks_Due = re.findall(regex_getOff,single_Lines[5])

		print("Task:")
		print(task_in_one)
		print("")
		print("Due at ")
		print(spilitted_Tasks_Due[0])
		print("\n")

		if(task_in_one == None):
			continue

		if(spilitted_Tasks_Due[0] == 'None'):
			continue

		day_regex = re.compile(r'\d+')
		day = re.findall(day_regex,spilitted_Tasks_Due[0])[0]

		month_regex_1 = re.compile(r'/\d+')
		month_regex_1_val = re.findall(month_regex_1,spilitted_Tasks_Due[0])[0]
		month_regex_2 = re.compile(r'\d+')
		month_regex_2_val = re.findall(month_regex_2,month_regex_1_val)[0] 

		dayString = day
		if int(day) < 10:
			dayString = '0'+dayString

		monthString = month_regex_2_val
		if int(month_regex_2_val) < 10:
			monthString = '0'+monthString

		
		UUID_Gen = uuid.uuid3(uuid.NAMESPACE_DNS, task_in_one)

		postToVerifiedTaskList = firebase.put('','/verified_Tasks/CSE110/'+str(UUID_Gen),
				{
					'courseID':'CSE110',
					'taskName':task_in_one,
					'taskDescription':'Task from course schedule',
					'dueDate':dayString+"/"+monthString+"/"+str(now.year)+' 09:00',
					'taskID':str(UUID_Gen),
					'priority':5,
					'verified':True
				})
		postToVerifiedTaskList = firebase.put('','/tasks/'+str(UUID_Gen),
			{
				'courseID':'CSE110',
					'taskName':task_in_one,
					'taskDescription':'Task from course schedule',
					'dueDate':dayString+"/"+monthString+"/"+str(now.year)+' 09:00',
					'taskID':str(UUID_Gen),
					'priority':5,
					'verified':True
			})

read_task_info_CSE110(1)


