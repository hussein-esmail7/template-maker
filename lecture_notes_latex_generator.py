'''
lecture_notes_latex_generator.py
Hussein Esmail
Created: 2021 12 11
Updated: 2021 12 14
Description: This program generates a LaTeX template for School course notes
'''

# Test Command:
# python3 lecture_notes_latex_generator.py -a "Hussein Esmail" -c "EECS 3311" -w "MWF" -l "VC 105" -s "A" -p "Andrew Skelton" -y "2022W" -n "3" -t "Software Design" -f "EECS3311.tex"

# TODO: Account for skipping reading week
# TODO: Ask for lecture times (during the day)
# TODO: Account for lab dates and times
# TODO: Account for tutorial dates and times

import os
import os.path
import getopt
import sys
import re
from datetime import datetime as date
import datetime

# ========= COLOR CODES =========
color_end               = '\033[0m'     # Resets color
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
str_prefix_q            = f"[{color_pink}Q{color_end}]"         # "[Q]"
str_prefix_y_n          = f"[{color_pink}y/n{color_end}]"       # "[y/n]"
str_prefix_ques         = f"{str_prefix_q}\t "                  # "[Q]  "
str_prefix_err          = f"[{color_red}ERROR{color_end}]\t "   # "[ERROR]"
str_prefix_done         = f"[{color_green}DONE{color_end}]\t "  # "[DONE]"
str_prefix_info         = f"[{color_cyan}INFO{color_end}]\t "   # "[INFO]"

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

def require_answer(q1):
    # Keeps asking question until user confirms their response is true
    q1ans = ""
    while True:
        q1ans = input(str_prefix_ques + " " + q1).strip()
        if len(q1ans) == 0:
            print(str_prefix_err + " You cannot provide a blank response!")
        elif yes_or_no(f"Is this correct - '{q1ans}'? "):
            break
    return q1ans

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def index_str(list, search_str):
    # Returns first index that contains string
    for num, item in enumerate(list):
        if search_str in item:
            return num
    return -1

def main(argv):
    author = "Hussein Esmail"
    filename = ""
    path_template_dir = os.path.expanduser("~/git/templates/")
    path_template_file = "lecture-template.tex"
    currentDate = date.now().strftime("%Y %m %d")
    lines_append = []
    weekdays = ""
    courseCode = ""
    courseLocation = ""
    courseTitle = ""
    courseSection = ""
    prof = ""
    semester = ""
    courseCredits = ""

    # Process user arguments
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    try:
        opts, args = getopt.getopt(argv,"ha:f:c:w:l:s:p:y:n:t:", ["author=", "filename=", "course-code=", "weekday=", "location=", "section=", "prof=", "semester=", "title="])
    except getopt.GetoptError:
        print('lecture_notes_latex_generator.py -a <author> -f <file name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('lecture_notes_latex_generator.py -a <author> -f <file name>')
            sys.exit()
        elif opt in ("-a", "--author"):
            author = arg
        elif opt in ("-f", "--filename"):
            filename = arg
        elif opt in ("-c", "--course-code"):
            courseCode = arg
        elif opt in ("-w", "--weekday"):
            weekdays = arg
        elif opt in ("-l", "--location"):
            courseLocation = arg
        elif opt in ("-s", "--section"):
            courseSection = arg
        elif opt in ("-p", "--prof"):
            prof = arg
        elif opt in ("-y", "--semester"): # y for year as well
            semester = arg
        elif opt in ("-n", "--credits"): # n for number
            courseCredits = int(arg)
        elif opt in ("-t", "--title"): # Course title
            courseTitle = arg

    # Ask user anything that is unanswered and required

    if courseCode == "": # If course code was not given in initial run line
        courseCode = require_answer("Course code (with spaces): ")

    if weekdays == "": # If weekdays the course occues was not given before
        # Does not use require_answer() because it has to check weekday regex
        while True:
            weekdays = input(str_prefix_ques + " Input weekdays this course happens (MTWRF): ").strip().replace(" ", "")
            if bool(re.match("^[MTWRFmtwrf]+$", weekdays)):
                break
            else:
                print("Please only enter only MTWRF characters!")

    if courseLocation == "": # Ask course location if not given before
        courseLocation = require_answer("Location of this course: ")

    if filename == "": # Ask for file name if not given before
        # Does not use require_answer() because it has to check for file ext.
        while True:
            filename = input(str_prefix_ques + " File name (tex): ")
            if not filename.endswith(".tex"):
                filename += ".tex"
            if yes_or_no("Is this correct - '" + filename + "'? "):
                break

    if courseTitle == "": # Ask for course title if not given before
        courseTitle = require_answer("Course title: ")

    if courseSection == "": # Ask for course section if not given before
        # Does not use require_answer() because it has to check it's 1 char
        while True:
            courseSection = input(str_prefix_ques + " Course Section (1 char): ").strip()
            if len(courseSection) != 1:
                print(str_prefix_err + " The course code has to be 1 character only!")
            elif yes_or_no("Is this correct - Section " + courseSection + "? "):
                break

    if prof == "": # Ask for professor if not given before
        prof = require_answer("Professor teaching this section: ")

    if semester == "": # Ask for which semester it takes place in if not given
        # Does not use require_answer() because it has to ckeck regex
        while True:
            semester = input(str_prefix_ques + " Year and Semester (Ex: 2021F): ")
            if bool(re.match("^[0-9]{4}(W|F|SU)$", semester)):
                # Regex: First 4 chars is year, after is term
                break
            else:
                print("Please only enter in the correct format.")

    # Confirming Week 1's start date
    week1monday = ""
    year = int(semester[:4]) # Get inputted year (first 4 characters)
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
    while True:
        confirm_weekday = yes_or_no(f"Is the start of {semester} {next_monday.strftime('%Y %m %d')} [y/n]? ")
        if confirm_weekday:
            break
        else: # If start date is not correct
            date_correct_input = ""
            date_correct = ""
            while True:
                date_correct_input = input(str_prefix_ques + " Input the date in the form of YYYY MM DD: ")
                if bool(re.match("^[0-9]{4} ^[0-9]{2} ^[0-9]{2}$", date_correct)):
                    date_correct = datetime.strptime(date_correct_str, "%Y %m %d")
                    if yes_or_no("Is this correct: " + date_correct.strftime('%a %b %d, %Y') + "? "):
                        d = date_correct
                else:
                    print(str_prefix_err + " You must follow the YYYY MM DD format. Example: '2021 01 07'.")

    if courseCredits == "": # Ask for number of credits if not given
        # Does not use require_answer() because it has to be a number
        while True:
            try:
                courseCredits = int(input(str_prefix_ques + " Course credit amount: "))
                if yes_or_no("Is this correct - " + str(courseCredits) + " credits? "):
                    break
            except:
                print("Your response caused an error!")

    # Read template file contents
    lines = open(path_template_dir + path_template_file, "r").readlines()

    # Change values in LaTeX template preamble 
    ncmd = "\\newcommand{\\"
    lines[index_str(lines, "% [FILENAME]")] = "% " + filename + "\n"
    lines[index_str(lines, "% Author: [AUTHOR]")] = "% Author: " + author + "\n"
    lines[index_str(lines, "% Created: [DATE]")] = "% Created: " + currentDate + "\n"
    lines[index_str(lines, "% Updated: [DATE]")] = "% Updated: " + currentDate + "\n"
    lines[index_str(lines, "% Description: [DESCRIPTION]")] = "% Description: Course notes for " + courseCode + "\n"
    lines[index_str(lines, ncmd + "myAuthor")] = ncmd + "myAuthor}{" + author + "}\n"
    lines[index_str(lines, ncmd + "mySubject")] = ncmd + "mySubject}{Lecture notes for " + courseCode + " in " + semester + "}\n"
    lines[index_str(lines, ncmd + "myKeywords")] = ncmd + "myKeywords}{" + courseCode + ", York University}\n"
    lines[index_str(lines, ncmd + "myCourseDateCreated")] = ncmd + "myCourseDateCreated}{" + currentDate + "}\n"
    lines[index_str(lines, ncmd + "myCourseCredits")] = ncmd + "myCourseCredits}{" + str(courseCredits) + "}\n"
    lines[index_str(lines, ncmd + "myCourseCode")] = ncmd + "myCourseCode}{" + courseCode + "}\n"
    lines[index_str(lines, ncmd + "myCourseTitle")] = ncmd + "myCourseTitle}{" + courseTitle + "}\n"
    lines[index_str(lines, ncmd + "myCourseProf")] = ncmd + "myCourseProf}{" + prof + "}\n"
    lines[index_str(lines, ncmd + "myCourseSemester")] = ncmd + "myCourseSemester}{" + semester + "}\n"
    lines[index_str(lines, ncmd + "myCourseSchedule")] = ncmd + "myCourseSchedule}{" + weekdays + "}\n"
    lines[index_str(lines, ncmd + "myCourseSection")] = ncmd + "myCourseSection}{" + courseSection + "}\n"
    lines[index_str(lines, ncmd + "myCourseLocation")] = ncmd + "myCourseLocation}{" + courseLocation + "}\n"
    
    # Index of where to insert new lines
    line_insert = index_str(lines, "% TODO: Lecture notes here")

    # Print sections by week here
    lectureCount = 1 # Counter since there can be multiple lectures in a week
    for weekNum in range(1, 12): # There are normally 12 weeks in a semester
        lines_append.append("\n\\section{Week " + str(weekNum) + "}") # Each week section line
        for lectureDay in weekdays: # Generating each subsection for every weekday in the week
            if lectureDay == "M":
                d = next_weekday(d, 0) # 0 = Monday
                weekday_short = "Mon"
            elif lectureDay == "T":
                d = next_weekday(d, 1) # 1 = Tuesday
                weekday_short = "Tue"
            elif lectureDay == "W":
                d = next_weekday(d, 2) # 2 = Wednesday
                weekday_short = "Wed"
            elif lectureDay == "R": # R = How York represents Thursday since T is used by Tuesday
                d = next_weekday(d, 3) # 3 = Thursday
                weekday_short = "Thu"
            elif lectureDay == "F":
                d = next_weekday(d, 4) # 4 = Friday
                weekday_short = "Fri"
            tDateFormatted = d.strftime("%Y %m %d")
            lines_append.append("\\subsection{Lecture " + str(lectureCount) + ": " + tDateFormatted + " (" + weekday_short + ")}")
            lines_append.append("\\begin{itemize*}")
            lines_append.append("    \\item ")
            lines_append.append("\\end{itemize*}\n")
            lectureCount += 1 # Increase lecture counter for the subsections

    # Merge arrays + write to file
    lines[line_insert:line_insert] = [line + "\n" for line in lines_append]
    open(filename, "w").writelines(lines)

    sys.exit() # Exit program with no errors

if __name__ == "__main__":
    if len(sys.argv) > 0:
        main(sys.argv[1:])
    else:
        main()
