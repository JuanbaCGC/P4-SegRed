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

#Read users.json
users_json = json.load(open('users.json'))
for user in users_json:
    UserList.append(user)

# Method that read the input filename
def read(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data

# Method that write in the input filename
def write(filename, content):
    with open(filename, "w") as file:
        json.dump(content, file, indent=4)

# Method that revoke a token after five minutes of its creation
def revokeToken(token):
    data = read('tokens.json')
    data.remove(token)
    write('tokens.json', data)

# Method that write a token in the tokens.json
def writeToken(token, username):
    newToken = {
        "token_id":token,
        "username":username
    }
    tokens = read('tokens.json')
    tokens.append(newToken)
    write('tokens.json', tokens)
    timer = threading.Timer(300.0, revokeToken,(newToken, ))
    timer.start()

# Method that search if the token given is correct
def verifyToken(token):
    data = read('tokens.json')
    for saved_token in data:
        if (saved_token['token_id'] == token):
            return (True,saved_token['username'])
    return (False,'The token does not exist')

# Method that provide the errors if the Authorization header is incorrect
def verifyHeader(username):
    #Get the Authorization header (the first position is "token", the second is the user_token) and verify the structure
    header = request.headers.get('Authorization')
    if(header is None):
        return jsonify({'error': "Header is empty. Enter Authorization header"}), HTTP_400_BAD_REQUEST
    else:
        authHeader = header.split()
        if(len(authHeader) != 2 or authHeader[0] != "token"):
            return jsonify({'error': "Incorrect authorization header. Try again with the following format: token user_token."}), HTTP_400_BAD_REQUEST
        #Verify that the token exist and it belongs to the user that do the request
        token_exist = verifyToken(authHeader[1])
        user_name = token_exist[1]
        if(token_exist[0] == False or user_name != username):
            return jsonify({'error': "Incorrect token."}), HTTP_400_BAD_REQUEST
        else:
            return jsonify({'Correct':'The authorization header is correct.'}), HTTP_200_OK

#Hashing function for a password using a random unique salt
def hashPass(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

# Method to compare the hash stored in the users.json and the provided password and see if they match
def matchHashedText(hashedPass, providedPass):
    #Check for the password in the hashed password
    _hashedPass, salt = hashedPass.split(':')
    return _hashedPass == hashlib.sha256(salt.encode() + providedPass.encode()).hexdigest()

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

# Method that validate the password
def validPass(password):
    number = False
    upChar = False
    lowChar = False
    special_char = False
    size = len(password) >= 8

    special_characters = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

    for c in password:
        if c.isdigit():
            number = True
        if c.isupper():
            upChar = True
        if c.islower():
            lowChar = True
        for sc in special_characters:
            if c == sc:
                special_char = True

    return size and number and upChar and lowChar and special_char

#/SIGNUP
@app.route('/signup', methods=['POST'])
@limiter.limit("30 per minute", key_func = lambda : getUsername())
def signup():
    try:
        parameters = request.get_json(force=True)
        name = parameters['username']
        if(validPass(parameters['password']) == False):
            return jsonify({'error': "Invalid password! The password must have at least one capital letter, one miscule letter, one digit and one special character."}), HTTP_400_BAD_REQUEST
        else:
            newUser = {
                "username": str(name),
                "hash-salt": hashPass(str(parameters['password']))
            }
    except KeyError:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST
    except BadRequest:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST
        
    userFound = [users for users in UserList if users['username'] == request.json['username']]
    if (len(userFound) > 0):
        return jsonify({'error': "There is a user with the same name. Try to signup with other user name."}), HTTP_403_FORBIDDEN
    else:
        UserList.append(newUser)
        data = read('users.json')
        data.append(newUser)
        write('users.json', data)
        if os.path.isdir(root+"/"+request.json['username']) is False:
            os.mkdir(root+"/"+request.json['username'])
        token = secrets.token_urlsafe(20)
        writeToken(token,request.json['username'])
        requests.get(f'http://10.0.2.4:5000/{name}/get_folder')
        return jsonify({"access_token": token}), HTTP_201_CREATED

#/LOGIN
@app.route('/login', methods=['POST'])
@limiter.limit("30 per minute", key_func = lambda : getUsername())
def login():
    try:
        parameters = request.get_json(force=True)
        userFound = [users for users in UserList if users['username'] == str(parameters['username']) and matchHashedText(users['hash-salt'],str(parameters['password']))]
    except KeyError:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST
    except BadRequest:
        return jsonify({'error': "Introduce the username and the password."}), HTTP_400_BAD_REQUEST
    if(len(userFound) > 0):
        token = secrets.token_urlsafe(20)
        writeToken(token,str(parameters['username']))
        return jsonify({"access_token": token}), HTTP_201_CREATED 
    else:
        return jsonify({'error': "Incorrect username or password."}), HTTP_403_FORBIDDEN

#/VERIFY
@app.route('/<string:username>/verify', methods=['GET'])
def get_verify(username):
        return verifyHeader(username)
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    app.teardown_appcontext(clearTokens())
