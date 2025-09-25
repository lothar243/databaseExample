import mysql.connector, os

# This example uses a Linux environment variables to store the credentials
# To work, you need to have a file named .bash_profile in your home directory with the following contents
# You will need to reconnect if you just created the file (it is run when you first start bash)
# You can alternatively load these credentials into environment variables with 'source filename'
"""
export SQL_HOST='127.0.0.1'
export SQL_USER='jeffdb'
export SQL_PWD='mypass'
export SQL_DB='sakila'
"""


connection = mysql.connector.connect(
    host=os.environ['SQL_HOST'],
    user=os.environ['SQL_USER'],
    password=os.environ['SQL_PWD'],
    db=os.environ['SQL_DB']
)

mycursor = connection.cursor()
mycursor.execute("select * from actor")
myresult = mycursor.fetchone()

print("In the actor table, we have the following items:")
while myresult is not None:
    print(myresult)
    myresult = mycursor.fetchone()


connection.close()