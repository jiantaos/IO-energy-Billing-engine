IO Energy Billing Engine
=====

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

