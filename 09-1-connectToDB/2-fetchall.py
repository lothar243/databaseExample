import mysql.connector, json

with open('/home/jeff/databaseExample/09-1-connectToDB/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']


connection = mysql.connector.connect(**creds)

mycursor = connection.cursor()
mycursor.execute("select * from speaker")
myresult = mycursor.fetchall()

print(f"{myresult=}")

print("In the speaker table, we have the following items:")
for row in myresult:
    print(row)

mycursor.close()
connection.close()