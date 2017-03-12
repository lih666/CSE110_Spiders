#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
import urllib2
import sys  


def read_task_info_CSE100(x):

    reload(sys)  
    sys.setdefaultencoding('utf8')


    url = 'https://sites.google.com/a/eng.ucsd.edu/cse-100-winter-2017/schedule-and-assignments'
    request = urllib2.Request(url)

    response = urllib2.urlopen(request)



    data=response.read().replace('\n',"")

    data = data.replace('\xa0',' ')
    data = data.replace('\xc2','')

    #Ten Weeks Task in total
    task_Regex = re.compile(r'<tbody>.*</tbody>')
    all_Task_Table = re.findall(task_Regex,data)
    table = re.findall(task_Regex, all_Task_Table[0])
    task_Spliter = re.compile(r'<tr.*?</tr>')
    lines = re.findall(task_Spliter,all_Task_Table[0])
    regex_spilt_Single_Line = re.compile(r'<td.*?</td>')
    regex_extractContents1 = re.compile(r'>.*[^</td>]')
    regex_extractContents2 = re.compile(r'>.*?<br')
    regex_extractContents3 = re.compile(r'>.*[^</span]')
    regex_extractContents4 = re.compile(r'>.*[^</a]')
    regex_extractContents5 = re.compile(r'<.*?>')
    for index in range(2,len(lines)):

        single_Lines = re.findall(regex_spilt_Single_Line,lines[index])
        num_of_slots = len(single_Lines)
        if(num_of_slots >= 4):
            date = re.findall(regex_extractContents1, single_Lines[0])[0][1:]
            if(date[0] != "<" and date[1] != "<"):
                date = date[:9]
                date = date[1:]
                if(date[-1] == "<"):
                    date = date[:-1]

                reading = re.findall(regex_extractContents1, single_Lines[2])[0]
                if(reading.find("br") == -1) and (len(set(reading)) > 5):
                    while (re.compile('<').search(reading)):
                        reading = re.sub(re.compile('<'), "", reading)
                    while (re.compile('>').search(reading)):
                        reading = re.sub(re.compile('>'), "", reading)
                    print("Date:", date)
                    print("Reading:", reading)
                    print("\n")
                else:
                    reading = re.findall(regex_extractContents2, reading)
                    for i in range(len(reading)):
                        temp = reading[i][1:][:-3]
                        if(temp.find("No") == -1):
                            while (regex_extractContents5.search(temp)):
                                temp = re.sub(regex_extractContents5, "", temp)
                            while (re.compile('<').search(temp)):
                                temp = re.sub(re.compile('<'), "", temp)
                            while (re.compile('>').search(temp)):
                                temp = re.sub(re.compile('>'), "", temp)
                            if len(set(temp)) > 5:
                                print("Date:", date)
                                print("Reading:", temp)
                                print("\n")

                pa = re.findall(regex_extractContents1, single_Lines[3])[0][1:][:-3]
                if len(set(pa)) > 10:
                    pa = re.findall(regex_extractContents4, pa)[0]
                    while (re.compile('<').search(pa)):
                        pa = re.sub(re.compile('<'), "", pa)
                    while (re.compile('>').search(pa)):
                        pa = re.sub(re.compile('>'), "", pa)
                    while (re.compile('/s').search(pa)):
                        pa = re.sub(re.compile('/s'), "", pa)
                    while (re.compile('/a').search(pa)):
                        pa = re.sub(re.compile('/a'), "", pa)
                    if len(set(pa)) > 2:
                        print("Date:", date)
                        print("PA:", pa)
                        print("\n")

read_task_info_CSE100(1)
