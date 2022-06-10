#!/bin/bash


# Usage:
# > ./sshproxy.sh -u bja
# > ssh cori

# .ssh/config is setup so that this does:
# > ssh -i ~/.ssh/nersc bja@cori.nersc.gov

# Check how long key is valid
# > ssh-keygen -L -f ~/.ssh/nersc-cert.pub | grep Valid


# Copyright 2018 Regents of the University of California

#
# NOTICE.  This software was developed under funding from the U.S.
# Department of Energy and the U.S. Government consequently retains
# certain rights. As such, the U.S. Government has been granted for
# itself and others acting on its behalf a paid-up, nonexclusive,
# irrevocable, worldwide license in the software to reproduce,
# distribute copies to the public, prepare derivative works, and
# perform publicly and display publicly, and to permit other to do
# so.

# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL BERKELEY LAB OR THE U.S. GOVERNMENT BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

progname=$(basename $0)
version="1.1.0"

# Save tty state for trap function below
original_tty_state=$(stty -g)

tmpkey=''
tmpcert=''
tmppub=''
pw=''

# Default values
id=nersc			# Name of key file
user=$USER			# Username
sshdir=~/.ssh			# SSH directory
scope="default"			# Default scope
url="https://sshproxy.nersc.gov"	# hostname for reaching proxy

#############
# Functions
#############

# Error(error string, ...)
# 
# prints out error string.  Joins multiple arguments with ": "


Error () {

	# Slightly complicated print statement so that output consists of
	# arguments joined with ": " 

	printf "$progname: %s" "$1" 1>&2
	shift
	printf ': %s' "$@" 1>&2
	printf "\n" 1>&2
}

# Bail(exit code, error string, ...)
# 
# prints out error string and exits with given exit code

Bail () {
	# get exit code
	exitcode=$1
	shift

	Error "$@"

	# restore terminal to original state, in case we're interrupted
	# while reading password

	stty $original_tty_state

	# Go bye-bye
	exit $exitcode
}


# Cleanup()
#
# Cleans up temp files on exit

Cleanup () {
	for f in "$tmpkey" "$tmpcert" "$tmppub"
	do
		if [[ "$f" != "" && -e "$f" ]]; then
			/bin/rm -f "$f"
		fi
	done
}

# Abort ()
#
# Trap on errors otherwise unhandled, does cleanup and exit(1)

Abort () {
	Bail 255 "Exited on interrupt/error"
}


Usage () {

	if [[ $# -ne 0 ]]; then
		printf "$progname: %s\n\n", "$*"
	fi
	printf "Usage: $progname [-u <user>] [-o <filename>] [-s <scope>] [-c <account>] [-p] [-a] [-x <proxy-url>] [-U <server URL>] [-v] [-h]\n"

	printf "\n"
	printf "\t -u <user>\tSpecify remote (NERSC) username\n"
	printf "\t\t\t(default: $user)\n"
	printf "\t -o <filename>\tSpecify pathname for private key\n"
	printf "\t\t\t(default: $sshdir/$id)\n"
	printf "\t -s <scope>\tSpecify scope (default: '$scope')\n"
	printf "\t -p\t\tGet keys in PuTTY compatible (ppk) format\n"
	printf "\t -a\t\tAdd key to ssh-agent (with expiration)\n"
	printf "\t -c <account>\tSpecify a collaboration account (no default)\n"
	printf "\t -x <URL>\tUse socks proxy to connect to sshproxy server.\n"
	printf "\t\t\t(format: <protocol>://<host>[:port], see curl manpage\n"
	printf "\t\t\tsection on "--proxy" for details)\n"
	printf "\t -U <URL>\tSpecify alternate URL for sshproxy server\n"
	printf "\t\t\t(generally only used for testing purposes)\n"
	printf "\t -v \t\tPrint version number and exit\n"
	printf "\t -h \t\tPrint this usage message and exit\n"
	printf "\n"
	
	exit 0
}

#############
# Actual code starts here...
#############

# Make sure we cleanup on exit

trap Cleanup exit
trap Abort int kill term hup pipe abrt


# for command-line arguments.  In reality, not all of these get used,
# but here for completeness
opt_scope=''	# -s
opt_url=''	# -U
opt_user=''	# -u
opt_out=''	# -o
opt_agent=0	# -a
opt_version=''	# -v
opt_putty=''     # -p
opt_socks=''     # -x

# Process getopts.  See Usage() above for description of arguments

while getopts "aphvs:k:U:u:o:x:c:" opt; do
	case ${opt} in

		h )
			Usage
		;;
 		v )
 			printf "$progname v$version\n"
 			exit 0
 		;;

		s )
			opt_scope=$OPTARG
			scope=$opt_scope
		;;

		U )
			url=$OPTARG
		;;

		u )
			user=$OPTARG
		;;

		o )
			opt_out=$OPTARG
		;;
		a )
			opt_agent=1
		;;
		p )
			opt_putty="?putty"
		;;

		x )
			opt_socks="--proxy $OPTARG"
		;;
		c )
			opt_collab=$OPTARG
		;;

		\? )
			Usage "Unknown argument"
		;;

		: )
			Usage "Invalid option: $OPTARG requires an argument"
		;;

	esac
done

# If user has specified a keyfile, then use that.
# Otherwise, if user has specified a scope, use that for the keyfile name
# And if it's the default, then use the "id" defined above ("nersc")
data=''
if [[ "$opt_collab" != "" ]] ; then
    if [[ "$opt_scope" == "" ]] ; then
        scope="collab"
        opt_scope=$opt_collab
    fi
    data='{"target_user": "'$opt_collab'"}'
fi

if [[ $opt_out != "" ]]; then
	idfile=$opt_out
elif [[ "$opt_scope" != "" ]]; then
	idfile="$sshdir/$opt_scope"
else
	idfile="$sshdir/$id"
fi

certfile="$idfile-cert.pub"
pubfile="$idfile.pub"

# Have user enter password+OTP.  Curl can do this, but does not
# provide any control over the prompt
#
# N.B. INPWPROMPT variable is used in Bail() above for when password
# prompt is interrupted by ctrl-c.  Otherwise terminal gets left in
# a weird state.

read -r -p "Enter the password+OTP for ${user}: " -s pw

# read -p doesn't output a newline after entry
printf "\n"

# Make temp files.  We want them in the same target directory as the
# final keys

tmpdir=$(dirname $idfile)
tmpdir="$tmpdir"
tmpkey="$(mktemp $tmpdir/key.XXXXXX)"
tmpcert="$(mktemp $tmpdir/cert.XXXXXX)"
tmppub="$(mktemp $tmpdir/pub.XXXXXX)"

# And get the key/cert
curl -s -S -X POST $opt_socks $url/create_pair/$scope/$opt_putty \
	-d "$data" -o $tmpkey -K - <<< "-u \"${user}:${pw}\""

# Check for error
err=$?
if [[ $err -ne 0 ]] ; then
	Bail 1 "Failed." "Curl returned" $err
fi

# Get the first line of the file to check for errors from the
# server

read x < $tmpkey

# Check whether password failed

if [[ "$x" =~ "Authentication failed. Failed login" ]]; then
	Error "The sshproxy server said: $x"
	Bail 2 "This usually means you did not enter the correct password or OTP"
fi

# Check whether the file appears to contain a valid key

if [[ "$x" == "PuTTY-User-Key-File-2: ssh-rsa" ]]; then
	mv $tmpkey $idfile.ppk
	printf "Successfully obtained PuTTY Key file %s\n" "$idfile.ppk"
	exit
fi

if [[ "$x" != "-----BEGIN RSA PRIVATE KEY-----" ]]; then
	Error "Did not get in a proper ssh private key. Output was:"
	cat $tmpkey 1>&2
	Bail 3 "Hopefully that's informative"
fi

# The private key and certificate are all in one file.
# Extract the cert into its own file, and move into place

grep ssh-rsa $tmpkey > $tmpcert \
	&& ssh-keygen -y -f $tmpkey > $tmppub \
	&& chmod 600 $tmpkey* \
	&& /bin/mv $tmpkey $idfile \
	&& /bin/mv $tmppub $pubfile \
	&& /bin/mv $tmpcert $certfile

if [[ $? -ne 0 ]]; then
	Bail 4 "An error occured after successfully downloading keys (!!!)"
fi

# A few shenanigans to clean up line formatting
valid=$(ssh-keygen -L -f $certfile | grep Valid)
shopt -s extglob
valid=${valid/+( )/}
valid=${valid/Valid/valid}


if [[ $opt_agent -ne 0 ]]; then
	# extract expiration date from "valid" line (above)
	expiry=${valid/valid*to /}

	distro=$(uname)
	dateError=0

	case $distro in
		Darwin|*BSD*)
			# Convert the date to epoch
			expepoch=$(date -j -f '%FT%T' $expiry +%s)

			# get current epoch time
			epoch=$(date -j +%s)
		;;

		Linux|GNU|CYGWIN*)
			# Convert the date to epoch
			expepoch=$(date -d $expiry +%s)

			# get current epoch time
			epoch=$(date +%s)
		;;

		*)
			Error "Unrecognized OS; I don't know how to convert a date to epoch time"
			dateError=1
		;;
	esac

	# compute the interval between expiration and now
	# (minus one second just to be sure)
	interval=$(( $expepoch - $epoch - 1 ))

	# add the interval to ssh-agent
	if [[ $dateError -gt 0 ]]; then
		Error "Can't add key to ssh-agent."
	elif [[ $interval -gt 0 ]]; then
		ssh-add -t $interval $idfile
	else
		Error "cert $certfile is either expired or otherwise invalid. Expiration read as: $expiry"
	fi

fi

# And give the user some feedback
printf "Successfully obtained ssh key %s\n" "$idfile"

printf "Key $idfile is %s\n" "$valid"
