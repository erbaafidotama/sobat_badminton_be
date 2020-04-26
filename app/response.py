from flask import jsonify, make_response


def ok(values, message):
    res = {
        'values': values,
        'message': message,
        'status': 200
    }

    res = values

    return make_response(jsonify(res)), 200


def badRequest(values, message):
    res = {
        'values': values,
        'message': message,
        'status': 400
    }

    return make_response(jsonify(res)), 400