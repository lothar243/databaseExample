import mysql.connector, os

connection = mysql.connector.connect(
    host=os.environ['SQL_HOST'],
    user=os.environ['SQL_USER'],
    password=os.environ['SQL_PWD'],
    db=os.environ['SQL_DB']
)
print(connection)
connection.close()