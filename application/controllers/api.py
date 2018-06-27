# -*- coding: utf8 -*-
from application import app
from flask import request, jsonify
from application import user
from application import common
from application.auth import jwtauth

auth = jwtauth.Auth()


@app.route('/register', methods=['POST'])
def register():
    """
    用户注册
    :return:json
    """
    username = request.form.get('username')
    password = request.form.get('password')
    password = user.Users.set_password(password)
    users = user.Users(username=username, password=password)
    result = user.Users.add(users)
    if users.id:
        return_user = {
            'id': users.id,
            'username': users.username,
        }
        return jsonify(common.true_return(return_user, '用户注册成功'))
    else:
        return jsonify(common.false_return('', '用户注册失败'))


@app.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return: json
    """
    username = request.form.get('username')
    passowrd = request.form.get('password')
    if not username or not passowrd:
        return jsonify(common.false_return('', '用户名和密码不能为空'))
    else:
        return auth.authenticate(username, passowrd)


@app.route('/user', methods=['GET'])
def get():
    """
    获取用户信息
    :return:
    """
    result = auth.identify(request)
    return jsonify(result)
