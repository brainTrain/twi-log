#!/usr/bin/python
import urllib
import httplib2
import socket
import sys


print "ok, we're gonna log some tweets to loggly for easier searchin"
LOGGLY_INPUT_KEY = raw_input("paste loggly input key: ")
twitter_user = raw_input("type twitter username (excluding the @ symbol): ")
twitter_count = raw_input("enter the number of tweets you'd like returned: ")

print 'searching for ' + twitter_count + 'tweets...'

'''
looks like twitter won't let you pull more than ~2k tweets via their api... at 
least not easily.  The max number of tweets you can pull in one request is 200,
so I default to one page if the twitter_count specified is under 200 tweets, 
calculate the number of pages if the twitter_count is above 200 tweets, and
default to what seems to be the max number of pages you can scrape if you're
trying to get over 2000 tweets
'''
number_of_pages = 1
if 2000  > int(twitter_count) > 200:
    number_of_pages = int(twitter_count)/200
elif int(twitter_count) > 2000:
    number_of_pages = 16
# load up the loggly input key
LOGGLY_URL_PROD = 'http://logs.loggly.com/inputs/' + LOGGLY_INPUT_KEY
# how long do we wanna wait for a response? 
INSERT_HTTP = httplib2.Http(timeout=10)

# grab tweets with the corresponding number of pages
while number_of_pages != 0:
    # build out the twitter api URL
    twitter_url = 'http://api.twitter.com/1/statuses/user_timeline.json?include_rts=true&screen_name=' + twitter_user + '&count=' + twitter_count + '&exclude_replies=true&trim_user=true&page=' + str(number_of_pages)

    # logging to prod
    try:
        new_tweets = twitter_url
        # grab the json blob
        tweets = urllib.urlopen(new_tweets).read()
        print 'sending tweet'
        # send that blob to loggly
        resp, content = INSERT_HTTP.request(LOGGLY_URL_PROD, 
                                            'POST', 
                                            body=tweets, 
                                            headers={'content-type':'application/json'})
        # print the output yo 
        print tweets
    # if things timeout, etc.. print out with error message and pass
    except socket.timeout, IOError:
        print 'hmm timeout... printing tweet, then on to the next one'
        print tweets
        pass
    # subtract number of pages by 1 to iterate
    number_of_pages -= 1


'''TODO:
    * handle multiple twitter usernames
    * handle twitter's 420 chillout response code
    * figure out how to make this dude run from the user's computer
      so they can search 150 an hour, and more users don't get in 
      eachothers way
'''
