def canvas_grade_sheet_reader(gradefile):
    '''
    Reads the canvas gradesheet, returns the first row and the remainder of the 
    grade sheet
    Input:
        - gradefile - Canvas gradesheet
    Output:
        - frow - First row of gradesheet with the points possible as Series
        - gradedf - Dataframe of Student grades
    '''
    import pandas as pd

    #Read in the gradesheet
    rawgradedf = pd.read_csv(gradefile)    
    #Pull the first row from the dataframe (dead row)
    frow = rawgradedf.loc[0]
    #Pull the rest of the dataframe that is worthwhile
    gradedf = rawgradedf.drop(0) 
    return frow, gradedf

def canvas_recombinator(wfname, frow, gradedf):
    '''
    Recombines the first row with the rest of the gradesheet and writes it out
    '''
    import pandas as pd

    #Concat the series and dataframe
    final = pd.DataFrame([frow.values.tolist()], \
                         columns = gradedf.columns.values).append(gradedf, ignore_index=True)
    final.to_csv(wfname, index=False)
