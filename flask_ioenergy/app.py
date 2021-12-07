import sqlite3
import pandas as pd
import psycopg2
import mysql.connector as msql
from mysql.connector import Error

from flask import Flask, render_template

from bundled_output import insert_csv, grid_energy_charges,rooftop_energy_charges
from bill_issuing import *


#open a connection to database.db file
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route("/")
def index():
    # import csv data
    dataset= pd.read_csv('D:\IO energy internship\multiple_csv\T2 2 Vic.csv')

    #insert csv to customer_data table
    insert_csv(dataset)

    # quote functions from bundled_output.py to get total grid charges and total rooftop charges 
    total_grid_charges = round(grid_energy_charges(),2)

    total_rooftop_charges = round(rooftop_energy_charges(),2)

    # initialize customer data
    create_customer_info_table()

    # enter the year and month,the customer account number you want to bill
    year_being_billed = 2021
    month_being_billed = 7
    retail_fee_rate = 1.6
    generate_bill_for = 9038075

    this_bill_issue_date,bill_cycle_end_date,bill_cycle_start_date,billing_days,pay_bill_date,invoice_number= bill_generate(year_being_billed,month_being_billed,generate_bill_for)

    daily_supply_charge = retail_fee_rate * billing_days

    total_ex_GST = total_grid_charges + total_rooftop_charges + daily_supply_charge

    total_GST = round(0.1 * total_ex_GST,2)

    total_current_charges = round((total_ex_GST + total_GST),2)
    
    return render_template('index.html', total_grid_charges=total_grid_charges,total_rooftop_charges=total_rooftop_charges,
    this_bill_issue_date = this_bill_issue_date, bill_cycle_end_date =  bill_cycle_end_date, bill_cycle_start_date = bill_cycle_start_date,daily_supply_charge = daily_supply_charge,
    total_GST=total_GST,total_current_charges=total_current_charges,pay_bill_date = pay_bill_date,invoice_number = invoice_number,generate_bill_for = generate_bill_for)
