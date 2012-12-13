#!/usr/bin/python
import time
import urllib
import httplib2
import random
import socket
import os
import base64
import json


#LOGGLY_URL_GUNROCK = 'http://logs.braintrain.uni.loggly.net/inputs/1a43e9e8-b5b2-4628-9a31-b78a775a5ad8'
LOGGLY_URL_GUNROCK = 'http://logs.braintrain.uni.loggly.net/inputs/13050e37-5319-4d75-a3b1-cbe2d178576a'
LOGGLY_URL_GUNROCK_NUMBER = 'http://logs.braintrain.uni.loggly.net/inputs/30562f96-1620-4913-9337-39ce1f15d257'
LOGGLY_URL_FRONTEND1 = 'http://proxy3.office.loggly.net/inputs/5d7749bb-1acf-4612-8d1c-aab80f26e557'
LOGGLY_URL_BOSSEMAILS = 'https://logs.loggly.com/inputs/7733d7fd-bf5f-445c-a702-7d4a65d95154'

INSERT_HTTP = httplib2.Http(timeout=10)

while 1:
    random_count = random.randint(2000,5000)
    counter = 0
    while counter <= random_count:
        #init json_blob
        json_blob_0 = {
            'user': None,
            'person': None,
            'red': None,
            'blue': None,
            'green': None,
            'yellow': None
        }
        json_blob_1 = {
            'whatever': None,    
            'dude': None,    
            'like': None,    
            'literally': None,    
        }
        for val in json_blob_0:        
            string_int_switch = random.randint(0,1)
            #random_graph_number = random.uniform(400.99199,400.99899)
            random_graph_number = random.randint(200,600)
            random_string = base64.urlsafe_b64encode(os.urandom(15)) 
            if string_int_switch:
                random_val = random_string
            else:
                random_val = random_graph_number

            json_blob_0[val] = random_val

        json_blob_0 = json.dumps(json_blob_0)

        for val in json_blob_1:        
            string_int_switch = random.randint(0,1)
            #random_graph_number = random.uniform(400.99199,400.99899)
            random_graph_number = random.randint(-100,1)
            random_string = base64.urlsafe_b64encode(os.urandom(15)) 
            if string_int_switch:
                #random_val = random_string
                random_val = random_graph_number
            else:
                random_val = random_graph_number

            json_blob_1[val] = random_val

        json_blob_1 = json.dumps(json_blob_1)

        #logging to office
        try:
            #resp, content = INSERT_HTTP.request(LOGGLY_URL_BOSSEMAILS, 
            #resp, content = INSERT_HTTP.request(LOGGLY_URL_GUNROCK_NUMBER, 
            resp, content = INSERT_HTTP.request(LOGGLY_URL_GUNROCK, 
                                                'POST', 
                                                body=json_blob_0, 
                                                headers={'content-type':'application/json'})
            resp, content = INSERT_HTTP.request(LOGGLY_URL_GUNROCK, 
                                                'POST', 
                                                body=json_blob_1, 
                                                headers={'content-type':'application/json'})
            print 'json_blob_0'
            print json_blob_0
            print 'json_blob_1'
            print json_blob_1
        # if there's a timeout exception, print some info, and pass
        except socket.timeout:
            print 'hmm timeout... printing tweet, then on to the next one'

            pass
        # update counter
        counter = counter + 1
    SLEEP_TIME = 900
    print "sleeping for %s minutes" % (SLEEP_TIME/60)
    # sleep for 15 minutes 
    time.sleep(SLEEP_TIME)
