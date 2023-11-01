#!/usr/bin/python3

from flask import Flask, render_template, request
import mysql.connector, os


app = Flask(__name__)


@app.route('/', methods=['GET'])
def showSpeakers():
    connection = mysql.connector.connect(
        host=os.environ['SQL_HOST'],
        user=os.environ['SQL_USER'],
        password=os.environ['SQL_PWD'],
        db=os.environ['SQL_DB']
    )
    mycursor = connection.cursor()

    # If there is a name and desc 'GET' variable, insert the new value into the database
    newName = request.args.get('name')
    newDesc = request.args.get('desc')
    if newName is not None and newDesc is not None:
        mycursor.execute("INSERT into speaker (name, description) values (%s, %s)", (newName, newDesc))
        connection.commit()

    # Fetch the current values of the speaker table
    mycursor.execute("Select * from speaker")
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('speaker-list.html', collection=myresult)
    #return "Hello world"


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")