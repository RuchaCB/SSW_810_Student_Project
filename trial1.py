from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)

@app.route('/student_courses')
def student_courses():
    query="""SELECT i.CWID, i.Name, i.Dept, g.Course, COUNT (* ) AS number_of_students
                FROM HW11_instructors i
                JOIN HW11_grades g ON i.CWID=g.Instructor_CWID
                GROUP BY g.Course ORDER BY i.CWID DESC;"""
    db = sqlite3.connect("/Users/ruchabhatawadekar/Desktop/SSW_810/Homework/Final/data_base/810_startup.db")
    results = db.execute(query)
    data = [{'cwid' : cwid, 'name' : name, 'dept' : dept, 'course' : course, 'students' : students }
        for cwid, name, dept, course, students in results]

    db.close()

    return render_template('student_courses.html',
                            title='Stevens Repository',
                            table_title="Number of completed courses by Student",
                            students=data)

app.run(debug = True)
   
