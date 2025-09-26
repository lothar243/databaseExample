#! /usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return(render_template('index.html'))

@app.route('/about')
def about():
    return(render_template('about.html'))

@app.route('/premade')
def premade():
    output = render_template('hello.html')
    return output

@app.route('/dynamic')
def dynamic():
    output = render_template('dynamic.html', myText="<h1>From Python</h1>")
    return output

@app.route('/forloop')
def forloop():
    mylist = [1, 2, 3, 4, 5, 6, 7, 8]
    return render_template('forloop.html', mylist=mylist)

@app.route('/basehome')
def basehome():
    return render_template('basehome.html')

@app.route('/baseabout')
def baseabout():
    return render_template('baseabout.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")