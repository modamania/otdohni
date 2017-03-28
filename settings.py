# encoding: utf-8
import os
import sys

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy


def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

SITE_ID = 1
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_MEDIA_PREFIX = 'media'
THUMBNAIL_SUBDIR = '_thumb'

GEOIP_PATH = os.path.join(PROJECT_DIR, 'GeoLiteCity.dat')
LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'apps', 'common','locale'),
    os.path.join(PROJECT_DIR, 'locale'),
)

#path to apps
sys.path.insert(0, rel('apps'))
sys.path.insert(0, rel('apps','threadedcomments'))
sys.path.insert(0, rel('libs'))

SESSION_COOKIE_DOMAIN = '.zaotdih.ru'

CONTENT_MANAGER_MAIL_LIST = (
    # example
    'support@zaotdih.ru',
)

# Django settings for otdohniomsk project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

MANAGERS = (
    ('Admin', 'support@zaotdih.ru'),
)

ADMINS = (
    ('Georgiy', 'iamstrugo@gmail.com'),
)

FILE_UPLOAD_PERMISSIONS = 0644

#DEBUG = True

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'otdohni_new',                      # Or path to database file if using sqlite3.
        'USER': 'webmaster',                      # Not used with sqlite3.
        'PASSWORD': 'MnwIZJywe0',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': { 'init_command': 'SET storage_engine=MyISAM;' }
    }#,
    #'otdohni_old': {
        #'ENGINE': 'django.db.backends.mysql',
        #'NAME': 'otdohni_old',
        #'USER': 'webmaster',
        #'PASSWORD': 'MnwIZJywe0',
        #'HOST': '',
        #'POST': '',
        #}
}

#CACHES = {
#        'default': {
#            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#            'LOCATION': ['127.0.0.1:11211', ],
#        }
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Omsk'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
)


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = rel('media')
STATIC_ROOT = rel('static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ASSETS_URL = STATIC_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '87s2+$eqc+dzd)pg0)8o%4@e-=j1e_cw=_(p1sd7g(zznnt0yk'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'core.middleware.CityAndDeviceRedirect',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'profile.middleware.OnlineUsers',
    #'django.middleware.cache.CacheMiddleware'
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    rel('templates')
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'menu.context.generate_menu',
    'profile.context_processors.online_users',

    'core.context.request_path',
    'core.context.media_url',
    'core.context.sites',
    'core.context.logo_and_wolf',

    'private_messages2.context.count_unread_message',

    'specprojects.context_processors.spec_menu',
]

INSTALLED_APPS = (
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    #'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'django_coverage',
    'raven.contrib.django',

    #apps
    'action',
    'adminsortable',
    'event',
    'elrte',
    'elfinder',
    'profile',
    'friendship',
    #'private_messages',
    'private_messages2',
    'tagging',
    'place',
    'api',
    'registration',
    'control',
    'core',
    'news',
    'newsletter',
    'sales',
    'common',
    'lunch',
    'loginza',
    'tea',
    'omskadmin',
    'rating',
    'robots',
    'staging',
    'taggit',
    'taggit_autocomplete',
    'photoreport',
    'gourmet',
    'fashion',
    'weather',
    'contacts',
    'expert',
    'city',
    'specprojects',
    'rollyourown.seo',
    'seo',
    'kinohod',
    'debug_toolbar.apps.DebugToolbarConfig',
    'debug_toolbar',
    'graber',
    'payments',
    'blog',

    #libs
    'ajax_validation',
    'chosen',
    'djangosphinx',
    'django_assets',
    'django_extensions',
    'south',
    'sorl.thumbnail',
    'importscript',
    'threadedcomments',
    'pytils',
    'filebrowser',
    'tinymce',
    'pagination',
    'yandex_maps',
    'watermarker',
    'captcha',
    'django_rq',
)

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 8,
    },
    'foursquare': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 8,
    },
    'asap': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 8,
    },
}
RQ_SHOW_ADMIN_LINK = True
USE_RQ = True
UPDATE_FOURSQUARW_WITH_VIEW = True

INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    # 'debug_toolbar.panels.profiling.ProfilingDebugPanel',
)

SOUTH_MIGRATION_MODULES = {
        'taggit': 'taggit.south_migrations',
    }

STATICFILES_FINDERS = (
   "django.contrib.staticfiles.finders.FileSystemFinder",
   "django.contrib.staticfiles.finders.AppDirectoriesFinder",
   "django_assets.finders.AssetsFinder"
)


CAPTCHA_OUTPUT_FORMAT = u'<table><tr><td>%(image)s</td><td>%(text_field)s</td></tr><tr><td colspan=2>%(hidden_field)s</td></tr></table>'

RAVEN_CONFIG = {
    'register_signals': True,
}

NEWSLETTER_SENDER = (u'zaotdih.ru', 'support@zaotdih.ru')

COMMENTS_APP = 'threadedcomments'

AUTHENTICATION_BACKENDS = [
    'profile.backends.OldAuth',
    'loginza.authentication.LoginzaBackend',
]

ACCOUNT_ACTIVATION_DAYS = 7

AUTH_PROFILE_MODULE = 'profile.Profile'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location
DEFAULT_FROM_EMAIL = 'support@zaotdih.ru'
SERVER_EMAIL = 'support@zaotdih.ru'
EMAIL_USE_TLS = False
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'webmaster'
EMAIL_HOST_PASSWORD = ''
#EMAIL_PORT = 587

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(PROJECT_DIR, 'cover')

DEFAULT_PER_PAGE = 25

COMPANY_PER_PAGE = 25

USERS_PER_PAGE = 25

NEWS_PER_PAGE = 10

CHART_VOTE_MIN = 1

EVENT_PAGINATION = 25
#Count of interview overview page
TEA_INTERVIEWS_COUNT = 5

#pagination settings
PAGINATION_DEFAULT_PAGINATION = 20

MAX_USERPIC_SIZE = 2048000

MONTHS = {
    1:_('January'), 2:_('February'), 3:_('March'), 4:_('April'), 5:_('May'), 6:_('June'),
    7:_('July'), 8:_('August'), 9:_('September'), 10:_('October'), 11:_('November'),
    12:_('December')
}

DISTRICT = (
    (None, _('none')),
    ('1', _('kirovskiy')),
    ('2', _('leninskiy')),
    ('3', _('oktyabrskiy')),
    ('4', _('sovetskiy')),
    ('5', _('centralniy')),
    ('6', _('pervomayskiy')),
)

SPHINX_API_VERSION = 0x116
SPHINX_SERVER = '127.0.0.1'
SPHINX_PORT = 9313


PAGINATOR_MAX_VISIBLE_PAGE = 5

#RSS
RSS_ITEM_COUNT = 30

#YANDEX MAPS
#KEY_API_Y_MAP = 'ANpUFEkBAAAAf7jmJwMAHGZHrcKNDsbEqEVjEUtCmufxQMwAAAAAAAAAAAAvVrubVT4btztbduoIgTLAeFILaQ=='
#YANDEX_MAPS_API_KEY = 'AALPclABAAAAgW1BQwMAoNe9MIgvxBc13xQKLQoo81GrYTkAAAAAAAAAAACEHT67O9ClHRVbal3zh77jC_yDjQ=='
YANDEX_MAPS_API_KEY = 'ADOiK1ABAAAAFXetFwIAZoFBJsQ04zGUejoklD75-9_VepAAAAAAAAAAAADYTxhn3e7Jks2yT0b0hvMrDlCT2A=='


FORMAT_MODULE_PATH ='otdohni2.formats'


#filebrowser settings-------------------------------
TINYMCE_JS_URL = STATIC_URL + 'js/tiny_mce/tiny_mce.js'
FILEBROWSER_DIRECTORY = 'uploads/'
FILEBROWSER_URL_FILEBROWSER_MEDIA = os.path.join(STATIC_URL, 'filebrowser/')
FILEBROWSER_PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/'
FILEBROWSER_URL_TINYMCE = STATIC_URL+'js/tiny_mce/'
FILEBROWSER_PATH_TINYMCE = os.path.join(STATIC_ROOT, 'js/tiny_mce/')

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm',],
    #'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv',],
    'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    #'Code': ['.html','.py','.js','.css'],
    'Flash': ['.swf',],
}
FILEBROWSER_SELECT_FORMATS = {
    'File': ['Folder',],
    'Image': ['Image'],
    'Media': ['Video','Audio',],
    #'Document': ['Document'],
    # for TinyMCE we can also define lower-case items
    'image': ['Image',],
    'file': ['Folder','Image','Document',],
    'media': ['Video','Audio', 'Flash'],
}

TINYMCE_DEFAULT_CONFIG = {

    "plugins" : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",

    "theme_advanced_buttons1" : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
    "theme_advanced_buttons2" : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
    "theme_advanced_buttons3" : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
    "theme_advanced_buttons4" : "insertlayer,moveforward,movebackward,absolute,|,styleprops,spellchecker,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,template,blockquote,pagebreak,|,insertfile,insertimage",
    "theme_advanced_toolbar_location" : "top",
    "theme_advanced_toolbar_align" : "left",
    "theme_advanced_statusbar_location" : "bottom",
    "theme_advanced_resizing" : "true",
#    'theme_advanced_buttons3': "",
    'relative_urls' : False,
    "advimage_update_dimensions_onchange": "true",
    "gecko_spellcheck" : "true",
    "height": "580px",
    "width": "620px",
    'theme': "advanced",
}

ADMIN_TOOLS_MENU = 'apps.adminmenu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'apps.admindashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'apps.admindashboard.CustomAppIndexDashboard'

ELRTE_ADMIN_FIELDS = {
    'news.NewsItem': ['full_text'],
    #'action.action': ['full_text']
    #'news.NewsItem': ['full_text']
}
ELRTE_LOAD_JQUERYUI = False
ELRTE_LOAD_JQUERY = False
ELRTE_OPTIONS = {
    'lang': 'ru',
    'toolbar': 'maxi'
}

ELFINDER = {
    "root": os.path.join(MEDIA_ROOT, 'uploads/'),
    "URL": os.path.join(MEDIA_URL, 'uploads/')
}

# Sphinx 0.9.9 +
SPHINX_API_VERSION = 0x116
SPHINX_PORT = 3312
ROOT_PATH='/var/lib/sphinxsearch/data/'

KINOHOD_API_KEY = 'ea81eb86-48d3-3a0c-895a-3644f3f29ca7'
KINOHOD_CITY_IDS = (
    {'site_id' : 1, 'city_id': 29},
    {'site_id' : 2, 'city_id': 8},
    {'site_id' : 4, 'city_id': 18},
    {'site_id' : 5, 'city_id': 47},
    {'site_id' : 6, 'city_id': 21},
    {'site_id' : 7, 'city_id': 33},
    {'site_id' : 8, 'city_id': 48},
    {'site_id' : 9, 'city_id': 14},
    {'site_id' : 10, 'city_id': 49},
    {'site_id' : 11, 'city_id': 10},
    {'site_id' : 12, 'city_id': 34},
    {'site_id' : 13, 'city_id': 3},
    {'site_id' : 14, 'city_id': 50},
    {'site_id' : 15, 'city_id': 31},
    {'site_id' : 16, 'city_id': 4},
    {'site_id' : 17, 'city_id': 12},
    {'site_id' : 18, 'city_id': 66},
    {'site_id' : 19, 'city_id': 32},
    {'site_id' : 20, 'city_id': 13},
    {'site_id' : 21, 'city_id': 67},
    {'site_id' : 22, 'city_id': 40},
    {'site_id' : 23, 'city_id': 15},
    {'site_id' : 24, 'city_id': 51},
    {'site_id' : 25, 'city_id': 41},
    {'site_id' : 26, 'city_id': 59},
    {'site_id' : 27, 'city_id': 9},
    {'site_id' : 28, 'city_id': 7},
    {'site_id' : 29, 'city_id': 65},
    {'site_id' : 30, 'city_id': 16},
    {'site_id' : 31, 'city_id': 63},
    {'site_id' : 32, 'city_id': 57},
    {'site_id' : 33, 'city_id': 60},
    {'site_id' : 34, 'city_id': 23},
    {'site_id' : 35, 'city_id': 6},
    {'site_id' : 36, 'city_id': 30},
    {'site_id' : 37, 'city_id': 5},
    {'site_id' : 38, 'city_id': 44},
    {'site_id' : 39, 'city_id': 17},
    {'site_id' : 40, 'city_id': 58},
    {'site_id' : 41, 'city_id': 37},
    {'site_id' : 42, 'city_id': 56},
    {'site_id' : 43, 'city_id': 42},
    {'site_id' : 44, 'city_id': 54},
    {'site_id' : 45, 'city_id': 62},
    {'site_id' : 46, 'city_id': 25},
    {'site_id' : 47, 'city_id': 26},
    {'site_id' : 48, 'city_id': 35},
    {'site_id' : 49, 'city_id': 38},
    {'site_id' : 50, 'city_id': 39},
    {'site_id' : 51, 'city_id': 11},
    {'site_id' : 52, 'city_id': 2},
    {'site_id' : 53, 'city_id': 1},
)
HOUR_CHANGE_DATES = 4


MAINMENU = [
    {'title': u'Афиша', 'url': reverse_lazy('event_list')},
    {'title': u'Места отдыха', 'url': reverse_lazy('place_list')},
    {'title': u'Фото', 'url': reverse_lazy('photoreport_list')},
    {'title': u'Конкурсы', 'url': reverse_lazy('action_list')},
    {'title': u'Новости', 'url': reverse_lazy('news_list')},
    {'title': u'Такси', 'url': '/taxi/'},
    {'title': u'Всё для праздника', 'url': '/holiday/'},
    {'title': u'Доставка еды', 'url': '/dostavka_edy/'},
    {'title': u'Бизнес-ланч', 'url': reverse_lazy('lunch_list')},
    {'title': u'Хобби', 'url': '/hobbi/'},
    {'title': u'Авто', 'url': '/avto/'},
    {'title': u'Скидки', 'url': '/sales/',
        'css_classes': 'menu_main__link_sales'},
    {'title': u'Чай со звездой', 'url': reverse_lazy('overview_tea'),
        'css_classes': 'menu_main__link_tea'},
    #{'title': u'Академия', 'url': reverse_lazy('overview_tea'),
    #    'css_classes': 'm_academia'},
]


try:
    from settings_local import *
except ImportError:
    pass
