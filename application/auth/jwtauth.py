# -*- coding: utf8 -*-
import datetime
import json

import jwt
import time
import base64
from flask import jsonify

from application import common
from application import configs
from application import user


class Auth(object):
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id:
        :param login_time:
        :return:string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + configs.jwt_config.get('JWT_EXPIRATION_DELTA'),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                configs.jwt_config.get('JWT_SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, configs.jwt_config.get('JWT_SECRET_KEY'), options={'verify': False})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token 过期请重新登录'
        except jwt.InvalidTokenError:
            return '无效 Token，请重新登录'

    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token, 登录失败返回失败原因
        :param username:
        :param password:
        :return:
        """
        user_info = user.Users.query.filter_by(username=username).first()
        if user_info is None:
            return jsonify(common.false_return('', '找不到用户'))
        else:
            if user.Users.check_password(user_info.password, password):
                login_time = int(time.time())
                user.Users.update(user.Users, user_info.id, login_time)
                token = self.encode_auth_token(user_info.id, login_time)
                return jsonify(common.true_return(token.decode(), '登录成功'))
            else:
                return jsonify(common.false_return('', '密码不正确'))

    def identify(self, request):
        """
        用户鉴权
        :param request:
        :return:
        """
        auth_token = request.headers.get('Authorization')
        if auth_token:
            auth_token_arr = auth_token.split(".")
            if not auth_token_arr or len(auth_token_arr) == 3:
                auth_header = json.loads(base64.b64decode(str(auth_token_arr[0]).encode()).decode())
                if auth_header['typ'] != 'JWT':
                    result = common.false_return('', '请传递正确的验证头信息')
                else:
                    payload = self.decode_auth_token(auth_token)
                    if not isinstance(payload, str):
                        users = user.Users.get_by_id(user.Users, payload['data']['id'])
                        if users is None:
                            result = common.false_return('', '找不到该用户')
                        else:
                            if users.login_time == payload['data']['login_time']:
                                return_user = {
                                    'id': users.id,
                                    'username': users.username
                                }
                                result = common.true_return(return_user, '请求成功')
                            else:
                                result = common.false_return('', 'Token已更改，请重新登录获取')
                    else:
                        result = common.false_return('', payload)
            else:
                result = common.false_return('', '请传递正确的验证头信息')
        else:
            result = common.false_return('', '没有提供认证Token')
        return result
