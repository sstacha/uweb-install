#!/bin/bash
# OLD_IMPORT: <bang>/usr/bin/env sh

# setup our django project directory if it does not exist
if [ ! -d "../website" ]; then
    echo "django website project folder does not exist; creating it and installing base packages..."
    pip install --upgrade pip
    pip install django
    pip install requests
    pip install gunicorn
    mkdir ../website
    mkdir -p ../website/data
fi

# setup a base docroot application in this project folder if we have not already done so
if [ -d "../website" ]; then
    echo "django project directory [website] found; continuing installation..."
    cd ../website
    if [ -f "manage.py" ]; then
        echo "manage.py already exists: skipping project install..."
    else
        echo "manage.py not found; performing initial project install"
        django-admin startproject docroot .

        # check that we have a settings.py file and a cms_settings.py file; if so append the block to the bottom
        if [[ -f '../docroot_files/cms_settings.py' && -f 'docroot/settings.py' ]]; then
            echo 'STATIC_ROOT = os.path.join(BASE_DIR, "static/")' >> docroot/settings.py
            echo '' >> docroot/settings.py
            cat ../docroot_files/cms_settings.py >> docroot/settings.py
        else
            echo 'WARNING: either the docroot_files/cms_settings.py or the docroot/settings.py was not found; cms settings were not appended!'
        fi

        # check that we have a urls.py file and a cms_urls.py file; if so append the block to the bottom
        if [[ -f '../docroot_files/cms_urls.py' && -f 'docroot/urls.py' ]]; then
            cat ../docroot_files/cms_urls.py >> docroot/urls.py
        else
            echo 'WARNING: either the docroot_files/cms_urls.py or the docroot/urls.py was not found; urls were not appended!'
        fi

        # copy all the current preloaded files into our newly created docroot directory if the files dir doesn't exist
        if [[ ! -d 'docroot/files' ]]; then
            mkdir docroot/files
            cp -Rf ../docroot_files/files/   docroot/files/
        fi

        # copy all the current preloaded cms files into a new app directory if the cms dir doesn't exist
        if [[ ! -d 'uweb/' ]]; then
            mkdir uweb
            cp -Rf ../cms_files/ uweb/
        fi

        # copy our gitignore file
        if [[ -f '../.gitignore' ]]; then
            cp ../.gitignore ../website/.gitignore
        else
            echo 'WARNING: the cms .gitignore file was not found or copied!  You must now do this manually.'
            echo 'WARNING: make sure your .secret_key file is not checked into your public repo!'
        fi

        # now that settings are built lets do migrations
        ./manage.py migrate

        # add an admin user
        echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin@example.com', 'admin', 'admin')" | python manage.py shell
#        sed -i 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \[\"\*\"\]/' docroot/settings.py
#        echo 'STATIC_ROOT = os.path.join(BASE_DIR, "static/")' >> docroot/settings.py
#        /venv/bin/pip install uwsgi

#        # create an initial requirements.txt file for the host to build a virtual envrionment from
#        /venv/bin/pip freeze > requirements.txt

#        # rename the original settings.py file to settings_common.py
#        # ours will be copied in next; which will insert the uweb application into the mix
#        mv docroot/settings.py docroot/settings_common.py
#        # copy all our default directories and files from the vagrant install folder to
#        # cp -R $UWEB_HOME/files/docroot/ docroot/
    fi
else
    echo "Something went wrong; no website directory found even though we set it up; this shouldn't happen..."
fi

# setup the base cms application in this project folder if we don't already have one
