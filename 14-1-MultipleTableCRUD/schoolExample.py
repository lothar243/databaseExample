#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json

with open('/home/jeff/databaseExample/14-1-MultipleTableCRUD/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

app = Flask(__name__)

@app.route('/')
def default():
    return render_template('base.html')

@app.route('/section-info', methods=['GET'])
def get_section_info():
    section_id = request.args.get('section_id')
    
    # redirect to all students if no id was provided
    if section_id is None:
        return redirect(url_for("get_sections"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # update section information if necessary
    section_info = (
        request.args.get('meeting_time'),
        request.args.get('meeting_days'),
        request.args.get('meeting_room'),
        section_id
    )
    if not None in section_info:
        mycursor.execute("UPDATE section set meeting_time=%s, meeting_days=%s, meeting_room=%s where id=%s", section_info)
        connection.commit()

    # check to see if a student needs to be dropped from course
    remove_student_id = request.args.get('remove_student_id')
    if remove_student_id is not None:
        mycursor.execute("DELETE from section_student where student_id=%s and section_id=%s", (remove_student_id, section_id))
        connection.commit()

    # retrive basic information for the section
    mycursor.execute("SELECT course_name, course_code, meeting_time, meeting_days, meeting_room from section join course on course_id=course.id where section.id=%s", (section_id,))
    try:
        course_name, course_code, meeting_time, meeting_days, meeting_room = mycursor.fetchall()[0]
    except:
        return render_template("error.html", message="Error retrieving section - does it exist?")
    
    # retrieve registration info
    mycursor.execute("""SELECT student_id, first_name, last_name from student 
                     join section_student on section_student.student_id=student.id 
                     join section on section_student.section_id=section.id 
                     where section.id=%s
                     order by last_name, first_name""", (section_id,)
                     )
    registeredStudents = mycursor.fetchall()


    mycursor.close()
    connection.close()
    return render_template("section-info.html",
                           section_id=section_id,
                           course_name=course_name,
                           course_code=course_code,
                           meeting_time=meeting_time,
                           meeting_days=meeting_days,
                           meeting_room=meeting_room,
                           registeredStudents=registeredStudents
                           )

@app.route('/student-info', methods=['GET'])
def get_student_info():
    student_id = request.args.get('student_id')
    
    # redirect to all students if no id was provided
    if student_id is None:
        return redirect(url_for("get_students"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    
    # check to see if the name needs to be updated
    new_first = request.args.get('first_name')
    new_last = request.args.get('last_name')
    if new_first is not None and new_last is not None:
        mycursor.execute("""UPDATE student set first_name=%s,last_name=%s where id=%s""", (new_first, new_last, student_id))
        connection.commit()

    # check to see if a section needs to be dropped
    drop_section_id = request.args.get('drop_section_id')
    if drop_section_id is not None:
        mycursor.execute("""DELETE from section_student where student_id=%s and section_id=%s""", (student_id, drop_section_id))
        connection.commit()

    # check to see if a section needs to be added
    add_section_id = request.args.get('add_section_id')
    if add_section_id is not None:
        mycursor.execute("""INSERT into section_student (student_id, section_id) values (%s, %s)""", (student_id, add_section_id))
        connection.commit()

    # retreve the student information from the database
    mycursor.execute("Select first_name, last_name from student where id=%s", (student_id,))
    student_first, student_last = mycursor.fetchone()
    if student_first is None or student_last is None:
        return """Error - unable to find student. <a href="/students">Return to the student list</a>"""
    
    # retrieve the student's courses from the database
    mycursor.execute("""SELECT section.id,course_name,course_code, meeting_time, meeting_days, meeting_room from section_student
                         join section on section.id=section_student.section_id
                         join course on course.id=section.course_id
                         where section_student.student_id=%s""", (student_id,))
    registered_sections = mycursor.fetchall()
    

    # retrieve a list of other courses the student can register for
    mycursor.execute("""SELECT section.id,course_name,course_code
                     from (
                         select id as section_id from section
                         except
                         select section_id from section_student where student_id=%s) as remainingsections
                     join section on remainingsections.section_id=section.id
                     join course on course.id=section.course_id""", (student_id,))
    all_sections = mycursor.fetchall()

    mycursor.close()
    connection.close()

    return render_template(
        "student_info.html", 
        student_id=student_id, 
        first_name=student_first, 
        last_name=student_last,
        registered_sections=registered_sections,
        unregistered_sections=all_sections
        )

@app.route('/students', methods=['GET'])
def get_students():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # check to see if a new student needs to be added
    new_student_id = request.args.get('new_student_id')
    new_student_first = request.args.get('new_student_first')
    new_student_last = request.args.get('new_student_last')
    if new_student_id is not None and new_student_first is not None and new_student_last is not None:
        mycursor.execute("INSERT INTO student (id, first_name, last_name) values (%s, %s, %s)", (new_student_id, new_student_first, new_student_last))
        connection.commit()

    # check to see if a student needs to be deleted
    delete_student_id = request.args.get('delete_student_id')
    if delete_student_id is not None:
        try:
            mycursor.execute("delete from student where id=%s",(delete_student_id,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting student, perhaps they are registered for a class")
        
    # retrieve all students
    mycursor.execute("SELECT id,first_name,last_name from student")
    pageTitle = "Showing all students"
    allStudents = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('students.html', studentList=allStudents, pageTitle=pageTitle)



@app.route('/sections', methods=['GET'])
def get_sections():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # check to see if a new section needs to be added
    new_section_info = (
        request.args.get('new_section_id'), 
        request.args.get('new_course_id'), 
        request.args.get('new_meeting_time'), 
        request.args.get('new_meeting_days'), 
        request.args.get('new_meeting_room')
    )
    
    if not None in (new_section_info):
        mycursor.execute("INSERT INTO section (id, course_id, meeting_time, meeting_days, meeting_room) values (%s, %s, %s, %s, %s)", new_section_info)
        connection.commit()

    # check to see if a section needs to be deleted
    delete_section_id = request.args.get('delete_section_id')
    if delete_section_id is not None:
        try:
            mycursor.execute("delete from section where id=%s",(delete_section_id,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting section, perhaps there are students registered for it")

    # retrieve all sections
    mycursor.execute("SELECT section.id, course_name, course_code, meeting_time, meeting_days, meeting_room from section join course on course_id=course.id")
    allSections = mycursor.fetchall()
    pageTitle = "Showing all sections"
    mycursor.execute("SELECT id, course_name, course_code from course")
    allCourses = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('sections.html', sectionList=allSections, pageTitle=pageTitle, allCourses=allCourses)

@app.route('/courses', methods=['GET'])
def get_courses():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # look to see if a new course should be added
    new_course_info = (
        request.args.get('new_course_id'),
        request.args.get('new_course_name'),
        request.args.get('new_course_code')
    )
    if not None in new_course_info:
        mycursor.execute("INSERT INTO course (id, course_name, course_code) values (%s, %s, %s)", new_course_info)
        connection.commit()

    # look to see if a course should be deleted
    delete_course_id = request.args.get('delete_course_id')
    if delete_course_id is not None:
        try:
            mycursor.execute("DELETE from course where id=%s", (delete_course_id,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting course, perhaps it has sections")

    # retrieve a list of all courses
    mycursor.execute("SELECT id, course_name, course_code from course")
    allCourses = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('courses.html', allCourses=allCourses)

@app.route('/course-info', methods=['GET'])
def get_course_info():
    course_id = request.args.get('course_id')
    
    # redirect to all courses if no id was provided
    if course_id is None:
        return redirect(url_for("get_courses"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # update course information
    course_name = request.args.get('course_name')
    course_code = request.args.get('course_code')
    if course_name is not None and course_code is not None:
        mycursor.execute("UPDATE course set course_name=%s, course_code=%s where id=%s", (course_name, course_code, course_id))
        connection.commit()

    # retrieve course information
    mycursor.execute("SELECT course_name, course_code from course where id=%s", (course_id,))
    try:
        course_name, course_code = mycursor.fetchall()[0]
    except:
        return render_template("error.html", message="Error retrieving course - perhaps it doesn't exist")
    
    # retrieve existing sections of course
    mycursor.execute("SELECT id, meeting_time, meeting_days, meeting_room from section where course_id=%s", (course_id,))
    existingSections = mycursor.fetchall()
    
    mycursor.close()
    connection.close()

    return render_template("course-info.html",
                           course_id=course_id,
                           course_name=course_name,
                           course_code=course_code,
                           existingSections=existingSections
                           )

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")