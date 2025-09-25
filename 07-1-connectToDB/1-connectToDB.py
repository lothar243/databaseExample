# this example uses a json file to store the credentials called secrets.json, with the following contents
# be sure to NOT add the secrets file to your git repository
# if you do accidentally add it, the best course of action is to rotate your secrets (change your password)
"""
{
    "mysqlCredentials": {
        "host":"127.0.0.1",
        "user":"jeffdb",
        "password":"mypass",
        "db":"sakila"
    }
}
"""

import mysql.connector, json

with open('/home/jeff/databaseExample/07-1-connectToDB/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

connection = mysql.connector.connect(**creds)

print(connection)
connection.close()