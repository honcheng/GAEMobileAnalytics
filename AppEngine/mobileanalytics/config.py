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

# API Key - this key must match the key in the app. 
gaemobileanalytics_api_key = "put-a-few-random-characters-here"

# Set this to True to require that the API key in the app matches the API key on the server
# The API key is encrypted
# There is no reason to set this to False, unless during debugging
require_key = False

# Paths for API
display_path = '/display'
chart_path = '/chart'
chart_event_path = '/chart/event'
record_path = '/record'
record_queue_path = '/record/queue'
record_event_path = '/record/event'
record_event_queue_path = '/record/event/queue'
