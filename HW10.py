from collections import defaultdict
from prettytable import PrettyTable
from q2 import read_file
import sqlite3
DB_File = "/Users/rahil/Documents/Stevens/SSW 810/HW11/810_startup.db"
db = sqlite3.connect(DB_File)

class Repository: 

    def __init__(self): 
        self.students = defaultdict(str) 
        self.instructors = defaultdict(str)
        self.grades = list()
        self.major = dict()
        self.track_instructor = defaultdict()
        self._count = 0

    def student_reader(self, path): 
        path = 'students.txt'
        for cwid, name, maj_name in read_file(path, 3, '\t', header=False): 
            maj_name = maj_name.strip()
            if cwid in self.students: 
                print("Error! Duplicate Student CWID!")
            else: 
                self.students[cwid] = Student(cwid, name, maj_name, self.major)    
                
    def instructor_reader(self, path): 
        path="instructors.txt"

        for cwid, name, department in read_file(path, 3, '\t', header=False): 

            self.instructors[cwid] = Instructor(cwid, name, department)
    
    def major_reader(self, path): 
        path = "majors.txt"

        for maj_name, course_type, course in read_file(path, 3, '\t', header=False): 
            course = course.strip()
            if maj_name not in self.major:
                
                self.major[maj_name] = Major(maj_name)
            
            self.major[maj_name].add_course(course_type, course)
    
    def grade_reader(self, path):
        path = 'grades.txt'
    
        for student_cwid, course, grade, instructor_cwid in read_file(path, 4,'\t', header=False):

            if student_cwid in self.students: 
                self.students[student_cwid].add_course(course, grade) 
            else: 
                print("Error! Student not found in the data file!")

            instructor_cwid = instructor_cwid.strip()

        #Code to keep track of instructors and increase the student count

            if instructor_cwid not in self.track_instructor:  
                self._count = 1
                self.track_instructor[instructor_cwid] = self._count
                self._count+=1
            else: 
                temp = self.track_instructor[instructor_cwid]
                temp+=1
                self.track_instructor[instructor_cwid] = temp

        #pushing course dictionary in to instructor dictionary
        
            if instructor_cwid in self.instructors:         

                c = self.track_instructor[instructor_cwid]
                self.instructors[instructor_cwid].add_student(c, course) #changed from .add_student(course)
            else: 
                print("Error! Instructor not found in the data file!")
        

    def student_print(self): 
        pt = PrettyTable(field_names=Student.student_header)
        for student in self.students.values():                          #Missing value of courses because of just values()?
            pt.add_row(student.pretty_table_values()) 

        print(pt)
    
    def instructor_print(self): 
        pt = PrettyTable(field_names=Instructor.instructor_header)      #Accessing instance variables from the class Instructor. Pretty simple (Classname.variables)
        
        for row in db.execute("select i.CWID, i.Name, i.Dept, g.Course, count(g.Student_CWID) as No_of_Students from Instructors i join Grades g on i.CWID = g.Instructor_CWID group by i.CWID, i.Name, i.Dept, g.Course"):
            pt.add_row(row)

        print(pt)
    
    def major_print(self): 
        pt = PrettyTable(field_names=Major.major_header)
        for major in self.major.values():                          #Missing value of courses because of just values()?
            pt.add_row(major.pretty_table_values()) 
        print(pt)

 


class Student: 
    
    student_header = ["CWID", "Name", "Major", "Completed Courses", "Remaining Courses", "Remaining Electives"]               #Class attribute shared amongst all the instances
    
    def __init__(self, cwid, name, maj_name, major): 
        self._cwid = cwid
        self._name = name
        self._maj_name = maj_name 
        self._major = major
        self._courses = dict() 

    def add_course(self, course, grade): 

        self._courses[course] = grade                                   #So smart! How python implicitly decided course is the key because of allocation of grade to the key
    
    def pretty_table_values(self):

        completed_courses, rem_required, rem_electives = self._major[self._maj_name].grade_check(self._courses)
        return[self._cwid, self._name, self._maj_name, completed_courses, rem_required, rem_electives]  # sorted(self._courses.keys()


class Instructor: 
    
    instructor_header = ["CWID", "Name", "Department", "Courses", "Students"] 
    def __init__(self, cwid, name, department): 
        self._cwid = cwid 
        self._name = name
        self._department = department
        self._no_of_student = dict()
        self._t = list()
        self._count = 0
        # self._no_of_student = defaultdict(int)                   
    
        
        
    def add_student(self, student_number, course): #if similar course then add a counter in itself, else add a new entry with refreshed counter
          
        self._no_of_student[course] = student_number


         
    def pretty_table_values(self): 
        return[self._cwid, self._name, self._department, self._no_of_student.keys(), self._no_of_student.values()]      #Check for ._no of students.key()




class Major: 

    major_header = ["Department", "Required", "Electives"]

    def __init__(self, name): 
        self._name = name
        self._required = set()
        self._electives = set()
        self._passing_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
    
    
    def add_course(self, flag, course): 

        if flag == 'E': 
            self._electives.add(course)
        elif flag == 'R': 
            self._required.add(course)
        else: 
            raise ValueError("Unexpected flag encountered!")
        
    
    def grade_check(self, courses): 

        completed_courses = {course for course, grade in courses.items() if grade in self._passing_grades}
        rem_required = self._required - completed_courses

        if self._electives.intersection(completed_courses): 
            rem_electives = None
        else: 
            rem_electives = self._electives
            rem_electives = list(rem_electives)
        
        return list(completed_courses), list(rem_required), rem_electives
        
    
    def pretty_table_values(self): 
        return[self._name, list(self._required), list(self._electives)]

def main(): 
    
    U1 = Repository()
    U1.major_reader('majors.txt')
    U1.student_reader('students.text')
    U1.instructor_reader('instructors.txt')
    U1.grade_reader('grades.txt')
    # print("\nMajors Summary")
    # U1.major_print()
    # print("\nStudent Summary")
    # U1.student_print()
    print("\nInstructor Summary (Database)")
    U1.instructor_print()
    


if __name__ == '__main__':
    main()