"""
Author: Art Grichine
Couse: CS499 - Independent study with Dr. Wortman
Institution: California State University, Fullerton
Environment: Python 3.4
"""
# Built-in libraries
import os
import collections

# scientific libraries
import pandas as pd
import numpy as np

# My functions
import Dataset_Generator as dg

def read_csv_dataset(file_handle):
    """ Get dataset from local path """
    if os.path.exists(file_handle):
        print('-- dataset.csv found locally')
        df = pd.read_csv(file_handle, index_col=0)

        with open(file_handle, 'w') as f:
            print('-- writing to local {} file'.format(file_handle))
            df.to_csv(f)

    return df

def handle_grades():
    print('1 Load Grades')
    print('2 Generate Grades')
    selection = input('Please Select: ')
    grades_df_list = []

    if selection == '1':
        amt_loading = input('How many grade datasets would you like to load? ')
        return amt_loading,[read_csv_dataset\
                            (input('Filename of course grades dataset: '))\
                            for file in range(int(amt_loading))]

    elif selection == '2':
        return dg.generate_grades(input('How many grade datasets would you like to generate? '))
    else:
        raise  # Throw error to main()

def handle_demand():
    print('1 Load Demand')
    print('2 Generate Demand')
    selection = input('Please Select: ')
    
    if selection == '1':
        return read_csv_dataset(input('Filename of demand dataset: '))
    elif selection == '2':
        dg.generate_demand()
        print('Demand generated')
        return read_csv_dataset('demand_data.csv')
    else:
        raise  # Throw error to main()

def forecast_enrollment(dfs_grades, df_demand):
    # compute grade statistics
    df_grade_stats = grade_progression(dfs_grades)

    # compute student demand
    student_demand(df_demand)

    # forecast enrollment

def student_demand(df):
    print(df.head())
    print(df.tail())

def grade_progression(dfs_grades):
    # create Pandas DataFrame to hold grade statistics
    df_grade_stats = pd.DataFrame()
    # Add courses to cooresponding values
    df_grade_stats['Course'] = dfs_grades[0]['Course']
    
    for i, df in enumerate(dfs_grades):
        # select columns that contain passing grades, A+ through C-
        passing_grades = list(df.columns[1:10])
        all_grades = list(df.columns[1:])

        # append passing grades from df to df_grade_stats
        df_grade_stats['Passing {}'.format(i)] = df[passing_grades].sum(axis=1)  # axis=1 is sum across columns
        # append total grades assigned from df to df_grade_stats
        df_grade_stats['Total {}'.format(i)] = df[all_grades].sum(axis=1)

    # extract all passing grade columns in new dataframe
    passing_columns = [x for x in df_grade_stats.columns if 'Passing' in x]
    df_grade_stats['Passing'] = df_grade_stats[passing_columns].sum(axis=1)

    # extract Total amounts of grades given
    total_grades_assigned = [x for x in df_grade_stats.columns if 'Total' in x]
    df_grade_stats['Total'] = df_grade_stats[total_grades_assigned].sum(axis=1)

    # compute course success ratio
    df_grade_stats['Success Ratio'] = df_grade_stats['Passing'].div(df_grade_stats['Total'], axis='index')

    # save df to directory
    df_grade_stats.to_csv('grade_stats.csv')

    return df_grade_stats

def main():
    # Used to make sure data is loaded before attempting to forecast enrollment
    grades_loaded = False
    demand_loaded = False

    # Dictionary containing menu items
    menu = {'1':'Generate or Load course grades.',
            '2':'Generate or Load student demand.',
            '3':'Compute course demand.',
            '4':'Exit'}
    # Sort dictionary in correct order
    menu = collections.OrderedDict(sorted(menu.items()))

    print('\nWelcome to the enrollement forcasting program. Please choose from the')
    print('following menu. Note: Data for student demand and course grades must')
    print('be loaded or generated before option 5 is available.\n')

    """
    ===================================
                   Menu
    ===================================
    """
    while True: 
        # Print menu
        for key, value in menu.items(): 
            print(key, value)

        selection = input('Please Select: ') 

        # Load/Generate Grades
        if selection == '1': 
            try:
                print()
                list_df_grades = handle_grades()
                print()
                grades_loaded = True
            except:
                print('Grades were not loaded successfully.\n')

        # Load/Generate Demand
        elif selection == '2': 
            try:
                print()
                df_demand = handle_demand()
                print()
                demand_loaded = True
            except:
                print('Demand was not loaded successfully.\n')

        # Forecast Enrollment
        elif selection == '3':
            if grades_loaded == False or demand_loaded == False:
                print('\nMust use option 1 and 2 to load grades/demand before option 3 is possible.\n')
            else:
                print()
                forecast_enrollment(list_df_grades, df_demand)
                print()

        # Exit
        elif selection == '4':
            print('\n\nGoodbye!')
            break

        # Unknown Menu Entry
        else: 
            print('\nUnknown Option Selected!\n')

if __name__ == '__main__':
    main()