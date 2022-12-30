#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_restful import Api
import requests
import json
import secrets
from werkzeug.exceptions import BadRequest
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from http_status_codes import HTTP_200_OK

app = Flask(__name__)
api = Api(app)
limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["30 per minute"]
    )

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
    parameters = request.get_json(force=True)
    headers = request.headers.get('Authorization')
    response = requests.post('https://10.0.2.3:5000/signup', json=parameters, headers=headers)
    return response.json(), response.status_code

#/LOGIN
@app.route('/login', methods=['POST'])
@limiter.limit("30 per minute", key_func = lambda : getUsername())
def login():
    parameters = request.get_json(force=True)
    headers = request.headers.get('Authorization')
    response = requests.post('https://10.0.2.3:5000/login', json=parameters, headers=headers)
    return response.json(), response.status_code

#GET DOCUMENT
#/<string:username>/<string:doc_id>
@app.route('/<string:username>/<string:doc_id>', methods=['GET'])
def get(username, doc_id):
    headers = {"Authorization":request.headers.get('Authorization')}
    response = requests.get(f'https://10.0.2.4:5000/{username}/{doc_id}', headers=headers)
    return response.json(), response.status_code

#POST DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['POST'])
def post(username,doc_id):
    parameters = request.get_json(force=True)
    headers = {"Authorization": request.headers.get('Authorization')}
    response = requests.post(f'https://10.0.2.4:5000/{username}/{doc_id}', json=parameters, headers=headers)
    return response.json(), response.status_code

#PUT DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['PUT'])
def put(username, doc_id):
    parameters = request.get_json(force=True)
    headers = {"Authorization": request.headers.get('Authorization')}
    response = requests.put(f'https://10.0.2.4:5000/{username}/{doc_id}', json=parameters, headers=headers)
    return response.json(), response.status_code

#DELETE DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['DELETE'])
def delete(username, doc_id):
    headers = {"Authorization":request.headers.get('Authorization')}
    response = requests.delete(f'https://10.0.2.4:5000/{username}/{doc_id}', headers=headers)
    return response.json(), response.status_code

#GET ALL DOCS
#/<string:username>/_all_docs
@app.route('/<string:username>/_all_docs' , methods=['GET'])
def get_all_docs(username):
    headers = {"Authorization":request.headers.get('Authorization')}
    response = requests.get(f'https://10.0.2.4:5000/{username}/_all_docs', headers=headers)
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, ssl_context=("brokercert.pem","brokerkey.pem"), port=5000)
