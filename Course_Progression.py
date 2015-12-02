"""
Author: Art Grichine
Couse: CS499 - Independent study with Dr. Wortman
Institution: California State University, Fullerton
Environment: Python 3.4
"""
import os

import Dataset_Generator

import pandas as pd
import numpy as np


def read_csv_dataset(file_handle):
    """ Get dataset from local path """
    if os.path.exists(file_handle):
        print('-- dataset.csv found locally')
        df = pd.read_csv(file_handle, index_col=0)

        with open(file_handle, 'w') as f:
            print('-- writing to local {} file'.format(file_handle))
            df.to_csv(f)
    
    return df

def main():
    df_students = read_csv_dataset('dataset.csv')
    df_grades = read_csv_dataset('grades_dataset.csv')
    
    """ Print top and bottom of data """
    print("* df_students.head()", df_students.head(), sep="\n", end="\n\n")
    print("* df_students.tail()", df_students.tail(), sep="\n", end="\n\n")
    
    print("* df_grades.head()", df_grades.head(), sep="\n", end="\n\n")
    print("* df_grades.tail()", df_grades.tail(), sep="\n", end="\n\n")
    
if __name__ == '__main__':
    Dataset_Generator       # Generate Data (not needed if dataset.csv/grades_dataset.csv exist)
    main()