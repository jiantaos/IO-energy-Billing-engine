
#!/usr/bin/env python
# coding: utf-8



# PostgreSQL (postgres) is a relational database management system
# postgres operations can be enacted from python using the psycopg2 python library
# this program is a series of functions to perform postgres opeartions using python

import datetime
import calendar
import psycopg2
import yaml
import csv
from urllib.request import urlopen
import json
import pandas as pd


# use a config file config.yaml with the database details to connect to the database
# this funtion returns the variable conn which can then be called for other database operations

def connect():
    
    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)       
            f.close()

            

    except:
        print("Error! Failed to load config file.")
    
    try:
        dbDetails = config['dbDetails']
        
        conn = psycopg2.connect(
            host = dbDetails['hostAddress'],
            port = dbDetails['port'],
            user = dbDetails['user'],
            password = dbDetails['password'],
            database = dbDetails['database'])
        
        cur = conn.cursor()
        
        return conn
    
    except:
        print("Error! Failed to establish a connection to "+dbDetails['hostAddress'])

def initializetable():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS customer_data;')

    cursor.execute("CREATE TABLE customer_data(customer_number integer NOT NULL,siteID VARCHAR(255) NOT NULL,type VARCHAR(255) NOT NULL,units VARCHAR(255) NOT NULL,datetime timestamp NOT NULL,value FLOAT(53) NOT NULL)")
        
    conn.commit()
    conn.close()
        
# printrows function takes the table name as a string as the argument and prints all rows    
  
def printrows(table):
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""SELECT * FROM """+table)
        for row in cur:
            print(row)

        count = cur.rowcount
        print(count, "rows successfully printed")    

        conn.close()
    
    except:
        print("Error! Failed to print rows")
# deletetable deletes all the contents of a given table      
    
def deletetable(table):
    
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""DELETE FROM """+table)
    conn.commit()
    conn.close()

# csvtotable writes the csv to a table given the arguments the csv file path and table name 
# The method is used just for apikeys.csv     
    
def csvtotable_apikeys(csvfile,table):    
    
    conn = connect()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS "+table +";")

    cur.execute("CREATE TABLE "+table+"(siteID VARCHAR(255) NOT NULL, api_key VARCHAR(255) NOT NULL,site_address VARCHAR(255) NOT NULL)")

    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
            cur.execute(
            "INSERT INTO "+table+" VALUES (%s, %s, %s)",
            row
        )
    cur.execute("ALTER TABLE apikeys ADD COLUMN customer_number SERIAL PRIMARY KEY;")

    conn.commit()
    
    conn.close()

# csvtotable writes the csv to a table given the arguments the csv file path and table name 
# The method is used just for XXTenants.csv     
    
def csvtotable_tenants(csvfile,table):    
    
    conn = connect()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS "+table +";")

    cur.execute("CREATE TABLE "+table+"(customer_number integer PRIMARY KEY, tenant VARCHAR(255) NOT NULL,site_address VARCHAR(255) NOT NULL,NMI VARCHAR(255) NOT NULL)")

    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
            cur.execute(
            "INSERT INTO "+table+" VALUES (%s, %s, %s, %s)",
            row
        )
    

    conn.commit()
    
    conn.close()

# rename table to add the given month and year
def rename_table(month,year):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("ALTER TABLE customer_data RENAME TO customer_data_"+month+year+";")

    conn.commit()
    conn.close()


# tablerow returns one row from a given table, where the first row is 1
    
def tablerow(table,rownum):
    
    conn = connect()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM """+table+""" limit 1 offset """+str(rownum-1))
    
    for row in cur:
        return row

# solaredge function uses the SolarEdge Inverter API to return data in json format for energy data  
# keytable is a table with a list of API keys in the database
# rownum is the number row of the site for which data will be returned
# start_date and end_date are the start and end dates, as strings in the format 'YYYY-MM-DD'
# the function returns the siteID and the json data
# eg. solaredge(apikeys,1,'2021-10-01','2021-10-31') returns ('2102764', {'energyDetails': ....)
    
def solaredge(keytable,rownum,start_date,end_date):

    conn = connect()
    cur = conn.cursor()
    
    siteID = tablerow(keytable,rownum)[0]
    APIkey = tablerow(keytable,rownum)[1]
    customer_number = tablerow(keytable,rownum)[3]

    url = "https://monitoringapi.solaredge.com/site/"+siteID+"/energyDetails?meters=SELFCONSUMPTION,PURCHASED&timeUnit=HOUR&startTime="+start_date+"%2000:00:00&endTime="+end_date+"%2023:59:59&api_key="+APIkey

    response = urlopen(url)

    data = json.loads(response.read())
     
    return siteID,data,customer_number

# insert energy writes the json data returned by solaredge() to the initialized customer data table in the database

def insertenergy(keytable,rownum,start_date,end_date):   
    
    conn = connect()
    cursor = conn.cursor()
 
    
    siteID = solaredge(keytable,rownum,start_date,end_date)[0] 
    data = solaredge(keytable,rownum,start_date,end_date)[1]
    customer_number = solaredge(keytable,rownum,start_date,end_date)[2]

    
    
    meters = data['energyDetails']['meters'] # meters refers to different data registers recorded by SolarEdge, eg. SelfConsumption, Purchased
    values = data['energyDetails']['meters'][0]['values'] #values are the recordings returned
  
    # use embedded for loops to return the different types of meters and all values for each
    #cur.execute("DROP TABLE IF EXISTS energy_table;")

    #cur.execute("CREATE TABLE energy_table(siteID VARCHAR(255) NOT NULL,type VARCHAR(255) NOT NULL,units VARCHAR(255) NOT NULL,datetime timestamp NOT NULL,value FLOAT(53) NOT NULL)")
    #print("schemal created")
    row = [0,0,0,0,0,0]

    df = pd.DataFrame([row],columns=['customer_number','siteID', 'type', 'units','datetime','value'])

    for j in meters:
        t = j['type']

        for i in values:
            row[0] = customer_number
            row[1] = siteID
            row[2] = t
            row[3] = data['energyDetails']['unit']
            row[4] = i['date']
            try:
                row[5] = i['value']
            except KeyError:
                row[5] = 0.0
        
            df_length = len(df)
            df.loc[df_length] = row

    df = df.iloc[1:,]
                                         
    # Creating a cursor object
    cursor = conn.cursor()

   

    #loop through the dataframe and insert the energy data stored in the dataframe to postgres table named"customer_data"
    for i,row in df.iterrows():
        #here %S means string values 
        sql = "INSERT INTO customer_data VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, tuple(row))
        # the connection is not auto committed by default, so we must commit to save our changes
        conn.commit()
            #try:
                #record_to_insert = (siteID,t,data['energyDetails']['unit'],i['date'],i['value'])
            #except KeyError:
                #record_to_insert = (siteID,t,data['energyDetails']['unit'],i['date'],0.0)

            #postgres_insert_query = """ INSERT INTO energy_table (siteID, type, units, datetime, value) VALUES (%s,%s,%s,%s,%s)"""
            
            #cursor = conn.cursor()
            
            #cursor.execute(postgres_insert_query, record_to_insert)

            #print(siteID,t,data['energyDetails']['unit'],i['date'],i['value'])
            
    
    conn.close()

# insertenergy("apikeys",1,"2021-10-01","2021-10-31")


# insert many uses insertenergy() and a while loop to insert the data from multiple sites into the customer data table    
    
def insertmany(keytable,firstrow,lastrow,start_date,end_date):
    
    a = firstrow
    b = lastrow + 1
    
    while a < b:
        insertenergy(keytable,a,start_date,end_date)
        a+=1
    
    return 

#  initializetable()
#  insertmany("apikeys",1,5,'2021-10-01','2021-10-31')

#lastrow returns the counted row number of the given table
def lastrow(table):


    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM "+table+";")
    lrow= cur.fetchall()

    return lrow[0][0]


# insert many uses insertenergy() and a while loop to insert data from  all sites into the customer data table 
# change table name to accordingly year and month  
def insertall(keytable,month,year):
    
    initializetable()
    # bill_cycle_start_date is the first date of the month that is billed for
    start_date = str(datetime.date(int(year),int(month),1))
    print(start_date)
    # bill_cycle_end_date is the last date of the month that is billed for 
    end_date = str(datetime.date(int(year),int(month),calendar.monthrange(int(year),int(month))[1]))
    print(end_date)

    
    a = 1
    b = lastrow(keytable) + 1
    
    while a < b:
        insertenergy(keytable,a,start_date,end_date)
        a+=1
    
    rename_table(month,year)
    return 

# insertall("apikeys","10","2021")

# initiate_variables:

billing_days = 31

normal_price = 0.21
night_price = 0.40
weekday_price = 0.295

self_consum_price = 0.25

normal_usage = 0
night_usage = 0
weekday_usage = 0

# calculate grid charges from different database stuff

def grid_energy_charges():

    conn = connect()
    cursor = conn.cursor()

    # postgred query according to the price plan

    # Add a weekday column to present the weekday of datetime
    # generate charges for grid data
    cursor.execute("SELECT value FROM customer_data WHERE (type = 'Purchased' and date_part('hour', datetime)<= 7) or (type = 'Purchased' and date_part('hour', datetime)>= 17) or (type = 'Purchased' and EXTRACT(DOW FROM datetime) = 6 and date_part('hour', datetime)>=7 and date_part('hour', datetime)<21) or (type = 'Purchased' and EXTRACT(DOW FROM datetime) = 0 and date_part('hour', datetime)>=7 and date_part('hour', datetime)<21);")
    results = cursor.fetchall()
    normal_usage = sum(e[0] for e in results)

    cursor.execute("SELECT value FROM customer_data WHERE (type = 'Purchased' and date_part('hour', datetime) >= 17 and date_part('hour', datetime) < 21) ;")
    results = cursor.fetchall()
    night_usage = sum(e[0] for e in results)

    cursor.execute("SELECT value FROM customer_data WHERE (type = 'Purchased' and EXTRACT(DOW FROM datetime) >= 0 and EXTRACT(DOW FROM datetime) <= 4 and date_part('hour', datetime) >= 7 and date_part('hour', datetime) < 17);")
    results = cursor.fetchall()
    weekday_usage = sum(e[0] for e in results)
        
    # conver usage from W to kW
    normal_usage = normal_usage/1000
    night_usage = night_usage/1000
    weekday_usage = weekday_usage/1000

    total_usage = normal_usage + night_usage + weekday_usage

    total_import_charges = normal_price * normal_usage + night_price * night_usage + weekday_price * weekday_usage
    print(total_import_charges)

    return total_import_charges

def rooftop_energy_charges():
    
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM customer_data where (type = 'SelfConsumption');")
    results = cursor.fetchall()
    self_consum_usage = sum(e[0] for e in results)

    #convert W to kW
    self_consum_usage = self_consum_usage/1000

    self_consum_charges = self_consum_usage * self_consum_price
    print(self_consum_charges)

    return self_consum_charges


# csvtotable_apikeys("apikeys.csv","apikeys")
# csvtotable_tenants("Mount Barker Shopping Centre Tenancies.csv","Tenants")

   












