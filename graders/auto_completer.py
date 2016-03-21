'''
File: auto_completer.py
Author: Adam Pah
Description:
Auto completes the grades column given that the assignment was submitted.
'''

#Standard path imports
from __future__ import division, print_function
import argparse
import glob
import os
import re

#Non-standard imports
import pandas as pd

import support

#Global directories and variables

def main(args):
    #Load up the data frame
    frow, grade_df = support.canvas_grade_sheet_reader(args.gradesheet)
    
    #Get all of the filenames
    fnames = [os.path.split(fname)[-1] for fname in glob.glob( os.path.join(args.assign_dir, '*') )]
    file_shortnames = [f.split('_')[0] for f in fnames]

    #Now we have to do something ridiculous. figure out the names from canvas
    shortnames = {}
    for name in grade_df.Student.values.tolist():
        sname = ''.join([x.lower() for x in re.sub(',', '', name).split(' ')])
        shortnames[sname] = name

    #Now lets...do something---go through every filename
    assign_dict = {}
    for shortname, fullname in shortnames.items():
        if shortname in file_shortnames:
            assign_dict[fullname] = frow[args.assignment_name]
        else:
            assign_dict[fullname] = 0

    #Now apply it back
    grade_df[args.assignment_name] = grade_df.Student.apply(lambda name: assign_dict[name])

    #Write it down
    support.canvas_recombinator(args.gradesheet, frow, grade_df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('gradesheet', help = 'Canvas gradesheet')
    parser.add_argument('assign_dir', help = 'Directory of assignments')
    parser.add_argument('assignment_name', help = 'Assignment name')
    args = parser.parse_args()
    main(args)
