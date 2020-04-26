from app import app
from app.controller import UserController, GorController
from flask import request

# ROUTES LOGIN
@app.route('/login', methods=['POST'])
def login():
    return UserController.login()

# ROUTES USERS
@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'GET':
        return UserController.index()
    else:
        return UserController.store()

@app.route('/users/<id>', methods=['PUT', 'GET', 'DELETE'])
def usersDetail(id):
    if request.method == 'GET':
        return UserController.show(id)
    elif request.method == 'PUT':
        return UserController.update(id)
    elif request.method == 'DELETE':
        return UserController.delete(id)


# ROUTES GOR
@app.route('/gor', methods=['POST', 'GET'])
def todo():
    if request.method == 'GET':
        return GorController.index()
    else:
        return GorController.store()


@app.route('/gor/<id>', methods=['PUT', 'GET', 'DELETE'])
def todoDetail(id):
    if request.method == 'GET':
        return GorController.show(id)
    elif request.method == 'PUT':
        return GorController.update(id)
    elif request.method == 'DELETE':
        return GorController.delete(id)