# -*- coding: utf-8 -*-
import re
import time

from flask import render_template, request, redirect, flash, session, jsonify
from whoosh import qparser

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip
from web.util import get_whoosh_ix, q

@app.route('/api/inspiration/search')
def inspiration_search():
    start_time = time.time()
    from web.model.whoose_schema import InspirationSchema
    query = request.args.get("q", "").strip()
    page = int(request.args.get("page") or 1) ## data validation
    limit = 10
    result_list = []

    ## do the search

    ix = get_whoosh_ix("inspiration", InspirationSchema)

    with ix.searcher() as searcher:
        parser = qparser.MultifieldParser(["labels" ,"content"], schema=ix.schema, group=qparser.OrGroup)
        search_expression = parser.parse(query)
        # app.logger.info("search_expression: %s", search_expression)

        results = searcher.search(search_expression)


        result_list = [ Inspiration.select().where(Inspiration.id==r["inspiration_id"]).get() \
                                     for r in results]

    app.logger.info("keyword:%s ==> %d result(s) found", query, len(result_list))
    next_page = ""
    if page*limit < len(result_list):
        next_page = page + 1;

    return jsonify({
                    "meta": {
                        "total_time": time.time()-start_time,
                        "model": "inspiration",
                        "keyword": query,
                    },
                    "objects": [_.to_json() for _ in result_list[page*limit-limit:page*limit]],
            })






