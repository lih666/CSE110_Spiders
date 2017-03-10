# http://ieng9.ucsd.edu/~cs30x/calendar.html

#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
def read_task_info_CSE30(x):
    data=(open("CSE30.html",'r').read()).replace('\n',"")

    #Ten Weeks Task in total
    task_Regex = re.compile(r'<table.*</table>')
    all_Task_Table = re.findall(task_Regex,data)
    task_Spliter = re.compile(r'<td.*?</td>')
    cells = re.findall(task_Spliter,all_Task_Table[0])
    event_extractor = re.compile(r'<font.*?</font>')
    regex_extractContents = re.compile(r'<.*?>')
    date_extractor = re.compile(r'<b>.*?<br>')

    month = "January"
    date = ""

    for i in range(len(cells)):
        cell = cells[i]
        #print(cell, "\n=====================================================\n\n")
        if cell.find("February") != -1:
            month = "February"
        elif cell.find("March") != -1:
            month = "March"

        events = re.findall(event_extractor, cell)
        for j in range(len(events)):
            event = events[j]

            while (regex_extractContents.search(event)):
                event = re.sub(regex_extractContents, "", event)
            if(event != "January" and event != "February" and event != "March" and event != "Holiday"):
                date = re.findall(date_extractor, cell)[0]
                while (event_extractor.search(date)):
                    date = re.sub(event_extractor, "", date)
                while (regex_extractContents.search(date)):
                    date = re.sub(regex_extractContents, "", date)
                if date == " 1":
                    date = "1"
                print(month, date, event)

        #print(month, date)


read_task_info_CSE30(1)
