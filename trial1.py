import datetime
import os
import unittest
from collections import defaultdict
from prettytable import PrettyTable
import unittest

def file_reader(path, num_fields, seperator=',', header=False):
    '''Read file'''
    a = open(path, 'r')
    with a:
        for i, line in enumerate(a):
            line_split = line.rstrip("\n")
            line_split = line_split.split(seperator)
            if len(line_split) != num_fields:
                raise ValueError(f"{path} line: {i+1}: read {len(line_split)} fields but expected {num_fields}")
            if header and i == 0 :
                continue
            yield tuple(line_split)


class Repository():

    def __init__(self, dir):
        self.students = dict()
        self.instructors = dict()
        self.majors = dict ()
        self.add_students(os.path.join(dir, "students.txt"))
        self.add_instructors(os.path.join(dir, "instructors.txt"))
        self.add_grades(os.path.join(dir, "grades.txt"))
        self.add_majors(os.path.join(dir, "majors.txt"))
        self.student_pt()
        self.instructor_pt()
        self.major_pt()

    def add_major_courses(self, major_file_path):
        for dept, r_e, course in file_reader(major_file_path, 3, "\t"):
            if dept not in self.majors:
                self.majors[dept] = Major(dept)
            self.majors[dept].add_course(course, r_e)

    def add_students(self, students_file_path):
        for s_cwid, s_name, major in file_reader(students_file_path, 3, "\t"):
            if s_cwid not in self.students:
                self.students[s_cwid] = Student(s_cwid, s_name, major)

    def add_instructors(self, instructor_file_path):
        for i_cwid, i_name, department in file_reader(instructor_file_path, 3, "\t"):
            if i_cwid not in self.instructors:
                self.instructors[i_cwid] = Instructor(i_cwid, i_name, department)

    def add_grades(self, grades_file_path):
        for s_cwid, course, grade, i_cwid in file_reader(grades_file_path, 4, "\t"):
            self.students[s_cwid].add_course(course, grade)
            self.instructors[i_cwid].add_course(course)

    def major_pt(self):
        pt = PrettyTable(field_names=Major.fields())
        for major in self.majors.values():
            pt.add_row(major.details())
        print(pt)
  
    def student_pt(self):
        print ('Student Summary')
        pt = PrettyTable(field_names = Student.fields())
        for student in self.students.values():
            pt.add_row(student.details())
        print(pt)

    def instructor_pt(self):
        print ('Instructor Summary')
        pt = PrettyTable(field_names = Instructor.fields())
        for instructor in self.instructors.values():
            for i in instructor.details():
                pt.add_row(i)
        print(pt)

class Major:
    def __init__(self, dept, req_elec, courses):
        self.dept = dept
        self.req_elec = req_elec
        self.courses = courses
        self.required = []
        self.elective = []
        self.course = dict ()

    def sort(self, ):
        for dept, req_elec, courses in file_reader('majors.txt', 3, "\t"):
            if str(req_elec) == 'R':
                self.required.append(courses)
            elif str(req_elec) == 'E':
                self.elective.append(courses)
        print ('self.required',self.required)
        print ('self.elective',self.elective)


    def details(self):
        return [self.dept, self.required, self.elective]

    @staticmethod
    def fields():
        return['Department','Required','Electives']

class Student:
    
    def __init__(self,s_cwid,s_name,major):
        self.s_cwid = s_cwid
        self.s_name = s_name
        self.major = major
        self.course = dict()
    
    def add_course(self,course,grade):
        self.course[course] = grade

    def details(self):
        return[self.s_cwid,self.s_name,sorted(self.course.keys())]

    @staticmethod
    def fields():
        return['CWID','name','course']
    
class Instructor:

    def __init__(self,i_cwid,i_name,dept):
        self.i_cwid = i_cwid
        self.i_name = i_name
        self.dept = dept
        self.course = defaultdict(int)
    
    def add_course(self,course):
        self.course[course] += 1
    
    def details(self):
        for course,Student in self.course.items():
            yield[self.i_cwid,self.i_name,self.dept, course,Student]

    @staticmethod
    def fields():
        return["Cwid","name","dept","course","students"]

'''
class RepositoryTest(unittest.TestCase):

    def test_init(self):
        path = "/Users/ruchabhatawadekar/Desktop/Stevens"
        repository = Repository(path)
        result1 = {'10103': ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']], '10115': ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']], '10172': ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']], '10175': ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']], '10183': ['10183', 'Chapman, O', ['SSW 689']], '11399': ['11399', 'Cordova, I', ['SSW 540']], '11461': ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']], '11658': ['11658', 'Kelly, P', ['SSW 540']], '11714': ['11714', 'Morton, A', ['SYS 611', 'SYS 645']], '11788': ['11788', 'Fuller, E', ['SSW 540']]}
        result2 = dict()

        for keys, values in repository.students.items():
            result2[keys] = values.details()

        self.assertEqual(result1, result2)
'''
    
def main():
    ob = Repository("/Users/ruchabhatawadekar/Desktop/Stevens")

if __name__ == '__main__':
    #unittest.main(exit=False, verbosity=2)
    main()
