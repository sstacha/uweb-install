#!/usr/bin/env sh

# install django required files or a base install
if [ -f "requirements.txt" ]; then
    echo "requirements.txt exists; installing or re-installing modules from it..."
    install -r requirements.txt
else
    echo "requirements.txt does not exist; installing base django modules..."
    if [ -f "manage.py" ]; then
        echo "manage.py already exists: skipping project install..."
    else
        # pip install --upgrade pip
        pip install django
        pip install uwsgi

        mkdir website
        cd website
        django-admin startproject docroot .
        manage.py migrate
        echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin@example.com', 'admin', 'admin')" | /venv/bin/python manage.py shell
        sed -i 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \[\"\*\"\]/' docroot/settings.py
        echo 'STATIC_ROOT = os.path.join(BASE_DIR, "static/")' >> docroot/settings.py
        /venv/bin/pip install uwsgi

        # create an initial requirements.txt file for the host to build a virtual envrionment from
        /venv/bin/pip freeze > requirements.txt

        # rename the original settings.py file to settings_common.py
        # ours will be copied in next; which will insert the uweb application into the mix
        mv docroot/settings.py docroot/settings_common.py
        # copy all our default directories and files from the vagrant install folder to
        # cp -R $UWEB_HOME/files/docroot/ docroot/
    fi
fi