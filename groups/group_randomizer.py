'''
File: group_randomizer.py
Author: Adam Pah
Description: 
Creates random group assignments.
Input:
    - email excel spreadsheet - columned with Name, Class, Email (no header)
Output:
    - group assignment excel - alphabetical order, saved in current directory where
                               script is run from.
'''

#Standard path imports
from __future__ import division, print_function
import argparse
import itertools
import random
import os

#Non-standard imports
import pandas as pd

#Global directories and variables

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)

def none_remover(grouplist):
    for i in range( len(grouplist) ):
        while None in grouplist[i]:
            grouplist[i].remove(None)
    return grouplist

def repacker(grouplist):
    #Final index
    fin_index = len(grouplist) - 1
    #First pick a random group
    igroup_index = random.choice( range(len(grouplist) - 1) )
    #Pop the last name off
    pname = grouplist[igroup_index].pop()
    #Add it to the last group
    grouplist[fin_index].append(pname)
    return grouplist

def main(args):
    '''
    Main function
    '''
    #Read the file in given whethere there is a header or not
    if args.header:
        df = pd.read_excel(args.filename, sheetname = args.sheetname)
    else:
        df = pd.read_excel(args.filename, sheetname = args.sheetname, header = None,
                           names = ['Name', 'Class', 'Email'])

    #Pull the names out to randomly shuffle
    rnames = df.loc[:, ['Name', 'Email']].values.tolist()
    random.shuffle(rnames)

    #Group and convert to lists
    groups = [list(x) for x in list(grouper(rnames, args.maxgroupsize))]

    #Remove any nones
    groups = none_remover(groups)

    #check to see what the smallest group size is empty elements there are in the final group
    min_group_size = min([len(x) for x in groups])
    while min_group_size <= (args.maxgroupsize - 2):
        repacker(groups)
        min_group_size = min([len(x) for x in groups])

    #unpack the groups to a dictionary
    revgroup = {}
    for i, group in enumerate(groups):
        for name, email in group:
            revgroup[name] = i

    #Add in a group column to the dataframe
    df['Group'] = df.Name.apply(lambda x: revgroup[x])

    #Write out the dataframe, just name and group id
    wfname, ext = os.path.splitext(args.filename)
    df.to_excel(wfname + '_groups' + ext, columns=['Name', 'Group'], index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('filename', help="Name of Excel document with student names/emails")
    parser.add_argument('--sheetname', default = 0, 
                        help="Sheetname to use in Excel document. Default is first sheet")
    parser.add_argument('--header', default=False, action = 'store_true',
                        help='If there is a header to the email file')
    parser.add_argument('--maxgroupsize', default = 4, type = int,
                        help='Maximum group size')
    args = parser.parse_args()
    main(args)
