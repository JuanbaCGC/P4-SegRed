#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_restful import Api
from http_status_codes import HTTP_200_OK

app = Flask(__name__)
api = Api(app)

#/VERSION
@app.route('/version', methods=['GET'])
def getVersion():
    return jsonify({"Version":"1.0"}), HTTP_200_OK

if __name__ == '__main__':
    app.run(debug=True, port=5000)
