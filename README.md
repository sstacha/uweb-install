# uweb-install
These instructions are intended to get a development environment set up and running for the uweb website project on OSX.  For other OS's please insert instructions later per OS when needed.

cd to install directory: ie, 
``` ShellSession
cd ~/dev/projects
```

CLONE THIS CODE TO YOUR NEW PROJECT DIRECTORY
``` ShellSession
git clone https://github.com/sstacha/uweb-install.git uweb 
cd uweb
```

INSTALL DEPENDENCIES (TO BE RUN ONCE) 
--------
``` ShellSession
# pv not needed until database migrations
# INSTALL PV (used to give a % complete on the import)
# brew install pv
```

INSTALL pyenv
``` ShellSession
brew install pyenv
```
NOTE: don't forget to set your bash profile with
- add to profile: 
``` ShellSession 
if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
```

INSTALL pyenv-virtualenv
``` ShellSession
brew install pyenv-virtualenv
```
NOTE: don't forget to set your bash profile with
- add to profile: 
``` ShellSession
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
```

INSTALL latest 3.x version of python
``` ShellSession
pyenv install 3.6.2
```

SET GLOBAL ENV FOR TERMINAL IF NOT OVERRIDDEN
``` ShellSession
pyenv global 3.6.2
```

SET VIRTUAL ENV FOR speweb to point to the 3.x version
``` ShellSession
pyenv virtualenv 3.6.2 uweb
```

SET UWEB DIRECTORY TO USE THE UWEB VIRTUAL ENVIRONMENT
``` ShellSession
pyenv local uweb
NOTE: will create a .python-version file
    that will automatically set the environment when you cd to this direcotry or below and release when you leave
```

CREATE AND INSTALL UWEB PROJECT
--------
``` ShellSession
# todo: wrap this in an install script ./install-website.sh (creates the website folder with all code)
pip install django
pip install uwsgi

mkdir website
cd website

NOTE: if you are restoring from an existing codebase you can skip these 2 steps and instead: git clone git://github.com/youruser/somename.git .
django-admin startproject docroot .
cp -R ../uweb_files/ docroot/

MANUAL STEPS TILL I CAN GET TO THIS:

    - FIRST TIME DEVELOPMENT
    - backup existing file (see uarchvie project): archive -c docroot/settings.py
    - configure our settings file:
        - manually append docroot_settings.py to the bottom of settings.py
        - later create a admin command or shell script to do so
        - configure ALLOWED_HOSTS:
            - dev: ALLOWED_HOSTS = ['*']
            - prod: ALLOWED_HOSTS = ['<machines to lock it down to>', 'machine2']

    - initialize our .gitignore file (gives you good default settings for a default project that you can modify)
        - cp ../.gitignore .
        
    - FIRST TIME DEVELOPMENT AND SERVER
    - generate our key
        - ./manage.py secret_key set
        NOTE: if clustered
        - ./manage.py secret_key set on first node
        - ./manage.py secret_key set <secret_key from first node> on other nodes
        
    - ./manage.py migrate
    - ./manage.py runserver 0.0.0.0:8000

```

NOTE: should work; test the docroot code
```
static file: http://localhost:8000/test.txt
static page no data: http://localhost:8000/test/
dynamic page static data: http://localhost:8000/test_static.html
dynamic page dyanmic data: http://localhost:8000/test.html
<ctrl><c> to stop
```

CREATE YOUR WEBSITE PROJECT FROM BASE UWEB CMS
--------
NOTE: if you already restored previously you obviously don't need to do any of this
``` ShellSession
NOTE: For this to work you can not create any files (readme or license); make sure it is a blank repo!
NOTE: recommend naming project website for ease of sync later
1) Create the remote repository, and get the URL such as git://github.com/youruser/somename.git
(from website directory) 1b - 1c are optional
1b) rm -rf .git (if you have anything)
1c) echo "# website" >> README.md
2) git init
3) git add .
4) git commit -m 'initial commit comment'
5) git remote add origin [URL From Step 1]
6) git push -u origin master


** IDEA: if I call data.dt directly intercept and return json context for quick web services. config for what dirs to apply since you don't want all data to automatically be a webservice if debug=false do we?
```

SCRIPTS (TO BE RUN PERIODICALLY) - The first time will set up; later will refresh. RUN EACH ONCE TO START WITH
--------

sync-code.sh (create to connect to repo and refresh our code, then copy it all except the settings file)
    - clones website if doesn't exist and pulls code
    - simply pulls and merges code if dir exists
    - sync-code.sh -f forces directory removal and does a new clone


sync-db.sh (create to remote scp sqllite.db file from prodcution to our local machine)
    - pulls the latest jenkins backup locally vis scp
    - deletes and recreates the django database from backup files
    
sync-files.sh
    - rsyncs files from production (only one copy with deltas)
    
    
NOTE: DO NOT PLACE THESE IN YOUR PATH.  I am using relative paths and the scripts expect to be run from the scripts folder.

INTEGRATION WITH GITHUB Desktop
---------------------------------
GitHub Desktop is a great tool for reviewing and diffing files before committing and pushing changes.  It is relatively straightforward except you have to remember that when you click the plus be sure to change the default setting of clone to add.  Pick the website direcotry and you are good to go.

INTEGRATION WITH IDE
----------------------
These instructions are for linking your new website project to pycharm.  JetBrains has several great products and I highly recommend them.  The general concepts though should be the same for most tools.
todo: get some help to create wiki pages for these types of instructions per tool; could also use other os's for above too

 - create new project
    - select django from left side
    - then pick the website directory
    - if <home>/.pyenv/uweb/ or .../uweb/ is not selected pick it 
    - It will tell you the directory is not empty and ask to build from existing sources; say yes
 
 IT SHOULD DEFAULT EVERYTHING AFTER THAT.  IF NOT:
 - click the wrench or go to project properties
    - under languages and frameworks choose Django
        - enable django support
        - set project to <install dir>/uweb/website (ex: /Users/sstacha/dev/uweb/website)
        - set settings to docroot/settings.py if it doesn't default
        - should automatically set manage.py for manage script
    - under build, execucution, deployment
        - under Console choose Python Console
            - set working directory (to website)
            - check add source roots to have them autoload
        - under Console choose Django Console
            - set working direcotry (to website)
            - check add source roots to have them autoload
 - drop down the empty dropdown and choose run configurations / edit configurations
    - click the + and select django server
    - name it website (or whatever you like)
    - set working directory to website
    - leave everything else default
 - click run or debug
 - open localhost:8000 in browser; should show django default ready for development screen
 
 NOTE: if you see a msg about migrations to apply then open terminal and run ./makemigrations and ./migrate
 
INSTALL PRODUCTION (ASSUMING UBUNTU SERVER)
--------
Even personal websites should have a staging or development installation (usually your laptop for new development work) and a production installation (usually an always on machine or hosted server).  I am not going to cover why we want to do this here.  I will put together a video or wiki page to explain that later.  This will only be the steps to get a production server installed and configured.  

In production, is is a good practice to set up a user for this purpose and log in or sudo as them to do everything instead of doing it as yourself.  This way if you (the administrator) leave you don't have to change much except add the new user and modify the sudoers file.  Scripts and such are written expecting a uweb user and www-data group.
If you choose to use your own user and group instead just modify the scripts after you copy them.

To set up the user and group on the server:
``` ShellSession
# set up our required users and groups we need
getent group www-data || groupadd www-data
id -u uweb &>/dev/null || useradd -g www-data -m -G sudo uweb
usermod -a -G www-data uweb
# test that you can sudo to uweb to do stuff
sudo su - uweb
```
Essentially, we will be following the same install steps above with the following exceptions:

 - Instead of installing to a directory that makes since on your development machine like <home>/dev/projects we want to install to something that makes sense for a production machine.  
``` ShellSession
# instead of cd ~/dev/projects
cd ~        
```
- Instructions to install pyenv from post here: https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get
``` ShellSession
# base required files
sudo apt-get install -y build-essential libbz2-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev
# optional scientific package headers (for Numpy, Matplotlib, SciPy, etc.)
sudo apt-get install -y libpng-dev libfreetype6-dev
# optional text based browser for testing
sudo apt-get install -y lynx
# run installer
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
# add the following lines to your ~.profile or ~.bashrc
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
# reload your shell and make sure it works by echo $PATH and searching for .pyenv
```
- Follow all instructions up to and including create and install uweb environment; skip all development integrations since we don't need them
    - install and configure our production webserver and uwsgi
``` ShellSession
# assuming you have sudo configured for your user and the administrator user in production to run all commands; google it if not
sudo su - uweb
# assuming using ubuntu server
# (optional) but recommended to download my uarchive script (into your home directory)
# instructions can be found here.  If not you will need to archive files on your own:
https://github.com/sstacha/uarchive
# make sure our environment packages are up to date and install the web server
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install nginx
# archive the current copy of the existing file if it exists
archive /etc/nginx/sites-available/default
NOTE: if you didn't download the uarcive project you can just make a copy in case you need to put it back later
# copy nginx config file: todo insert command here when you do it (replaces anything there!)
sudo cp -f $HOME/uweb/production_files/default /etc/nginx/sites-available/default
# if using consolidated storage (variable is set) set the file as current archived version
archive -c /etc/nginx/sites-available/default
    
# NOTE: NOT WORKING! SKIP TO GUNICORN INSTALLATION BELOW    
        <!-- # initialize uwsgi
        sudo mkdir -p /etc/uwsgi/sites
        sudo mkdir -p /run/uwsgi
        sudo chown <your user>:www-data /run/uwsgi  
            ex: sudo chown sstacha:www-data /run/uwsgi
        sudo chmod g+w /run/uwsgi
        echo "should have created and modified permissions for /run/uwsgi"
        echo "$(ls -al /run/)"
        # copy the uwsgi config in place
        sudo cp -f $HOME/uweb/production_files/uwsgi_uweb.ini /etc/uwsgi/sites/uwsgi_uweb.ini
        # test through uwsgi: todo insert commands and steps here
        sudo uwsgi --http :8080 --chdir $HOME/uweb/website --home $HOME/.pyenv/uweb -w docroot.wsgi
        # note: if something goes wrong to access uwsgi logs:
        sudo journalctl -xe
        # test thorugh nginx: todo insert commands and steps here
        lynx http://localhost     
        # set up uwsgi as a service so it loads on startup
        sudo cp -f $HOME/uweb/production_files/uwsgi.service /etc/systemd/system/uwsgi.service
        sudo systemctl enable uwsgi
        sudo systemctl start uwsgi
        sudo systemctl status uwsgi
        NOTE: if problems with uwsgi see original doc here: https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04
        -->
    
NOTE: could not get uwsgi to work on python3 with pyenv on ubuntu server 16.04.  If someone does please send me the instructions.
NOTE: changing to Gunicorn for now; much easier and shouldn't need much prossessing with this minimalist approach
# from your website directory uninstall uwsgi if you have it installed
pip uninstall uwsgi
# install gunicorn
pip install gunicorn
# test that gunicorn install works
gunicorn docroot.wsgi
    open a new shell window and ssh back into the box
    lynx localhost:8000
        you should see the start using django page
        hit q then y to quit in the lynx session
        hit <ctl>-c to stop the gunicorn session
# set up gunicorn (wsgi) as a service so it loads on startup
sudo cp -f $HOME/uweb/production_files/gunicorn.service /etc/systemd/system/gunicorn.service
NOTE: if not using the uweb user and www-data group change the user and group in this script now
# enable and start our new gunicorn service
systemctl enable gunicorn
systemctl start gunicorn
systemctl status gunicorn
# make sure it is running and check for pid file
ls $HOME/uweb/website
(you should see a uweb.sock file)
# re-start our nginx service and print the status to console to pick up the new config and uwsgi integration
systemctl stop nginx
systemctl start nginx
systemctl status nginx
# NOTE References for future lookups
https://gist.github.com/Atem18/4696071
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
```

    
