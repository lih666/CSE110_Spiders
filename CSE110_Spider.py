#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
def read_task_info_CSE110(x):


	data=(open("CSE110.html",'r').read()).replace('\n',"")

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

read_task_info_CSE110(1)


