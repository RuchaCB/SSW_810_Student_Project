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

        self.majors = dict ()
        self.req_elec = dict()
        self.list_courses = []
        self.required = []
        self.elective = []
        self.add_majors(os.path.join(dir, "majors.txt"))
        self.major_pt()

    def add_majors(self, major_file_path):
        for dept, r_e, courses in file_reader(major_file_path, 3, "\t"):
            if dept not in self.majors:
                if r_e not in self.req_elec:
                    self.req_elec[r_e]= courses
                else:
                    self.req_elec[r_e]= courses
                self.majors[dept]=self.req_elec
                '''self.required.append(courses)
                elif str(req_elec)=='E':
                    self.elective.append(courses)
                self.majors[dept]= self.required, self.elective
            else:
                if str(req_elec)=='R':
                    self.required.append(courses)
                elif str(req_elec)=='E':
                    self.elective.append(courses)
                self.majors[dept]= self.required, self.elective'''
        print(self.majors)
'''
    def major_pt(self):
        print ('Major Summary')
        pt = PrettyTable(field_names=['Department', 'Required', 'Electives'])
        for major in self.majors:
            pt.add_row(major)
        print (pt)

    def major_pt(self):
        print ('Major Summary')
        pt = PrettyTable(field_names=['Department', 'Required', 'Electives'])
        for key, value in self.majors.items():
            print (key, value)
            for i in [value]:
                print (i)
                
                pt.add_row([key, i[0], i[1]])
            #for req, elec in value:
            #    print (req, elec)
                
        print (pt)

'''
def main():
    ob = Repository("/Users/ruchabhatawadekar/Desktop/Stevens")

if __name__ == '__main__':
    #unittest.main(exit=False, verbosity=2)
    main()
