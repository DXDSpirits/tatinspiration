# -*- coding: utf-8 -*-

from flask_failsafe import failsafe

# for flask failsafe
@failsafe
def create_app():
    from web.app import app
    return app

if(__name__ == "__main__"):
    app = create_app()
    from web.app import auth
    app.debug = app.config["DEBUG_MODE"]
    # move this to script 
    from web.model import Label, Inspiration, LabelInspirationRelationShip, InspirationIndex
    init_class = [auth.User, Label, Inspiration, LabelInspirationRelationShip, InspirationIndex]

    for kls in init_class:
        kls.create_table(fail_silently=True)

    app.run(host='0.0.0.0')
