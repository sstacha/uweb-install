#!/usr/bin/env sh

# setup our django project directory if it does not exist
if [ ! -d "../website" ]; then
    echo "django website project folder does not exist; creating it and installing base packages..."
    pip install django
    pip install requests
    pip install gunicorn
    mkdir ../website
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
        ./manage.py migrate

        # check that we have a settings.py file and a cms_settings.py file; if so append the block to the bottom
        if [[ -f ../docroot_files/cms_settings.py && -f docroot/settings.py ]]; then
            cat ../docroot_files/cms_settings.py >> docroot/settings.py
        fi

        # copy all the current preloaded files into our newly created docroot directory if the files dir doesn't exist
        if [[ ! -d docroot/files ]]; then
            mkdir docroot/files
            cp -Rf ../docroot_files/files/   docroot/files/
        fi

#        echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin@example.com', 'admin', 'admin')" | /venv/bin/python manage.py shell
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
