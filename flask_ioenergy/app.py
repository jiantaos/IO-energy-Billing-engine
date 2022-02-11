import sqlite3
import pandas as pd
import psycopg2
import mysql.connector as msql
from mysql.connector import Error

from flask import Flask, render_template,request

from insert_energy import csvtotable,insertenergy, grid_energy_charges,rooftop_energy_charges
from bill_issuing import *




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route("/search",methods=['GET', 'POST']) 
def search():

    email = request.form.get('email')
    # import csv data
    dataset= pd.read_csv('D:\IO energy internship\multiple_csv\T2 2 Vic.csv')

    # using functions in insert_energy
    csvtotable('apikeys.csv', "apikeys")

    # enter the year and month,the customer account number you want to bill
    print(request.form.get('customerID'))
    print(request.values.get('selyear'))
    print(request.values.get('selmonth'))

    year_being_billed = int(request.values.get('selyear'))
    month_being_billed = int(request.values.get('selmonth'))

    # bill_cycle_start_date is the first date of the month that is billed for
    bill_cycle_start_date = datetime.date(year_being_billed,month_being_billed,1)
    # bill_cycle_end_date is the last date of the month that is billed for 
    bill_cycle_end_date = datetime.date(year_being_billed,month_being_billed,calendar.monthrange(year_being_billed,month_being_billed)[1])

    insertenergy("apikeys",1,str(bill_cycle_start_date),str(bill_cycle_end_date))

    # quote functions from bundled_output.py to get total grid charges and total rooftop charges 
    total_grid_charges = round(grid_energy_charges(),2)

    total_rooftop_charges = round(rooftop_energy_charges(),2)

    # initialize customer data
    create_customer_info_table()


    retail_fee_rate = 1.6
    generate_bill_for = request.form.get('customerID')

    this_bill_issue_date,bill_cycle_end_date,bill_cycle_start_date,billing_days,pay_bill_date,invoice_number= bill_generate(year_being_billed,month_being_billed,generate_bill_for)

    daily_supply_charge = retail_fee_rate * billing_days

    total_ex_GST = total_grid_charges + total_rooftop_charges + daily_supply_charge

    total_GST = round(0.1 * total_ex_GST,2)

    total_current_charges = round((total_ex_GST + total_GST),2)
    
    return render_template('invoice.html', total_grid_charges=total_grid_charges,total_rooftop_charges=total_rooftop_charges,
    this_bill_issue_date = this_bill_issue_date, bill_cycle_end_date =  bill_cycle_end_date, bill_cycle_start_date = bill_cycle_start_date,daily_supply_charge = daily_supply_charge,
    total_GST=total_GST,total_current_charges=total_current_charges,pay_bill_date = pay_bill_date,invoice_number = invoice_number,generate_bill_for = generate_bill_for)



