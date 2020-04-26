from app.model.user import Users
from app import response, app, db
from flask import request
from app.controller import GorController
import datetime
from flask_jwt_extended import *
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy(app)

# @jwt_required
def index():
    try:
        users = Users.query.all()
        data = transform(users)
        return response.ok(data, "")
    except Exception as e:
        print(e)


def transform(users):
    array = []
    for i in users:
        array.append(singleTransform(i))
    return array

def singleTransform(users, withGor=True):
    data = {
        'id': users.id,
        'name': users.name,
        'email': users.email,
    }

    if withGor:
        gorObject = GorController.get(users.id)
        print('gorObject', gorObject)
        data['gor'] = gorObject
    return data

@jwt_required
def show(id):
    try:
        users = Users.query.filter_by(id=id).first()
        if not users:
            return response.badRequest([], 'Empty....')
        print('WOOOOO')
        data = singleTransform(users)
        return response.ok(data, "")
    except Exception as e:
        print(e)

@jwt_required
def store():
    print('OOIII')
    try:
        print('request', request.json['name'])
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        print('DB', db)
        users = Users(name=name, email=email)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        print('CEK RESPON', response)
        return response.ok('', 'Successfully create data!')

    except Exception as e:
        print(e)

@jwt_required
def update(id):
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        print('NAME', name)
        user = Users.query.filter_by(id=id).first()
        user.email = email
        user.name = name
        print('USER', user.name)
        user.setPassword(password)

        db.session.commit()

        return response.ok('', 'Successfully update data!')

    except Exception as e:
        print(e)

@jwt_required
def delete(id):
    print('ID', id)
    try:
        user = Users.query.filter_by(id=id).first()
        print('USER', user)
        if not user:
            return response.badRequest([], 'Empty....')

        db.session.delete(user)
        db.session.commit()

        return response.ok('', 'Successfully delete data!')
    except Exception as e:
        print(e)

def login():
    try:
        print(request.json['email'])
        print(request.json['password'])
        email = request.json['email']
        password = request.json['password']

        user = Users.query.filter_by(email=email).first()
        if not user:
            print('KOSONG')
            return response.badRequest([], 'Empty....')

        if not user.checkPassword(password):
            return response.badRequest([], 'Your credentials is invalid')

        data = singleTransform(user, withGor=False)
        expires = datetime.timedelta(days=1)
        expires_refresh = datetime.timedelta(days=3)
        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_access_token(data, expires_delta=expires_refresh)
        print('data', data)
        return response.ok({
            "data": data,
            "token_access": access_token,
            "token_refresh": refresh_token,
        }, "")
    except Exception as e:
        print(e)

@jwt_refresh_token_required
def refresh():
    try:
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)

        return response.ok({
            "token_access": new_token
        }, "")

    except Exception as e:
        print(e)