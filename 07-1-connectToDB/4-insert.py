#!/usr/bin/env python3
# This example uses a .env file to store the mysql credentials
# You will need to install the dotenv package with 'pip install dotenv'
# You will also need a .env file in your project directory with the following contents:
"""
SQL_HOST='127.0.0.1'
SQL_USER='jeffdb'
SQL_PWD='mypass'
SQL_DB='sakila'
"""


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