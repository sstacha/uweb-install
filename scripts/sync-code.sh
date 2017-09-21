#!/bin/bash
# script to install or pull code from git repo
# -f : force directory re-creation for fresh install

# constants (change if not using default environment setup)
GIT_DIR="website"
#GIT_REPO="https://github.com/spe-sa/website-code.git"
GIT_REPO="git@git.spe.org:django/website-code.git"

debug () {
		if [ "$_opt_verbose" = "true" ] ; then
        	# log all messages
        	echo $1;
        fi
}

show_help() {
    echo "usage: sync-code.sh [-h?][-v][-f]"
    echo " ex: sync-code.sh -f"
    echo "     -h or ?: show usage help"
    echo "     -v: show verbose logging"
    echo "     -f: force deletion and recreation of code folder"
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
    f)  _opt_force=true
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

_opt_arg=$@
debug "options: "
debug "verbose: $_opt_verbose"
debug "force: $_opt_force"
debug "argument: $_opt_arg"
debug ""

if [[ -d "../$GIT_DIR" ]]; then
    debug "directory was found checking force == true"
    if [[ "$_opt_force" == "true" ]]; then
        echo "You have requested to force reload code in [../$GIT_DIR] which will delete the directory and start over.  You probably should archive and backup the existing code first.  If unsure say no and make an archive first."
        echo 'Are you sure? [y/N]'
        read _user_answer
        debug "[force restore] user answer: [$_user_answer]"
        echo ""
        if [[ "$_user_answer" != "y" && "$_user_answer" != "Y" ]]; then
            echo " "
            echo "done"
            exit 0
        fi
        rm -rf ../$GIT_DIR
        debug "[force restore] deleted directory: [../$GIT_DIR]"
    fi
fi

if [[ -d "../$GIT_DIR" ]]; then
    debug "[../$GIT_DIR] exists; pulling from repo to get latest version of code"
    git pull ../$GIT_DIR
else
    # re-clone the git repo to this directory
    git clone $GIT_REPO ../$GIT_DIR
    debug "cloned [$GIT_REPO] into directory: [../$GIT_DIR]"
fi
echo "done"
