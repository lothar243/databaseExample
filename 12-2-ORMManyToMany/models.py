from extensions import db

# Association table for the many-to-many relationship
section_student = db.Table('section_student',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('section_id', db.Integer, db.ForeignKey('section.id'), primary_key=True)
)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    # Define the relationship
    sections = db.relationship('Section', secondary=section_student, backref=db.backref('students', lazy='dynamic'))

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    meeting_time = db.Column(db.String(30))
    meeting_days = db.Column(db.String(30))
    meeting_room = db.Column(db.String(30))
    # Foreign key to Course
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10))
    course_name = db.Column(db.String(30))
    # One-to-many relationship with sections
    sections = db.relationship('Section', backref='course', lazy=True)