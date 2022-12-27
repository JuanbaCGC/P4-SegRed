#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os
from flask_restful import Api
import sys
import json
from werkzeug.exceptions import BadRequest
from pathlib import Path
from http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

MAX_DOCUMENTS = 5

app = Flask(__name__)
api = Api(app)
root = str(Path.home())+"/Server"

#GET DOCUMENT
#/<string:username>/<string:doc_id>
@app.route('/<string:username>/<string:doc_id>', methods=['GET'])
def get(username, doc_id):
    validate = verifyHeader(username)
    if(validate[0] == True):
        documents_list = os.listdir(root+"/"+username)
        if doc_id+".json" not in documents_list:
            return jsonify({'error': "You don't have any document with this name."}), HTTP_404_NOT_FOUND
        else:
            file = open(root+"/"+username+"/"+doc_id+".json", "r")
            return jsonify(json.load(file)), HTTP_200_OK
    else:
        return validate

#POST DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['POST'])
def post(username,doc_id):
    validate = verifyHeader(username)
    if(validate[0] == True):
        documents_list = os.listdir(root+"/"+username)
        if len(documents_list) == MAX_DOCUMENTS:
            return jsonify({'error': "You have the maximum number of documents ("+str(MAX_DOCUMENTS)+"). If you want to create another one, you must delete other document."}), HTTP_400_BAD_REQUEST    
        if doc_id in documents_list:
            return jsonify({'error': "You have another document with this name! Try again with other name."}), HTTP_400_BAD_REQUEST
        else:
            try:
                parameters = request.get_json(force=True)
            except BadRequest:
                return jsonify({'error': "Introduce the doc content with a json struct."}), HTTP_400_BAD_REQUEST
            try:
                content = json.dumps(parameters['doc_content'])
            except TypeError:
                return jsonify({'error': "Introduce the doc content with a json struct."}), HTTP_400_BAD_REQUEST
            except KeyError:
                return jsonify({'error': "Introduce the doc content."}), HTTP_400_BAD_REQUEST
            file = open(root+"/"+username+"/"+doc_id+".json", "w")
            file.write(str(content))
            size = sys.getsizeof(str(content))
            return jsonify({"size": size}), HTTP_201_CREATED 
    else:
        return validate

#PUT DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['PUT'])
def put(username, doc_id):
    validate = verifyHeader(username)
    if(validate[0] == True):
        documents_list = os.listdir(root+"/"+username)
        if doc_id+".json" not in documents_list:
            return jsonify({'error': "The document "+doc_id+" does not exist! Try again with other document."}), HTTP_404_NOT_FOUND
        else:
            try:
                parameters = request.get_json(force=True)
            except BadRequest:
                return jsonify({'error': "Introduce the doc content with a json struct."}), HTTP_400_BAD_REQUEST
            try:
                content = json.dumps(parameters['doc_content'])
            except TypeError:
                return jsonify({'error': "Introduce the doc content with a json struct."}), HTTP_400_BAD_REQUEST
            except KeyError:
                return jsonify({'error': "Introduce the doc content."}), HTTP_400_BAD_REQUEST
            file = open(root+"/"+username+"/"+doc_id+".json", "w")
            file.write(str(content))
            size = sys.getsizeof(str(content))
            return jsonify({"size": size}), HTTP_201_CREATED 
    else:
        return validate

#DELETE DOCUMENT
@app.route('/<string:username>/<string:doc_id>', methods=['DELETE'])
def delete(username, doc_id):
    validate = verifyHeader(username)
    if(validate[0] == True):
        documents_list = os.listdir(root+"/"+username)
        if doc_id+".json" not in documents_list:
            return jsonify({'error': "The document "+doc_id+" does not exist! Try again with other document."}), HTTP_404_NOT_FOUND
        else:
            os.remove(root+"/"+username+"/"+doc_id+".json")
        return jsonify({}), HTTP_200_OK 
    else:
        return validate

#GET ALL DOCS
#/<string:username>/_all_docs
@app.route('/<string:username>/_all_docs' , methods=['GET'])
def get_all_docs(username):
    validate = verifyHeader(username)
    if(validate[0] == True):
        if os.path.exists(root+"/"+username):
            if len(os.listdir(root+"/"+username)) == 0:
                return jsonify({'error': "You don't have any document."}), HTTP_404_NOT_FOUND
            else:
                documents_found={}
                for filename in os.listdir(root+"/"+username):
                    file = open(root+"/"+username+"/"+filename, "r")
                    documents_found[filename] = json.load(file)
                return jsonify(documents_found), HTTP_200_OK 
        else:
            return jsonify({'error': "This username does not exist."}), HTTP_404_NOT_FOUND
    else:
        return validate

if __name__ == '__main__':
    app.run(debug=True, port=5000)