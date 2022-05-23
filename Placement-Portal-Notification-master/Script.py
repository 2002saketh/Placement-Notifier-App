from selenium import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
usr = "username" #Portal Login Username
pwd = "password" #Portal Login Password
import time
import datetime
from pyvirtualdisplay import Display
import selenium.webdriver.support.ui as ui
 
while True:
	display = Display(visible=0, size=(1024, 768))
	display.start()
	browser.implicitly_wait(30)
	#Load the driver
	driver = webdriver.Chrome(ChromeDriverManager().install())
	now = datetime.datetime.now()
	driver.get("Link to portal")
	 
	assert "Recruitment Automation System" in driver.title
	#Fill in Username and Password
	elem = driver.find_element_by_id("id_username")
	elem.send_keys(usr)
	elem = driver.find_element_by_id("id_password")
	elem.send_keys(pwd)
	elem.send_keys(Keys.RETURN)
	#Fetch the last date when the notification was seen
	f = open("lastDate.txt","r+")
	lastDate = str(f.read())
 
	#Get all available notifications
	allNotifications = driver.find_elements_by_class_name("panel-heading")
 
	#Get Dates and Time of all notifications
	allDates = driver.find_elements_by_class_name("col-sm-3")
	totalDates = len(allDates)
	newDate = allDates[0].text
	
	#Update the latest date in the file
	if(newDate != lastDate):
		f = open("lastDate.txt", "w+")
		f.write(str(newDate))
		f.close()
 
	sendEmail = False
	message = "Following are the unread notifications:\n\n"
	#Grab all notifications till lastDate != notification date
	for i in range(totalDates):
		if(str(allDates[i].text) == str(lastDate)):
			break
		sendEmail = True
		message += str(i+1) + ". "
		message += allNotifications[i].text
		message += "\n"
 
	#Send E-mail if any new notification is present
	if(sendEmail):
		import smtplib
		subject = '[Placment Portal] New Notification'
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.ehlo()
		s.starttls() 
		email = "email"
		s.login(email, "password")
		body = '\r\n'.join(['To: %s' % email,
	                    'From: %s' % email,
	                    'Subject: %s' % subject,
	                    '', message])
		s.sendmail(email, email, body.encode("utf-8")) 
		s.quit()
    browser.implicitly_wait(30)
	driver.close()
	display.stop()
	#Log last run time
	print ("Script last ran on: " + now.strftime("%Y-%m-%d %H:%M:%S"))
	time.sleep(5) 