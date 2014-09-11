#################
# conditions.sh #
#################

# Bash-Library containing common conditionals in human-readable form

IsDirectory() {
    if [ -d $1 ]; then
        return 0
    else
        return 1
    fi
}


IsEmptyString() {
    if [ -z $1 ]; then
        return 0
    else
        return 1
    fi
}

