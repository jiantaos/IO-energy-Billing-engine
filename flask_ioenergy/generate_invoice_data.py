#!/usr/bin/env python
# coding: utf-8

from datetime import date
from construct_database import csvtotable_apikeys,csvtotable_tenants,insertall
from price_plan import price_plan_1





# The following procedure executes the function of create a customer data table of all sites in apikeys.csv 
# And present their energy usage data(Purchased/Self-Consumption)
# The table name starts with customer_data_[month + year]

csvtotable_apikeys("apikeys.csv","apikeys")
csvtotable_tenants("Mount Barker Shopping Centre Tenancies.csv","Tenants")


def insert_until_latest(keytable,first_month,first_year):

    todays_date = date.today()
    current_month = todays_date.month + 1
    current_year = todays_date.year + 1
    b = lastrow(keytable) + 1
    
    while first_year < current_year:
        while first_
        insertall(keytable,first_month,first_year)
        first_month + = 1
  

insertall("apikeys","4","2021")

price_plan_1("1","customer_data_042021")


# Loop through all sites energy usage data and create INVOICE DATA table for a particular months

''''
# importing date class from datetime module
from datetime import date
  
# creating the date object of today's date
todays_date = date.today()
  
# printing todays date
print("Current date: ", todays_date)
  
# fetching the current year, month and day of today
print("Current year:", todays_date.year)
print("Current month:", todays_date.month)
print("Current day:", todays_date.day)
'''''