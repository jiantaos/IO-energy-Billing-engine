
#!/usr/bin/env python
# coding: utf-8

# io energy construct different price plans for different customers as competitive advantages 
# Price plans are designed in colored graphs and converted into coding methods by python 
# These converted price plans then would be used to applied in calculating the invoice amount each month for each customer

import psycopg2
import yaml
import csv
from urllib.request import urlopen
import json
import pandas as pd
import calendar



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

# functions start with price plan represents every price plan converted the format of python codes
# initialized variables includes settled prices and customer usage extraxt from 'customer_data' table for each period in price plans 
# customer_number is the unique customer the price plan applied on 

def price_plan_1(customer_number,table):

    # make an connection to the aim database containing customer energy data
    conn = connect()
    cursor = conn.cursor() 
    
    #initialise variables
    billing_days = 31

    normal_price = 0.21
    night_price = 0.40
    weekday_price = 0.295

    rooftop_solar_price = 0.25

    normal_usage = 0
    night_usage = 0
    weekday_usage = 0

    ##################################################### Grid energy charges("Purchased")##########################################################

    # postgred query according to the price plan
    cursor.execute("SELECT value FROM "+table+" WHERE (customer_number ="+customer_number+"and type = 'Purchased' and date_part('hour', datetime)<= 7) or (customer_number ="+customer_number+"and type = 'Purchased' and date_part('hour', datetime)>= 17) or (customer_number ="+customer_number+"and type = 'Purchased' and EXTRACT(DOW FROM datetime) = 6 and date_part('hour', datetime)>=7 and date_part('hour', datetime)<21) or (customer_number ="+customer_number+"and type = 'Purchased' and EXTRACT(DOW FROM datetime) = 0 and date_part('hour', datetime)>=7 and date_part('hour', datetime)<21);")
    results = cursor.fetchall()
    normal_usage = sum(e[0] for e in results)

    cursor.execute("SELECT value FROM "+table+" customer_data WHERE (customer_number ="+customer_number+"and type = 'Purchased' and date_part('hour', datetime) >= 17 and date_part('hour', datetime) < 21) ;")
    results = cursor.fetchall()
    night_usage = sum(e[0] for e in results)

    cursor.execute("SELECT value FROM "+table+" WHERE (customer_number ="+customer_number+"and type = 'Purchased' and EXTRACT(DOW FROM datetime) >= 0 and EXTRACT(DOW FROM datetime) <= 4 and date_part('hour', datetime) >= 7 and date_part('hour', datetime) < 17);")
    results = cursor.fetchall()
    weekday_usage = sum(e[0] for e in results)
        
    # conver usage from W to kW
    normal_usage = normal_usage/1000
    night_usage = night_usage/1000
    weekday_usage = weekday_usage/1000

    total_usage = normal_usage + night_usage + weekday_usage

    total_grid_charges = normal_price * normal_usage + night_price * night_usage + weekday_price * weekday_usage
    
    total_grid_charges = round(total_grid_charges,2)
    print("Total grid charges:"+total_grid_charges)

    ####################################################### Rooftop Energy Charges("SelfConsumption")###########################################


    cursor.execute("SELECT value FROM "+table+" where customer_number ="+customer_number+"and (type = 'SelfConsumption');")
    results = cursor.fetchall()
    rooftop_solar_usage = sum(e[0] for e in results)

    # convert W to kW
    rooftop_solar_usage = rooftop_solar_usage/1000

    rooftop_solar_charges = rooftop_solar_usage * rooftop_solar_price

    rooftop_solar_charges = round(rooftop_solar_charges,2)
    print("Total solar charges:"+rooftop_solar_charges)

    ######################################################## Daily Supply Charge ####################################################################

    retail_fee_rate = 1.6
    billing_days = calendar.monthrange(2021,1)[1]

    daily_supply_charge = retail_fee_rate*billing_days
    daily_supply_charge = round(daily_supply_charge,2)

    ######################################################## GST and Final Amount ###################################################################

    total_ex_GST = total_grid_charges + rooftop_solar_charges + daily_supply_charge

    total_GST = round(0.1 * total_ex_GST,2)

    total_current_charges = round((total_ex_GST + total_GST),2)
    print("Total current charges:"+total_current_charges)
    return total_grid_charges,rooftop_solar_charges,daily_supply_charge,total_ex_GST,total_GST,total_current_charges

# price_plan_1("1")
#csvtotable_apikeys("apikeys.csv","apikeys")
#csvtotable_tenants("Mount Barker Shopping Centre Tenancies.csv","Tenants")




   












