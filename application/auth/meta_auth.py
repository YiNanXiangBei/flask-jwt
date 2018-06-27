import base64
import json

from flask import request
from functools import wraps

from application import common
from application.auth.jwtauth import Auth
from application.models import user


def jwt_required(func):
    @wraps(func)
    def wrapper():
        auth_token = request.headers.get('Authorization')
        if auth_token:
            auth_token_arr = auth_token.split(".")
            if not auth_token_arr or len(auth_token_arr) == 3:
                auth_header = json.loads(base64.b64decode(str(auth_token_arr[0]).encode()).decode())
                if auth_header['typ'] != 'JWT':
                    result = common.false_return('', '请传递正确的验证头信息')
                else:
                    payload = Auth.decode_auth_token(auth_token)
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
                        result = common.false_return('', payload, 301)
            else:
                result = common.false_return('', '请传递正确的验证头信息')
        else:
            result = common.false_return('', '没有提供认证Token')
        return func(result)

    return wrapper
