#!/bin/bash
# script to install or refresh the content files from production to local

# constants (change if not using default environment setup)
HOST="jenkins"
HOST_FILES_DIR="/backups/djangoprod/djangocms/website_content/media/"
FILES_DIR="website_content/media/"

debug () {
		if [ "$_opt_verbose" = "true" ] ; then
        	# log all messages
        	echo $1;
        fi
}

show_help() {
    echo "usage: sync-files.sh [-h?][-v][-f]"
    echo "     -h or ?: show usage help"
    echo "     -v: show verbose logging"
    echo ""
}

# parse all options using getargs...
# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

while getopts "h?vf" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    v)  _opt_verbose=true
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

_opt_arg=$@
debug "options: "
debug "verbose:$_opt_verbose"
debug "argument: $_opt_arg"
debug ""

echo "You have requested to sync files from production to local copy [../$FILES_DIR]."
echo 'Are you sure? [y/N]'
read _user_answer
debug "user answer: [$_user_answer]"
echo ""
if [[ "$_user_answer" != "y" && "$_user_answer" != "Y" ]]; then
    echo " "
    echo "done"
    exit 0
fi
mkdir -p ../$FILES_DIR
rsync -avz --delete $HOST:$HOST_FILES_DIR ../$FILES_DIR
echo "synced files: [../$FILES_DIR] from [$HOST:$HOST_FILES_DIR]"
echo "done"