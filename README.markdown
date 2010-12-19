GAEMobileAnalytics is a mobile analytics app running on Google App Engine. It is still a work in progress.

There are 2 components available:
* Server - coded in Python, runs on Google App Engine
* Client - library available in **Objective-C** for iOS, and **C#** for Windows Phone 7

A demo can be found [here](http://www.honcheng.com/2010/11/Open-Source-Analytics-App-on-AppEngine---GAEMobileAnalytics). 

## Instruction for iOS
to be added soon

## Instruction for Windows Phone 7

Logger.OnApplicationStarted(...)

* call this everytime the app is started
* this method gives the bare minimum analytics:
  * number of sessions daily
  * number of downloads daily
  * distribution of phone models

Logger.LogEvent(string eventName, Dictionary<string, object> parameters)

* call this method to log event
* group similar events with the same eventName
* you can track multiple parameters 
* example : tracking facebook/twitter button with share/view option

	Dictionary<string, object> parameters = new Dictionary<string, object>();  
	parameters.Add("title","twitter");  
	parameters.Add("action", "share");  
	Logger.LogEvent("BUTTON_CLICKED", parameters);  
OR 
	Dictionary<string, object> parameters = new Dictionary<string, object>();
	parameters.Add("title","twitter");
	parameters.Add("action", "view");
	Logger.LogEvent("BUTTON_CLICKED", parameters);
OR
	Dictionary<string, object> parameters = new Dictionary<string, object>();
	parameters.Add("title","facebook");
	parameters.Add("action", "share");
	Logger.LogEvent("BUTTON_CLICKED", parameters);

* example : track failure of action by phone model
   Dictionary<string, object> parameters = new Dictionary<string, object>();
   parameters.Add("phone",Info.DeviceName());
   Logger.LogEvent("FAILED_TO_OBTAIN_DATA", parameters);

## Dependencies

* pytz

