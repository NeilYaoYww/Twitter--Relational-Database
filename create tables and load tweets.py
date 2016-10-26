# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 19:13:29 2016

@author: Weiwei Yao
"""

'''
CSC455
FINAL PROJECT
Weiwei Yao
'''
import urllib.request as urllib
import json
import sqlite3
import time



# 1. a.Create a 3rd table incorporating the Geo table (in addition to tweet and user tables that you already have) and extend your schema accordingly.
#create tweet table
tweet='''CREATE TABLE tweet
(created_at VARCHAR(50), 
id_str NUMBER(20), 
text VARCHAR(500), 
source VARCHAR(120), 
in_reply_to_user_id NUMBER(15), 
in_reply_to_screen_name VARCHAR(25), 
in_reply_to_status_id NUMBER(20), 
retweet_count NUMBER(10), 
contributors VARCHAR(4),
user_id NUMBER(20),
CONSTRAINT tweetPK PRIMARY KEY (id_str),
CONSTRAINT tweetFK FOREIGN KEY(user_id) REFERENCES user(id)
);'''

#create user table
user='''CREATE TABLE user
(id NUMBER(20),
name VARCHAR(20),
screen_name VARCHAR(20), 
description VARCHAR(300), 
friends_count NUMBER(10),
CONSTRAINT userPK PRIMARY KEY (id),
CONSTRAINT userFK FOREIGN KEY(id) REFERENCES geo(userid));
'''

#create geo table
geo='''CREATE TABLE geo
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
userid NUMBER(20),
longitude float(20), 
latitude float(20), 
type VARCHAR(30));
'''

# Open a connection to database
conn = sqlite3.connect("CSC455-FinalP.db")

# Request a cursor from the database
cursor = conn.cursor()

# Get rid of the tweet table if we already created it
cursor.execute("DROP TABLE IF EXISTS tweet;")
cursor.execute("DROP TABLE IF EXISTS user;")
cursor.execute("DROP TABLE IF EXISTS geo;")
# Create the table in tweet.db
cursor.execute(geo)
cursor.execute(user)
cursor.execute(tweet)

# 1.b.	Use python to download from the web and save to a local text file (not into database yet) at least 500,000 lines worth of tweets. Test your code with fewer rows first – you can reduce the number of tweets if your computer is running too slow to handle 500K tweets in a reasonable time. How long did it take to save?
response = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")
#f = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\alltweet.txt","wb")
f= open("alltweet.txt","wb")
start = time.time()
for i in range(500000): #read 500,000 tweets
    lines = response.readline()
    f.write(lines)
end= time.time()
print ("Difference is ", (end-start), 'seconds')
print ("Difference is ", (end-start)/60, 'minutes')
print ("Performance : ", 500000/(end-start), ' operations per second ')
'''
Difference is  228.05480337142944 seconds
Difference is  3.800913389523824 minutes
Performance :  2192.455465126325  operations per second
'''

# 1.c Repeat what you did in part-b, but instead of saving tweets to the file, populate the 3-table schema that you created in SQLite. Be sure to execute commit and verify that the data has been successfully loaded (report row counts for each of the 3 tables). If you use the posted example code be sure to turn off batching for this part. (i.e., batchRows set to 1). How long did this step take?

errorcount=0
start = time.time()
for i in range(500000):
    try:
        line = response.readline().decode("utf8")
        jsonobject=json.loads(line)
        if 'retweeted_status' in jsonobject.keys():
            retweetcount = jsonobject['retweeted_status']['retweet_count']
        else:
            retweetcount = jsonobject['retweet_count']
        cursor.execute("INSERT OR IGNORE INTO user VALUES(?,?,?,?,?);",(jsonobject['user']['id'], jsonobject['user']['name'], jsonobject['user']['screen_name'],
        jsonobject['user']['description'], jsonobject['user']['friends_count']))    
    
        cursor.execute("INSERT OR IGNORE INTO tweet VALUES (?,?,?,?,?,?,?,?,?,?);",(jsonobject['created_at'], jsonobject['id_str'], jsonobject['text'],
        jsonobject['source'], jsonobject['in_reply_to_user_id'], jsonobject['in_reply_to_screen_name'],
        jsonobject['in_reply_to_status_id'], retweetcount, jsonobject['contributors'], jsonobject['user']['id'] ))   
        
        if jsonobject['geo'] != None:
            cursor.execute("INSERT OR IGNORE INTO geo(userid,longitude,latitude,type) VALUES (?,?,?,?);",(jsonobject['user']['id'], jsonobject['geo']['coordinates'][0], 
                           jsonobject['geo']['coordinates'][1],jsonobject['geo']['type']))
        else:
            continue
    except (ValueError):
        errorcount+=1
print(errorcount)
end= time.time()
print ("Difference is ", (end-start), 'seconds')
print ("Difference is ", (end-start)/60, 'minutes')
print ("Performance : ", 500000/(end-start), ' operations per second ')
'''
Difference is  161.05110335350037 seconds
Difference is  2.684185055891673 minutes
Performance :  3104.6046229346293  operations per second 
'''   

RowsforTw=cursor.execute("SELECT * FROM tweet;").fetchall()   
len(RowsforTw)
'''Out[21]: 499776'''
RowsforUs=cursor.execute("SELECT * FROM user;").fetchall()
len(RowsforUs)   
'''Out[22]: 447304'''
RowsforGe=cursor.execute("SELECT * FROM geo;").fetchall()   
len(RowsforGe)
'''Out[23]: 11986'''
f.close() 
cursor.close()
conn.commit()
conn.close()

# 1.d Use your locally saved tweet file (created in part-b) to repeat the database population step from part-c. That is, load 500,000 tweets into the 3-table database using your saved file with tweets (do not use the URL to read twitter data). How does the runtime compare with part-c?
f=open("alltweet.txt","r",encoding="utf8")
#f = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\alltweet.txt","r",encoding="utf8")
alllines=f.readlines()
errorcount=0
start = time.time()
for line in alllines:
    try:
        #line = response.readline().
        jsonobject=json.loads(line)
        if 'retweeted_status' in jsonobject.keys():
            retweetcount = jsonobject['retweeted_status']['retweet_count']
        else:
            retweetcount = jsonobject['retweet_count']
        
        cursor.execute("INSERT OR IGNORE INTO user VALUES(?,?,?,?,?);",(jsonobject['user']['id'], jsonobject['user']['name'], jsonobject['user']['screen_name'],
        jsonobject['user']['description'], jsonobject['user']['friends_count']))    
    
        cursor.execute("INSERT OR IGNORE INTO tweet VALUES (?,?,?,?,?,?,?,?,?,?);",(jsonobject['created_at'], jsonobject['id_str'], jsonobject['text'],
        jsonobject['source'], jsonobject['in_reply_to_user_id'], jsonobject['in_reply_to_screen_name'],
        jsonobject['in_reply_to_status_id'], retweetcount, jsonobject['contributors'], jsonobject['user']['id'] ))   
        
        if jsonobject['geo'] != None:
            cursor.execute("INSERT OR IGNORE INTO geo(userid,longitude,latitude,type) VALUES (?,?,?,?);",(jsonobject['user']['id'], jsonobject['geo']['coordinates'][0], 
                           jsonobject['geo']['coordinates'][1],jsonobject['geo']['type']))
        else:
            continue
    except ValueError:
        errorcount+=1
f.close()
print(errorcount)
end= time.time()
print ("Difference is ", (end-start), 'seconds')
print ("Difference is ", (end-start)/60, 'minutes')
print ("Performance : ", 500000/(end-start), ' operations per second ')
'''
0
Difference is  40.301029682159424 seconds
Difference is  0.6716838280359904 minutes
Performance :  12406.630896116816  operations per second 
Compared to part c, it is 120 seconds faster.
'''    

# 1. e Re-run the previous step with batching size of 500 (i.e. by inserting 500 rows at a time with executemany). You can adapt the posted example code. How does the runtime compare when batching is used?

# Open a connection to database
conn = sqlite3.connect("CSC455-FinalP-Batching.db")

# Request a cursor from the database
c = conn.cursor()

# Get rid of the tweet table if we already created it
c.execute("DROP TABLE IF EXISTS tweet;")
c.execute("DROP TABLE IF EXISTS user;")
c.execute("DROP TABLE IF EXISTS geo;")
# Create the table in tweet.db
c.execute(geo)
c.execute(user)
c.execute(tweet)

start   = time.time()
def batching(tweets):
    batchRows = 500
    batchdgeo = []   
    batchdtwe = []
    batchduse = []
    while len(tweets) > 0:
        line = tweets.pop(0)
        jsonobject = json.loads(line)
        
        #geo table
        geoline=[]
        if jsonobject['geo'] != None:
            geoline.append(jsonobject['user']['id'])           
            geoline.append(jsonobject['geo']['coordinates'][0])
            geoline.append(jsonobject['geo']['coordinates'][1])
            geoline.append(jsonobject['geo']['type'])

            '''if jsonobject['geo']['coordinates'] != None:
                geoline=[jsonobject['user']['id'], jsonobject['geo']['coordinates'][0], jsonobject['geo']['coordinates'][1], jsonobject['geo']['type']]
            else:
                geoline=[jsonobject['user']['id'], 'NULL', 'NULL', jsonobject['geo']['type']]'''
            batchdgeo.append(geoline)  
               
        if len(batchdgeo) >= batchRows or len(tweets) == 0:
            c.executemany('INSERT OR IGNORE INTO geo(userid,longitude,latitude,type) VALUES(?,?,?,?)', batchdgeo)
            batchdgeo = []
           
        #tweet
        tweetline=[]
        if 'retweeted_status' in jsonobject.keys():
            retweetcount = jsonobject['retweeted_status']['retweet_count']
        else:
            retweetcount = jsonobject['retweet_count']
        tweetline=[jsonobject['created_at'], jsonobject['id_str'], jsonobject['text'],jsonobject['source'], jsonobject['in_reply_to_user_id'], jsonobject['in_reply_to_screen_name'],
                   jsonobject['in_reply_to_status_id'], retweetcount, jsonobject['contributors'], jsonobject['user']['id']]
        batchdtwe.append(tweetline)
        
        if len(batchdtwe) >= batchRows or len(tweets) == 0:
            c.executemany('INSERT OR IGNORE INTO tweet VALUES (?,?,?,?,?,?,?,?,?,?)', batchdtwe)
            batchdtwe = []
           
    
        #user
        userline=[]
        userline=[jsonobject['user']['id'], jsonobject['user']['name'], jsonobject['user']['screen_name'],
                  jsonobject['user']['description'], jsonobject['user']['friends_count']]
        batchduse.append(userline)
        if len(batchduse) >= batchRows or len(tweets) == 0:
            c.executemany('INSERT OR IGNORE INTO user VALUES(?,?,?,?,?)', batchduse)
            batchduse = []


f=open("alltweet.txt","r",encoding="utf8")
alllines=f.readlines()
batching(alllines)
end   = time.time()
f.close()
print ("Batching took ", (end-start), ' seconds.')
'''
Batching took  94.27300000190735  seconds.
In my case, batching is about 50 seconds slower than non-batching.
'''

RowsforGe=c.execute("SELECT * FROM geo;").fetchall()   
len(RowsforGe)
'''Out[53]: 11986'''
Rowsforus=c.execute("SELECT * FROM user;").fetchall()   
len(Rowsforus)
'''Out[54]: 447304'''
Rowsfortw=c.execute("SELECT * FROM tweet;").fetchall()   
len(Rowsfortw)
'''Out[55]: 499776'''

c.close()
conn.commit()
conn.close()
