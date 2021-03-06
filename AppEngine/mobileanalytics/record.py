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

from datastore import MobileDevice
from datastore import DailyMobileDeviceAccess
from datastore import DailyNewUsers
from datastore import DailySessions
from datastore import DailyUniqueUsersSession
from datastore import Events
from datastore import NonDiscreetEvents
from google.appengine.ext import db
from django.utils import simplejson
import datetime
from datetime import date
from datetime import timedelta
import config
import hashlib
import logging

chart_colors = ['FF0000','3072F3','0a8f00','d97b00','c700d9','00d9a3','2f2f2f','0000ff','2aff00','ff00c6','6d6d6d','6d6d6d','6d6d6d','6d6d6d','6d6d6d']

class DisplayAnalytics(object):
	def __init__(self):
		pass

	def clearEventsDatabase(self):
		query = Events.all()
		events = query.fetch(1000)
		db.delete(events)
		query = Events.all()
		logging.info('step 1')
		while query.count(1000)>0:
			events = query.fetch(1000)
			db.delete(events)
			logging.info('loop')
			query = Events.all()
		return query.count(1000)

	def showDeviceOSVersionDistribution(self, width=None, height=None):
		devices = db.GqlQuery("SELECT * FROM MobileDevice")
		os_vers = {}
		for device in devices:
			if device.os_ver not in os_vers.keys():
				os_vers[device.os_ver] = 1
			else:
				os_vers[device.os_ver] = os_vers[device.os_ver] + 1
		all_data = "<br><br><br><b>OS Versions</b><br><br>"
		
		chart_api_url = 'http://chart.apis.google.com/chart'
		chd = ""
		chl = ""
		chco = ""
		data = "<table>"
		data += "<tr><td>OS Versions</td><td>total</td></tr>" 
		color_index = 0
		for os_ver in os_vers.keys():
			data += "<tr><td>%s</td><td>%s</td></tr>" % (os_ver, os_vers[os_ver])
			chl += "%s [%s]|" % (os_ver, os_vers[os_ver])
			chd += "%s," % os_vers[os_ver]
			if (color_index>len(chart_colors)-1):
				color_index = 0
			chco += "%s|" % chart_colors[color_index]
			color_index += 1
		data += "</table>"
		
		if len(os_vers.keys())==0:
			return "no data yet"

		if width==None:
			width = 800
		if height==None:
			height = 300

		chart_data = "<img src='%s?chs=%sx%s&chd=t:%s&chl=%s&cht=p'/>" % (chart_api_url, width, height, chd[:-1], chl[:-1])
		#all_data += "<br>%s" % chart_data
	
		return chart_data
	
	def showDeviceManufacturerDistribution(self, width=None, height=None):
		devices = db.GqlQuery("SELECT * FROM MobileDevice")
		manufacturers = {}
		for device in devices:
			if device.manufacturer not in manufacturers.keys():
				manufacturers[device.manufacturer] = 1
			else:
				manufacturers[device.manufacturer] = manufacturers[device.manufacturer] + 1
		all_data = "<br><br><br><b>Manufacturers</b><br><br>"
		
		chart_api_url = 'http://chart.apis.google.com/chart'
		chd = ""
		chl = ""
		chco = ""
		data = "<table>"
		data += "<tr><td>manufacturers</td><td>total</td></tr>" 
		color_index = 0
		for manufacturer in manufacturers.keys():
			data += "<tr><td>%s</td><td>%s</td></tr>" % (manufacturer, manufacturers[manufacturer])
			chl += "%s [%s]|" % (manufacturer,manufacturers[manufacturer])
			chd += "%s," % manufacturers[manufacturer]
			if (color_index>len(chart_colors)-1):
				color_index = 0
			chco += "%s|" % chart_colors[color_index]
			color_index += 1
		data += "</table>"
		
		if len(manufacturers.keys())==0:
			return "no data yet"

		if width==None:
			width = 800
		if height==None:
			height = 300
		
		chart_data = "<img src='%s?chs=%sx%s&chd=t:%s&chl=%s&cht=p'/>" % (chart_api_url, width, height, chd[:-1], chl[:-1])
		#all_data += "<br>%s" % chart_data
	
		return chart_data
	
	def showDeviceModelDistribution(self, width=None, height=None):
		devices = db.GqlQuery("SELECT * FROM MobileDevice")
		device_models = {}
		for device in devices:
			if device.device_model not in device_models.keys():
				device_models[device.device_model] = 1
			else:
				device_models[device.device_model] = device_models[device.device_model] + 1
		all_data = "<br><br><br><b>Phone models</b><br><br>"
		
		chart_api_url = 'http://chart.apis.google.com/chart'
		chd = ""
		chl = ""
		chco = ""
		data = "<table>"
		data += "<tr><td>model</td><td>total</td></tr>" 
		color_index = 0
		for device_model in device_models.keys():
			data += "<tr><td>%s</td><td>%s</td></tr>" % (device_model, device_models[device_model])
			chl += "%s [%s]|" % (device_model,device_models[device_model])
			chd += "%s," % device_models[device_model]
			if (color_index>len(chart_colors)-1):
				color_index = 0
			chco += "%s|" % chart_colors[color_index]
			color_index += 1
		data += "</table>"
		
		if len(device_models.keys())==0:
			return "no data yet"
		
		if width==None:
			width = 800
		if height==None:
			height = 300
		#chart_data = "<img src='%s?chs=600x300&chd=t:%s&chl=%s&cht=p&chco=%s'/>" % (chart_api_url, chd[:-1], chl[:-1], chco[:-1])
		chart_data = "<img src='%s?chs=%sx%s&chd=t:%s&chl=%s&cht=p'/>" % (chart_api_url, width, height, chd[:-1], chl[:-1])
		
		#all_data += "<br>%s" % chart_data
		
		return chart_data
	
	def getLineChartURL(self, x_values, y_values, chart_width, chart_height, other_parameters=None):
		
		chd = ''
		chl = ''
		
		if chart_width==None:
			chart_width = 800
		if chart_height==None:
			chart_height = 300

		# assume each label fits into 50 pixel
		n_label = int(chart_width)/50
		n_skip = 1
		while len(x_values)/n_skip > n_label:
			n_skip += 1
		
		for i in range(0, len(x_values)):
			if i%n_skip==0:
				chl += x_values[i]
			if i!=len(x_values)-1:
				chl += "|"
		
		max_y = max(y_values)
		for i in range(0,len(y_values)):
			chd += '%s' % int(y_values[i]/float(max_y)*100)
			if i!=len(y_values)-1:
				chd += ","
			
		chart_api_url = 'http://chart.apis.google.com/chart'	
		chart_url = '%s?chs=%sx%s&chd=t:%s&chl=%s&cht=lc&chxt=y&chxr=0,0,%s' % (chart_api_url, chart_width, chart_height, chd, chl, max_y)
		if other_parameters!=None:
			for key in other_parameters.keys():
				chart_url += "&%s=%s" % (key, other_parameters[key])
		
		return chart_url
	
	def showNonDiscreetEvent(self, eventName, paramKey, width, height, xSize, minX, maxX, osVer=None):
		
		paramKeys = []
		if paramKey!=None:
			paramKeys = paramKey.split(',')
		if len(paramKeys)>0:
			paramKey = None
		
		osVers = []
		if osVer!=None:
			osVers = osVer.split(',')
		if len(osVers)>0:
			osVer = None
		
		query = "SELECT * FROM NonDiscreetEvents WHERE event_name='%s' " % eventName
		if paramKey:
			query += "AND param_key='%s' " % param_key
		if minX:
			query += "AND param_value>%s " % minX
		if maxX:
			query += "AND param_value<%s " % maxX
		if osVer:
			query += "AND os_ver='%s' " % osVer
			
		query += "ORDER BY param_value"
		events = db.GqlQuery(query)
		 
		"""
		if paramKey==None:
			if minX==None and maxX==None:
				events = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE event_name=:event_name ORDER BY param_value", event_name=eventName)
			elif minX!=None and maxX!=None:
				events = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE event_name=:event_name AND param_value>:min_x AND param_value<:max_x ORDER BY param_value", event_name=eventName, min_x=minX, max_x=maxX)
			elif minX==None and maxX!=None:
				events = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE event_name=:event_name AND param_value<:max_x ORDER BY param_value", event_name=eventName, max_x=maxX)
			else:
				events = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE event_name=:event_name AND param_value>:min_x ORDER BY param_value", event_name=eventName, min_x=minX)
		else:
			if minX==None and maxX==None:
				events = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE event_name=:event_name AND param_key=:param_key ORDER BY param_value", event_name=eventName, param_key=paramKey)
			elif minX!=None and maxX!=None:
				events = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE event_name=:event_name AND param_key=:param_key AND param_value>:min_x AND param_value<:max_x ORDER BY param_value", event_name=eventName, param_key=paramKey, min_x=minX, max_x=maxX)
			elif minX==None and maxX!=None:
				events = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE event_name=:event_name AND param_key=:param_key AND param_value<:max_x ORDER BY param_value", event_name=eventName, param_key=paramKey, max_x=maxX)
			else:
				events = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE event_name=:event_name AND param_key=:param_key AND param_value>:min_x ORDER BY param_value", event_name=eventName, param_key=paramKey, min_x=minX)
		"""	
		
		all_x_values = []
		for event in events:
			should_add = False
			if len(paramKeys)>0:
				if event.param_key in paramKeys:
					should_add = True
			else:
				should_add = True
			
			if should_add:
				should_add = False
				if len(osVers)>0:
					if event.os_ver in osVers:
						should_add = True
				else:
					should_add = True
				if should_add:
					all_x_values.append(event.param_value)
					
		if minX==None:
			start_x = min(all_x_values)
		else:
			start_x = minX
		lower_limit = start_x
		upper_limit = lower_limit + xSize
		chl_list = []
		y_values = []
		
		for x_value in all_x_values:
			if len(y_values)==0:
				y_values.append(0)
				mid_point = "%s" % (int((lower_limit+upper_limit)/2))
				chl_list.append(mid_point)
			
			if x_value <= upper_limit:
				y_values[-1] = y_values[-1] + 1
			else:
				lower_limit += xSize
				upper_limit += xSize
				while x_value > upper_limit:
					lower_limit += xSize
					upper_limit += xSize
					y_values.append(0)
					mid_point = "%s" % (int((lower_limit+upper_limit)/2))
					if chl_list[-1]!=mid_point:
						chl_list.append(mid_point)
				y_values.append(1)
				
			mid_point = "%s" % (int((lower_limit+upper_limit)/2))
			if chl_list[-1]!=mid_point:
				chl_list.append(mid_point)

		if len(y_values)==0:
			return "no data yet"
	
		chart_url = self.getLineChartURL(chl_list, y_values, width, height)
		chart_data = "<img src='%s'/>" % chart_url
		return chart_data
	
	def showEvents(self, eventName=None, paramKey=None, width=None, height=None):
		"""
		records = db.GqlQuery("SELECT * FROM Events ORDER BY event_name, param_key, date, param_value")
		data = "<table border=1><tr><td>event_name</td><td>key</td><td>value</td><td>total</td><td>date</td><td>os</td><td>os_ver</td><td>app_ver</td><td>duration</td></tr>"
		events = {}
		for record in records:
			data += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (record.event_name, record.param_key, record.param_value, record.total, record.date, record.os, record.os_ver, record.app_ver, record.duration)
		data += "</table>"
		"""
		
		if eventName!=None and paramKey!=None:
			events = db.GqlQuery("SELECT * FROM Events WHERE event_name=:event_name AND param_key=:param_key ORDER BY date", event_name=eventName, param_key=paramKey)
		elif eventName!=None and paramKey==None:
			events = db.GqlQuery("SELECT * FROM Events WHERE event_name=:event_name ORDER BY date", event_name=eventName)
		else:
			events = db.GqlQuery("SELECT * FROM Events ORDER BY date")
		
		distinct_events = []
		events_info = {}
		
		earliest_date_str = ""
		earliest_date = ""
		for event in events:
			if earliest_date_str=="":
				earliest_date = event.date
				earliest_date_str = event.date.strftime('%d %b')
			if event.event_name not in distinct_events:
				distinct_events.append(event.event_name)
			if event.event_name not in events_info.keys():
				events_info[event.event_name] = {}
			if event.param_key not in events_info[event.event_name].keys():
				events_info[event.event_name][event.param_key] = []
			if event.param_value not in events_info[event.event_name][event.param_key]:
				events_info[event.event_name][event.param_key].append(event.param_value)
		"""
		for event_name in distinct_events:
			records2 = db.GqlQuery("SELECT * FROM Events WHERE event_name=:event_name ORDER BY event_name, param_key, date, param_value", event_name=event_name)
			data += "<br><br><table border=1><tr><td>event_name</td><td>key</td><td>value</td><td>total</td><td>date</td></tr>"
			for record2 in records2:
				data += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (record2.event_name, record2.param_key, record2.param_value, record2.total, record2.date)
			data += "</table>"
		"""
		
		all_data = ""
		
		
		for event_name in events_info.keys():
			for param_key in events_info[event_name].keys():
				chart_api_url = 'http://chart.apis.google.com/chart'
				chd = ""
				chl = ""
				chl_list = []
				chco =""
				chdl = ""
				data = "<br><br><table border=1><tr><td>event_name</td><td>key</td><td>value</td><td>total</td><td>date</td></tr>"
				count2 = 0
				all_y_values = []
				
				for param_value in events_info[event_name][param_key]:
					records = db.GqlQuery("SELECT * FROM Events WHERE event_name=:event_name AND param_key=:param_key AND param_value=:param_value ORDER BY date", event_name=event_name, param_key=param_key, param_value=param_value)
					
					last_date_str = earliest_date_str
					last_date = earliest_date
					last_total = 0
					count = 0
					chco += "%s," % chart_colors[count2]
					chdl += "%s" % param_value
					if count2!=len(events_info[event_name][param_key])-1:
						chdl += "|"
					#if count2!=0:
					#	chd += "|"
					y_values = []	
					for record in records:
						date_str = record.date.strftime('%d %b')
						if last_date_str!=date_str:
							date_str2 = last_date_str #.split(' ')[0]
							#if date_str2=='1' or chl=='':
							if len(chl_list)==0:
								date_str2 = last_date_str
								
							data += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (record.event_name, record.param_key, record.param_value, last_total, last_date_str)
							#chd += "%s," % last_total
							y_values.append(last_total)
							if count2==0:
								chl_list.append(date_str2) #chl += "%s|" % date_str2
							last_total = 0
							
							new_date = last_date + datetime.timedelta(days=1)
							new_date_str = new_date.strftime('%d %b')
							while new_date_str!=date_str:
								date_str2 = new_date_str #.split(' ')[0]
								#if date_str2=='1' or chl=='':
								if len(chl_list)==0:
									date_str2 = new_date_str
									
								data += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (record.event_name, record.param_key, record.param_value, last_total, new_date_str)
								#chd += "%s," % last_total
								y_values.append(last_total)
								if count2==0:
									chl_list.append(date_str2) #chl += "%s|" % date_str2
								new_date = new_date + datetime.timedelta(days=1)
								new_date_str = new_date.strftime('%d %b')
							
						last_total += record.total
						if count==records.count()-1:
							date_str2 = date_str #.split(' ')[0]
							#if date_str2=='1':
							#	date_str2 = date_str
							
							data += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (record.event_name, record.param_key, record.param_value, last_total, date_str)
							#chd += "%s" % last_total
							y_values.append(last_total)
							if count2==0:
								chl_list.append(date_str) #chl += "%s" % date_str
						last_date_str = date_str
						last_date = record.date
						count += 1
						#data += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (record.event_name, record.param_key, record.param_value, record.total, record.date)
					count2 += 1
					"""
					max_y = max(y_values)
					for i in range(0,len(y_values)):
						perc = y_values[i]/float(max_y)*100
						chd += "%.2f" % perc
						if i!=len(y_values)-1:
							chd+=","
					"""
					all_y_values.append(y_values)
					
				data += "</table>"
				max_y = 0
				for y_values in all_y_values:
					y = max(y_values)
					if y>max_y:
						max_y = y
				
				for i in range(0,len(all_y_values)):
					y_values = all_y_values[i]
					if i!=0:
						chd += "|"
					for j in range(0,len(y_values)):
						perc = int(y_values[j]/float(max_y)*100)
						chd += "%s" % perc
						if j!=len(y_values)-1:
							chd+=","
				
				if width==None:
					width = 800
				if height==None:
					height = 300
					
				# assume each label fits into 50 pixel
				n_label = int(width)/50
				n_skip = 1
				while len(chl_list)/n_skip > n_label:
					n_skip += 1

				for i in range(0, len(chl_list)):
					if i%n_skip==0:
						chl += chl_list[i]
					if i!=len(chl_list)-1:
						chl += "|"	
					
				chart_data = "<img src='%s?chs=%sx%s&chd=t:%s&chl=%s&cht=lc&chco=%s&chxt=y&chxr=0,0,%s&chdl=%s'/>" % (chart_api_url, width, height, chd, chl, chco[:-1], max_y, chdl)
				#chart_url = self.getLineChartURL(chl_list, y_values, width, height)
				#chart_data = "<img src='%s'/>" % chart_url
				
				if eventName==None and paramKey==None:
					all_data += "<br><br><br><b>Event: %s - %s</b><br><br>" %  (event_name, param_key)
				all_data += chart_data
				#all_data += "<table><tr><td>%s</td><td>%s</td></tr></table>" % (chart_data, data)
		
		return all_data
	
	def showTotalNewUsers(self, width=None, height=None):
		records = db.GqlQuery("SELECT * FROM DailyNewUsers ORDER BY date")
		
		chl_list = []
		last_date = ""
		last_total = 0
		count = 0
		cumulative_total = 0
		y_values = []
		for record in records:
			date_str = record.date.strftime('%d %b')		
			if last_date!=date_str and count!=0:
				date_str2 = last_date 
				if len(chl_list)==0:
					date_str2 = last_date
				cumulative_total += last_total
				y_values.append(cumulative_total)
				chl_list.append(date_str2) 
				last_total = 0
			last_total += record.total
			if count==records.count()-1:
				date_str2 = date_str
				cumulative_total += last_total
				y_values.append(cumulative_total)
				chl_list.append(date_str2)
			last_date = date_str
			count += 1	

		if len(y_values)==0:
			return "no data yet"
	
		chart_parameters = {}
		chart_parameters['chm'] = 'A%s,666666,0,%s,20' % (max(y_values),len(y_values)-1)
		
		chart_url = self.getLineChartURL(chl_list, y_values, width, height, other_parameters=chart_parameters)
		chart_data = "<img src='%s'/>" % chart_url
		return chart_data
		
	def showDailyNewUsers(self, width=None, height=None):
		records = db.GqlQuery("SELECT * FROM DailyNewUsers ORDER BY date")

		chl_list = []
		last_date = ""
		last_total = 0
		count = 0
		y_values = []
		
		for record in records:
			date_str = record.date.strftime('%d %b')
			if last_date!=date_str and count!=0:
				date_str2 = last_date
				if len(chl_list)==0:
					date_str2 = last_date
				y_values.append(last_total)
				chl_list.append(date_str2)
				last_total = 0
			last_total += record.total
			if count==records.count()-1:
				date_str2 = date_str 
				y_values.append(last_total)
				chl_list.append(date_str2)
			last_date = date_str
			count += 1	
		
		if len(y_values)==0:
			return "no data yet"
		
		chart_url = self.getLineChartURL(chl_list, y_values, width, height)
		chart_data = "<img src='%s'/>" % chart_url
		return chart_data

	def showDailySessions(self, width=None, height=None):
		records = db.GqlQuery("SELECT * FROM DailySessions ORDER BY date")
		last_date = ""
		last_total = 0
		count = 0
		chl_list = []
		
		y_values = []
		for record in records:
			date_str = record.date.strftime('%d %b')
			if last_date!=date_str and count!=0:
				date_str2 = last_date
				if len(chl_list)==0:
					date_str2 = last_date
					
				y_values.append(last_total)
				chl_list.append(date_str2)
				last_total = 0
			last_total += record.total
			if count==records.count()-1:
				date_str2 = date_str 
				y_values.append(last_total)
				chl_list.append(date_str2) 
			last_date = date_str
			count += 1	
		
		if len(y_values)==0:
			return "no data yet"
		
		chart_url = self.getLineChartURL(chl_list, y_values, width, height)
		chart_data = "<img src='%s'/>" % chart_url
	
		return chart_data
	
	def showMobileDevices(self):
		records = db.GqlQuery("SELECT * FROM MobileDevice")
		data = "<table border=1><tr><td>device_id</td><td>device_model</td><td>os</td><td>os_ver</td><td>app_ver</td><td>manufacturer</td><td>telco</td><td>date</td></tr>"
		for record in records:
			sg_date = record.date.replace(tzinfo=pytz.utc).astimezone(sg_tz)
			data += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (record.device_id, record.device_model, record.os, record.os_ver, record.app_ver, record.manufacturer, record.telco, sg_date)
		data += "</table>"
		return data
		
	def showAccessRecord(self):
		records = db.GqlQuery("SELECT * FROM DailyMobileDeviceAccess")
		data = "<table border=1><tr><td>device_id</td><td>date</td><td>total</td></tr>"
		for record in records:
			data += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (record.device_id, record.date, record.total)
		data += "</table>"
		return data

class RecordAnalytics(object):
	def __init__(self, device_id, os, os_ver, app_ver, time=None, secret_key=None):
		self.device_id = device_id
		self.os = os
		self.os_ver = os_ver
		self.app_ver = app_ver
		if time!=None:
			self.time = time
		if secret_key!=None:
			self.secret_key = secret_key

	def incrementDailyNewUser(self):
		today = datetime.date.today()
		records = db.GqlQuery("SELECT * FROM DailyNewUsers WHERE date=DATETIME(:year, :month, :day, 0, 0, 0) AND os=:os AND os_ver=:os_ver AND app_ver=:app_ver", year=today.year, month=today.month, day=today.day, os=self.os, os_ver=self.os_ver, app_ver=self.app_ver)
		count = 0
		for record in records:
			count += 1
			record.total = record.total + 1
			record.put()
		if count==0:
			user = DailyNewUsers()
			user.total = 1
			user.os = self.os
			user.os_ver = self.os_ver
			user.app_ver = self.app_ver
			user.put()
		
	def recordDeviceIfRequired(self, device_model, manufacturer, telco=None):
		records = db.GqlQuery("SELECT * FROM MobileDevice WHERE device_id='%s'" % self.device_id)
		count = 0
		for record in records:
			count += 1
			record.os = self.os
			record.os_ver = self.os_ver
			record.app_ver = self.app_ver
			record.device_model = device_model
			record.manufacturer = manufacturer
			record.telco = telco
			record.put()
		if count==0:
			
			device = MobileDevice()
			device.device_id = self.device_id
			device.os = self.os
			device.os_ver = self.os_ver
			device.app_ver = self.app_ver
			device.device_model = device_model
			device.manufacturer = manufacturer
			device.telco = telco
			device.put()
			
			self.incrementDailyNewUser()

	def recordSingleEvent(self, event_name, param_key, param_value, is_discreet,duration=None):
		today = datetime.date.today()
		if is_discreet:
			records = db.GqlQuery("SELECT * FROM Events WHERE date=DATETIME(:year, :month, :day, 0, 0, 0) AND os=:os AND os_ver=:os_ver AND param_key=:param_key AND param_value=:param_value AND app_ver=:app_ver AND event_name=:event_name", year=today.year, month=today.month, day=today.day, os=self.os, os_ver=self.os_ver, param_key=param_key, param_value=param_value, app_ver=self.app_ver, event_name=event_name)
		else:
			records = db.GqlQuery("SELECT * FROM NonDiscreetEvents WHERE date=DATETIME(:year, :month, :day, 0, 0, 0) AND os=:os AND os_ver=:os_ver AND param_key=:param_key AND param_value=:param_value AND app_ver=:app_ver AND event_name=:event_name", year=today.year, month=today.month, day=today.day, os=self.os, os_ver=self.os_ver, param_key=param_key, param_value=float(param_value), app_ver=self.app_ver, event_name=event_name)
		count = 0
		
		for record in records:
			count += 1
			record.total = record.total + 1
			record.put()
		if count==0:
			try:
				if is_discreet:
					event = Events()
					event.param_value = param_value
				else:
					event = NonDiscreetEvents()
					event.param_value = float(param_value)
				event.total = 1
				event.event_name = event_name
				event.param_key = param_key
				event.os = self.os
				event.os_ver = self.os_ver
				event.app_ver = self.app_ver
				event.put()
			except:
				pass
	
	def recordEvent(self, event_name, parameters, is_discreet, duration=None):
		
		for key in parameters:
			if duration==None:
				self.recordSingleEvent(event_name, key, parameters[key], is_discreet)
			else:
				self.recordSingleEvent(event_name, key, parameters[key], is_discreet, duration=duration)

	def recordAccess(self):
		records = db.GqlQuery("SELECT * FROM DailyMobileDeviceAccess WHERE device_id='%s'" % self.device_id)
		count = 0
		for record in records:
			count += 1
			record.total = record.total + 1;
			record.put()
		if count==0:
			dailyMobileDeviceAccess = DailyMobileDeviceAccess()
			dailyMobileDeviceAccess.device_id = self.device_id
			dailyMobileDeviceAccess.total = 1;
			dailyMobileDeviceAccess.put()
	
	def incrementSession(self):
		today = datetime.date.today()
		records = db.GqlQuery("SELECT * FROM DailySessions WHERE date=DATETIME(:year, :month, :day) AND os=:os AND os_ver=:os_ver AND app_ver=:app_ver", year=today.year, month=today.month, day=today.day, os=self.os, os_ver=self.os_ver, app_ver=self.app_ver)
		count = 0
		for record in records:
			count += 1
			record.total = record.total + 1
			record.put()
		if count==0:
			session = DailySessions()
			session.total = 1
			session.os = self.os
			session.os_ver = self.os_ver
			session.app_ver = self.app_ver
			session.put()
	
	def onApplicationExited(self, duration):
		pass
		
	def onApplicationStarted(self, device_model, manufacturer, telco=None):
		self.recordAccess()
		self.incrementSession()
		self.recordDeviceIfRequired(device_model, manufacturer, telco)

	def getSecretKey(self, api_key, time):
		seed = "%s%s" % (api_key, time) 
		encryption = hashlib.sha256(seed)
		data = seed + "<br>"
		data += encryption.hexdigest()
		return data.upper()

	def allowLogging(self):
		if not config.require_key:
			return True
		else:
			actual_secret_key = self.getSecretKey(config.gaemobileanalytics_api_key, self.time)
			return actual_secret_key==self.secret_key
		
