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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import mobileanalytics
from django.utils import simplejson
from google.appengine.api.labs import taskqueue

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

class QueueRecordAnalytics(webapp.RequestHandler):
	def post(self):
		device_id = self.request.get("device_id")
		os = self.request.get("os")
		os_ver = self.request.get("os_ver")
		app_ver = self.request.get("app_ver")
		device_model = self.request.get("device_model")
		manufacturer = self.request.get("manufacturer")
		telco = self.request.get("telco")
		t = self.request.get("t")
		s = self.request.get("s")
		
		analytics = mobileanalytics.RecordAnalytics(device_id, os, os_ver, app_ver, time=t, secret_key=s)
		analytics.onApplicationStarted(device_model, manufacturer, telco=telco)

class RecordAnalytics(webapp.RequestHandler):
	def get(self):
		display = mobileanalytics.DisplayAnalytics()
		
		#data = display.showAccessRecord()
		#self.response.out.write(data + "<br>")
		
		#data = display.showMobileDevices()
		#self.response.out.write(data + "<br>")
		
		data = display.showDailyNewUsers()
		self.response.out.write("<br><br><b>total number of new users daily</b><br><br>")
		self.response.out.write(data + "<br>")
		
		data = display.showTotalNewUsers()
		self.response.out.write("<br><br><b>total number of new users</b><br><br>")
		self.response.out.write(data + "<br>")
		
		data = display.showDailySessions()
		self.response.out.write("<br><br><b>total number of sessions daily</b><br><br>")
		self.response.out.write(data + "<br>")

		data = display.showDeviceModelDistribution()
		self.response.out.write("<br><br><br><b>Phone models</b><br><br>")
		self.response.out.write(data + "<br>")
		
		data = display.showDeviceManufacturerDistribution()
		self.response.out.write("<br><br><br><b>Manufacturers</b><br><br>")
		self.response.out.write(data + "<br>")
		
		data = display.showDeviceOSVersionDistribution()
		self.response.out.write("<br><br><br><b>OS Versions</b><br><br>")
		self.response.out.write(data + "<br>")
		
	def post(self):
		device_id = self.request.get("device_id")
		if device_id:
			os = self.request.get("os")
			os_ver = self.request.get("os_ver")
			app_ver = self.request.get("app_ver")
			device_model = self.request.get("device_model")
			manufacturer = self.request.get("manufacturer")
			telco = self.request.get("telco")
			t = self.request.get("t")
			s = self.request.get("s")
			
			analytics = mobileanalytics.RecordAnalytics(device_id, os, os_ver, app_ver, time=t, secret_key=s)
			if analytics.allowLogging:
				taskqueue.add(url=mobileanalytics.config.record_queue_path, params={'device_id': device_id, 'os':os, 'os_ver':os_ver, 'app_ver':app_ver, 'device_model':device_model, 'manufacturer':manufacturer, 'telco':telco, 't':t, 's':s})	

class QueueRecordAnalyticsDiscreetEvent(webapp.RequestHandler):
	def post(self):
		device_id = self.request.get("device_id")
		os = self.request.get("os")
		os_ver = self.request.get("os_ver")
		app_ver = self.request.get("app_ver")
		event = self.request.get("event")
		parameters = self.request.get("parameters")
		t = self.request.get("t")
		s = self.request.get("s")
		obj = simplejson.loads(parameters)
		
		analytics = mobileanalytics.RecordAnalytics(device_id, os, os_ver, app_ver, time=t, secret_key=s)
		analytics.recordEvent(event, obj, 1)

class GetAnalyticsChartForNonDiscreetEvents(webapp.RequestHandler):
	def get(self):
		display = mobileanalytics.DisplayAnalytics()
		event_name = self.request.get("event_name")
		param_key = self.request.get("param_key")
		width = self.request.get("width")
		height = self.request.get("height")
		os_ver = self.request.get("os_ver")
		
		if os_ver=='':
			os_ver = None
		if width=='':
			width = None
		if height=='':
			height = None
		if self.request.get("x_size")=='':
			x_size = None
		else:
			x_size = float(self.request.get("x_size"))
		if param_key=='':
			param_key = None
		if self.request.get("min_x")=='':
			min_x = None
		else:
			min_x = float(self.request.get("min_x"))
		if self.request.get("max_x")=='':
			max_x = None
		else:
			max_x = float(self.request.get("max_x"))
		
		data = display.showNonDiscreetEvent(event_name, param_key, width, height, x_size, min_x, max_x, osVer=os_ver)
		self.response.out.write(data)

class GetAnalyticsChartForEvents(webapp.RequestHandler):
	def get(self):
		display = mobileanalytics.DisplayAnalytics()
		event_name = self.request.get("event_name")
		param_key = self.request.get("param_key")
		width = self.request.get("width")
		height = self.request.get("height")
		
		if width=='':
			width = None
		if height=='':
			height = None
		
		if event_name!='' and param_key!='':
			data = display.showEvents(eventName=event_name, paramKey=param_key, width=width, height=height)
			self.response.out.write(data)
		elif event_name!='' and param_key=='':
			data = display.showEvents(eventName=event_name, width=width, height=height)
			self.response.out.write(data)
		else:
			data = display.showEvents(width=width, height=height)
			self.response.out.write(data)

class RecordAnalyticsEvent(webapp.RequestHandler):
	def get(self):
		pass
		
	def post(self):
		device_id = self.request.get("device_id")
		if device_id:
			os = self.request.get("os")
			os_ver = self.request.get("os_ver")
			app_ver = self.request.get("app_ver")
			event = self.request.get("event")
			parameters = self.request.get("parameters")
			t = self.request.get("t")
			s = self.request.get("s")
			if self.request.get("is_discreet")=='':
				is_discreet = 1
			else:
				is_discreet = int(self.request.get("is_discreet"))
				
			analytics = mobileanalytics.RecordAnalytics(device_id, os, os_ver, app_ver, time=t, secret_key=s)
			if analytics.allowLogging:
				if is_discreet:
					taskqueue.add(url=mobileanalytics.config.record_event_queue_path, params={'device_id': device_id, 'os':os, 'os_ver':os_ver, 'app_ver':app_ver, 'event':event, 'parameters':parameters, 't':t, 's':s})
				else:
					taskqueue.add(url=mobileanalytics.config.record_event_queue_path + "/nondiscreet", params={'device_id': device_id, 'os':os, 'os_ver':os_ver, 'app_ver':app_ver, 'event':event, 'parameters':parameters, 't':t, 's':s})
					
class QueueRecordAnalyticsNonDiscreetEvent(webapp.RequestHandler):
	def post(self):
		device_id = self.request.get("device_id")
		os = self.request.get("os")
		os_ver = self.request.get("os_ver")
		app_ver = self.request.get("app_ver")
		event = self.request.get("event")
		parameters = self.request.get("parameters")
		t = self.request.get("t")
		s = self.request.get("s")
		obj = simplejson.loads(parameters)
		
		analytics = mobileanalytics.RecordAnalytics(device_id, os, os_ver, app_ver, time=t, secret_key=s)
		analytics.recordEvent(event, obj, 0)

class GetAnalyticsChart(webapp.RequestHandler):
	def get(self):
		data = self.request.get("data")
		width = self.request.get("width")
		height = self.request.get("height")
		
		if width=='':
			width = None
		if height=='':
			height = None
		
		chart_content = ""
		display = mobileanalytics.DisplayAnalytics()
		if data=='' or data=='new_users':
			chart_content = display.showDailyNewUsers(width=width, height=height)
		elif data=='sessions':
			chart_content = display.showDailySessions(width=width, height=height)
		elif data=='devices':
			chart_content = display.showDeviceModelDistribution(width=width, height=height)
		elif data=='total_users':
			chart_content = display.showTotalNewUsers(width=width, height=height)
		elif data=='os_ver':
			chart_content = display.showDeviceOSVersionDistribution(width=width, height=height)
		elif data=='manufacturers':
			chart_content = display.showDeviceManufacturerDistribution(width=width, height=height)
		self.response.out.write(chart_content)	
		
class DisplayAnalytics(webapp.RequestHandler):
	def get(self):
		
		data = self.request.get("data")
		
		menu_content = "<table width='100%'>"
		menu_content += "<tr height=35><td align='center' bgcolor='#00CCFF'><a href='/display?data=new_users'>new users</a></td></tr>"
		menu_content += "<tr height=35><td align='center' bgcolor='#CCC'><a href='/display?data=sessions'>sessions</a></td></tr>"
		menu_content += "<tr height=35><td align='center' bgcolor='#00CCFF'><a href='/display?data=devices'>devices</a></td></tr>"
		menu_content += "<tr height=35><td align='center' bgcolor='#CCC'><a href='/display?data=events'>events</a></td></tr>"
		menu_content += "</table>"
		
		chart_content = ""
		display = mobileanalytics.DisplayAnalytics()
		if data=='' or data=='new_users':
			chart_content = display.showDailySessions()
		elif data=='sessions':
			chart_content = display.showDailyNewUsers()
		elif data=='devices':
			chart_content = display.showDeviceModelDistribution()
		elif data=='events':
			pass
		
		table_content = "<table border=0 height=400>"
		table_content += "<tr><td width=130 valign='top'>%s</td><td width=650>%s</td></tr>" % (menu_content, chart_content)
		table_content += "</table>"
		
		self.response.out.write(table_content)	

class RunTest(webapp.RequestHandler):
	def get(self):
		self.response.out.write("Test")	

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
											( mobileanalytics.config.display_path, DisplayAnalytics),
											( mobileanalytics.config.chart_path, GetAnalyticsChart),
											( mobileanalytics.config.chart_event_path, GetAnalyticsChartForEvents),
											( mobileanalytics.config.chart_event_path + "/nondiscreet", GetAnalyticsChartForNonDiscreetEvents),
											( mobileanalytics.config.record_path, RecordAnalytics),
											( mobileanalytics.config.record_queue_path, QueueRecordAnalytics),
											( mobileanalytics.config.record_event_path, RecordAnalyticsEvent),
											( mobileanalytics.config.record_event_queue_path, QueueRecordAnalyticsDiscreetEvent),
											( mobileanalytics.config.record_event_queue_path + "/nondiscreet", QueueRecordAnalyticsNonDiscreetEvent)
											],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
