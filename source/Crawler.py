#run the code in 虛擬環境

#database
import codecs
import mysql.connector
import time
import serial
#spider
import requests
from bs4 import BeautifulSoup
import serial
from time import sleep

mydb = mysql.connector.connect(
       host = "localhost",   # Database IP address
       user = "# Database username",    # Database username 
       passwd = "# Database password",   # Database password
       database = "# Database name"     # Database name
    )

no=1
data=[]#declare a list
temp=""#溫度
rain_chance=""#降雨機率
humidity=""#濕度
ray=""#紫外線
air=""#空氣品質
wind_speed=""#風速

def get_web_content():
    page=requests.get('https://weather.yam.com/%E6%A5%A0%E6%A2%93%E5%8D%80/%E9%AB%98%E9%9B%84%E5%B8%82')#goverment website cannot get the info. we want
    #print(page.status_code)#check, if output=200,then success
    return page.text#HTML source code

def get_info_weather():
    soup=BeautifulSoup(get_web_content(),'html.parser')
    #print(soup.text) print content we get and without HTML tags
    tmp=soup.find('div',class_='detail').find_all('p','')#type:bs4.element.ResultSet
    global data# will modify the global variable
    global temp
    global rain_chance
    global humidity
    global ray
    global air
    global wind_speed

    for i in tmp:
        data.append(str(i))#cannot write "global data.append()"
    #for d in data:
        #print(d)
        
    temp=data[0][3:-4]
    rain_chance=data[1][3:-4]
    humidity=data[2][3:-4]
    ray=data[3][3:-4]
    air=data[4][3:-4]
    wind_speed=data[5][3:-4]
    #print(temp)  體感溫度 : 14℃
    #print(rain_chance)  降雨機率 : 20%
    #print(humidity)  相對濕度 : 86%
    #print(ray)  紫外線 : 0 (低量級)
    #print(air)  空氣品質 : 普通
    #print(wind_speed)  風速 : 5km/h
    
#database
def connect_DB():
    mycursor = mydb.cursor()#execute up instruction
    mycursor.execute("INSERT INTO data (no,temperature,rain_chance,humidity,ray,air,wind_speed) VALUES('"+ str(no) + "','""','""','""','""','""','""')")
    
def input_DB():
    
    mycursor = mydb.cursor()#execute up instruction
    
    #Insert data to table
    
    mycursor.execute("UPDATE data SET temperature='"+temp+"',rain_chance='"+rain_chance+"',humidity='"+humidity+"',ray='"+ray+"',air='"+air+"',wind_speed='"+wind_speed+"'WHERE no=1")
    mydb.commit()    # table内容有更新，必須使用此句
    print("Insert data compeleted.\n")
    
    
get_info_weather()
connect_DB()
input_DB()
