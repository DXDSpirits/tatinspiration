# -*- coding: utf-8 -*-

import logging

DEBUG_MODE          = True
LESS_DEBUG          = True
JS_DEBUG            = True
PRODUCTION          = False

SITENAME            = "Boring"#your site here
SITE_DOMAIN         = ""#your site here
PORT                = "5000"
SECRET_KEY          = "secret_keyplzchangeit"

WHOOSH_BASE         = "/Users/yang/whoosh"

DATABASE = {
    'name': '',
    'engine': '',
    'user': '',
    'passwd': '',
}

REDIS = {
    "host": 'localhost',
    "port": 6379,
}

try:
    from local_conf import *
except ImportError, e:
    pass
except Exception, e:
    logging.warn("Cannot import configurations from local_config, error: %s" % e)

SITE = "http://" + SITE_DOMAIN + ":" + PORT
