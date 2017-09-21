#!/bin/bash
# script to install or pull code from git repo

# constants (change if not using default environment setup)
DB="django"
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="root"
DB_BACKUP_ZIP="django.mysqlprod.spe.org.sql.gz"
DB_BACKUP_SQL="django.mysqlprod.spe.org.sql"

debug () {
		if [ "$_opt_verbose" = "true" ] ; then
        	# log all messages
        	echo $1;
        fi
}

show_help() {
    echo "usage: sync-db.sh [-h?][-v][-f]"
    echo "     -h or ?: show usage help"
    echo "     -v: show verbose logging"
    echo "     -s: skip scp file download from jenkins"
    echo ""
}

# parse all options using getargs...
# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

while getopts "h?vfs" opt; do
    case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    v)  _opt_verbose=true
        ;;
    s)  _opt_skip=true
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

_opt_arg=$@
debug "options: "
debug "verbose:$_opt_verbose"
debug "skip scp:$_opt_skip"
debug "argument: $_opt_arg"
debug ""

echo "You have requested to reload the website database($DB).  All existing pages and data will be over-written."
echo 'Are you sure? [y/N]'
read _user_answer
debug "user answer: [$_user_answer]"
echo ""
if [[ "$_user_answer" != "y" && "$_user_answer" != "Y" ]]; then
    echo " "
    echo "done"
    exit 0
fi
# add a env check to skip the file download
# NOTE: to use export SKIP_SCP=true before running this script
if [[ ! "$_opt_skip" == "true" ]]; then
    # remove any existing archive file
    if [[ -f $DB_BACKUP_ZIP ]]; then
        rm -f $DB_BACKUP_ZIP
    fi
    # remove any existing sql file
    if [[ -f $DB_BACKUP_SQL ]]; then
        rm $DB_BACKUP_SQL
    fi
    # get the current backup file from last jenkins export
    scp jenkins.spe.org:/backups/djangoprod/$DB_BACKUP_ZIP .
    # if anything went wrong bail ( we should have a backup zip file to work from now )
    if [ ! -f $DB_BACKUP_ZIP ]; then
        echo "$DB_BACKUP_ZIP does not exist; something must have gone wrong with the scp - exiting"
        exit 111
    fi
    # unzip it
    gunzip $DB_BACKUP_ZIP
fi
# if anything went wrong bail ( we should have a backup sql file to work from now )
if [ ! -f $DB_BACKUP_SQL ]; then
    echo "$DB_BACKUP_SQL does not exist; something must have gone wrong with the unzip - exiting"
    exit 112
fi
echo ""
echo ""
# drop any existing database
mysql -h $DB_HOST -u $DB_USER --password=$DB_PASSWORD --protocol=tcp -e 'drop database django'
# recreate it
mysql -h $DB_HOST -u $DB_USER --password=$DB_PASSWORD --protocol=tcp -e 'create database django'
# restore the data to it
echo "restoring database[$DB] from backup sql file [$DB_BACKUP_SQL]"
# mysql -h $DB_HOST --user=$DB_USER --password=$DB_PASSWORD --protocol=tcp $DB < $DB_BACKUP_SQL
# use pv so we don't just get a blank line for a long time; we can see whats processing
pv $DB_BACKUP_SQL | mysql -h $DB_HOST --user=$DB_USER --password=$DB_PASSWORD --protocol=tcp $DB
echo ""
echo "database restored"
echo "done"