#!/usr/bin/python3

from flask import Flask, request
import mysql.connector, os


app = Flask(__name__)
posts = []

@app.route('/reflected', methods=['GET'])
def reflected():
    """View this attack by having the webpage repeat: <script>alert("XSS!")</script>"""
    output = request.args.get("myval")
    if output is None:
        output = ""
    return output + """<form>What value would you like to show on this page?<input type="text" name="myval"><input type="submit"></form>"""

@app.route('/stored', methods=['GET'])
def stored():
    """View this attack by adding <script>alert("XSS!")</script> as a post"""
    newpost = request.args.get("myval")
    if newpost is not None:
        posts.append(newpost)
    output = "<table border=\"1\"><tr><th>Post</th></tr>"
    for post in posts:
        output += "<tr><td>" + post + "</td></tr>"
    output += "</table>"
    output += """<form>Add a post?<input type="text" name="myval"><input type="submit"></form>"""
    return output

@app.route('/dom', methods=['GET'])
def dom():
    """View this attack by visiting the site: http://localhost:8000/dom?default=<script>alert("XSS!")</script>"""
    output = """Select your language:
<select><script>
document.write("<OPTION value=1>"+decodeURIComponent(document.location.href.substring(document.location.href.indexOf("default=")+8))+"</OPTION>");
document.write("<OPTION value=2>English</OPTION>");
</script></select>"""
    return output



if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")