#!/usr/bin/python
import time
import urllib
import httplib2
import random
import socket


LOGGLY_URL_OFFICE = 'http://proxy3.office.loggly.net/inputs/07446c06-b773-458a-a2ec-924efc21e58f'
LOGGLY_URL_GUNROCK = 'http://logs.braintrain.uni.loggly.net/inputs/36bf2ef1-1c57-4599-b276-85d1c16f09f3'

INSERT_HTTP = httplib2.Http(timeout=10)

twitter_url = 'http://api.twitter.com/1/statuses/user_timeline.json?include_rts=true&screen_name=bonus500&count=1&exclude_replies=true&trim_user=true&page='

# starting at 1 for human readablilty
counter = 1 

while 1:
    random_tweet_number = str(random.randint(1,1824))
    # just print some info to figure out if there's a pattern to these failures
    print '\n'
    print '=================================================='
    print '====== Iteration:' + str(counter) 
    print '====== Random Tweet:' + random_tweet_number
    print '=================================================='

    new_tweet = twitter_url + random_tweet_number
    tweet = urllib.urlopen(new_tweet).read()
    
    #logging to office
    try:
        resp, content = INSERT_HTTP.request(LOGGLY_URL_OFFICE, 
                                            'POST', 
                                            body=tweet, 
                                            headers={'content-type':'application/json'})
        resp, content = INSERT_HTTP.request(LOGGLY_URL_GUNROCK, 
                                            'POST', 
                                            body=tweet, 
                                            headers={'content-type':'application/json'})
        print tweet
    # if there's a timeout exception, print some info, and pass
    except socket.timeout:
        print 'hmm timeout... printing tweet, then on to the next one'
        print tweet

        pass
    
    time.sleep(65)

    counter += 1



''' Some Docs to help me remember:

Simple scenario:

ssh into your remote box. type "screen" Then start the process you want.

Press Ctrl-A then Ctrl-D. This will "detach" your screen session but leave your processes running. You can now log out of the remote box.

If you want to come back later, log on again and type "screen -r" This will "resume" your screen session, and you can see the output of your process.


source: http://askubuntu.com/questions/8653/how-to-keep-processes-running-after-ending-ssh-session

==================================================
====== Iteration:878
====== Random Tweet:1348
==================================================
Traceback (most recent call last):
  File "twitter.py", line 40, in <module>
    headers={'content-type':'application/json'})
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/httplib2/__init__.py", line 1544, in request
    (response, content) = self._request(conn, authority, uri, request_uri, method, body, headers, redirections, cachekey)
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/httplib2/__init__.py", line 1294, in _request
    (response, content) = self._conn_request(conn, request_uri, method, body, headers)
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/httplib2/__init__.py", line 1268, in _conn_request
    conn.connect()
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/httplib2/__init__.py", line 890, in connect
    raise socket.error, msg
socket.error: [Errno 61] Connection refused

'''

