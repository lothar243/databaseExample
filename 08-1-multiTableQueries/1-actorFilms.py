#!/usr/bin/env python3
# This example uses a credentials stored in a .env file defining SQL_HOST, SQL_USER, SQL_PWD, and SQL_DB

import mysql.connector, os
from dotenv import load_dotenv
load_dotenv()

def getConnection():
    connection = mysql.connector.connect(
        host=os.getenv('SQL_HOST'),
        user=os.getenv('SQL_USER'),
        password=os.getenv('SQL_PWD'),
        db=os.getenv('SQL_DB')
    )
    return connection

def printActors():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("select * from actor")
    myResult = myCursor.fetchone()

    print("In the actor table, we have the following items: ")
    while myResult is not None:
        print(myResult)
        myResult = myCursor.fetchone()
    connection.close()
    print()

def printFilms():
    connection = getConnection()
    myCursor = connection.cursor()
    myCursor.execute("select film_id, title from film")
    myResult = myCursor.fetchone()

    print("In the film table, we have the following items: ")
    while myResult is not None:
        print(myResult)
        myResult = myCursor.fetchone()
    connection.close()
    print()

def printFilmsForActor():
    connection = getConnection()
    myCursor = connection.cursor()
    actor_id = input("For which actor_id would you like to view the films? ")
    myCursor.execute("select film.film_id, title from film join film_actor on film.film_id=film_actor.film_id where actor_id=%s", (actor_id,))
    myResult = myCursor.fetchall()
    print(f"There are {len(myResult)} films: ")
    for row in myResult:
        print(row)

def printActorsForFilm():
    connection = getConnection()
    myCursor = connection.cursor()
    film_id = input("For which film_id would you like to view the actors? ")
    myCursor.execute("select actor.actor_id, first_name, last_name from actor join film_actor on actor.actor_id=film_actor.actor_id and film_id=%s", (film_id,))
    myResult = myCursor.fetchall()
    print(f"There are {len(myResult)} actors: ")
    for row in myResult:
        print(row)


menuText = """Please select one of the following options:
1) Print Actors
2) Print Films
3) Print Films an actor appears in
4) Print Actors in a film
5) Add an actor to a film (unimplemented)
6) Remove an actor from a film (unimplemented)
q) Quit
"""

if __name__ == "__main__":
    menuOption = "1"
    while menuOption != 'q':
        menuOption = input(menuText)
        if menuOption == "1":
            printActors()
        elif menuOption == "2":
            printFilms()
        elif menuOption == "3":
            printFilmsForActor()
        elif menuOption == "4":
            printActorsForFilm()