/**
 * Copyright (c) 2010 Muh Hon Cheng
 * Created by honcheng on 12/16/10.
 * 
 * Permission is hereby granted, free of charge, to any person obtaining 
 * a copy of this software and associated documentation files (the 
 * "Software"), to deal in the Software without restriction, including 
 * without limitation the rights to use, copy, modify, merge, publish, 
 * distribute, sublicense, and/or sell copies of the Software, and to 
 * permit persons to whom the Software is furnished to do so, subject 
 * to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be 
 * included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT 
 * WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR 
 * PURPOSE AND NONINFRINGEMENT. IN NO EVENT 
 * SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
 * IN CONNECTION WITH THE SOFTWARE OR 
 * THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 * 
 * @author 		Muh Hon Cheng <honcheng@gmail.com>
 * @copyright	2010	Muh Hon Cheng
 * @version
 * 
 */

#import "GAEMobileAnalytics.h"
#import <CommonCrypto/CommonDigest.h>
#import <CoreTelephony/CTTelephonyNetworkInfo.h>
#import <CoreTelephony/CTCarrier.h>
#import "SBJSON.h"

@interface GAEMobileAnalytics()
- (void)postToUrl:(NSString*)baseUrl parameters:(NSMutableDictionary*)parameters;
- (NSString*)getSHA256Hash:(NSString*)input;
@end

@implementation GAEMobileAnalytics
@synthesize apiKey, secretKey, basicAnalyticsRecordUrl, eventsAnalyticsRecordUrl;

static GAEMobileAnalytics *defaultLogger = nil;

+ (GAEMobileAnalytics *)defaultLogger
{
	@synchronized(self)
	{
		if (defaultLogger==nil)
		{
			[[self alloc] init];
		}
	}
	return defaultLogger;
}

+ (id)allocWithZone:(NSZone *)zone
{
	@synchronized(self)
	{
		if (defaultLogger==nil)
		{
			defaultLogger = [super allocWithZone:zone];
			return defaultLogger;
		}
	}
	return nil;
}

- (id)copyWithZone:(NSZone *)zone 
{
    return self;
}

- (id)retain {
    return self;
}

- (unsigned)retainCount 
{
    return UINT_MAX;  //denotes an object that cannot be released
}

- (void)release 
{
    //do nothing
}

- (id)autorelease 
{
    return self;
}

- (void)dealloc {
	[super dealloc];
}

- (id)initWithApiKey:(NSString*)_apiKey baseUrl:(NSString*)basicUrl eventsUrl:(NSString*)eventsUrl
{
	if (self = [super init]) 
	{
		self.apiKey = _apiKey;
		self.basicAnalyticsRecordUrl = basicUrl;
		self.eventsAnalyticsRecordUrl = eventsUrl;
		
		[self postToUrl:self.basicAnalyticsRecordUrl parameters:nil];
	}
	return self;
}

- (void)logEvent:(NSString*)eventName parameters:(NSMutableDictionary*)parameters discreet:(BOOL)discreet
{
	NSMutableDictionary *post_parameters = [NSMutableDictionary dictionary];
	[post_parameters setObject:[NSNumber numberWithBool:discreet] forKey:@"is_discreet"];
	[post_parameters setObject:eventName forKey:@"event"];
	
	if (parameters)
	{
		SBJSON *jsonParser = [SBJSON new];
		NSString *jsonString = [jsonParser stringWithObject:parameters];
		[jsonParser release];
		
		[post_parameters setObject:jsonString forKey:@"parameters"];
	}
	[self postToUrl:self.eventsAnalyticsRecordUrl parameters:post_parameters];
}

- (void)postToUrl:(NSString*)baseUrl parameters:(NSMutableDictionary*)parameters
{
	if (startTime==0)
	{
		startTime = [[NSDate date] timeIntervalSince1970];
		NSString *seed = [NSString stringWithFormat:@"%@%i", self.apiKey, startTime];
		self.secretKey = [self getSHA256Hash:seed];
	}
	
	if (!parameters)
	{
		parameters = [NSMutableDictionary dictionary];
	}
	
	[parameters setObject:[NSNumber numberWithInt:startTime] forKey:@"t"];
	[parameters setObject:self.secretKey forKey:@"s"];
	[parameters setObject:[[UIDevice currentDevice] uniqueIdentifier] forKey:@"device_id"];
	[parameters setObject:[[UIDevice currentDevice] systemName] forKey:@"os"];
	[parameters setObject:[[UIDevice currentDevice] systemVersion] forKey:@"os_ver"];
	[parameters setObject:@"Apple" forKey:@"manufacturer"];
	
	NSString *bundle_identifier = [[[NSBundle mainBundle] infoDictionary] objectForKey:(NSString*)kCFBundleIdentifierKey];
	[parameters setObject:bundle_identifier forKey:@"app_id"];
	
	NSString *app_version = [[[NSBundle mainBundle] infoDictionary] objectForKey:(NSString*)kCFBundleVersionKey];
	[parameters setObject:app_version forKey:@"app_ver"];
	
	NSString *app_name = [[[NSBundle mainBundle] infoDictionary] objectForKey:(NSString*)kCFBundleNameKey];
	[parameters setObject:app_name forKey:@"app_name"];
	
	CTTelephonyNetworkInfo *telephony = [[CTTelephonyNetworkInfo alloc] init];
	CTCarrier *carrier = [telephony subscriberCellularProvider];
	
	NSString *carrierName = [carrier carrierName];
	if (carrierName==nil) carrierName = @"No Carrier Info";
	carrierName = [carrierName stringByAddingPercentEscapesUsingEncoding:NSUTF8StringEncoding];
	[parameters setObject:carrierName forKey:@"telco"];
	
	NSMutableURLRequest *request = [[[NSMutableURLRequest alloc] initWithURL:[NSURL URLWithString:baseUrl]
																 cachePolicy:NSURLRequestReloadIgnoringLocalAndRemoteCacheData
															 timeoutInterval:60] autorelease];
	[request setHTTPMethod:@"POST"];
	
	NSMutableString *parameterString = [NSMutableString stringWithString:@""];
	int i;
	for (i=0; i<[[parameters allKeys] count]; i++)
	{
		NSString *key = [[parameters allKeys] objectAtIndex:i];
		id value = [parameters objectForKey:key];
		if (i!=0) [parameterString appendString:@"&"];
		[parameterString appendFormat:@"%@=%@", key, value];
	}
	
	NSData *postData = [parameterString dataUsingEncoding:NSASCIIStringEncoding allowLossyConversion:YES];
	NSString *postLength = [NSString stringWithFormat:@"%d", [postData length]];
	[request setValue:postLength forHTTPHeaderField:@"Content-Length"];
	[request setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];
	[request setHTTPBody:postData];
	
	//NSLog(@"%@", request);
	
	[[NSURLConnection alloc] initWithRequest:request delegate:nil];
}

- (NSString*)getSHA256Hash:(NSString*)input
{
	const char *cStr = [input UTF8String];
	unsigned char result[CC_SHA256_DIGEST_LENGTH];
	CC_SHA256(cStr, strlen(cStr), result);
	
	NSString *sha256Key = [NSString 
						stringWithFormat: @"%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X",
						result[0], result[1],
						result[2], result[3],
						result[4], result[5],
						result[6], result[7],
						result[8], result[9],
						result[10], result[11],
						result[12], result[13],
						result[14], result[15],
						result[16], result[17],
						result[18], result[19],
						result[20], result[21],
						result[22], result[23],
						result[24], result[25],
						result[26], result[27],
						result[28], result[29],
						result[30], result[31]
						];
	return sha256Key;
}

@end
