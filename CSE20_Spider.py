#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
import datetime
def read_task_info_CSE20(x):


	data=(open("CSE20.html",'r').read()).replace('\n',"")

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


read_task_info_CSE20(1)

