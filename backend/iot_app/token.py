from backend.iot_app.models import *
from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

SECRET_KEY = "ccyccyccy"


def create_token(api_user):

    # 第一个参数是内部的私钥，随便设置
    # 第二个参数是有效期(秒)
    s = Serializer(SECRET_KEY, expires_in=3600)
    token = s.dumps({"id": api_user}).decode("ascii")
    return token


def verify_token(token):

    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(SECRET_KEY)
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    # 拿到转换后的数据，根据模型类去数据库查询用户信息
    user = User.query.get(data["id"])
    return user
