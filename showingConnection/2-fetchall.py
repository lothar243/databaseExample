import mysql.connector, json

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']


connection = mysql.connector.connect(**creds)

mycursor = connection.cursor()
mycursor.execute("select * from speaker")
myresult = mycursor.fetchall()

print("In the speaker table, we have the following items:")
for row in myresult:
    print(row)

mycursor.close()
mydb.close()