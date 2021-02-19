#!/bin/bash

# === PROGRAM DESCRIPTION ===
# This program generates a template 
# file for the chosen file type

# Make sure the bash version is compatible with this program
case $BASH_VERSION in 
    ''|[0-3].*) echo "ERROR: Bash 4.0+ required" >&2; exit 1;; 
    esac

# Prompt text. The variable must be named 'PS3' for it to work.
# Make sure there is a trailing space at the end or it will look weird
PROMPT_TEXT='Please enter your file type choice: '
# PS3 is assigned after config is imported in case the user set something different
# For those interested:
#   PS1 is the line in terminal that asks for your commands normally. Usually it's "username: current_directory"
#   PS2 is the line that asks you to keep typing if you type a command with open quotes or something like that

# Today's date, used for file creation date section. You can also change 
# the date format by reading the manual page at 'man date'
DATE_FORMAT=$(date '+%Y %m %d')   

# Full name of the user, used in AUTHOR sections of the file that is going to be created.
USERNAME=$(id -F) # If this cannot be run, run $(whoami) instead

# Default file name
TEMPLATE_NAME="template"

# Default template folder path (where all the template files are stored)
TEMPLATE_FOLDER="$HOME/.config/template-maker/copy"

REPLACE_USERNAME="[CREATOR]"
REPLACE_DATE="[DATE]"
REPLACE_FILENAME="[FILE NAME]"
REPLACE_FILEFRONT="[FILE FRONT]"

# Source the config file
CONFIG=$HOME/.config/template-maker/config
if [ -f "$CONFIG" ]; then                       # If the config file exists
    source "$CONFIG"                            # Import the settings from there
else                                            # If the config file doesn't exist
    mkdir -p "$HOME/.config/template-maker"     # Make this directory if it doesn't exist
    cp "${{BASH_SOURCE[0]}/config" "$CONFIG"    # Copy the config file from the template
    echo "Config file made at $CONFIG"
fi

# Setting prompt text
PS3=$PROMPT_TEXT

# Error handling in case of empty strings in config
if [ -z "$USERNAME" ]; then
    USERNAME=$(whoami) 
fi
if [ -z "$TEMPLATE_NAME" ]; then  
    TEMPLATE_NAME="template"
fi
if [ "${TEMPLATE_FOLDER: -1}" != "/" ] ; then # If the last character is not a "/", add it there
    TEMPLATE_FOLDER="${TEMPLATE_FOLDER}/"
fi
# Variable for the file name will be stored here
file_name=""

# Text from the template file will be stored here
file_text=""

# List of file types to ask
# The StackExchance answer I found this from also 
# included a 'Quit' option but the user can just press ^C || ^D
options=(".c (C)"
        ".cpp (C++)"
        ".css (CSS)"
        ".html (HTML)"
        ".java (Java)"
        ".ms (Groff)"
        ".py (Python)"
        ".sh (Shell Script)")

# Used for checking if template files are in the 'copy directory'
all_filetypes=("c" "cpp" "css" "html" "java" "ms" "py" "sh")

for file in all_filetypes; do
    ls "${TEMPLATE_FOLDER}/.${file}" | wc -l
done

# This section of code is so that you don't need to retype all the entries in the 
# case statement, instead use indexes
declare -A options_reverse=()       # Create an associative array
for idx in "${!options[@]}"; do     # For each item in the options array
  val=${options[$idx]}              
  options_reverse[$val]=$idx        # entry of $options is = index, number = the value
done

# This function finds a filename that does not exist already so it doesn't override any existing files
function name_that_file() { 
    # ${1} = file name without extension
    # ${2} = file extension without the ".". (Ex: a Python file will be "py", not ".py")
    template_name="${1}.${2}"
    counter=0
    if [ -f "$template_name" ] ; then               # If the file already exists in the directory
        while [ -f "$template_name" ] ; do          # While the next file exists, find another name  
            ((counter=counter+1))                   # Add 1 to the name counter
            template_name="${1} ($counter).${2}"    # Make a new name (wikk check on next loop)
        done                                        # Exits loop when it found an unused name
        file_name="$template_name"                  
    else                                            # If the original file name is available
        file_name="${1}.${2}"
    fi
}

function fill_in_info() {
    # Format: variable=${variable//ReplaceFrom/ReplaceTo}
    # // is used instead of / before ReplaceFrom to replace all occurences. / just does the first
    # "[DATE]" doesn't work, so "\[DATE\]" has to be used
    file_text=${file_text//$REPLACE_DATE/$DATE_FORMAT}              # Replace the [DATE] with the actual date with the proper formatting
    file_text=${file_text//$REPLACE_USERNAME/$USERNAME}             # Replace [CREATOR] with the user's actual name
    file_text=${file_text//$REPLACE_FILENAME/$file_name}            # Replace all mentions of the file's own name with the actual name
    file_text=${file_text//$REPLACE_FILEFRONT/${file_name%.*}}      # File name but without the extension. Mainly used for Java
}

select option in "${options[@]}" # Asks for the option choice
do
    # case $option in 
    case "${options_reverse[$option]}" in
        0) # C programming file
            name_that_file "$TEMPLATE_NAME" "c"
            file_text=$(cat ${TEMPLATE_FOLDER}template.c)
            fill_in_info
            echo "$file_name created."
            echo "$file_text" > "$file_name"
            exit 0
            ;;
        1) # C++ programming file
            name_that_file "$TEMPLATE_NAME" "cpp"
            file_text=$(cat ${TEMPLATE_FOLDER}template.cpp)
            fill_in_info
            echo "$file_name created."
            echo "$file_text" > "$file_name"
            exit 0
            ;;
        2) # CSS programming file
            name_that_file "style" "css"
            file_text=$(cat ${TEMPLATE_FOLDER}style.css)
            fill_in_info
            echo "$file_name created."
            echo "$file_text" > "$file_name"
            exit 0
            ;;
        3) # HTML File
            name_that_file "index" "html"
            file_text=$(cat ${TEMPLATE_FOLDER}index.html)
            fill_in_info
            echo "$file_name created."
            echo "$file_text" > "$file_name"
            exit 0
            ;;
        4) # Java programming file
            name_that_file "$TEMPLATE_NAME" "java"
            file_text=$(cat ${TEMPLATE_FOLDER}template.java)
            fill_in_info
            echo "$file_name created."
            echo "$file_text" > "$file_name"
            exit 0
            ;;
        5) # Groff markup file
            name_that_file "$TEMPLATE_NAME" "ms"
            file_text=$(cat ${TEMPLATE_FOLDER}template.ms)
            fill_in_info
            echo "$file_name created."
            echo "$file_text" > "$file_name"
            exit 0
            ;;
        6) # Python programming file
            name_that_file "$TEMPLATE_NAME" "py"
            file_text=$(cat ${TEMPLATE_FOLDER}template.py)
            fill_in_info
            echo "$file_name created."
            echo "$file_text" > "$file_name"
            exit 0
            ;;
        7) # Bash shell script
            name_that_file "$TEMPLATE_NAME" "sh"
            file_text=$(cat ${TEMPLATE_FOLDER}template.sh)
            fill_in_info
            echo "$file_name created."
            echo "$file_text" > "$file_name"
            exit 0
            ;;
        *) echo "Invalid option: '$REPLY'";;
    esac
done

exit 0

