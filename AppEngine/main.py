#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import mobileanalytics
from django.utils import simplejson
from google.appengine.api.labs import taskqueue

class ClearEvents(webapp.RequestHandler):
	def get(self):
		display = mobileanalytics.DisplayAnalytics()
		count = display.clearEventsDatabase()
		self.response.out.write("<b>total events</b>: %s" % count)

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

class QueueRecordAnalyticsEvent(webapp.RequestHandler):
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
		analytics.recordEvent(event, obj)

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
		pass 
		#do not record events
		#device_id = self.request.get("device_id")
		#if device_id:
		#	os = self.request.get("os")
		#	os_ver = self.request.get("os_ver")
		#	app_ver = self.request.get("app_ver")
		#	event = self.request.get("event")
		#	parameters = self.request.get("parameters")
		#	t = self.request.get("t")
		#	s = self.request.get("s")
		#	
		#	analytics = mobileanalytics.RecordAnalytics(device_id, os, os_ver, app_ver, time=t, secret_key=s)
		#	if analytics.allowLogging:
		#		taskqueue.add(url=mobileanalytics.config.record_event_queue_path, params={'device_id': device_id, 'os':os, 'os_ver':os_ver, 'app_ver':app_ver, 'event':event, 'parameters':parameters, 't':t, 's':s})

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
			chart_content = display.showDailyNewUsers()
		elif data=='sessions':
			chart_content = display.showDailySessions()
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
											( '/admin/clear_events', ClearEvents),
											( mobileanalytics.config.display_path, DisplayAnalytics),
											( mobileanalytics.config.chart_path, GetAnalyticsChart),
											( mobileanalytics.config.chart_event_path, GetAnalyticsChartForEvents),
											( mobileanalytics.config.record_path, RecordAnalytics),
											( mobileanalytics.config.record_queue_path, QueueRecordAnalytics),
											( mobileanalytics.config.record_event_path, RecordAnalyticsEvent),
											( mobileanalytics.config.record_event_queue_path, QueueRecordAnalyticsEvent)
											],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()