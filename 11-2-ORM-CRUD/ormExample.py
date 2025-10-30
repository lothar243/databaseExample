#! /usr/bin/python3
"""Example showing how to use SQLAlchemy with a single table or with one-to-many relationships"""

import json
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # creates a flask application object

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

# example database uri = "mysql+pymysql://jeff:mypass@localhost/sakila"
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://{creds['user']}:{creds['password']}@{creds['host']}/{creds['db']}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Actor(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    last_update = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class Language(db.Model):
    __tablename__ = "language"

    language_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    films = db.relationship("Film",
                         back_populates="language",
                         foreign_keys="Film.language_id")
    original_films = db.relationship("Film",
                                  back_populates="original_language",
                                  foreign_keys="Film.original_language_id")


class Film(db.Model):
    __tablename__ = "film"

    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    # two foreign keys into language
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"), nullable=False)
    original_language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))

    # relationships
    language = db.relationship("Language",
                            back_populates="films",
                            foreign_keys=[language_id])
    original_language = db.relationship("Language",
                                     back_populates="original_films",
                                     foreign_keys=[original_language_id])


@app.route('/')
def index():
    """Display a menu with links to the various endpoints"""
    return render_template("index.html")


@app.route('/create')
def create():
    """Display a form for creating a new actor"""
    return render_template("createform.html")


@app.route('/newActor')
def insert():
    """Insert a new actor, given first and last name"""
    actor = Actor(first_name=request.args.get("firstName"), last_name=request.args.get("lastName"))
    db.session.add(actor)
    db.session.commit()
    return redirect("read")


@app.route('/updateform')
def updateform():
    """Display a form with an actor's name pre-populated, for use in updating the name"""
    actor = Actor.query.get(request.args.get("id"))
    return render_template("updateform.html", actor=actor)


@app.route('/update')
def update():
    """Update actor based on id, first and last name"""
    actor = Actor.query.get(request.args.get("id"))
    actor.first_name = request.args.get("firstName")
    actor.last_name = request.args.get("lastName")
    db.session.commit()
    return redirect("read")


@app.route('/delete')
def remove():
    """Delete an actor based on specified id"""
    actor = Actor.query.get(request.args.get("id"))
    db.session.delete(actor)
    db.session.commit()
    return redirect("read")


@app.route('/read')
def read():
    """Display all actors"""
    actors = Actor.query.all()
    output = render_template("showactors.html", actors=actors)
    return output


@app.route('/readFilms')    # for demonstration of one-to-many relationships
def read_films():
    """Display all the films and their language"""
    films = Film.query.all()
    output = render_template("showfilms.html", films=films)
    return output


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
