import sqlite3
import pandas as pd
import psycopg2
import mysql.connector as msql
from mysql.connector import Error

dataset= pd.read_csv('D:\IO energy internship\multiple_csv\T2 2 Vic.csv')

dataset

df = pd.DataFrame(dataset)

def create_database():
    try:
        conn = msql.connect(host='localhost', user='iodb',  
                            password='123456',database="ioenergy") #give ur username, password
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE employee")
            print("Database is created")
    except Error as e:
        print("Error while connecting to MySQL", e)


def insert_csv(dataset):
    try:
        conn = msql.connect(host='localhost', database='ioenergy', user='iodb', password='123456')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute('DROP TABLE IF EXISTS customer_data;')
            print('Creating table....')
    # in the below line please pass the create table statement which you want #to create
            cursor.execute("CREATE TABLE customer_data(time datetime NOT NULL, consumption FLOAT(53) NOT NULL,export FLOAT(53) NOT NULL, import FLOAT(53) NOT NULL,self_consumption FLOAT(53) NOT NULL,system_production FLOAT(53) NOT NULL )")
            print("Table is created....")
            #loop through the data frame
            for i,row in dataset.iterrows():
                #here %S means string values 
                sql = "INSERT INTO customer_data VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, tuple(row))
                print("Record inserted")
                # the connection is not auto committed by default, so we must commit to save our changes
                conn.commit()
    except Error as e:
                print("Error while connecting to MySQL", e)
    


# initiate_variables:

billing_days = 31

normal_price = 0.21
night_price = 0.40
weekday_price = 0.295

self_consum_price = 0.25

normal_usage = 0
night_usage = 0
weekday_usage = 0


def grid_energy_charges():

    try:
        conn = msql.connect(host='localhost', database='ioenergy', user='iodb', password='123456')
        
        cursor = conn.cursor()
        # MYSQL query according to the price plan
        cursor.execute("SELECT import FROM customer_data WHERE hour(time) < 7 or hour(time) >= 21 union all SELECT import FROM customer_data WHERE weekday(time) > 4 and hour (time) >= 7 and hour(time) < 21;")
        results = cursor.fetchall()
        normal_usage = sum(e[0] for e in results)

        
        cursor.execute("SELECT import FROM customer_data WHERE hour(time) >= 17 and hour(time) < 21 ;")
        results = cursor.fetchall()
        night_usage = sum(e[0] for e in results)
        

        cursor.execute("SELECT import FROM customer_data WHERE weekday(time) >= 0 and weekday(time) <= 4 and hour (time) >= 7 and hour(time) < 17;")
        results = cursor.fetchall()
        weekday_usage = sum(e[0] for e in results)
        
        # conver usage from W to kW
        normal_usage = normal_usage/1000
        night_usage = night_usage/1000
        weekday_usage = weekday_usage/1000

        total_usage = normal_usage + night_usage + weekday_usage

        total_import_charges = normal_price * normal_usage + night_price * night_usage + weekday_price * weekday_usage

        return total_import_charges
    
    except Error as e:
                print("Error while connecting to MySQL", e)

def rooftop_energy_charges():
     
    try:
        conn = msql.connect(host='localhost', database='ioenergy', user='iodb', password='123456')
      
        cursor = conn.cursor()

        cursor.execute("Select self_consumption from customer_data;")
        results = cursor.fetchall()
        self_consum_usage = sum(e[0] for e in results)

        #convert W to kW
        self_consum_usage = self_consum_usage/1000

        self_consum_charges = self_consum_usage * self_consum_price

        return self_consum_charges

    except Error as e:
                print("Error while connecting to MySQL", e)



    







