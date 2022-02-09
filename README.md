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

![SCREEN1.PNG](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/fd7dade0-33aa-4fe1-b199-9dd343d62b02/SCREEN1.png)

SCREEN2: COMPANY LEVEL ANALYSIS

![SCREEN2.PNG](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5783b705-8819-4475-9580-5979ddc007d8/SCREEN2.png)

- Back-end data:

The Back-end invoice data is generated using the price plan times energy usage data got from API to get the final invoice amount each month for each customer. 

SHEET 1: INVOICES DATA

![INOVICE DATA.PNG](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/14e081a1-7220-427d-850a-978898dc57f4/INOVICE_DATA.png)

SHEET 2: PAYMENT RECEIVED DATA 




An API using flask structure that can automatically convert customer energy usage data in xml/csv data type to an completed customer invoice online. 
![](https://github.com/jiantaos/IO-energy-Billing-engine/blob/main/flask_ioenergy/images/showcase.png)


Prerequisites
----------
an constrcuted MYSQL server

Installing
----------

Install and update using `pip`_:

.. code-block:: text

    $ pip install -U Flask

.. _pip: https://pip.pypa.io/en/stable/getting-started/

    $ flask run
      * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
      
File Stucture
----------
<pre>
|-- apps
|	|-- 
|	|-- ... (more to add)
|-- static
|	|-- base
|	|	|-- css 			# CSS files containing all basic and bootstrap based files
|	|	|-- js      			# JS files containing all basic and bootstrap based files
|	|--index
|	|	|-- css				# CSS files for homepage
|	|	|-- js 				# js files for homepage
|	|	|-- img  			# images for homepage
|	|-- ... (more to add)
|-- templates
|	|-- index 				# all index html files
|	|-- base.html 				# the main base html files
|	|-- ... (more to add)
|--  
</pre>


Language and Tools
------------

<pre>
VERSION CONTROL:  Git, Github
BACK       END:   python,MYSQL
FRONT      END:   CSS, HTML, Javascript, bootstrap
</pre>


MYSQL Server
<pre>
Host:localhost
Database:ioenergy
user:iodb
password:123456
</pre>

Reminds
----------
xml_mysql.py is a independent file from the flask app which can be complied seperately to insert xml into mysql database 

Contributing
----------

Eden Song - IO energy

