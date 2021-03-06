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
    df_courses = student_demand(df_demand)

    # forecast enrollment
    df_forecast = pd.DataFrame({'course number' : [x for x in dg.cs_courses.keys()],
                               'course name'   : [x for x in dg.cs_courses.values()] })

    # add the column from df_course which contains the amount of students currently enrolled in each course
    df_forecast['enrolled'] = df_courses['current']
    # multiply course pass rate by number currently enrolled and round to nearest whole number
    df_forecast['passing'] = df_courses['current'].multiply(\
                             df_grade_stats['Success Ratio'], axis='index').round()
    df_forecast['demand'] = df_courses['wanted']

    df_forecast.sort_values(by='course number', inplace=True)

    # output top and bottom of DataFrame to user
    print("* df_forecast.head()", df_forecast.head(), sep="\n", end="\n\n")
    print("* df_forecast.tail()", df_forecast.tail(), sep="\n", end="\n\n")

    # save dataframe to directory
    df_forecast.to_csv('forecast.csv')

def student_demand(df):
    # create new DataFrame which holds all courses
    df_course = pd.DataFrame({'course number' : [x for x in dg.cs_courses.keys()],
                              'course name'   : [x for x in dg.cs_courses.values()] })

    # extract current course list
    current_courses = df['Current Courses'].tolist()
    # extract wanted course list
    wanted_courses = df['Wanted Courses'].tolist()

    # count number of students currently taking each course
    courses = []
    for course in dg.cs_courses.keys():
        # create tuple of (course number, current course sum, wanted course sum)
        courses.append((course, 
                       sum([x.count(course) for x in current_courses]),
                       sum([x.count(course) for x in wanted_courses])))

    # append number of students currently taking a course to df
    df_course['current'] = [x[1] for x in courses]
    # append number of students wanting to take a course to df
    df_course['wanted'] = [x[2] for x in courses]
    
    ''' Alternate way of performing two lines above
    for x in courses:
        df_course['current'], df_course['wanted'] = x[1:3]
    '''
    
    # save stats to directory
    df_course.to_csv('student_stats.csv')
    
    # return demand df
    return df_course

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
        #df_grade_stats['Passing' + str(i)]
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
            '3':'Forecast Enrollment.',
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

        selection = int(input('Please Select: ')) 

        # Load/Generate Grades
        if selection == 1: 
            try:
                print()
                list_df_grades = handle_grades()
                print()
                grades_loaded = True
            except:
                print('Grades were not loaded successfully.\n')

        # Load/Generate Demand
        elif selection == 2: 
            try:
                print()
                df_demand = handle_demand()
                print()
                demand_loaded = True
            except:
                print('Demand was not loaded successfully.\n')

        # Forecast Enrollment
        elif selection == 3:
            if grades_loaded == False or demand_loaded == False:
                print('\nMust use option 1 and 2 to load grades/demand before option 3 is possible.\n')
            else:
                print()
                forecast_enrollment(list_df_grades, df_demand)
                print("\nFile has been saved to 'forecast.csv' in the working directory")
                print()

        # Exit
        elif selection == 4:
            print('\n\nGoodbye!')
            break

        # Unknown Menu Entry
        else: 
            print('\nUnknown Option Selected!\n')

if __name__ == '__main__':
    main()