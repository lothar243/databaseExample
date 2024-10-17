#!/usr/bin/python3


import mysql.connector, os

connection = mysql.connector.connect(
    host=os.environ['SQL_HOST'],
    user=os.environ['SQL_USER'],
    password=os.environ['SQL_PWD'],
    db=os.environ['SQL_DB']
)

mycursor = connection.cursor()
mycursor.execute("insert into actor (first_name, last_name) values ('jeff', 'arends');")
connection.commit()

connection.close()