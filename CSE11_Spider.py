# https://cseweb.ucsd.edu/~ricko/CSE11/calendar.html

#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
def read_task_info_CSE11(x):
    data=(open("CSE 11 Calendar.htm",'r').read()).replace('\n',"")

    #Ten Weeks Task in total
    task_Regex = re.compile(r'<table.*</table>')
    all_Task_Table = re.findall(task_Regex,data)
    task_Spliter = re.compile(r'<td.*?</td>')
    cells = re.findall(task_Spliter,all_Task_Table[0])
    event_extractor = re.compile(r'<font.*?</font>')
    regex_extractContents = re.compile(r'<.*?>')
    date_extractor = re.compile(r'<b>.*?<br>')

    month = "September"
    date = ""
    countPA = 1

    for i in range(len(cells)):
        cell = cells[i]
        #print(cell, "\n=====================================================\n\n")
        if cell.find("October") != -1:
            month = "October"
        elif cell.find("November") != -1:
            month = "November"
        elif cell.find("December") !=-1:
            month = "December"

        events = re.findall(event_extractor, cell)
        for j in range(len(events)):
            event = events[j]

            while (regex_extractContents.search(event)):
                event = re.sub(regex_extractContents, "", event)
            if(event != "October" and event != "November" and event != "December" and event != "September" and event != "Holiday"):
                date = re.findall(date_extractor, cell)[0]
                while (event_extractor.search(date)):
                    date = re.sub(event_extractor, "", date)
                while (regex_extractContents.search(date)):
                    date = re.sub(regex_extractContents, "", date)
                if date == " 1":
                    date = "1"
                if(event == "PA due"):
                    event = "PA"+str(countPA)+" due"
                    countPA += 1
                print(month, date, event)

        #print(month, date)


read_task_info_CSE11(1)