#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/showStudents', methods=['GET'])
def showStudents():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    mycursor2 = connection.cursor()

    # If there is a section_id 'GET' variable, use this to refine the query
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
        pageTitle = f"Showing all students in section {sectionID}, {courseName} ({courseNumber})"
    else:
        mycursor.execute("SELECT id,first_name,last_name from student")
        pageTitle = "Showing all students"
        myresult = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('students.html', studentList=myresult, pageTitle=pageTitle)

@app.route('/showSections', methods=['GET'])
def showSections():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a student_id 'GET' variable, use this to refine the query
    studentID = request.args.get('student_id')
    if studentID is not None:
        # Check if the student is registering for a new class
        registerSectionId = request.args.get('register_section_id')
        if registerSectionId is not None:
            mycursor.execute("""INSERT into section_student (student_id, section_id) values (%s, %s)
                             """, (studentID, registerSectionId))
            connection.commit()

        mycursor.execute("""SELECT section.id,course_name,course_code,first_name,last_name 
                         from student 
                         join section_student on student.id=section_student.student_id
                         join section on section.id=section_student.section_id
                         join course on course.id=section.course_id
                         where student.id=%s""", (studentID,))
        sections = mycursor.fetchall()
        print(sections)
        if len(sections) >= 1:
            studentName = sections[0][3] + " " + sections[0][4]
            mycursor.execute("""SELECT section.id, course_name, course_code
                                FROM section
                                Join course on course.id=section.course_id
                                WHERE section.id not in (
                                    SELECT section_id
                                    from section_student
                                    where section_student.student_id=%s
                                )
                             """, (studentID,))
            othersections = mycursor.fetchall()
            print(othersections)
        else:
            studentName = "Unknown"
            othersections = None
        pageTitle = f"Showing all sections for student: {studentName})"
    else:
        mycursor.execute("""SELECT section.id, course_name, course_code from section
                         join course on section.course_id=course.id""")
        pageTitle = "Showing all sections"
        sections = mycursor.fetchall()
        othersections = None

    mycursor.close()
    connection.close()
    print(f"{studentID=}")
    return render_template('sections.html', 
                           studentList=sections, 
                           pageTitle=pageTitle, 
                           othersections=othersections, 
                           studentId=studentID 
                           )


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")