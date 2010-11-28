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
using Microsoft.Phone.Info;
using System.Collections.Generic;
using System.Diagnostics;
using System.Xml;
using System.Xml.Linq;

namespace com.honcheng.appenginemobileanalytics.WP
{
    static public class Info
    {
        public static string UniqueID()
        {
            //return GetWindowsLiveAnonymousID();
            try
            {
                byte[] id = (byte[])DeviceExtendedProperties.GetValue("DeviceUniqueId");
                return Convert.ToBase64String(id);
            }
            catch (Exception e)
            {
                return "unknown";
            }
        }

        public static string AppName()
        {
            string value = System.Reflection.Assembly.GetExecutingAssembly().FullName.Split(',')[0];
            return value;
        }

        public static string AppVersion()
        {
            //string value = System.Reflection.Assembly.GetExecutingAssembly().FullName.Split('=')[1].Split(',')[0];
            //return value;
            return GetAppAttribute("Version");
        }

        public static string GetAppAttribute(string attributeName)
        {
            XDocument appManifestXML = XDocument.Load("WMAppManifest.xml");
            if (appManifestXML != null)
            {
                using (XmlReader reader = appManifestXML.CreateReader(ReaderOptions.None))
                {
                    reader.ReadToDescendant("App");
                    if (!reader.IsStartElement())
                    {
                        throw new System.FormatException("WMAppManifest.xml is missing");
                    }
                    return reader.GetAttribute(attributeName);
                }
            }
            else
            {
                return null;
            }
        }

        public static string Manufacturer()
        {
            try
            {
                string manufacturer = (string)DeviceExtendedProperties.GetValue("DeviceManufacturer");
                return manufacturer;
            }
            catch (Exception e)
            {
                return "unknown";
            }
            
        }

        public static string OS()
        {
            return "WP";
        }

        public static string OSVersion()
        {
            try
            {
                string os_version = System.Environment.OSVersion.ToString();
                return os_version;
            }
            catch (Exception e)
            {
                return "unknown";
            }
        }

        public static string DeviceFirmwareVersion()
        {
            try
            {
                string firmware = DeviceExtendedProperties.GetValue("DeviceFirmwareVersion").ToString();
                return firmware;
            }
            catch (Exception e)
            {
                return "unknown";
            }
            
        }

        public static string DeviceName()
        {
            try
            {
                string value = DeviceExtendedProperties.GetValue("DeviceName").ToString();
                return value;
            }
            catch (Exception e)
            {
                return "unknown";
            }

        }

        private static readonly int ANIDLength = 32;
        private static readonly int ANIDOffset = 2;
        public static string GetWindowsLiveAnonymousID()
        {
            string result = string.Empty;
            object anid;
            if (UserExtendedProperties.TryGetValue("ANID", out anid))
            {
                if (anid != null && anid.ToString().Length >= (ANIDLength + ANIDOffset))
                {
                    result = anid.ToString().Substring(ANIDOffset, ANIDLength);
                }
            }

            if (Microsoft.Devices.Environment.DeviceType == Microsoft.Devices.DeviceType.Emulator)
            {
                result = "WP7Emulator";
            }

            return result;
        }

        public static Dictionary<string, object> GlobalParameters()
        {
            Dictionary<string, object> parameters = new Dictionary<string, object>();

            parameters.Add("device_id", UniqueID());
            parameters.Add("os", OS());
            parameters.Add("os_ver", OSVersion());
            parameters.Add("manufacturer", Manufacturer());
            parameters.Add("device_model", DeviceName());
            parameters.Add("app_ver", AppVersion());
            parameters.Add("app_name", AppName());

            Debug.WriteLine(">>>> " + AppVersion());

            return parameters;
        }

        
    }
}
