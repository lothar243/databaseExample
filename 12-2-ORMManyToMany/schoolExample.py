#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import json
from extensions import db
from models import *
from sqlalchemy import text

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{creds['user']}:{creds['password']}@{creds['host']}/{creds['db']}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the app with SQLAlchemy

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/showStudents', methods=['GET'])
def showStudents():
    sectionID = request.args.get('section_id')
    if sectionID is not None:
        section = Section.query.get(sectionID)
        students = section.students
        pageTitle = f"Showing all students in section {section.id}, {section.course.course_name} ({section.course.course_code})"
    else:
        students = Student.query.all()
        pageTitle = "Showing all students"
    return render_template('students.html', studentList=students, pageTitle=pageTitle)


@app.route('/showSections', methods=['GET'])
def showSections():
    # If there is a student_id 'GET' variable, use this to refine the query
    studentID = request.args.get('student_id')
    if studentID is not None:
        student = Student.query.get(studentID)

        # Check if the student is registering for a new class
        registerSectionId = request.args.get('register_section_id')

        if registerSectionId is not None:
            # I need a copy of both objects before I can form the link
            section = Section.query.get(registerSectionId)
            student.sections.append(section)
            db.session.commit()
        sections = student.sections

        # sometimes it is still easier to use a raw query, like fetching the sections the student is not registered for
        unregisteredSectionQuery = text("""SELECT section.id, course_name, course_code
                                        FROM section
                                        Join course on course.id=section.course_id
                                        WHERE section.id not in (
                                            SELECT section_id
                                            from section_student
                                            where section_student.student_id=:student_id
                                        )""")
        result = db.session.execute(unregisteredSectionQuery, {"student_id": studentID})
        othersections = result.fetchall()            
        pageTitle = f"Showing all sections for student: {student.first_name} {student.last_name})"
    else:
        sections = Section.query.all()
        othersections = None

    for section in sections:
        print(section.id)
    return render_template('sections.html', 
                           sectionList=sections, 
                           pageTitle=pageTitle, 
                           othersections=othersections, 
                           studentId=studentID 
                           )


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")