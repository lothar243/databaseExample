import mysql.connector, os

connection = mysql.connector.connect(
    host=os.environ['SQL_HOST'],
    user=os.environ['SQL_USER'],
    password=os.environ['SQL_PWD'],
    db=os.environ['SQL_DB']
)

mycursor = connection.cursor()
mycursor.execute("select * from speaker")
myresult = mycursor.fetchone()

print("In the speaker table, we have the following items:")
while myresult is not None:
    print(myresult)
    myresult = mycursor.fetchone()


connection.close()