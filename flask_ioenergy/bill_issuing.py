import datetime
import calendar
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error


dataset= pd.read_csv('D:\IO energy internship\multiple_csv\T2 2 Vic.csv')

df = pd.DataFrame(dataset)










def last_bill_issued(account_number,bill_count):
    return str(account_number) + "/" + str(bill_count).zfill(2) 

def next_bill(account_number,bill_count):
    return str(account_number) + "/" + str(bill_count+1).zfill(2)

# create an info table for the convenience of searching for customer infomation for a particular customer  
def create_customer_info_table():
    #initiate variables

    account_number = 9038075
    bill_count = 0
    last_bill_issue_date = "2021-08-18"
    last_bill_issue_amount = 6281.19
    payment_recevied = 6281.19

    total_bills_issued = 1
    price_plan = "IO_CI_01"
    #create table 
    try:
        conn = msql.connect(host='localhost', database='ioenergy', user='iodb', password='123456')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute('DROP TABLE IF EXISTS customer_info;')
            print('Creating table....')
    # in the below line please pass the create table statement which you want #to create
            cursor.execute("CREATE TABLE customer_info(account_number INTEGER,Bill_Count INTEGER,Last_Bill_Issued VARCHAR(20),Last_Bill_Issued_Date date,Last_Bill_Issued_Amount FLOAT(53),Payments_Received FLOAT(53),Next_Bill VARCHAR(20),Total_Bill_Issued INTEGER,Price_Plan VARCHAR(20))")
            print("Table is created....")
           
            #insert variables
            
            sql = "INSERT INTO customer_info(account_number,Bill_Count,Last_Bill_Issued,Last_Bill_Issued_Date,Last_Bill_Issued_Amount,Payments_Received,Next_Bill,Total_Bill_Issued,Price_Plan) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(account_number,bill_count,last_bill_issued(account_number,bill_count),last_bill_issue_date,last_bill_issue_amount,payment_recevied,next_bill(account_number,bill_count),total_bills_issued,price_plan))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
    except Error as e:
                print("Error while connecting to MySQL", e)





def bill_generate(year_being_billed,month_being_billed,generate_bill_for):

    #search for customer records
  
    conn = msql.connect(host='localhost', database='ioenergy', user='iodb', password='123456')
    
    cursor = conn.cursor()

    # get the invoice number of the customer 
    cursor.execute("SELECT Next_Bill FROM customer_info WHERE account_number = {};".format(generate_bill_for))
    results = cursor.fetchall()
    invoice_number = results[0][0]
    
    
    
    #create variables that would be used on the invoice

    now = datetime.datetime.now()
    # issue date is always today
    this_bill_issue_date = now.strftime("%Y-%m-%d")
    print(this_bill_issue_date)
    
    
    # bill_cycle_end_date is the last date of the month that is billed for 
    #bill_cycle_end_date = datetime.date(year_being_billed,month_being_billed,calendar.monthrange(year_being_billed,month_being_billed)[1])
    bill_cycle_end_date = datetime.date(year_being_billed,month_being_billed,calendar.monthrange(year_being_billed,month_being_billed)[1])
   
    # bill_cycle_start_date is the first date of the month that is billed for
    bill_cycle_start_date = datetime.date(year_being_billed,month_being_billed,1)
    
    # billing_days is the period between start day and end day
    billing_days = (bill_cycle_end_date-bill_cycle_start_date).days + 1
   
    # pay day is 14 days after the issue date
    pay_date = now + datetime.timedelta(days=14)
    pay_bill_date = pay_date.strftime("%Y-%m-%d")
    

    return this_bill_issue_date,bill_cycle_end_date,bill_cycle_start_date,billing_days,pay_bill_date,invoice_number







    
    

      









#print (last_bill_issued(account_number,bill_count))

#print(next_bill(account_number,bill_count))

