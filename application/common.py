# -*- coding: utf8 -*-


def true_return(data, msg, code=200):
    return {
        "code": code,
        "status": True,
        "data": data,
        "msg": msg
    }


def false_return(data, msg, code=400):
    return {
        "code": code,
        "status": False,
        "data": data,
        "msg": msg
    }
