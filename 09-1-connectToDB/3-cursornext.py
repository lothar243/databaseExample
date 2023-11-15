import mysql.connector, os

# This example uses Linux environment variables to store the credentials
# To work, you need to have a file named .bash_profile in your home directory with the following contents
"""
export SQL_HOST='127.0.0.1'
export SQL_USER='www'
export SQL_PWD='mypass'
export SQL_DB='miscon'
"""


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