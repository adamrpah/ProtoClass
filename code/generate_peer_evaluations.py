'''
File: generate_peer_evaluations.py
Author: Adam Pah
Description: 
Generates peer evaluations given a group assignment spreadsheet.
Input:
    * group evaluation excel spreadsheet (generated with group_randomizer.py)
Output:
    * directory of peer evaluation sheets
'''

#Peer eval is name, perc, reason

#Standard path imports
from __future__ import division, print_function
import argparse
import os

#Non-standard imports
import pandas as pd

#Global directories and variables
peer_dir = 'PeerEvalations'

def main(args):
    #Load the assigned group sheets
    df = pd.read_excel(args.filename, sheetname = 0)

    #Get all of the groups
    groups = df.Group.unique().tolist()

    #Create the directory 
    try:
        os.mkdir(peer_dir)
    except:
        pass

    #Create and save all of the sheets
    for group in groups:
        #Subdf
        gdf = df[df.Group == group]
        #Create the deadlist
        groupset = [[x, '', ''] for x in gdf.Name.values.tolist()]
        #Make the new dataframe
        peerdf = pd.DataFrame(groupset, columns = ['Name', 'ContributionPercentage', 'Reason'])
        #Save it down
        wfname = os.path.join(peer_dir, 'Group-' + str(group) + '.xlsx')
        peerdf.to_excel(wfname, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('filename', help = 'Group assignment Excel spreadsheet')
    args = parser.parse_args()
    main(args)
