# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 20:19:28 2016

@author: Weiwei Yao
"""

'''
CSC455
FINAL PROJECT
Weiwei Yao
'''

'''
4. Export all three tables (Tweet, User and Geo tables) from the database into a |-separated text file. 
In this part, you do not have to modify the table within the database, just output file data (do not generate INSERT statements, just raw data)

4.a
For the Geo table, create a single default entry for the ‘Unknown’ location and round longitude and latitude to a maximum of 4 digits after the decimal.
'''
import os
#os.chdir("C:\\Users\\WYAO2\\Desktop\\CSC455-Final")
os.chdir("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project")

geo=cursor.execute("SELECT * FROM geo;").fetchall()
start = time.time()
n=0
#geooutput = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\geo.txt", 'w')
geooutput = open("geo.txt", 'w')
for line in geo:
    insert=''
    for item in line:
        if item == None: #convert Nones to Null
            insert += 'NULL' + '| '
        else:
            if type(item) in [int,float]:  #round longitude and latitude to a maximum of 4 digits after the decimal
                insert += str(round(item, 4)) + '| '
            else:
                insert += item + '| '
    insert+= '\n'
    geooutput.write(insert)
    n+=1

geooutput.write(str(n+1)+ "| unknown |unknown |unknown| unknown|") #create an unknown entry
print(str(n),'rows are written to the file')
geooutput.close()
end = time.time()
print ("Difference is ", (end-start), 'seconds')
'''
11986 rows are written to the file
Difference is  0.07813143730163574 seconds
'''

#geooutput = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\geo.txt", 'r')
geooutput = open("geo.txt", 'r')
for i in range(5):
    row=geooutput.readline()
    print(row)
geooutput.close()
'''
1| 160370249| 14.6703| 121.044| Point| 

2| 233079540| -7.3519| 110.2135| Point| 

3| 146612119| 47.8487| -122.222| Point| 

4| 348864517| 38.7677| -77.1596| Point| 

5| 128825864| -6.1494| 106.729| Point| 

11987| unknown |unknown |unknown| unknown|
'''

'''
4.b
For the Tweet table, replace NULLs by a reference to ‘Unknown’ entry (i.e., the foreign key column that references Geo table should 
refer to the “Unknown” entry you created in part-a. Report how many known/unknown locations there were in total 
(e.g., 10,000 known, 490,000 unknown,  2% locations are available)
'''
tweet=cursor.execute("SELECT * FROM tweet LEFT JOIN (SELECT ID,userid, longitude, latitude FROM geo)Y ON tweet.user_id=Y.userid;").fetchall() #join the tweet and geo table


start = time.time()
n=0
unknown=0
known=0
#geooutput = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\geo.txt", 'w')
tweetoutput = open("tweet.txt", 'w')
for line in tweet:
    insert=''
    location=''
    line=list(line)
    if line[-4]==None: #count the unknown
        location=str(11987) #refer to unknown entry I created in 4.a
        unknown+=1 
    else: #count the known
        location=str(line[-4]) #refer to the ID in geo table
        known+=1
    for item in line[0:-4]:
        if item == None: #convert Nones to Null
            insert += 'NULL' + '| '
        else:
            if type(item) in [int,float]:  
                insert += str(item) + '| '
            else:
                insert += "'" +str(item.encode('utf8')).replace("'", "") + "'" + '| '
    insert+=location
    insert+= '\n'
    tweetoutput.write(insert)
    n+=1 #count the total number
  
print(str(n),'rows are written to the file')
print(str(unknown),'unknown locations')
print(str(known),'known locations')
print(str(percent),'% locations are available')
tweetoutput.close()
end = time.time()
percent= round((known/n)*100,2)

print ("Difference is ", (end-start), 'seconds')
'''
501180 rows are written to the file
487028 unknown locations
14152 known locations
2.82 % locations are available
Difference is  7.630326986312866 seconds
'''
tweetoutput = open("tweet.txt", 'r')
for i in range(5):
    row=tweetoutput.readline()
    print(row)
tweetoutput.close()
'''
'bThu May 29 00:00:43 +0000 2014'| 471803285746495489| 'bThere is no wealth but life. ~John Ruskin #wisdomink'| 'b<a href="http://www.hootsuite.com" rel="nofollow">HootSuite</a>'| NULL| NULL| NULL| 0| NULL| 213646047| 11987

'bThu May 29 00:00:43 +0000 2014'| 471803285738106880| 'bMucho la Plop esto, la Plop aquello, pero de los viernes es la fiesta con la gente m\xc3\xa1s linda. \nEn las otras vienen directo de la frontera.'| 'bweb'| NULL| NULL| NULL| 0| NULL| 38950479| 11987

'bThu May 29 00:00:43 +0000 2014'| 471803285767462913| 'bmotive. When a political idea finds its way into such heads,'| 'b<a href="http://eto-secret4.ru" rel="nofollow">eto prosto NEW secret</a>'| NULL| NULL| NULL| 0| NULL| 2443526930| 11987

'bThu May 29 00:00:43 +0000 2014'| 471803285750681600| 'b@im_2realbih bol!'| 'b<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>'| 290322075| 'bim_2realbih'| 471800733541486600| 0| NULL| 284813188| 11987

'bThu May 29 00:00:43 +0000 2014'| 471803285759078401| 'bA veces no entendemos por que, cuando, donde , como y ahora que hago, por que . Dios es perfecto y a veces... http://t.co/iCyBxph8s9'| 'b<a href="http://www.facebook.com/twitter" rel="nofollow">Facebook</a>'| NULL| NULL| NULL| 0| NULL| 146270795| 11987
'''


'''
4.c
For the User table file add a column (true/false) that specifies whether “screen_name” or “description” attribute contains within it the “name” attribute 
of the same user. That is, your output file should contain all of the columns from the User table, plus the new column. 
You do not have to modify the original User table.
'''
user=cursor.execute("SELECT * FROM user;").fetchall()
start = time.time()
n=0
#geooutput = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\geo.txt", 'w')
useroutput = open("user.txt", 'w')
for line in user:
    insert=''
    line=list(line)
    for item in line:
        if item == None: #convert Nones to Null
            insert += 'NULL' + '| '
        else:
            if type(item) in [int,float]:  
                insert += str(item) + '| '
            else:
                insert += "'" +str(item.encode('utf8')).replace("'", "") + "'" + '| '
    if str(line[1]) in str(line[2]) or str(line[1]) in str(line[3]):
        insert += "True| " 
    else:
        insert += "False| "     
    insert+= '\n'
    useroutput.write(insert)
    n+=1
    
print(str(n),'rows are written to the file')
useroutput.close()
end = time.time()
print ("Difference is ", (end-start), 'seconds')
'''
447304 rows are written to the file
Difference is  7.343000173568726 seconds
'''
useroutput = open("user.txt", 'r')
for i in range(5):
    row=useroutput.readline()
    print(row)
useroutput.close()

'''
213646047| 'bWisdom Ink'| 'bWisdom_Ink'| 'bWisdom Ink Online Magazine:  Expressing our #joy & #love via our articles. Celebrating diversity & the growth of #consciousness. #zen #meditation #spiritual'| 4821| True| 

38950479| 'bYarer Sofier'| 'bfirekites'| 'bVisite nuestro stand en la planta cuarta. Gran liquidaci\xc3\xb3n en rev\xc3\xb3lveres, cuchillos y todos los complementos de la mujer inquieta.'| 99| False| 

2443526930| 'bVera Luciani'| 'brosaxonahag'| 'bProud coffee advocate ; studies in  # all about-Devoted alcohol lover .'| 261| False| 

284813188| 'bJ e s s'| 'b_SameOleSHIT'| NULL| 683| False| 

146270795| 'brocio murillo lopez'| 'bgomitatica'| NULL| 4| False| 
'''
