# -*- coding: utf-8 -*-

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip

if(__name__ == "__main__"):
    app.debug = app.config["DEBUG_MODE"]
    # move this to script 
    init_class = [auth.User, Label, Inspiration, LabelInspirationRelationShip]

    for kls in init_class:
        kls.create_table(fail_silently=True)

    app.run(host='0.0.0.0')
