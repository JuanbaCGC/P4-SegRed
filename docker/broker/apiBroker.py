#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os
from flask_restful import Api
import sys
import requests
import json
import uuid
import hashlib
import secrets
import threading
from werkzeug.exceptions import BadRequest
from flask_limiter import Limiter
from pathlib import Path
from flask_limiter.util import get_remote_address
from http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

MAX_DOCUMENTS = 5

app = Flask(__name__)
api = Api(app)
root = str(Path.home())+"/Server"
limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["30 per minute"]
    )

UserList=[]

if os.path.isdir(root) is False:
    os.mkdir(root)

# Method that write in the input filename
def write(filename, content):
    with open(filename, "w") as file:
        json.dump(content, file, indent=4)

# Method to clear the tokens.json
def clearTokens():
    write('tokens.json', [])

# Method to get the identification of the user in order to count her requests
def getUsername():
    try:
        name = str(request.get_json(force=True)['username'])
    except KeyError:
        return str(secrets.token_urlsafe(20))
    except BadRequest:
        return str(secrets.token_urlsafe(20))
    return name

#/VERSION
@app.route('/version', methods=['GET'])
def getVersion():
    return jsonify({"Version":"1.0"}), HTTP_200_OK

#/SIGNUP
@app.route('/signup', methods=['POST'])
@limiter.limit("30 per minute", key_func = lambda : getUsername())
def signup():
    try:
        parameters = request.get_json(force=True)
    except KeyError:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST
    except BadRequest:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST

    headers = request.headers.get('Authorization')
    respuesta = requests.post('http://10.0.2.3:5000/signup', json=parameters, headers=headers)
    #respuesta = requests.post('http://10.0.1.2:5000/signup', json=parameters, headers=headers)
    return respuesta.json()

#/LOGIN
@app.route('/login', methods=['POST'])
@limiter.limit("30 per minute", key_func = lambda : getUsername())
def login():
    try:
        parameters = request.get_json(force=True)
    except KeyError:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST
    except BadRequest:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST

    headers = request.headers.get('Authorization')
    respuesta = requests.post('http://10.0.2.3:5000/login', json=parameters, headers=headers)

    return respuesta.json()

#GET DOCUMENT
#/<string:username>/<string:doc_id>
@app.route('/<string:username>/<string:doc_id>', methods=['GET'])
def get(username, doc_id):

    headers = {"Authorization":request.headers.get('Authorization')}
    respuesta = requests.get(f'http://10.0.2.4:5000/{username}/{doc_id}', headers=headers)

    return respuesta.json()

#POST DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['POST'])
def post(username,doc_id):
    try:
        parameters = request.get_json(force=True)
    except KeyError:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST
    except BadRequest:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST

    headers = {"Authorization": request.headers.get('Authorization')}
    # Request para el files
    respuesta = requests.post(f'http://10.0.2.4:5000/{username}/{doc_id}', json=parameters, headers=headers)
    return respuesta.json()

#PUT DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['PUT'])
def put(username, doc_id):
    try:
        parameters = request.get_json(force=True)
    except KeyError:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST
    except BadRequest:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST

    headers = {"Authorization": request.headers.get('Authorization')}
    # Request para el files
    respuesta = requests.put(f'http://10.0.2.4:5000/{username}/{doc_id}', json=parameters, headers=headers)
    return respuesta.json()

#DELETE DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['DELETE'])
def delete(username, doc_id):
    
    headers = {"Authorization":request.headers.get('Authorization')}
    respuesta = requests.delete(f'http://10.0.2.4:5000/{username}/{doc_id}', headers=headers)

    return respuesta.json()

#GET ALL DOCS
#/<string:username>/_all_docs
@app.route('/<string:username>/_all_docs' , methods=['GET'])
def get_all_docs(username):
    
    headers = {"Authorization":request.headers.get('Authorization')}
    respuesta = requests.get(f'http://10.0.2.4:5000/{username}/_all_docs', headers=headers)

    return respuesta.json()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    app.teardown_appcontext(clearTokens())
