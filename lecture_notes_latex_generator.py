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

# ========= COLOR CODES =========
color_end               = '\033[0m'
color_darkgrey          = '\033[90m'
color_red               = '\033[91m'
color_green             = '\033[92m'
color_yellow            = '\033[93m'
color_blue              = '\033[94m'
color_pink              = '\033[95m'
color_cyan              = '\033[96m'
color_white             = '\033[97m'
color_grey              = '\033[98m'

# ========= COLORED STRINGS =========
str_prefix_q            = f"[{color_pink}Q{color_end}]"
str_prefix_y_n          = f"[{color_pink}y/n{color_end}]"
str_prefix_ques         = f"{str_prefix_q}\t "
str_prefix_err          = f"[{color_red}ERROR{color_end}]\t "
str_prefix_done         = f"[{color_green}DONE{color_end}]\t "
str_prefix_info         = f"[{color_cyan}INFO{color_end}]\t "

def yes_or_no(str_ask):
    while True:
        y_n = input(f"{str_prefix_q} {str_prefix_y_n} {str_ask}").lower()
        if len(y_n) == 0:
            return True
        elif y_n[0] == "y":
            return True
        elif y_n[0] == "n":
            return False
        if y_n[0] == "q":
            sys.exit()
        else:
            print(f"{str_prefix_err} {error_neither_y_n}")

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

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
    # Confirming Week 1's start date
    week1monday = ""
    year = semester[:4] # Get inputted year (first 4 characters)
    partOfYear = semester[4:] # W or F of SU (rest of string after 4 characters)
    if partOfYear == "W":
        month = 1 # January
    elif partOfYear == "F":
        month = 9 # September
    elif partOfYear == "SU":
        month = 5 # Summer semester starts in May (2022: May 9)
    if date.now().month > 1:
        d = datetime.date(year, 1, 7)
    else:
        d = datetime.date(date.now().year, 1, 7)
    next_monday = next_weekday(d, 0)
    currentDate = date.now().strftime("%Y %m %d")
    while True:
        confirm_weekday = yes_or_no(f"Is the start of {semester} {next_monday.strftime('%Y %m %d')} [y/n]? ")
        if confirm_weekday:
            break
        else:
            print("NOT DONE - Incorrect start date")
    lectureCount = 1
    for weekNum in range(1, 12): # There are normally 12 weeks in a semester
        # TODO: Account for skipping reading week
        print("\n\\section{Week " + str(weekNum) + "}") # Each week section line
        for lectureDay in weekdays: # Generating each subsection for every weekday in the week
            if lectureDay == "M":
                d = next_weekday(d, 0) # 0 = Monday
            elif lectureDay == "T":
                d = next_weekday(d, 1) # 1 = Tuesday
            elif lectureDay == "W":
                d = next_weekday(d, 2) # 2 = Wednesday
            elif lectureDay == "R": # R = How York represents Thursday since T is used by Tuesday
                d = next_weekday(d, 3) # 3 = Thursday
            elif lectureDay == "F":
                d = next_weekday(d, 4) # 4 = Friday
            tDateFormatted = d.strftime("%Y %m %d")
            print("\\subsection{Lecture " + str(lectureCount) + ": " + tDateFormatted + "}")
            print("\\begin{itemize*}")
            print("\t\\item ")
            print("\\end{itemize*}\n")
            lectureCount += 1 # Increase lecture counter for the subsections
    # TODO: Place newly generated lines here
    sys.exit()


if __name__ == "__main__":
    main()
