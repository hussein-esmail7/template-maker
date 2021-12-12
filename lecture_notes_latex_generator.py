'''
lecture_notes_latex_generator.py
Hussein Esmail
Created: 2021 12 11
Updated: 2021 12 11
Description: This program generates a LaTeX template for School course notes
'''

import os
import sys
import re
from datetime import datetime as date

def yes_or_no(str_ask):
    while True:
        y_n = input(f"{str_prefix_q} {str_prefix_y_n} {str_ask}").lower()
        if y_n[0] == "y":
            return True
        elif y_n[0] == "n":
            return False
        if y_n[0] == "q":
            sys.exit()
        else:
            print(f"{str_prefix_err} {error_neither_y_n}")

def main():
    author = "Hussein Esmail"
    fileName = sys.argv[-1] # Filename passed by templatemaker
    courseCode = ""
    while True:
        courseCode = input("Course code (with spaces): ")
        if yes_or_no(f"Is your code {courseCode} [y/n]? "):
            break
    weekdays = ""
    while True:
        weekdays = input("Input weekdays this course happens (MTWRF): ").strip().replace(" ", "")
        if bool(re.match("^[MTWRFmtwrf]+$", weekdays)):
            break
        else:
            print("Please only enter only MTWRF characters!")
    prof = ""
    while True:
        prof = input("Prof: ")
        if yes_or_no(f"Is your prof {prof} [y/n]? "):
            break
    semester = ""
    while True:
        semester = input("Year and Semester (Ex: 2021F): ")
        if bool(re.match("^[0-9]{4}(W|F|SU)$", semester)):
            break
        else:
            print("Please only enter in the correct format.")

    currentDate = date.now().strftime("%Y %m %d")
    # TODO: Place newly generated lines here
    sys.exit()


if __name__ == "__main__":
    main()
