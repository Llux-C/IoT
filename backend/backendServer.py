from backend.iot_app import create_app
from backend.iot_app import db
from backend.iot_app.models import *
from flask import request, jsonify
from backend.iot_app import token
import datetime

app = create_app()


# TODO:通过蓝图，将该文件分成三个文件，现在文件架构不够结构化

@app.route('/getMessage', methods=['GET'])
def getMessage():
    Id = request.args.get('clientId')
    # print(Id)
    messages = Message.query.all()
    result = {
        "code": 0,
        "data": []
    }
    for message in messages:
        # print(message.id, message.alert, message.clientId, message.info, message.lat, message.lng, message.timestamp,
        #       message.value)
        if Id == message.clientId:
            mess = {
                "alert": message.alert,
                "info": message.info,
                "lat": message.lat,
                "lng": message.lng,
                "timestamp": message.timestamp,
                "value": message.value
            }
            result.get("data").append(mess)
            # print("200")
    print(result)
    return result


@app.route('/register', methods=['POST'])
def register():
    # name = request.args.get("name")
    # password = request.args.get("password")
    # email = request.args.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    email = request.form.get("email")
    result = {
        "code": 0,
        "message": "register success!"
    }
    new_id = 0
    # 判断是否重名、重邮箱
    users = User.query.all()
    for user in users:
        if name == user.name or email == user.email:
            result['code'] = -1
            result['message'] = "The user_name or email has existed!"
            return result
        new_id = user.id
    # 插入
    new_user = User(id=new_id + 1, name=name, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()
    return result


@app.route('/tokenLogin', methods=['POST'])
def tokenLogin():
    token_received = request.form.get("token")
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="token is invalid!")
    return jsonify(code=0, msg="login success!", data=token_received)


@app.route('/login', methods=['POST'])
def login():
    password = request.form.get("password")
    email = request.form.get("email")
    code = 0
    msg = "login success!"
    # 判断是否存在且正确
    user = User.query.filter(User.email == email).all()
    if user is None:
        code = -1
        message = "Not exist the user!"
        return jsonify(code=code, msg=msg)
    if user.password != password:
        code = -2
        message = "Password error!"
        return jsonify(code=code, msg=msg)
    token.create_token(user.id)
    return jsonify(code=code, msg=msg, data=token)


@app.route('/alterPassword', methods=['POST'])
def alterPassword():
    token_received = request.form.get("token")
    old_password = request.form.get("oldPsw")
    new_password = request.form.get("newPsw")
    user = token.verify_token(token_received)
    if user in None:
        return jsonify(code=-1, msg="Token has been 失效!")
    if user.password != old_password:
        return jsonify(code=-1, msg="The old password is wrong!")
    user.password = new_password
    db.session.commit()
    return jsonify(code=0, msg="Alter Psw success!")


@app.route('/alterName', methods=['POST'])
def alterName():
    token_received = request.form.get("token")
    new_name = request.form.get("newName")
    user = token.verify_token(token_received)
    if user in None:
        return jsonify(code=-1, msg="Token has been 失效!")
    user.name = new_name
    db.session.commit()
    return jsonify(code=0, msg="Alter userName success!")


@app.route('/getDevice', methods=['GET'])
def getDevice():
    token_received = request.args.get("token")
    user = token.verify_token(token_received)
    if user in None:
        return jsonify(code=-1, msg="Token has been 失效!")
    devices = Device.query.filter(Device.user == user.name).all()
    result = {
        "code": 0,
        "data": []
    }
    for device in devices:
        dev = {
            "code": device.code,
            "name": device.name,
            "description": device.description,
            "create_time": device.create_time,
            "user": device.user,
        }
        result.get("data").append(dev)
    return jsonify(code=0, msg="getSuccess!", data=result)


@app.route('/selectDevice', methods=['GET'])
def selectDevice():
    token_received = request.args.get("token")
    deviceName = request.args.get("name")
    user = token.verify_token(token_received)
    if user in None:
        return jsonify(code=-1, msg="Token has been 失效!")
    devices = Device.query.filter(Device.user == user.name).filter(Device.name == deviceName).all()
    result = {
        "code": 0,
        "data": []
    }
    for device in devices:
        dev = {
            "code": device.code,
            "name": device.name,
            "description": device.description,
            "create_time": device.create_time,
            "user": device.user,
        }
        result.get("data").append(dev)
    return jsonify(code=0, msg="selectSuccess!", data=result)


@app.route('/alterDevice', methods=['POST'])
def alterDevice():
    token_received = request.form.get("token")
    deviceCode = request.form.get("code")
    deviceOldName = request.form.get("oldName")
    deviceNewName = request.form.get("newName")
    deviceDescription = request.form.get("description")

    new_device = Device.query.filter(Device.name == deviceNewName).all()
    if new_device is not None:
        return jsonify(code=-1, msg="The newName has existed and it cannot be the same!")
    user = token.verify_token(token_received)
    if user in None:
        return jsonify(code=-1, msg="Token has been 失效!")
    device = Device.query.filter(Device.name == deviceOldName).all()
    device.code = deviceCode
    device.name = deviceNewName
    device.description = deviceDescription
    db.session.commit()
    return jsonify(code=0, msg="alterSuccess!")


@app.route('/createDevice', methods=['POST'])
def createDevice():
    token_received = request.form.get("token")
    user = token.verify_token(token_received)
    if user in None:
        return jsonify(code=-1, msg="Token has been 失效!")

    deviceCode = request.form.get("code")
    deviceName = request.form.get("name")
    deviceDescription = request.form.get("description")
    deviceUser = request.form.get("user")
    result = {
        "code": 0,
        "message": "create success!"
    }
    new_id = 0
    # 判断是否重名
    devices = Device.query.all()
    for device in devices:
        if deviceName == device.name:
            result['code'] = -1
            result['message'] = "The deviceName has existed!"
            return result
        new_id = device.id
    # 插入
    new_device = Device(id=new_id + 1, code=deviceCode, name=deviceName, description=deviceDescription,
                        create_time=datetime.datetime.now(), user=deviceUser)
    db.session.add(new_device)
    db.session.commit()
    return result


@app.route('/deleteDevice', methods=['GET'])
def deleteDevice():
    token_received = request.form.get("token")
    user = token.verify_token(token_received)
    if user in None:
        return jsonify(code=-1, msg="Token has been 失效!")

    deviceName = request.form.get("name")
    device = Device.query.filter(Device.name == deviceName).all()
    db.session.delete(device)
    db.session.commit()
    return jsonify(code=0, msg="deleteSuccess!")


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
