# ITEMS BETWEEN THESE HEADINGS WILL BE UPDATED
# ------------------------ UWEB SETTINGS ------------------------------------
# add our different roots for static files to be served up
IMAGES_ROOT = os.path.join(BASE_DIR, "images/")
CACHED_ROOT = os.path.join(BASE_DIR, "cache/")
DOCROOT_ROOT = os.path.join(BASE_DIR, "docroot/files/")
STATICFILES_DIRS = (
    IMAGES_ROOT,
    CACHED_ROOT,
    DOCROOT_ROOT,
)

# add our docroot application to the installed apps and middleware initializations
MIDDLEWARE += (
    'uweb.middleware.routes.DocrootFallbackMiddleware',
)
INSTALLED_APPS += (
    'docroot',
    'uweb',
)

# added for a deficency in the way apache handles WSGI; would like to push this to web server at some point
#   to eliminate 2 file checks for every request
# don't allow our cms to serve up any templates or python code as staic files; include .htaccess for good measure
# to disable checks set USE_STATIC_FORBIDDEN = False (eliminates 2 file system checks per request)
USE_STATIC_FORBIDDEN = False
STATIC_FORBIDDEN_EXTENSIONS = ['.dt', '.py', ]
STATIC_FORBIDDEN_FILE_NAMES = ['.htaccess', ]

# add logging and our loggers
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': './django.log',
        #     'formatter': 'simple'
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'docroot': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },

    }
}
if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']
else:
    # make sure all production servers never show debugging info.  set them to info if they are debug
    for logger in LOGGING['loggers']:
        if LOGGING['loggers'][logger]['level'] == 'DEBUG':
            LOGGING['loggers'][logger]['level'] = 'INFO'

# SECURITY WARNING: keep the secret key used in production secret! (do not version .secret_key)
# ----------- secret key handler
try:
    with open('.secret_key') as file:
        SECRET_KEY = file.read()
except FileNotFoundError:
    print('WARNING: .secret_key NOT FOUND DEFAULTING TO [%s] from config file' % str(SECRET_KEY))
    print('     it is recommended you run [./manage.py secret_key set] from the console!')
    print('')

# ------------------------ UWEB SETTINGS ------------------------------------
