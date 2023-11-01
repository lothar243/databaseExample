#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
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
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        mycursor.execute("DELETE from speaker where id=%s", (deleteID,))
        connection.commit()

    # Fetch the current values of the speaker table
    mycursor.execute("Select * from speaker")
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('speaker-list.html', collection=myresult)

@app.route("/updateSpeaker")
def updateSpeaker():
    connection = mysql.connector.connect(
        host=os.environ['SQL_HOST'],
        user=os.environ['SQL_USER'],
        password=os.environ['SQL_PWD'],
        db=os.environ['SQL_DB']
    )
    id = request.args.get('id')
    newName = request.args.get('name')
    newDesc = request.args.get('desc')
    if id is None:
        return "Error, id not specified"
    elif newName is not None and newDesc is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE speaker set name=%s, description=%s where id=%s", (newName, newDesc, id))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showSpeakers'))

    mycursor = connection.cursor()
    mycursor.execute("select * from speaker where id=%s;", (id,))
    _, existingName, existingDesc = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('speaker-update.html', id=id, existingName=existingName, existingDesc=existingDesc)
    # return "hello world"


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")