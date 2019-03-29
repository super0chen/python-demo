import json

from flask import jsonify, make_response

user_data = [
    {
        'id': 1,
        'name': '张三',
        'age': 23
    },
    {
        'id': 2,
        'name': '李四',
        'age': 24
    }
]


def getTest():
    data = {
        'status': 'success',
        'users': user_data
    }
    return json.dumps(data, ensure_ascii=False, indent=1)


def getById(id):
    for user in user_data:
        if user['id'] == id:
            return jsonify(status='success', user=user)


def userCookie():
    resonseHtml = '<h1>This document carries a cookie!</h1>'
    response = make_response(resonseHtml)
    response.set_cookie('answer', '42')
    return response
