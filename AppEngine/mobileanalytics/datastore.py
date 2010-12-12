#
#  Copyright (c) 2010 Muh Hon Cheng
#  Created by honcheng on 11/29/10.
#  
#  Permission is hereby granted, free of charge, to any person obtaining 
#  a copy of this software and associated documentation files (the 
#  "Software"), to deal in the Software without restriction, including 
#  without limitation the rights to use, copy, modify, merge, publish, 
#  distribute, sublicense, and/or sell copies of the Software, and to 
#  permit persons to whom the Software is furnished to do so, subject 
#  to the following conditions:
#  
#  The above copyright notice and this permission notice shall be 
#  included in all copies or substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT 
#  WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR 
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT 
#  SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
#  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
#  IN CONNECTION WITH THE SOFTWARE OR 
#  THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#  
#  @author 		Muh Hon Cheng <honcheng@gmail.com>
#  @copyright	2010	Muh Hon Cheng
#  @version     0.1
#  
#

from google.appengine.ext import db

#
# dependency tables
#

# this is registered everytime users start the app, but not updated if there is no changes
class MobileDevice(db.Model):
	device_id = db.StringProperty()
	device_model = db.StringProperty()
	os = db.StringProperty()
	os_ver = db.StringProperty()
	app_ver = db.StringProperty()
	manufacturer = db.StringProperty()
	telco = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	
# this record is kept for x number of days. records older than x number of days are then purged
# developer determine the x number of days they want to keep the record
class DailyMobileDeviceAccess(db.Model):
	total = db.IntegerProperty()
	device_id = db.StringProperty()
	date = db.DateProperty(auto_now_add=True)

#
# tables useful for analytics display
#
	
# this depends on MobileDevices. Check that the device_id does not already exist in MobileDevices before incrementing the total here
# for daily, weekly, and monthly display new users, by OS, by OS version
class DailyNewUsers(db.Model):
	total = db.IntegerProperty()
	date = db.DateProperty(auto_now_add=True)
	os = db.StringProperty()
	os_ver = db.StringProperty()
	app_ver = db.StringProperty()
	
# no dependency on table, just increment when users exit the app (with duration included)
# this is use for daily, weekly, and monthly display, by OS, by OS version
class DailySessions(db.Model):
	total = db.IntegerProperty()
	date = db.DateProperty(auto_now_add=True)
	os = db.StringProperty()
	os_ver = db.StringProperty()
	app_ver = db.StringProperty()
	duration = db.IntegerProperty()
	
# this depends on DailyMobileDeviceAccess. If record does not already exists in the record for that particular day, increment the total
# this is use for daily, weekly, and monthly display, by OS, by OS version
class DailyUniqueUsersSession(db.Model):
	total = db.IntegerProperty()
	date = db.DateProperty()
	os = db.StringProperty()
	os_ver = db.StringProperty()
	app_ver = db.StringProperty()
	
# this depends on DailyMobileDeviceAccess. 
# this table is updated with a cronjob every x hours determined by developers
# availability of this data depends on how long the DailyMobileDeviceAccess data is kept by developer	
class AccessFrequency(db.Model):
	total = db.IntegerProperty()
	days = db.IntegerProperty()
	os = db.StringProperty()
	os_ver = db.StringProperty()
	app_ver = db.StringProperty()

# no dependency on other table
# developer specify the event name, and the key-value pair associated with this
# there can be multiple key-value pairs for one event, and they can be sent in clusters and by itself
# clustered events are recorded separately without saving the relationship between different key-value of the same event name
# it is up to developer to specify relevant key-value pairs if they want to find relationship between different key-value in the same event
# average duration of event is saved in seconds, if required.
class Events(db.Model):
	event_name = db.StringProperty()
	param_key = db.StringProperty()
	param_value = db.StringProperty()
	total = db.IntegerProperty()
	date = db.DateProperty(auto_now_add=True)
	os = db.StringProperty()
	os_ver = db.StringProperty()
	app_ver = db.StringProperty()
	duration = db.IntegerProperty()
	

		
		
		