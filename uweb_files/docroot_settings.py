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
    'docroot.middleware.routes.DocrootFallbackMiddleware',
)
INSTALLED_APPS += (
    'docroot',
)

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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './django.log',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'docroot': {
            'handlers': ['file'],
            'level': 'DEBUG',
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

# ----------- secret key handler
try:
    with open('.secret_key') as file:
        # SECURITY WARNING: keep the secret key used in production secret! (do not version .secret_key)
        # note: can not error if no file since then ./manage.py command could not be completed
        SECRET_KEY = file.read()
        print('USING SECRET_KEY=%s' % SECRET_KEY)
except FileNotFoundError:
    print(".secret_key file was not found!")
    # todo: figure out how to print as an alert or error not just text
    print('USING STATIC SECRET_KEY=%s' % SECRET_KEY)

# ------------------------ UWEB SETTINGS ------------------------------------
