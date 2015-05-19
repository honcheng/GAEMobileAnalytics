GAEMobileAnalytics is a mobile analytics app running on Google App Engine. It is still a work in progress.

There are 2 components available:
* Server - coded in Python, runs on Google App Engine
* Client - library available in **Objective-C** for iOS, and **C#** for Windows Phone 7

A demo can be found [here](http://www.honcheng.com/2010/11/Open-Source-Analytics-App-on-AppEngine---GAEMobileAnalytics). 

## Instruction for App Engine

1. Get the source code [here](https://github.com/honcheng/GAEMobileAnalytics)
2. Register a new Google App Engine application [here](http://appengine.google.com)
3. Use GoogleAppEngineLauncher to add this project as an existing application
4. Open app.yaml and replace the application name with the one you just registered
5. Open config.py and change **gaemobileanalytics_api_key** to any random characters you want. Make sure you keep this key private. Enter the same key in the client library
6. Edit the following path if you do not want to use the default paths:
	* display_path
	* chart_path 
	* chart_event_path
	* record_path
	* record_queue_path
	* record_event_path
	* record_event_queue_path
7. Deploy and you should be ready for the client (iOS or WP7) integration

## Instruction for iOS

A sample application is included in **iOS/gaemobileanalytics**.

To integrate GAEMobileAnalytics into your iOS application:

1. Drag **iOS/gaemobileanalytics/Classes/GAEMobileAnalytics.h** and **iOS/gaemobileanalytics/Classes/GAEMobileAnalytics.m** into your XCode project
2. Add **#import "GAEMobileAnalytics.h"** to your AppDelegate
3. In your **- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions** method, add  

    [[GAEMobileAnalytics defaultLogger] initWithApiKey:<api_key> baseUrl:<record_path> eventsUrl:<record_event_path>];  
	
	replace <api_key> with **gaemobileanalytics_api_key** in config.py  
	replace <record_path> with **hostname+record_path** in config.py .e.g http://myapp.appspot.com/log  
	replace <record_event_path> with **hostname+record_path** in config.py .e.g http://myapp.appspot.com/log/event  

4. Use **[[GAEMobileAnalytics defaultLogger] logEvent:<event_name> parameters:<parameters> discreet:<is_discreet?>]** to log events

You can find more information about the instruction above in the sample application

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

## About me

I make apps for iPhone, iPad, Android, WP7 and Google App Engine. 
[Follow me in Twitter](http://twitter.com/honcheng)

