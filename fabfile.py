# -*- coding: utf-8 -*-

import os
import logging

from fabric.api import local
from fabric.context_managers import lcd

_warn = logging.warn
CURRENT_PATH = os.path.join(os.getcwd(),os.path.dirname(__file__))

def cleaning():
    """Delete all pyc and *.orig files in project directories."""
    local("find . -name '*.orig' -exec rm -i {} \;")
    local("find . -type f -name '*.pyc' -exec rm {} \;")

def update_req():
    """Updating requirements for pip"""
    # check whether in virtualenv
    if not os.environ.get("VIRTUAL_ENV"):
        _warn("You are not in an Virtualenv, please activate it first")
        return
    local("pip freeze|grep -v distribute > %s/pip_requirements.txt" % CURRENT_PATH)


    
