#!/bin/bash
# OLD_IMPORT: <bang>/usr/bin/env sh

# check we have a django project directory
if [ ! -d "../website" ]; then
    echo "WARNING: django website project folder does not exist; you probably should run ./install-uweb first..."
else
    echo "django project directory [website] found; continuing installation..."
    # make sure we have a example_files to pull from and a files directory to copy them to
    if [[ -d '../example_files/files/' && -d '../website/docroot/files/' ]]; then
        cp -Rf ../example_files/files/   ../website/docroot/files/
    else
        echo 'WARNING: files folder or example_files folder doesnt exist; recommend re-installing...'
    fi
fi