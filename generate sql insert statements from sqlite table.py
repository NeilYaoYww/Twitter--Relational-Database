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
3. a
Export the contents of the User table from a SQLite table into a sequence of INSERT statements within a file. 
This is very similar to what you did in Assignment 4. However, you have to add a unique ID column which has to be a string (you cannot use any numbers). 
Hint: one possibility is to replace digits with letters, e.g., chr(ord('a')+1) gives you a 'b' and chr(ord('a')+2) returns a 'c'
'''

def insertsfromtable(table):
    n=0
    results = cursor.execute('SELECT * FROM ' + table + ';').fetchall()
    output = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\userinsert.txt", 'w')
    for rows in results:
        unicol=  "'" +str(rows[1].encode('utf8')).replace("'", "") + chr(ord('a')+n%24) +"'"  #create a unique string column

        #unicol="'" + str(unicol.encode('utf8')).replace("'", "") + "'"
        insert = 'INSERT INTO ' + table + ' VALUES ('  + unicol  + ', '
        for attr in rows:
            # Convert None to NULL
            if attr == None: 
                insert = insert + 'NULL' + ', '
            else:
                if isinstance(attr, (int, float)):
                    value = str(attr)
                else: 
                    # Escape all single quotes in the string
                    value = "'" + str(attr.encode('utf8')).replace("'", "") + "'"
                    
                insert = insert + value + ', '
        
        insert = insert[:-2] + '); \n'
        output.write(insert)
        n+=1
    print(n)    
    output.close()
    
start = time.time()
insertsfromtable('user')
end = time.time()
print ("Difference is ", (end-start), 'seconds')


'''
447304
Difference is  6.080479145050049 seconds
'''
output = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\userinsert.txt", 'r')
for i in range(2):
    row=output.readline()
    print(row)
output.close()
'''
INSERT INTO user VALUES ('bWisdom Inka', 213646047, 'bWisdom Ink', 'bWisdom_Ink', 'bWisdom Ink Online Magazine:  Expressing our #joy & #love via our articles. Celebrating diversity & the growth of #consciousness. #zen #meditation #spiritual', 4821); 

INSERT INTO user VALUES ('bYarer Sofierb', 38950479, 'bYarer Sofier', 'bfirekites', 'bVisite nuestro stand en la planta cuarta. Gran liquidaci\xc3\xb3n en rev\xc3\xb3lveres, cuchillos y todos los complementos de la mujer inquieta.', 99); 
'''

'''
3. b
Create a similar collection of INSERT for the User table by reading/parsing data from the local tweet file that you have saved earlier. 
How do these compare in runtime? Which method was faster?
'''
def insertsfromtxt(table):
    f = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\alltweet.txt","r",encoding="utf8")
    alllines=f.readlines()
    f.close()
    output = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\txtuserinsert.txt", 'w')
    n=0
    for line in alllines:
        try:
            jsonobject=json.loads(line)
            for i in ['name','id','screen_name','description','friends_count']: 
                if jsonobject['user'][i] == None:  #convert none to null
                    jsonobject['user'][i] = 'NULL'
                else:
                    if type(jsonobject['user'][i]) in [int, float]: #format numbers and floats
                        jsonobject['user'][i]=str(jsonobject['user'][i])
                    else: #format strings
                        jsonobject['user'][i]="'" + str(jsonobject['user'][i].encode('utf8')).replace("'", "") + "'"
            
            unicol=  "'" +str(jsonobject['user']['name'].encode('utf8')).replace("'", "") + chr(ord('a')+n%24) +"'"  ##create a unique string column
            insert='INSERT OR IGNORE INTO ' + table + ' VALUES ('  + unicol  + ', ' + jsonobject['user']['id'] + ', '+jsonobject['user']['name']+', ' + jsonobject['user']['screen_name'] + ', '+jsonobject['user']['description'] + ', ' + jsonobject['user']['friends_count'] + '); \n'
            output.write(insert)
            n+=1
        except:
            continue
    print(n)    
    output.close()
          
start = time.time()
insertsfromtxt('user')
end = time.time()
print ("Difference is ", (end-start), 'seconds')
'''
500000
Difference is  41.264307498931885 seconds
Exproting from the existing SQL table is faster(about 35 seconds).
'''

output = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\txtuserinsert.txt", 'r')
for i in range(2):
    row=output.readline()
    print(row)
output.close()
'''
INSERT OR IGNORE INTO user VALUES ('b"bWisdom Ink"a', 213646047, 'bWisdom Ink', 'bWisdom_Ink', 'bWisdom Ink Online Magazine:  Expressing our #joy & #love via our articles. Celebrating diversity & the growth of #consciousness. #zen #meditation #spiritual', 4821); 

INSERT OR IGNORE INTO user VALUES ('b"bYarer Sofier"b', 38950479, 'bYarer Sofier', 'bfirekites', 'bVisite nuestro stand en la planta cuarta. Gran liquidaci\xc3\xb3n en rev\xc3\xb3lveres, cuchillos y todos los complementos de la mujer inquieta.', 99); 
'''


# 4. a
geo=cursor.execute("SELECT * FROM geo;").fetchall()
start = time.time()
n=0
unknown=0
geooutput = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\geo.txt", 'w')
for line in geo:
    #line=list(line)
    #
    #print(type(line))
    if line[2] != None and line[3] != None:
    #try: #round longitude and latitude to a maximum of 4 digits after the decimal
        long=line[2]
        long=round(long,4)
        lang=line[3]
        lang=round(lang,4)
        #insert= "'"+ str(line[0])+ '| ' + str(line[1])+ '| ' + str(long) +'| ' + str(lang) + '| ' + str(line[4])+ "'" +'\n'
        #geooutput.write(insert)
    else:  #catch ‘Unknown’ location 
        long='Unknown'
        lang='Unknown'
        unknown+=1
    insert= str(line[0])+ ' | ' + str(line[1])+ ' | ' + str(long) +' | ' + str(lang) + ' | ' + str(line[4])
    insert += '\n'
    geooutput.write(insert)
    n+=1
print('There are '+str(unknown)+ ' unknown values.')
print(str(n),'rows are written to the file')
geooutput.close()
end = time.time()
print ("Difference is ", (end-start), 'seconds')
'''
There are 0 unknown values.
11986 rows are written to the file
Difference is  0.07813143730163574 seconds
'''

geooutput = open("C:\\Users\\Weiwei Yao\\Desktop\\CSC-455\\Final Project\\geo.txt", 'r')
for i in range(5):
    row=geooutput.readline()
    print(row)
geooutput.close()
'''
1 | 160370249 | 14.6703 | 121.044 | Point

2 | 233079540 | -7.3519 | 110.2135 | Point

3 | 146612119 | 47.8487 | -122.222 | Point

4 | 348864517 | 38.7677 | -77.1596 | Point

5 | 128825864 | -6.1494 | 106.729 | Point
'''

# 4. b

# 4. c

a=[2,3,4,5,6,7]
a.replace(',','|')