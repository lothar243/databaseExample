#!/usr/bin/python3

from flask import Flask, render_template, request, jsonify
import mysql.connector, os
import json


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



if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")