#!/usr/bin/python3

import json
import mysql.connector
from flask import Flask, render_template, request, make_response, jsonify


app = Flask(__name__)

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

@app.route('/api/actors', methods=['GET'])
def get_actors():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor(dictionary=True) # Return records as dictionaries instead of lists

    mycursor.execute("Select actor_id, first_name, last_name, last_update from actor")
    actors = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return jsonify(actors)

@app.route('/api/actors/<int:actor_id>', methods=['GET'])
def get_actor(actor_id: int):
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor(dictionary=True)

    mycursor.execute("Select first_name, last_name, last_update from actor where actor_id=%s", (actor_id,))
    actor = mycursor.fetchall()
    mycursor.close()
    connection.close()
    if len(actor) == 0:
        return jsonify({'error': "Actor does not exist"}), 404
    return jsonify(actor)

@app.route('/api/actors/<int:actor_id>/movies', methods=['GET'])
def get_actor_movies(actor_id: int):
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor(dictionary=True)
    QUERY = """Select film.film_id, title 
                from actor 
                join film_actor on actor.actor_id=film_actor.actor_id
                join film on film.film_id=film_actor.film_id
                where actor.actor_id=%s"""
    mycursor.execute(QUERY, (actor_id,))
    actor = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return jsonify(actor)

def has_authorization():
    # Instead of hard-coding this, you should have the username and password store in the database. 
    # You would also want to check for the appropriate authorization
    # I'm just putting this here as a proof of concept
    return request.cookies.get('username') == "jeff" and request.cookies.get('password') == "mypass"

@app.route('/api/actors', methods=['POST'])
def create_actor():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    if not has_authorization():
        return jsonify({'error': 'Authentication and authorization required'})
    if firstname is None or lastname is None:
        return jsonify({'error': 'Must supply both first and last name for actor'})
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    mycursor.execute("Insert into actor (first_name, last_name) values (%s, %s)", (firstname, lastname))
    connection.commit()
    row_id = mycursor.lastrowid # get the row id of the newly inserted record
    mycursor.close()
    connection.close()
    return jsonify({'status':'success', 'location': f'/actors/{row_id}'})

@app.route('/api/actors/<int:actor_id>/delete', methods=['DELETE'])
def delete_actor(actor_id: int):
    if not has_authorization():
        return jsonify({'error': 'Authentication and authorization required'})
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    mycursor.execute("delete from actor where actor_id=%s", (actor_id,))
    connection.commit()
    mycursor.close()
    connection.close()
    return jsonify({'status': 'success'})

    

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    response = make_response('You are now logged in<br><a href="/">Return</a>')
    response.set_cookie('username', 'jeff')
    response.set_cookie('password', 'mypass')
    return response

@app.route('/logout', methods=['GET'])
def logout():
    response = make_response('You are now logged out<br><a href="/">Return</a>')
    response.set_cookie('username', '', expires=0)
    response.set_cookie('password', '', expires=0)
    return response


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")