using System;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using System.Diagnostics;
using System.Collections.Generic;
using System.Text;
using System.Security.Cryptography;

namespace com.honcheng.appenginemobileanalytics.WP
{
    static public class Logger
    {
        private static string APIKey;
        private static string SecretKey;
        private static int startTime;
        private static string BasicAnalyticsRecordURL;
        private static string EventsAnalyticsRecordURL;

        public static void OnApplicationStarted(string apiKey, string basicURL, string eventsURL)
        {
            APIKey = apiKey;
            BasicAnalyticsRecordURL = basicURL;
            EventsAnalyticsRecordURL = eventsURL;

            Dictionary<string, object> parameters = new Dictionary<string, object>();
            string parameterString = GenerateUrl(null, parameters);

            try
            {
                Uri uri = new Uri(BasicAnalyticsRecordURL, UriKind.Absolute);
                WebClient webClient = new WebClient();
                webClient.DownloadStringCompleted += new DownloadStringCompletedEventHandler(webClient_DownloadStringCompleted);
                //webClient.DownloadStringAsync(uri);
                webClient.UploadStringAsync(uri,"POST",parameterString);
              
            }
            catch (Exception e)
            {
                Debug.WriteLine("error " + BasicAnalyticsRecordURL + " | " + e.ToString());
            }
            

        }

        public static void LogEvent(string eventName, Dictionary<string, object> parameters)
        {
            Debug.WriteLine("log event " + eventName);

            string parameterString = "{";
            int total = parameters.Keys.Count;
            int index = 0;
            foreach (string key in parameters.Keys)
            {
                parameterString += "\"" + key + "\":\"" + parameters[key] + "\"";
                if (index != total - 1) parameterString += ",";
                index += 1;
            } 
            parameterString += "}";

            Dictionary<string, object> parameters2 = new Dictionary<string, object>();
            parameters2.Add("event", eventName);
            parameters2.Add("parameters", parameterString);
            //urlString = GenerateUrl(urlString, parameters2);
            //Debug.WriteLine(urlString);
            string parameterString2 = GenerateUrl(null, parameters2);

            try
            {
                Uri uri = new Uri(EventsAnalyticsRecordURL, UriKind.Absolute);
                WebClient webClient = new WebClient();
                webClient.DownloadStringCompleted += new DownloadStringCompletedEventHandler(webClient_DownloadStringCompleted);
                //webClient.DownloadStringAsync(uri);
                webClient.UploadStringAsync(uri, "POST", parameterString2);
            }
            catch (Exception e)
            {
                Debug.WriteLine("error " + EventsAnalyticsRecordURL + " | " + e.ToString());
            }

            
        }

        static void webClient_DownloadStringCompleted(object sender, DownloadStringCompletedEventArgs e)
        {
            //throw new NotImplementedException();
        }

        public static string GenerateUrl(string baseUrl, Dictionary<string, object> parameters)
        {
            if (startTime == 0)
            {
                startTime = (int)(DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalSeconds;
                string seed = APIKey + startTime;
                SecretKey = GetSHA256Hash(seed);
            }

            if (parameters == null) parameters = new Dictionary<string, object>();
            parameters.Add("t", startTime);
            parameters.Add("s", SecretKey);

            Dictionary<string, object> globalParameters = Info.GlobalParameters();
            string parameterString = "";

            int count = 0;
            foreach (KeyValuePair<string, object> parameter in globalParameters)
            {
                if (count == 0) parameterString += parameter.Key + "=" + parameter.Value;
                else parameterString += "&" + parameter.Key + "=" + parameter.Value;
                count += 1;
            }
            if (parameters != null)
            {
                foreach (KeyValuePair<string, object> parameter in parameters)
                {
                    parameterString += "&" + parameter.Key + "=" + parameter.Value;
                }
            }

            //Debug.WriteLine(parameterString);

            if (baseUrl==null)
            {
                return parameterString;
            }
            else
            {
                return baseUrl + "?" + parameterString;
            }            
        }

        public static string GetSHA256Hash(string input)
        {
            SHA256 sha256 = new SHA256Managed();
            byte[] sha256Bytes = Encoding.UTF8.GetBytes(input);
            byte[] cryString = sha256.ComputeHash(sha256Bytes);
            string sha256Str = string.Empty;
            for (int i = 0; i < cryString.Length; i++)
            {
                sha256Str += cryString[i].ToString("X");
            }
            return sha256Str;
        }
    }
}
