#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: api/auth/views.py
# Author: Collins Abitekaniza <abtcolns@gmail.com>
# Date: 10.07.2017
# Last Modified: 10.07.2017

from api.app import app
from api.app import db
from flask import request, jsonify
from .security.decorators import require_fields
from .models import User
import hashlib
import jwt


@app.route("/auth/login", methods=['POST'])
@require_fields('username', 'password')
def login():
    """This is the API login endpoint, call with credentials to get token
---
       tags:
        - Authentication
       parameters:
        - name: username
          in: body
          required: true
          type: string
        - name: password
          in: body
          required: true
          type: string
         """
    username, passphrase = request.form['username'].lower(
    ), request.form['password']
    instance = User.query.filter_by(username=username).first()
    # return if user doesn't exist else verify hash
    if not instance:
        return jsonify({
            "error_msg": "User {} doesn't exist".format(username)
            }), 401
    else:
        salted_phrase = '{}{}'.format(passphrase, instance.salt)
        if instance.password == hashlib.sha256(salted_phrase.encode()).hexdigest():
            payload = {
                "id": instance.id,
                "email": instance.email
            }
            return jsonify({
                "token": jwt.encode(payload, app.secret_key, algorithm='HS256').decode('utf-8')
            })

        return jsonify({
            "error_msg": "Wrong user password, please try again"
        }), 401


@app.route("/auth/register", methods=['POST'])
@require_fields('username', 'password', email='[^@]+@[^@]+\.[^@]+')
def register():
    """This is the API register endpoint
---
       tags:
        - Authentication
       parameters:
        - name: username
          in: body
          type: string
          required: true
        - name: password
          in: body
          type: string
          required: true
        - name: email
          in: body
          type: email
          required: true
         """

    username, email = request.form['username'].lower(), request.form['email']
    passphrase = request.form['password']

    if not User.query.filter_by(username=username).first():
        gen_salt = User.make_salt()
        salted_phrase = '{}{}'.format(passphrase, gen_salt)
        # also save salt for later reconstruction
        user = User(username=username, email=email, salt=gen_salt,
                    password=hashlib.sha256(salted_phrase.encode()).hexdigest())
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "success_msg": "User {} added successfully".format(username)
        })
    else:
        return jsonify({
            "error_msg": "User {} already exists".format(username)
        })
