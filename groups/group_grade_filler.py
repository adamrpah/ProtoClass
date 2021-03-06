'''
File: group_grade_filler.py
Author: Adam Pah
Description: 
Fills the group grades given the grade from one student to all group members
Input:
    * Canvas grade assignment
    * Group assignments
    * The assignment integer
'''

#Standard path imports
from __future__ import division, print_function
import argparse
import glob

#Non-standard imports
import pandas as pd

import support

#Global directories and variables

def main(args):
    #Read in the gradesheet
    frow, gradedf = support.canvas_grade_sheet_reader(args.gradefile)

    ######
    #Read in the group assignments
    groupdf = pd.read_excel(args.groupfile, sheetname = 0)
    groups = groupdf.Group.unique().tolist()

    ######
    #Apply the grades from one student to all students
    assign_grades = {'Student, Test': ''}
    for group in groups:
        groupnames = groupdf[groupdf.Group == group].Name.tolist()
        #Get the group names, pull the assignment column grade max
        group_grade = gradedf[gradedf.Student.isin(groupnames)][args.assignment_name].max()
        #Record it
        for x in groupnames:
            assign_grades[x] = group_grade

    #Map all grades back
    gradedf[args.assignment_name] = gradedf.Student.apply(lambda name: assign_grades[name])

    #Sub back in the first row, write it out
    support.canvas_recombinator(args.gradefile, frow, gradedf)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('gradefile', help = 'The Canvas grade file')
    parser.add_argument('groupfile', help = 'The Group assignments')
    parser.add_argument('assignment_name', action = 'store', type = str,
                        help = 'The column name of the assignment in the Canvas grade file')
    args = parser.parse_args()
    main(args)
