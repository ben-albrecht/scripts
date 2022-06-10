#!/bin/sh

#
# Source this file to log commands and exit codes
#

LOG_DIR=~/.exit-logs
BASH_PID=$$
LOG_FILE=${LOG_DIR}/${BASH_PID}.csv

mkdir -p ~/.exit-logs
rm -f ${LOG_FILE}

trap 'previous_exit_code=$?; previous_command=$this_command; this_command=$BASH_COMMAND; [ ! -z "$previous_command" ] && echo \"$previous_command\", $previous_exit_code >> ${LOG_FILE}' DEBUG
