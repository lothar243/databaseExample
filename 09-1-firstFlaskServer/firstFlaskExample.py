#! /usr/bin/python3

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def default():
    return '<html><body><h1>Hello, this was rendered directly from Python</h1><p><a href="/withGetVariables?fname=jeff&lname=arends">View an example that makes use of GET variables</a></p></body</html>'

@app.route('/xssExample')
def xssRoute():
    return '<html><body><h1>Hello, this was rendered directly from Python</h1><p><a href="/withGetVariables?fname=jeff&lname=arends<script>alert(\'xss!\')</script>">This link demonstrates reflective XSS</a></p></body</html>'

@app.route('/withGetVariables', methods=['GET'])
def withGetVariables():
    firstname = request.args.get('fname')
    lastname = request.args.get('lname')
    output = f"Hello {firstname} {lastname}"
    return output

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")