from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')

def hello():
    return "Hello world!"

@app.route('/goodbye')

def goodbye(): 
    return("Bye!")


@app.route('/instructor_courses')

def instructor_courses(): 
    
    query = """select i.cwid, i.name, i.dept, g.course, count(g.Student_CWID) as students from instructors i join grades g on i.cwid = g.Instructor_CWID group by i.cwid, i.name, i.dept, g.course """

    DB_FILE = DB_File = "/Users/rahil/Documents/Stevens/SSW 810/HW12/hw11_startup.db"
    db = sqlite3.connect(DB_FILE)
    results = db.execute(query)

    data = [{'cwid': cwid, 'name': name, 'department': department, 'course': course, 'students': students}
            for cwid, name, department, course, students in results]
    
    db.close()

    return render_template('instructor_courses.html', 
                            title = 'Stevens Repository', 
                            table_title = 'Instructor Summary', 
                            instructors = data)

app.run(debug=True)
