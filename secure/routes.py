from flask import Flask, request, jsonify, redirect,url_for
from db_helper.query_runner import * 
import re
import hashlib, hmac
import random
import string
import jwt
import os
import datetime
from functools import wraps

no_secret = os.environ['concealme']
current_token = {'token':""}

def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if current_token['token']:
                token = current_token['token']
            else:
                return jsonify({'data':None,'error':"no token found"})

            try:
                data = jwt.decode(token, no_secret, algorithms=['HS256'])
                uid = data['user_id']
           
                @get_current_user
                def get_user():
                    query = """SELECT * FROM user_info WHERE user_id = %s """ % uid
                    return query
                current_user = get_user()
            except:
                return jsonify({'data':None,'error':'Token is invalid'})
            
            return f(current_user, *args, **kwargs)
        return decorated


def secure_routes(app):
    
    def make_token(user_id):
        return jwt.encode({'user_id':user_id, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, no_secret, algorithm='HS256').decode('UTF-8')

    def make_salt(length=5):
        return ''.join(random.choice(string.letters) for x in xrange(length)) 

    def make_hash(name,password,salt=None):
        if not salt:
            salt=make_salt()
        h = hashlib.sha256(name + password + salt).hexdigest()
        return '%s,%s' % (salt,h)

    def valid_pw(name, password, h):
        salt = h.split(',')[0]
        return h == make_hash(name,password,salt)

    @app.route('/signup', methods=['POST'])
    def signup():
        name = request.json['username']
        password = request.json['password']
        name_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        pass_re = re.compile(r"^.{3,20}$")

        if not (name and password):
            return jsonify({'data':None,'error':'user name or password not found'})
           
        if name_re.match(name) and pass_re.match(password):
            return redirect(url_for('userobj', name=name,password=password))
        else:
            return jsonify({'data':None,'error':'invalid username or password'})

    @app.route('/userobj/<name>/<password>')
    def userobj(name,password):
        pw_hash = make_hash(name,password)

        @check_user_query
        def checkUser():
            query = """
            SELECT name FROM user_info WHERE name = '%s';""" % name
            return query

        @add_user_query
        def addUser():
            query = """
            INSERT INTO user_info (name, pw_hash)
            VALUES('%s','%s') RETURNING user_id;
            """ % (name,pw_hash)
            return query

        if checkUser():
            return jsonify({'data':None,'error':'username %s exits' % name})
        else: 
            user_id = addUser()
            token = make_token(user_id)
            current_token['token'] = token
            return jsonify({'data':{'name':name,'id':user_id,'token':token},'error':None})


    @app.route('/login',methods=['POST'])
    def login():
        name = request.json['username']
        password = request.json['password']

        @get_current_user
        def get_user():
            query="""
            SELECT pw_hash, user_id, name FROM user_info WHERE name = '%s'
            """ % name
            return query
        got_user = get_user()

        if got_user and valid_pw(name, password,got_user[0]):
            token = make_token(got_user[1])
            current_token['token'] = token
            return jsonify({'data':{'name':got_user[2],'id':got_user[1],'token':token},'error':None})
        
        return jsonify({'data':None,'error':'invalid username or password'})


    @app.route('/user')
    @token_required
    def user(current_user):
        return jsonify({'name':current_user[1],'user_id':current_user[0]})
        
