#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

app = Flask(__name__)


@app.route('/student', methods=['GET'])
def showStudents():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a name and desc 'GET' variable, insert the new value into the database
    sectionID = request.args.get('section_id')
    if sectionID is not None:
        mycursor.execute("""SELECT student.id,first_name,last_name,course_name,course_code from student 
                         join section_student on student.id=section_student.student_id
                         join section on section.id=section_student.section_id
                         join course on course.id=section.course_id
                         where section.id=%s""", (sectionID,))
        myresult = mycursor.fetchall()
        if len(myresult) >= 1:
            courseName = myresult[0][3]
            courseNumber = myresult[0][4]
        else:
            courseName = courseNumber = "Unknown"
        # print(myresult)
        pageTitle = f"Showing all students in section {sectionID}, {courseName} ({courseNumber})"
    else:
        mycursor.execute("SELECT id,first_name,last_name from student")
        pageTitle = "Showing all students"
        myresult = mycursor.fetchall()

    # Fetch the current values of the speaker table
    mycursor.close()
    connection.close()
    return render_template('student.html', studentList=myresult, pageTitle=pageTitle)

@app.route('/section', methods=['GET'])
def showSections():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a name and desc 'GET' variable, insert the new value into the database
    studentID = request.args.get('student_id')
    if studentID is not None:
        mycursor.execute("""SELECT section.id,course_name,course_code,first_name,last_name from student 
                         join section_student on student.id=section_student.student_id
                         join section on section.id=section_student.section_id
                         join course on course.id=section.course_id
                         where student.id=%s""", (studentID,))
        myresult = mycursor.fetchall()
        print(myresult)
        if len(myresult) >= 1:
            studentName = myresult[0][2] + " " + myresult[0][3]
        else:
            studentName = "Unknown"
        # print(myresult)
        pageTitle = f"Showing all sections for student: {studentName})"
    else:
        mycursor.execute("""SELECT section.id, course_name, course_code from section
                         join course on section.course_id=course.id""")
        pageTitle = "Showing all sections"
        myresult = mycursor.fetchall()

    # Fetch the current values of the speaker table
    mycursor.close()
    connection.close()
    return render_template('section.html', studentList=myresult, pageTitle=pageTitle)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")