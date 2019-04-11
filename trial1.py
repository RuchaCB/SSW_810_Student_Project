import datetime
import os
import unittest
from collections import defaultdict
from prettytable import PrettyTable
import unittest

def file_reader(path, num_fields, sep=",", header=False):
    try:
        fp = open(path, "r")
    except FileNotFoundError:
        print("Can't open", path)
    else:
        with fp:
            for index, line in enumerate(fp):
                line_split = line.strip().split(sep)
                if len(line_split) != num_fields:
                    raise ValueError(f"{path} line: {index+1}: read {len(line_split)} fields but expected {num_fields}")
                if index == 0 and header:
                    continue   
                yield tuple(line_split)

class Repository:
    def __init__(self, dir):
        self.students = dict()
        self.instructors = dict()
        self.majors = dict()
        self.add_students(os.path.join(dir, "students.txt"))
        self.add_instructors(os.path.join(dir, "instructors.txt"))
        self.add_grades(os.path.join(dir, "grades.txt"))
        self.add_major(os.path.join(dir, "majors.txt"))
        self.remaining_courses()
        self.major_pt()
        self.student_pt()
        self.instructor_pt()

    def add_students(self, students_file_path):
        for s_cwid, s_name, major in file_reader(students_file_path, 3, "\t"):
            if s_cwid not in self.students:
                self.students[s_cwid] = Student(s_cwid, s_name, major)
    
    def add_instructors(self, instructor_file_path):
        for i_cwid, i_name, dept in file_reader(instructor_file_path, 3, "\t"):
            if i_cwid not in self.instructors:
                self.instructors[i_cwid] = Instructor(i_cwid, i_name, dept)

    def add_grades(self, grades_file_path):
        for s_cwid, course, grade, i_cwid in file_reader(grades_file_path, 4, "\t"):
            self.students[s_cwid].add_course(course, grade)
            self.instructors[i_cwid].add_course(course)
     
    def add_major(self, major_file_path):
        for dept, r_or_e, course in file_reader(major_file_path, 3, "\t"):
            if dept not in self.majors:
                self.majors[dept] = Major(dept)
            self.majors[dept].add_course(course, r_or_e)

    def remaining_courses(self):
        for student in self.students.values():
            student.req, student.elec = self.majors[student.major].get_req(student.courses)
     
    def student_pt(self):
        print ('Student Summary')
        pt = PrettyTable(field_names=Student.fields())
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

    def major_pt(self):
        print("Major Summary")
        pt = PrettyTable(field_names = Major.fields())
        for major in self.majors.values():
            pt.add_row(major.details())
        print(pt)

class Student:

    def __init__(self, s_cwid, s_name, major):
        self.s_cwid = s_cwid
        self.s_name = s_name
        self.major = major
        self.courses = dict()
        self.req = []
        self.elec = []

    def add_course(self, course, grade):
        if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C']:
            self.courses[course] = grade

    def details(self):
        return [self.s_cwid, self.s_name, self.major, sorted(self.courses.keys()), self.req, self.elec]

    @staticmethod
    def fields():
        return ["S_CWID", "S_name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives"]

class Instructor:

    def __init__(self, i_cwid, i_name, dept):
        self.i_cwid = i_cwid
        self.i_name = i_name
        self.dept = dept
        self.courses = defaultdict(int) 

    def add_course(self, course):
        self.courses[course] += 1

    def details(self):
        for course, students in self.courses.items():
            yield [self.i_cwid, self.i_name, self.dept, course, students]

    @staticmethod
    def fields():
        return ["I_CWID", "I_name", "Dept", "Course", "Students"]

class Major:
    def __init__(self, major):
        self.major = major
        self.req = list()
        self.elec = list()

    def add_course(self, course, r_or_e):
        if r_or_e == "R":
            self.req.append(course)
        elif r_or_e == "E":
            self.elec.append(course)

    def get_req(self, courses_completed):
        result1 = []
        result2 = []
        for course in self.req:
            if course not in courses_completed:
                result1.append(course)
        
        for elective in self.elec:
            if elective not in courses_completed:
                result2.append(elective)
            else:
                result2 = "-"
                break  
        return (result1, result2)

    def details(self):
        return [self.major, sorted(self.req), sorted(self.elec)]

    @staticmethod
    def fields():
        return ["Dept", "Required", "Electives"]

class MajorTest(unittest.TestCase):
    def test_init(self):
        m1 = Major('SSW')
        self.assertEqual(m1.major, "SSW")


class StudentTest(unittest.TestCase):
    def test_init(self):
        s1 = Student("110", "Rucha, C", "SE")
        self.assertEqual(s1.s_cwid, "110")
        self.assertEqual(s1.s_name, "Rucha, C")
        self.assertEqual(s1.major, "SE")
        self.assertEqual(s1.courses, {})

    def test_add_course(self):
        s1 = Student("110", "Rucha, C", "SE")
        s1.add_course("SSW 540", "A")
        s1.add_course("SSW 810", "A")
        s1.add_course("SSW 564", "A")
        self.assertEqual(s1.courses, {'SSW 540': 'A','SSW 564': 'A','SSW 810': 'A'})
        
    def test_details(self):
        s1 = Student("110", "Rucha, C", "SSW")
        s2 = Student("210", "Ved, C", "CS")
        s1.add_course("SSW 540", "A")
        s1.add_course("SSW 810", "A")
        s1.add_course("SSW 564", "A")
        s2.add_course("CS 540", "A")
        s2.add_course("CS 810", "A")
        s2.add_course("CS 564", "A")
        self.assertEqual(s1.details(), ['110', 'Rucha, C', 'SSW', ['SSW 540', 'SSW 564', 'SSW 810'], [], []])
        self.assertEqual(s2.details(), ['210', 'Ved, C', 'CS', ['CS 540', 'CS 564', 'CS 810'], [], []])

class InstructorTest(unittest.TestCase):
    def test_init(self):
        i1 = Instructor("310", "Chintan, M", "SSW")

        self.assertEqual(i1.i_cwid, "310")
        self.assertEqual(i1.i_name, "Chintan, M")
        self.assertEqual(i1.dept, "SSW")
        self.assertEqual(i1.courses, {})
        self.assertEqual(i1.courses['test_key'], 0)

    
    def test_add_course(self):
        i1 = Instructor("310", "Chintan, M", "SSW")
        i1.add_course("SSW 540")
        i1.add_course("SSW 810")
        i1.add_course("SSW 540")
        i1.add_course("SSW 810")
        i1.add_course("SSW 540")
        i1.add_course("SSW 564")
        self.assertEqual(i1.courses, {'SSW 540': 3, 'SSW 564': 1, 'SSW 810': 2})

class RepositoryTest(unittest.TestCase):

    def test_init(self):
        ob = Repository("/Users/ruchabhatawadekar/Desktop/Stevens")
        result1 = {'10103': ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']], '10115': ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']], '10172': ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']], '10175': ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']], '10183': ['10183', 'Chapman, O', ['SSW 689']], '11399': ['11399', 'Cordova, I', ['SSW 540']], '11461': ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']], '11658': ['11658', 'Kelly, P', ['SSW 540']], '11714': ['11714', 'Morton, A', ['SYS 611', 'SYS 645']], '11788': ['11788', 'Fuller, E', ['SSW 540']]}
        result2 = dict()

        for student_cwid, values in ob.students.items():
            result2[student_cwid] = values.details()
        self.assertEqual(result1, result2)

def main():
    unittest.main(exit=False, verbosity=2)
    ob = Repository("/Users/ruchabhatawadekar/Desktop/Stevens")
    

if __name__ == '__main__':
    main()



