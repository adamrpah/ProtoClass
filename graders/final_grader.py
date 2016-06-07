'''
File: final_grader.py
Author: Adam Pah
Description:    
Given a rubric and a directory of finals, grades the final multiple choice answers.

'''

#Standard path imports
from __future__ import division, print_function
import argparse
import glob
import os

#Non-standard imports
import pandas as pd

#Global directories and variables

def main(args):
    #Load the answer key
    #Answer key must have the headings ['Problem', 'Your Answer', 'Answer Format']
    answer_df = pd.read_excel(args.answer_key, sheet=0)

    #Score
    scores = {}

    #Go through the individual sheets
    for student_answer in glob.glob(os.path.join( args.assign_dir, '*xlsx') ):
        print(student_answer)
        student_df = pd.read_excel(student_answer, sheet=0)
        #Check to make sure that the column headings are equal
        if (student_df.columns != answer_df.columns).all():
            print('ERROR with: %s' % student_answer)
        else:
            #Proceed with grading
            equal = (answer_df['Your Answer'].str.lower() == student_df['Your Answer'].str.lower())
            #Count all the false values
            eqval = equal.value_counts()
            #Pull the students name
            path, fname = os.path.split(student_answer)
            student_name = fname.split('_')[0]
            #True grade set
            scores[student_name] = eqval[eqval.index == True].values[0]

    #Sort and print a csv
    with open('exam_scores.csv', 'w') as wfile:
        print('Student,Score', file=wfile)

        for sname in sorted( list(scores.keys()) ):
            print( '%s,%d' % (sname, scores[sname]), file=wfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('assign_dir', help='Directory of assignments')
    parser.add_argument('answer_key', help='Answer key')
    args = parser.parse_args()
    main(args)
