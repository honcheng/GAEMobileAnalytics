GAEMobileAnalytics version 0.1

dependencies:
- pytz

This is a mobile analytics app running on Google AppEngine. It's still pretty rough. Only spent a few days on this, so I doubt it's ready for production. More internal testing required. 

Platform-specific library will be included. The first library will be for Windows Phone 7 in C#

The current version is being tested on SG Buses for Windows Phone 7. 


Instruction for Windows Phone 7
--------------------------------
Logger.OnApplicationStarted(É.)
- call this everytime the app is started
- this method gives the bare minimum analytics
  - number of sessions daily
  - number of downloads daily
  - distribution of phone models

Logger.LogEvent(string eventName, Dictionary<string, object> parameters)
- call this method to log event
- group similar events with the same eventName
- you can track multiple parameters 
- example : tracking facebook/twitter button with share/view option
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
- example : track failure of action by phone model
   Dictionary<string, object> parameters = new Dictionary<string, object>();
   parameters.Add("phone",Info.DeviceName());
   Logger.LogEvent("FAILED_TO_OBTAIN_DATA", parameters);
