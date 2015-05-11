# -*- coding: utf-8 -*-
import re
from flask import render_template, request, redirect, flash, session, jsonify
from whoosh import qparser

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip
from web.util import get_whoosh_ix, q

@app.route('/api/inspiration/search')
def inspiration_search():
    from web.model.whoose_schema import InspirationSchema
    query = request.args.get("q", "").strip()
    result_list = []

    ## find label firstly 
    label = Label.select().where(Label.name==query).first()
    ## shortcut
    LIR = LabelInspirationRelationShip
    if label:
        result_list = [rs.inspiration for rs in LIR.select(LIR.inspiration) \
                                                   .where(LIR.label==label)]

    ## then do the search

    ix = get_whoosh_ix("inspiration", InspirationSchema)

    with ix.searcher() as searcher:
        parser = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)
        search_expression = parser.parse(query)


        results = searcher.search(search_expression)


        result_list += [ Inspiration.select().where(Inspiration.id==r["inspiration_id"]).get() \
                                     for r in results]
    return jsonify({
                    "meta": {
                        "model": "inspiration",
                        "keyword": query,
                    },
                    "objects": [_.to_json() for _ in result_list],
            })






