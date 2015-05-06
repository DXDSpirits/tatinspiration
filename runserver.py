# -*- coding: utf-8 -*-

from web.app import app, auth


if(__name__ == "__main__"):
    app.debug = app.config["DEBUG_MODE"]
    # move this to script 
    auth.User.create_table(fail_silently=True)
    app.run(host='0.0.0.0')
