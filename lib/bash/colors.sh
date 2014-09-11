#############
# colors.sh #
#############
#
# A colorized-bash library
#
# Usage:
#   source ~/repos/scripts/lib/bash/colors.sh
#   echo -e "${LightRed}Hello World!"

# Determine OS
if [[ $OSTYPE == *linux* ]]; then
    Color_Prefix="\e["
elif [[ $OSTYPE == *darwin* ]]; then
    Color_Prefix="\x1B["
fi

# No Color
NC="${Color_Prefix}0m"

# Declare Colors
Black="${Color_Prefix}0;30m"
DarkGray="${Color_Prefix}1;30m"
Blue="${Color_Prefix}0;34m"
LightBlue="${Color_Prefix}1;34m"
Green="${Color_Prefix}0;32m"
LightGreen="${Color_Prefix}1;32m"
Cyan="${Color_Prefix}0;36m"
LightCyan="${Color_Prefix}1;36m"
Red="${Color_Prefix}0;31m"
LightRed="${Color_Prefix}1;31m"
Purple="${Color_Prefix}0;35m"
LightPurple="${Color_Prefix}1;35m"
Orange="${Color_Prefix}0;33m"
Yellow="${Color_Prefix}1;33m"
LightGray="${Color_Prefix}0;37m"
White="${Color_Prefix}1;37m"
