import xml.etree.ElementTree as ET
import mysql.connector as mysql


# insert xml file into mysql
conn = mysql.connect(host='localhost', database='ioenergy', user='iodb', password='123456')

if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")

# get xml elements
tree = ET.parse('D:\IO energy internship\multiple_xml\energy202110.xml')
root = tree.getroot()

for child in root:
    print(child.tag, child.attrib)



cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS customer_data2;')
#insert xml datetime data and value data into mysql database
cursor.execute("CREATE TABLE customer_data2(date datetime, value FLOAT(53))")

emp = tree.findall('.//dateValue')




for ep in emp:
    date = ep.find('date').text
    value = ep.find('value').text

    print(value)
    
    employee = "INSERT INTO customer_data2 VALUES (%s,%s)"

    cursor.execute(employee,(date,value))
    conn.commit()
    