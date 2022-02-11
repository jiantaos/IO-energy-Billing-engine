import sqlite3
import pandas as pd
import psycopg2
import mysql.connector as msql
from mysql.connector import Error

# read customer invoices
dataset= pd.read_csv('D:\IO energy internship\multiple_csv\T1 2 Vic.csv')

connection = msql.connect(host='localhost', database='ioenergy', user='iodb', password='123456')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


for i,row in dataset.iterrows():
                #here %S means string values 
                sql = "INSERT INTO customer_data VALUES (%s,%s,%s,%s,%s,%s)"
                cur.execute(sql, tuple(row))
                print("Record inserted")
                # the connection is not auto committed by default, so we must commit to save our changes
                connection.commit()


connection.close()
