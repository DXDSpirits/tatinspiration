# -*- coding: utf-8 -*-
from flask import request, jsonify


from web.app import app
from web.model import User

@app.route('/api/user/login', methods=['POST'])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')
    if(User.is_valid(email=email, password=password)):
        return  jsonify(
            rcode=200,
        )
    else:
        return jsonify(rcode=403, 
                       error_message="email & password are not maatched"
                )



