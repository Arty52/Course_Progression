"""
Author: Art Grichine
Couse: CS499 - Independent study with Dr. Wortman
Institution: California State University, Fullerton
"""
import random

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cs_courses = {'120'  : 'Introduction to Programming',
              '121'  : 'Programming Concepts',
              '131'  : 'Data Structures Concepts',
              '223H' : 'Visual BASIC Programming',
              '223J' : 'Java Programming',
              '223N' : 'C# Programming',
              '223p' : 'Python Programming',
              '223C' : 'C Programming',
              '240'  : 'Computer Organization and Assembly Language',
              '254'  : 'Software Development and Open Source Systems',
              '301'  : 'EPP/Programming Lab Practicum',
              '311'  : 'Technical Writing for Computer Science',
              '313'  : 'The Computer Impact',
              '315'  : 'Social and Ethical issues in computing',
              '322L' : 'Introduction to Computer-Aided Design',
              '323'  : 'Programming Languages and Translation',
              '332'  : 'File Structures and Database Systems',
              '335'  : 'Algorithm Engineering',
              '351'  : 'Operating Systems Concepts',
              '353'  : 'Introduction to Computer Security',
              '362'  : 'Foundations of Software Engineering',
              '386'  : 'Introduction to Game Design and Production',
              '431'  : 'Database and Applications',
              '439'  : 'Theory of Computation',
              '440'  : 'Computer System Architecture',
              '452'  : 'Cryptography',
              '454'  : 'Cloud Computing and Security',
              '456'  : 'Network Security Fundamentals',
              '462'  : 'Software Design',
              '463'  : 'Software Testing',
              '464'  : 'Software Architecture',
              '466'  : 'Software Process',
              '471'  : 'Computer Communications',
              '473'  : 'Web Programming and Data Management',
              '476'  : 'Java Enterprise Application Development',
              '477'  : 'Introduction to Grid Computing',
              '481'  : 'Artificial Intelligence',
              '483'  : 'Data Mining and Pattern Recognition',
              '484'  : 'Principles of Computer Graphics',
              '485'  : 'Computational Bioinformatics',
              '486'  : 'Game Programming',
              '489'  : 'Game Development Project',
              '491T' : 'Variable Topics in Computer Science',
              '495'  : 'Internship in Computer Science',
              '499'  : 'Independent Study'}

# Return a value between 0 and 6. Considers 
# probability p of courses a student is enrolled in
def generate_random_course_amount():   
    return np.random.choice(7, 1, p = [0, 0.1, 0.1, 0.2, 0.3, 0.2, 0.1])[0]

# Generate a list of random samples of student course choices
def generate_samples(amount):
    samples = []
    
    # select a random course load for each student
    for i in range(0, amount):
        samples.append(random.sample(cs_courses.keys(), generate_random_course_amount()))

    return samples

def generate_grades(classes):
    course_distributions = []
    
    for i in range(0, classes):
        mu, sigma = 80, 10 # mean and standard deviation
        s = np.random.normal(mu, sigma, 100) # create random normal distribution

        count, bins, ignored = plt.hist(s, 12, normed=True)

        # Plot probability density function (red line)
        if i==0:
            plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
                            np.exp( - (bins - mu) ** 2 / (2 * sigma**2) ),
                            linewidth=2, color='r')

            plt.title('Grade distribution')
            plt.show()

        # Dictionary containing grade from distribution
        grades = {'A+' : [grade for grade in s if grade >= 97],
                  'A'  : [grade for grade in s if grade >= 93 and grade < 97],
                  'A-' : [grade for grade in s if grade >= 90 and grade < 93],
                  'B+' : [grade for grade in s if grade >= 87 and grade < 90],
                  'B'  : [grade for grade in s if grade >= 83 and grade < 87],
                  'B-' : [grade for grade in s if grade >= 80 and grade < 83],
                  'C+' : [grade for grade in s if grade >= 77 and grade < 80],
                  'C'  : [grade for grade in s if grade >= 73 and grade < 77],
                  'C-' : [grade for grade in s if grade >= 70 and grade < 73],
                  'D+' : [grade for grade in s if grade >= 67 and grade < 70],
                  'D'  : [grade for grade in s if grade >= 60 and grade < 67],
                  'F'  : [grade for grade in s if grade <  60]}

        # List of dictionaries (grades)
        course_distributions.append(grades)

    grades_df = pd.DataFrame({'A+' : [len(grade['A+']) for grade in course_distributions],
                              'A'  : [len(grade['A']) for grade in course_distributions],
                              'A-' : [len(grade['A-']) for grade in course_distributions],
                              'B+' : [len(grade['B+']) for grade in course_distributions],
                              'B'  : [len(grade['B']) for grade in course_distributions],
                              'B-' : [len(grade['B-']) for grade in course_distributions],
                              'C+' : [len(grade['C+']) for grade in course_distributions],
                              'C'  : [len(grade['C']) for grade in course_distributions],
                              'C-' : [len(grade['C-']) for grade in course_distributions],
                              'D+' : [len(grade['D+']) for grade in course_distributions],
                              'D'  : [len(grade['D']) for grade in course_distributions],
                              'F'  : [len(grade['F']) for grade in course_distributions]})

    grades_df.to_csv('grades_dataset.csv')

classes = 100
generate_grades(classes)

students = 1000

df = pd.DataFrame({'Current Courses' : [sample for sample in generate_samples(students)],
                   'Wanted Courses'  : [sample for sample in generate_samples(students)]})

# Show directory top and bottom of directory
print("* df.head()", df.head(), sep="\n", end="\n\n")
print("* df.tail()", df.tail(), sep="\n", end="\n\n")

# Save to current directory
df.to_csv('dataset.csv')