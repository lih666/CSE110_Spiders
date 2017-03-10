#(([abcdefghijklmnopqrstuvwxyz, ])*)
import re
def read_task_info_CSE110(x):


    data=(open("CSE8B Schedule-Winter17.html",'r').read()).replace('\n',"")

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
                if(len(RQ) > 0):
                    RQ = RQ[0][1:]
                    if(RQ[:2] != "No"):
                        if(RQ[:2] == "RQ"):
                            print("Due Date: Week", Week, Date, "9AM")
                            print("Reading Quiz:", RQ)
                            print("\n")
                        else:
                            print("Due Date: Week", Week, Date, "9AM")
                            print("Reading Quiz:", re.findall(re.compile(r'>.*[^</a]'), RQ)[0][1:])
                            print("\n")
                if(len(PSA) > 0):
                    PSA = PSA[0][1:]
                    if(PSA[5:] == "due") :
                        print("Due Date: Week", Week, Date)
                        print("PSA:", PSA)
                        print("\n")
                if(len(Stepik) > 0):
                    Stepik = re.findall(re.compile(r'>.*[^</a]'), Stepik[0][1:])[0][1:]
                    if(Stepik[0] != "<"):
                        print("Due Date: Week", Week, Date)
                        print("Stepik:", Stepik)
                        print("\n")
                    else:
                        Stepik = re.findall(re.compile(r'>.*[^</a></div]'), Stepik)[0][1:]
                        print("Due Date: Week", Week, Date)
                        print("Stepik:", Stepik)
                        print("\n")



read_task_info_CSE110(1)
