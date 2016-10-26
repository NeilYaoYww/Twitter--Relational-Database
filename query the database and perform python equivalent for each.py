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

# Open a connection to database
conn = sqlite3.connect("CSC455-FinalP.db")

# Request a cursor from the database
cursor = conn.cursor()

'''
2.a Write and execute SQL queries to do the following. Don’t forget to report the running times in each part – you do not need to report the output:
2.a.i
Find tweets where tweet id_str contains “44” or “77” anywhere in the column
'''

start = time.time()
i=cursor.execute("SELECT id_str FROM Tweet WHERE id_str LIKE '%44%' OR id_str LIKE '%77%';").fetchall()  
print(len(i))
end= time.time()
print ("Difference is ", (end-start), 'seconds')
print ("Performance : ", len(i)/(end-start), ' operations per second ')
'''
99203
Difference is  9.775977611541748 seconds
Performance :  10147.629622522725  operations per second 
'''

'''
2.a.ii
Find how many unique values are there in the “in_reply_to_user_id” column
'''
start = time.time()
ii=cursor.execute("SELECT COUNT (DISTINCT in_reply_to_user_id) FROM tweet;").fetchall()  
print(ii)
end= time.time()
print ("Difference is ", (end-start), 'seconds')
'''
[(90524,)]
Difference is  21.07410717010498 seconds
'''


'''
2.a.iii
Find the tweet(s) with the longest text message
'''
start = time.time()
iii=cursor.execute("SELECT text FROM tweet WHERE length(text)=(SELECT max(length(text)) FROM Tweet);").fetchall()  
print(iii)
end= time.time()
print ("Difference is ", (end-start), 'seconds')
'''
[('RT @Yoledingo: &lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt; http://t.co/7IqaxAzmFV vi…',)]
Difference is  0.593787670135498 seconds
'''

'''
2.a.iv
Find the average longitude and latitude value for each user name.
'''
start = time.time()
iv=cursor.execute("SELECT geo.userid, user.name, AVG(longitude), AVG(latitude) FROM geo LEFT JOIN user ON user.id=geo.userid GROUP BY geo.userid;").fetchall() 
print(len(iv))
iv[0:3]
end= time.time()
print ("Difference is ", (end-start), 'seconds')
print ("Performance : ", len(iv)/(end-start), ' operations per second ')
'''
11405
Difference is  0.05200505256652832 seconds
Performance :  230419.91900057308  operations per second 
Out[31]: 
[(7819, 'Cody Landefeld', 33.48155, -112.073076),
 (355203, 'Jacqui Maher', 40.6895, -73.973056),
 (647853, 'ゼビウス', 4.691722, -74.034499)]
'''


'''
2.a.v
Re-execute the query in part iv) 10 times and 100 times and measure the total runtime (just re-run the same exact query using a for-loop). 
Does the runtime scale linearly? (i.e., does it take 10X and 100X as much time?)
'''
start = time.time()
for i in range(10):
    cursor.execute("SELECT geo.userid, AVG(longitude), AVG(latitude) FROM geo, tweet WHERE tweet.id_str=geo.userid GROUP BY geo.userid;").fetchall()
end= time.time()
print ("Difference is ", (end-start), 'seconds')
'''
Difference is  0.5080509185791016 seconds
'''

start = time.time()
for i in range(100):
    cursor.execute("SELECT geo.userid, AVG(longitude), AVG(latitude) FROM geo, tweet WHERE tweet.id_str=geo.userid GROUP BY geo.userid;").fetchall()
end= time.time()
print ("Difference is ", (end-start), 'seconds')
'''
Difference is  5.025502681732178 seconds
The runtime does scale linearly. The runtime of 100x is 10 times as that of 10x.
'''

'''
2.b
Write python code that is going to read the locally saved tweet data file from 1-b and perform the equivalent computation for parts 2-i and 2-ii only. 
How does the runtime compare to the SQL queries?
'''
start = time.time()
f = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\alltweet.txt","r",encoding="utf8")
alllines=f.readlines()
n=0
i=[]
for line in alllines:

    jsonobject=json.loads(line)
    if '44' in str(jsonobject['id_str']) or '77' in str(jsonobject['id_str']):
        n+=1
        #i.append(jsonobject)

print(n)
end= time.time()
print ("Difference is ", (end-start), 'seconds') 
f.close()           
'''
99248
Difference is 36.17661714553833 seconds
The runtime is roughly 26 seconds slower than sql queries.
'''

start = time.time()
#f = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\alltweet.txt","r",encoding="utf8")
#alllines=f.readlines()
n=0
i=[]
for line in alllines:
    jsonobject=json.loads(line)
    rid=jsonobject['in_reply_to_user_id'] 
    if rid not in i:
        i.append(rid)
        n+=1
print(n)
end= time.time()
print ("Difference is ", (end-start), 'seconds')    
f.close()
'''
90525
Difference is  103.07430648803711 seconds
The runtime is roughly 80 seconds slower than sql queries.
'''

'''
2.c
Extra-credit: Perform the python equivalent for 2-iii
'''
start = time.time()
f = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\alltweet.txt","r",encoding="utf8")
alllines=f.readlines()
n=0
text=''
for line in alllines:
    jsonobject=json.loads(line)
    textlen=len(jsonobject['text'])
    if textlen>n:
        n=textlen
        text=jsonobject['text']
print(n,text)
end= time.time()
print ("Difference is ", (end-start), 'seconds') 
f.close()  
'''
434 RT @Yoledingo: &lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt; http://t.co/7IqaxAzmFV vi…
Difference is  278.7839376926422 seconds
'''


'''
2.d
Extra-credit: Perform the python equivalent for 2-iv
'''
start = time.time()
f = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\alltweet.txt","r",encoding="utf8")
alllines=f.readlines()
f.close()  
users={}
n=0
for line in alllines:
    try:
        jsonobject=json.loads(line)
        if jsonobject['geo'] != None: 
            name=str(jsonobject['user']['name'])
            if name not in users: 
                users[name]=[jsonobject['geo']['coordinates'][0]] #for distinct users, record longitude and latitude 
                users[name].append(jsonobject['geo']['coordinates'][1])           
                users[name].append(1)
            else: # for users with multiple records, create sum and count for further analysis
                users[name][0]+=jsonobject['geo']['coordinates'][0]
                users[name][1]+=jsonobject['geo']['coordinates'][1]
                users[name][2]+=1
    except KeyError:
        n+=1
print(n)
print(len(users))
'''
0
11036
'''
for i in users.keys():
    if users[i][2]>1:
        users[i][0]=users[i][0] / users[i][2] #calculate average for longitude
        users[i][1]=users[i][1] / users[i][2] #calculate average for latitude 
   
end= time.time()
print ("Difference is ", (end-start), 'seconds') 
'''
Difference is  116.42418384552002 seconds
Reading from SQL is way more fast than reading from txt file.
'''

countKeys = users.keys()
countVals = users.values()
countPairs = zip(countVals, countKeys)
#sort the zip based on coutVals
frequency=sorted(countPairs, key=lambda x: x[0])
frequency[-4:]
'''
Out[43]: 
[([62.586906, 39.839572, 1], 'Викуля'),
 ([63.996352, -22.622959, 1], 'Lady Pecan'),
 ([64.592585, 40.59022, 1], 'никто иной'),
 ([64.85704, -147.690908, 1], 'kJt. ')]
'''

cursor.close()
conn.commit()
conn.close()

