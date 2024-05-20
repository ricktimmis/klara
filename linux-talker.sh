#!/bin/bash
# Kompanion Utility Script, for Text to speech

function logger(){
LOG_FILE=./assistant.log

# Checking if there are two arguments passed in
if [ "$#" -ne 1 ]; then
    echo "Invalid number of arguments provided. Usage: logger message"
fi

# Arguments
LOG_MESSAGE=$1

echo $(date +"%Y-%m-%d %T") - $LOG_MESSAGE >> $LOG_FILE
}



# Arguments
RAW_MESSAGE=$1
# if command -v logger.sh > /dev/null 2>&1; then
#echo $RAW_MESSAGE
   logger "$RAW_MESSAGE"
## fi
#
#    if command -v JustSpeak > /dev/null 2>&1; then
#         # Check if the current hour is between 08 and 22
#             `JustSpeak -text "$RAW_MESSAGE"` > /dev/null 2>&1
#    else
#        echo "Command JustSpeak not found, skipping voice output"
#    fi

# Some Rough Cleaning
MESSAGE=$(echo "$RAW_MESSAGE" | sed 's/\n/./g' | sed 's/-//g' | sed 's/GroupLayout://g')
IFS='.'
# Read the RAW_MESSAGE into an array
array=($MESSAGE)
# Print all array elements
for i in "${array[@]}"
  do
#    if [[ "$i" == *":" ]]
#    then
#      i="News From $i"
#    fi
#    i=$(echo "$i" | sed -e 's/<[^>]*>//g')

    if command -v JustSpeak > /dev/null 2>&1; then
#         # Check if the current hour is between 08 and 22
#         if (( 8 <= currentHour && currentHour < 22 )); then
             `JustSpeak -text "$i"`  > /dev/null 2>&1
#         else
#             echo "It's not between 08:00 and 22:00 - JustSpeak command was not executed"
#         fi
    else
        echo "Command JustSpeak not found, skipping voice output"
    fi
  done