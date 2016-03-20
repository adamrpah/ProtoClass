'''
File: grade_equivocater.py
Author: Adam Pah
Description: 
Changes assigned grade to be the average percentage of the full group grade as assigned by group members
Input:
    * Canvas assigned grades 
    * Directory of Peer evaluation excel sheets
    * Assignment name from Canvas sheet
'''

#Standard path imports
from __future__ import division, print_function
import argparse
import glob
import os

#Non-standard imports
import pandas as pd

import support

#Global directories and variables

def concat_spreadsheets(indir):
    '''
    Given the directory, concatenate all spreadsheets
    '''
    ind_dfs = []
    for efile in glob.glob( os.path.join(indir, '*.xlsx') ):
        ind_dfs.append( pd.read_excel(efile, sheetname = 0) )
    #Load it together
    full_df = pd.concat(ind_dfs)
    return full_df

def perc_applicator(row, assign_name, percentages):
    '''
    Pandas apply function
    Applies the percentage to teh given grade for an assignment
    '''
    return percentages[row.Student] * row[assign_name]

def main(args):
    # Read in the grade sheet
    frow, gradedf = support.canvas_grade_sheet_reader(args.gradefile)

    # Concate it all
    peerdf = concat_spreadsheets(args.peerdir)

    #Average out all the sheets
    groupdf = peerdf.groupby('Name').mean()
    percentages = dict( zip(groupdf.index.tolist(), 
                            [x/100.0 for x in groupdf.ContributionPercentage.values.tolist()]) )
    percentages['Student, Test'] = 0.0

    #Apply the percentages
    gradedf[args.assignment_name] = gradedf.apply(lambda row: perc_applicator(row, args.assignment_name, percentages), axis = 1)

    #Write it out
    support.canvas_recombinator(args.gradefile, frow, gradedf)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('gradefile', help = 'Canvas gradesheet')
    parser.add_argument('peerdir', help = 'Directory of peer evaluations')
    parser.add_argument('assignment_name', action = 'store', type = str,
                        help = 'The column name of the assignment in the Canvas grade file')
    args = parser.parse_args()
    main(args)
