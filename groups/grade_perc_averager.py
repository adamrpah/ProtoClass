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

def concat_spreadsheets(indir, debug):
    '''
    Given the directory, concatenate all spreadsheets
    '''
    ind_dfs = []
    for efile in glob.glob( os.path.join(indir, '*.xlsx') ):
        print(efile)
        temp = pd.read_excel(efile, sheetname = 0)
        temp['ContributionPercentage'] = temp['ContributionPercentage'] / temp['ContributionPercentage'].max()
        if debug == True:
            print(efile)
            print(temp.loc[:, ['Name', 'ContributionPercentage']])
        ind_dfs.append( temp)
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
    # Concate it all
    peerdf = concat_spreadsheets(args.peerdir, args.debug)

    #Average out all the sheets
    countdf = peerdf.groupby('Name').agg(['count'])
    temp_additions = {'Name': [],
                      'ContributionPercentage': [],
                      'Reason': []}
    for name, ncount in zip(countdf.index, countdf[countdf.columns[0]]):
        while ncount < 4:
            temp_additions['Name'].append(name)
            temp_additions['ContributionPercentage'].append(1.0)
            temp_additions['Reason'].append('')
            ncount += 1
    temp_add_df = pd.DataFrame(temp_additions)
    #Append the temp addition
    pdf = pd.concat([peerdf, temp_add_df])

    #Group it up
    groupdf = pdf.groupby('Name').mean()
    percentages = dict( zip(groupdf.index.tolist(), 
                            groupdf.ContributionPercentage.values.tolist()) )

    if args.debug == True:
        print( percentages )

    with open('peer_percentages.csv', 'w') as wfile:
        print('Student,AvgPerc', file=wfile)
        for name in sorted( list(percentages.keys()) ):
            print('%s,%f' % (name, percentages[name]), file=wfile )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('peerdir', help = 'Directory of peer evaluations')
    parser.add_argument('--debug', help = 'debug mode', action = 'store_true')
    args = parser.parse_args()
    main(args)
