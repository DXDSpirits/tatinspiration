# -*- coding: utf-8 -*-
import re
import time

from flask import render_template, request, redirect, flash, session
from whoosh import qparser

from web.app import app, auth
from web.model import Label, Inspiration, LabelInspirationRelationShip
from web.util import get_whoosh_ix, q, compress_jsonify
from web.util.lru import lru_cache_function




@lru_cache_function(max_size=64, expiration=15*60)
def _search(query, page, limit):
    from web.model.whoose_schema import InspirationSchema
    result_list = []
    total = 0

    ## do the search

    ix = get_whoosh_ix("inspiration", InspirationSchema)

    with ix.searcher() as searcher:
        parser = qparser.MultifieldParser(["labels" ,"content"], schema=ix.schema, group=qparser.OrGroup)
        search_expression = parser.parse(query)
        # app.logger.info("search_expression: %s", search_expression)

        results = searcher.search_page(search_expression, page, pagelen=limit)
        total = len(results)

        result_list = filter(None, [Inspiration.select().where(Inspiration.id==r["inspiration_id"]).first() \
                                     for r in results])

    app.logger.info("keyword:%s ==> %d result(s) found", query, total)
    next_page = ""
    if page*limit < total:
        next_page = request.script_root + request.path + "?"
        args_list = []
        for k in request.args:
            if "page" == k:
                args_list.append("page=%d"%(page+1))
            else:
                args_list.append(k+"="+request.args[k])
        if "page" not in request.args:
            args_list.append("page=%d"%(page+1))
        next_page += "&".join(args_list)

    return {
            "meta": {
                "model": "inspiration",
                "keyword": query,
                "next": next_page,
                "count": total
            },
            "objects": [_.to_json() for _ in result_list]
    }


@app.route('/api/inspiration/search')
def inspiration_search():
    start_time = time.time()
    query = request.args.get("q", "").strip()
    page = int(request.args.get("page") or 1) ## data validation
    limit = int(request.args.get("limit") or 100)

    dict_data = _search(query, page, limit)
    dict_data["meta"]["total_time"] = time.time() - start_time

    return compress_jsonify(dict_data)

    






