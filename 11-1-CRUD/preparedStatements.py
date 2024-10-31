#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json


with open('/home/jeff/databaseExample/09-1-connectToDB/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

connection = mysql.connector.connect(**creds)


app = Flask(__name__)


@app.route('/', methods=['GET'])
def showActors():
    mycursor = connection.cursor()

    # If there is a name and desc 'GET' variable, insert the new value into the database
    firstName = request.args.get('first_name')
    lastName = request.args.get('last_name')
    if firstName is not None and lastName is not None:
        mycursor.execute("INSERT into actor (first_name, last_name) values (%s, %s)", (firstName, lastName))
        connection.commit()
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        mycursor.execute("DELETE from actor where actor_id=%s", (deleteID,))
        connection.commit()

    # Fetch the current values of the speaker table
    mycursor.execute("Select * from actor")
    myresult = mycursor.fetchall()
    mycursor.close()
    return render_template('actor-list.html', collection=myresult)

@app.route("/updateActor")
def updateActor():
    id = request.args.get('id')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    if id is None:
        return "Error, id not specified"
    elif first_name is not None and last_name is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE actor set first_name=%s, last_name=%s where actor_id=%s", (first_name, last_name, id))
        mycursor.close()
        connection.commit()
        return redirect(url_for('showActors'))

    mycursor = connection.cursor()
    mycursor.execute("select first_name, last_name from actor where actor_id=%s;", (id,))
    existingFirst, existingLast = mycursor.fetchone()
    mycursor.close()
    return render_template('actor-update.html', id=id, existingFirst=existingFirst, existingLast=existingLast)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")