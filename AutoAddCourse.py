import mechanize,sys
import urllib,urllib2
import re
from firebase import firebase

firebase = firebase.FirebaseApplication('https://dopeaf1-f4532.firebaseio.com/',None)
stdout_1 = sys.stdout


def check_valid_uid(uid):
	getUser = firebase.get('/users/'+uid,None)

	if(getUser != None):
		return True
	else:
		print(getUser)
		print('Sorry, the UID you provided is not correct. Please try again.')
		return False



def check_no_dup_user(courseID,uid):
	getResult = firebase.get('/classes/'+courseID,None)

	if(getResult == None):
		firebase.put('','/classes/'+courseID,{
			"courseID":"CSE105",
			"numTasks":0,
			"quarter":"WI17",
			"courseName":courseID
			})

	getResult = firebase.get('/classes/'+courseID+'/users/'+uid,None)

	if(getResult != None):
			for index in range(0,len(getResult)):
				if(getResult[index] == uid):
					print('The user has already enrolled in '+courseID)
					return False

			print('The use does not have course '+courseID)
			return True

	return True


def check_user_no_dup_course(courseID, uid):

	if(check_valid_uid(uid)):
		#getResult = firebase.get('/users/'+uid+'/enrolledCourses'+courseID)
		getResult = firebase.get('/users/'+uid+'/enrolledCourses',None)

		#Check repeat iteratively
		if(getResult != None):
			userCourseList = getResult
			for index in range(0,len(getResult)):
				if(getResult[index] == courseID):
					print('The user has already enrolled in '+courseID)
					return False

			print('The use does not have course '+courseID)
			return True

		print('Ahhh, the user is null')
		return True



def update_course_for_user(courseID, uid):

	if(check_valid_uid(uid)):

		if( check_user_no_dup_course(courseID,uid) ):
			print('haha1')
			userCourseList = firebase.get('/users/'+uid+'/enrolledCourses',None)
			length = '0'
			if(userCourseList != None):
				length = str(len(userCourseList))
			firebase.put('','/users/'+uid+'/enrolledCourses/'+length,courseID)

		if(check_no_dup_user(courseID, uid) ):
			print('haha2')
			courseUserList = firebase.get('/classes/'+courseID+'/users/'+uid,None)
			length = '0'
			if(courseUserList != None):
				length = str(len(courseUserList))
			firebase.put('','/classes/'+courseID+'/users/'+length,uid)


def log_to_file(filename):
	sys.stdout = open(filename,'w')

def log_to_stdout():
	sys.stdout = stdout_1

def login(username, password):
	while True:
		log_to_file(username+'Log.txt')

		#cookie
		cj = mechanize.CookieJar()

		#Browser
		br = mechanize.Browser()

		#options
		br.set_handle_equiv(True)
		#br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)

		#Follows refresh 0 but not hangs on refresh > 0
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		#debugging?
		br.set_debug_http(True)
		br.set_debug_redirects(True)
		br.set_debug_responses(True)

		#User-Agent (this is cheating, ok?)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36')]

		#cookie start
		br.set_cookiejar(cj)
		br.open("https://act.ucsd.edu/studentEnrolledClasses/enrolledclasses")

		#chose from the first form
		br.select_form(nr=0)

		#fill in the username, password in the website and sesnd 
		br.form['urn:mace:ucsd.edu:sso:username'] = username
		br.form['urn:mace:ucsd.edu:sso:password'] = password
		
		#submit the form and login
		br.submit()

		#print the response from the server side
		br_response = br.response().read()
		# print br_response
		if br_response.find("SAMLResponse") != -1:
			break
		else:
			log_to_stdout()
			print "The password is incorrect. Please retype your password."
			username = raw_input("Please enter username:")
			password = raw_input("Please enter password:")
	
	#Login, jump, choose form, jump , print
	br.select_form(nr=0)
	br.submit()
	br_response = br.response().read()
	#print br_response

	#save
	f = open("%s.html"%username,"w")
	f.writelines(br_response)
	f.close()
	log_to_stdout()
	read_course_info(username+'.html');

def read_course_info(x):

	data=(open(x,'r').read()).replace('\n',"")

	#Student name
	nameP = re.compile(r'<span>Student:</span>.*?</span>')
	nameSearch = re.findall(nameP,data)
	nameFilt = re.compile(r'<span>[\w,\.\s]*?</span>')
	nameOffArr = re.findall(nameFilt,nameSearch[0])
	nameFinalFilt = re.compile(r'[A-Z][^><]*')
	nameResult = re.findall(nameFinalFilt,nameOffArr[0])


	#Welcome Info
	print("Hello, "+nameResult[0]+"\n\n")
	print("Here are your courses and professor names\n\n")

	#result would be pieces of courses html strings
	pattern1 = re.compile(r'<tr align="left"><td>.*?</tr>')
	results = re.findall(pattern1,data)

	#course subject pattern
	subjectP = re.compile(r'<td>\w{3,4}</td>')
	subSUBP = re.compile(r'[A-Z]{3,4}')

	#course number pattern
	courseP = re.compile(r'>[0-9]{1,4}[A-Z]?</a>')
	subCourseP = re.compile(r'[0-9]{1,4}[A-Z]?')

	#professor
	profPwithMail = re.compile(r'<font color="red">(Letter|Pass Not Pass)</font></td><td><nobr><a class="sl_table_header_link" href=".*?</a>')
	subProfwithmail = re.compile(r'edu">.*</a')
	takeoffArr = re.compile(r'>.*</a?')
	takeoffArr2 = re.compile(r'td>[A-Z].*</td>')
	finalProf = re.compile(r'[^>].*[^</atd]')
	finalProf2 = re.compile(r'[A-Z][\w\s,.]*[^<]')

	if results:
		for index in range(0,len(results)):
			val = results[index]
			val1 = results[index]
			val2 = results[index]

			subj = re.findall(subjectP,val)
			course = re.findall(courseP,val1)
			profandPNP = re.search(r'<font color="red">(Letter|Pass/No Pass)</font></td><td><nobr><a class="sl_table_header_link" href=".*?</a>',val2)

			#Special case where the prof does not have
			#school mail updated on website
			if profandPNP is None:
				profandPNP = re.search(r'<font color="red">(Letter|Pass/No Pass)</font></td><td>.*?&nbsp?',val2)
				profandOffArr = re.search(takeoffArr2,profandPNP.group())
				profFinal = re.search(finalProf2,profandOffArr.group())


				subjStr = re.findall(subSUBP,subj[0])[0]
				courseStr = re.findall(subCourseP,course[0])[0]
				profStr = re.findall(finalProf,profFinal.group())[0]
				print(subjStr+"\t"+courseStr+"\t"+profStr)
				print('Now Update '+subjStr+courseStr)
				update_course_for_user(subjStr+courseStr,uid)
				continue


			subjStr = re.findall(subSUBP,subj[0])[0]
			courseStr = re.findall(subCourseP,course[0])[0]
			profStr = re.findall(finalProf,re.findall(takeoffArr,re.findall(subProfwithmail,profandPNP.group())[0])[0])[0]

			print(subjStr+"\t"+courseStr+"\t"+profStr)
			print('Now Update '+subjStr+courseStr)
			update_course_for_user(subjStr+courseStr,uid)

	else:
		print 'not match'

		print("\n\n\n\n")

	print("\n\n\n\n")
	return
	

if __name__ == '__main__':
	uid = raw_input("Please paste the UID in mail:")
	username = raw_input("Please enter username:")
	password = raw_input("Please enter password:")

	userCourseList = []
	courseUserList = []
	login(username,password)