import sys
import twitter
import time
from sense_hat import SenseHat
from keyGrabber import grab_key
sense = SenseHat()
consumer_key = grab_key("twitter_consumer_key")
consumer_secret = grab_key("twitter_consumer_secret")
access_token_key = grab_key("twitter_access_token_key")
access_token_secret = grab_key("twitter_access_token_secret")
api = twitter.Api(consumer_key=consumer_key,
				consumer_secret=consumer_secret,
				access_token_key=access_token_key,
				access_token_secret=access_token_secret)

def flash_dot(sense):
	red = (255,0,0)
	black = (0,0,0)
	sense.set_pixel(0,7, red)
	time.sleep(1)
	sense.set_pixel(0,7, black)
	time.sleep(1)
	sense.set_pixel(0,7, red)
	time.sleep(1)
	sense.set_pixel(0,7, black)
	time.sleep(1)
	sense.set_pixel(0,7, red)

def flash_message_waiting(sense):
	blue = (0,200,255)
	black = (0,0,0)
	sense.set_pixel(1,7, blue)
	time.sleep(1)
	sense.set_pixel(1,7, black)
	time.sleep(1)
	sense.set_pixel(1,7, blue)
	time.sleep(1)
	sense.set_pixel(1,7, black)
	time.sleep(1)
	sense.set_pixel(1,7, blue)

def checkMentions(api, newest_mention_id):
	print("Checking Mentions...")
	queue = api.GetMentions(since_id=newest_mention_id)
	return queue

def print_messages(queue, sense, screen):
	blue = (0,200,255)
	red = (255,0,0)
	i = len(queue)-1
	while(i>=0):
		sense.stick.wait_for_event()
		message = queue[i].AsDict()
		sense.show_message(message['user']['screen_name'] + ": "+message['text'])
		sense.clear()
		sense.set_pixel(1,7, blue)
		sense.set_pixel(0,7, red)
		i=i-1
	sense.clear()


print(api.VerifyCredentials())
newest_mention = api.GetMentions(count=1)[0]
print(newest_mention.AsDict())
newest_mention_id = newest_mention.AsDict()['id_str']
print(newest_mention.AsDict()['user']['screen_name'])
print(newest_mention.AsDict()['text'])
new_messages = False

while(True):
	sense.low_light = True
	#show active flashdot
	flash_dot(sense)
	#check for new mentions
	message_queue = checkMentions(api, newest_mention_id)
	if(len(message_queue) > 0):
		new_messages = True
	if(not new_messages):
		#wait 1 minute for recheck
		time.sleep(60)
	if(new_messages):
		newest_mention_id = message_queue[0].AsDict()['id_str']
		#show message waiting symbol if needed
		flash_message_waiting(sense)
		#wait for input if message waiting
		print_messages(message_queue, sense, sense.get_pixels)
		new_messages = False



