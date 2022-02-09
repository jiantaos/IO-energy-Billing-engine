IO Energy Billing Engine

The billing engine is a standalone piece of software to generate electricity bills.

**Overview**

An electricity bill calculates how much a customer needs to pay for electricity, based on their consumption and price plan, and tells a customer how much they need to pay and breaks down into components.

A billing engine takes data inputs and accurately calculates and generates and electricity bill.

A billing engine maintains a record of billing history

**Requirements**

- Generate electricity bills
    - Create pdf
    - Send by email
- Track bill history
    - Assign bills a number
    - maintain history of previous bills
- User sign in
- Track what price plan a customer is in

**Data**

- Data will be stored in a database
- Data will include
    - Customer data
    - NEM12 smart meter data
    - Other energy data (from solar inverters)
    - Price plans

**Invoice&Payment Management Panel**

- The final processed data will be shown on an invoice&Payment Management Panel constructed by Powerbi
- The Panel will contain two pages:
    - Customer Analysis:
        - Total Billing and Balance Pending till date for selected Customer
        - Customer Level detailing
    - Company Level Analysis:
        - Total Billings and Amount Pending till date
        - Top Customers who haven’t paid

SCREEN1: CUSTOMER ANALYSIS

![SCREEN1.PNG](https://github.com/jiantaos/IO-energy-Billing-engine/blob/main/PowerBI/SCREEN1.PNG)

SCREEN2: COMPANY LEVEL ANALYSIS

![SCREEN2.PNG](https://github.com/jiantaos/IO-energy-Billing-engine/blob/main/PowerBI/SCREEN2.PNG)

- Back-end data:

The Back-end invoice data is generated using the price plan times energy usage data got from API to get the final invoice amount each month for each customer. 

SHEET 1: INVOICES DATA

![INOVICE DATA.PNG](https://github.com/jiantaos/IO-energy-Billing-engine/blob/main/PowerBI/INOVICE%20DATA.PNG)

SHEET 2: PAYMENT RECEIVED DATA 
![PAYMENT DATA.PNG](https://github.com/jiantaos/IO-energy-Billing-engine/blob/main/PowerBI/PAYMENT%20RECEIVED%20DATA.PNG)



Contributing
----------

Eden Song - IO energy

