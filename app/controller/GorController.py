from app.model.gor import Gors as Gor
from flask import request, jsonify
from app import response, db
from app.controller import UserController
from flask_jwt_extended import *

@jwt_required
def index():
    try:
        id = request.args.get('user_id')
        if id==None:
            gors = Gor.query.all()
            data = transform(gors)
            return response.ok(data, "")
        else:
            gor = Gor.query.filter_by(user_id=id).all()
            data = transform(gor)
            return response.ok(data, "")
    except Exception as e:
        print(e)


def get(values):
    print('CHECK INI', values)
    try:
            gor = Gor.query.filter_by(user_id=values).all()
            data = transform(gor, withUser=True)
            print('CKECK DATA', data)
            return data
    except Exception as e:
        print(e)

@jwt_required
def store():
    try:
        nama_gor = request.json['nama_gor']
        alamat_gor = request.json['alamat_gor']
        user_id = request.json['user_id']

        gor = Gor(user_id=user_id, nama_gor=nama_gor, alamat_gor=alamat_gor)
        db.session.add(gor)
        db.session.commit()

        return response.ok('', 'Sukses Create GOR!!')
    except Exception as e:
        print(e)

@jwt_required
def update(id):
    try:
        nama_gor = request.json['nama_gor']
        alamat_gor = request.json['alamat_gor']

        gor = Gor.query.filter_by(id=id).first()
        gor.nama_gor = nama_gor
        gor.alamat_gor = alamat_gor

        db.session.commit()

        return response.ok('', 'Successfully update GOR!')

    except Exception as e:
        print(e)


@jwt_required
def show(id):
    try:
        gor = Gor.query.filter_by(id=id).first()
        if not gor:
            return response.badRequest([], 'Empty....')

        data = singleTransform(gor)
        return response.ok(data, "")
    except Exception as e:
        print(e)


@jwt_required
def delete(id):
    try:
        gor = Gor.query.filter_by(id=id).first()
        if not gor:
            return response.badRequest([], 'Empty....')

        db.session.delete(gor)
        db.session.commit()

        return response.ok('', 'Successfully delete data!')
    except Exception as e:
        print(e)


def transform(values, withUser=False):
    array = []
    for i in values:
        array.append(singleTransform(i, withUser))
    return array


def singleTransform(values, withUser=False):
    print('LIHAT INI', withUser)
    if withUser == True:
        data = {
            'id': values.id,
            'user_id': values.user_id,
            'nama_gor': values.nama_gor,
            'alamat_gor': values.alamat_gor,
            'created_at': values.created_at,
            'updated_at': values.updated_at,
            # 'user': UserController.singleTransform(values.users, withGor=False)
        }
    else:
        data = {
            'id': values.id,
            'user_id': values.user_id,
            'nama_gor': values.nama_gor,
            'alamat_gor': values.alamat_gor,
            'created_at': values.created_at,
            'updated_at': values.updated_at,
            'user': UserController.singleTransform(values.users, withGor=False)
        }
    print('singleTransform', data)

    return data