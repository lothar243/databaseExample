#! /usr/bin/python3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy                     # need to install flask-sqlalchemy and pymysql
from datetime import datetime
import json

app = Flask(__name__) # creates a flask application object

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

# example database uri = "mysql+pymysql://jeff:mypass@localhost/sakila"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{creds['user']}:{creds['password']}@{creds['host']}/{creds['db']}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Actor(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    last_update = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create')
def create():
    return render_template("createform.html")

@app.route('/newActor')
def insert():
    actor = Actor(first_name=request.args.get("firstName"), last_name=request.args.get("lastName"))
    db.session.add(actor)
    db.session.commit()
    return redirect("read")

@app.route('/updateform')
def updateform():
    actor = Actor.query.get(request.args.get("id"))
    return render_template("updateform.html", actor=actor)

@app.route('/update')
def update():
    actor = Actor.query.get(request.args.get("id"))
    actor.first_name = request.args.get("firstName")
    actor.last_name = request.args.get("lastName")
    db.session.commit()
    return redirect("read")

@app.route('/delete')
def remove():
    actor = Actor.query.get(request.args.get("id"))
    db.session.delete(actor)
    db.session.commit()
    return redirect("read")


@app.route('/read')
def read():
    actors = Actor.query.all()
    output = render_template("showactors.html", actors=actors)
    return output

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")