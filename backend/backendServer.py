import json

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
    data = json.loads(request.data)
    name = data['name']
    password = data['password']
    email = data['email']
    print(name, email, password)
    result = {
        "code": 0,
        "msg": "Register success!"
    }
    new_id = 0
    # 判断是否重名、重邮箱
    users = User.query.all()
    for user in users:
        if name == user.name or email == user.email:
            result['code'] = -1
            result['msg'] = "The user_name or email has existed!"
            return result
        new_id = user.id
    # 插入
    new_user = User(id=new_id + 1, name=name, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()
    return result


@app.route('/tokenLogin', methods=['POST'])
def tokenLogin():
    data = json.loads(request.data)
    token_received = data["token"]
    print(token_received)
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="token is invalid!")
    return jsonify(code=0, msg="login success!", data=token_received)


@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    password = data["password"]
    email = data["email"]
    print(email, password)
    code = 0
    msg = "login success!"
    # 判断是否存在且正确
    user = User.query.filter(User.email == email).all()
    if user is None:
        code = -1
        msg = "Not exist the user!"
        return jsonify(code=code, msg=msg)
    print(user[0].password)
    if user[0].password != password:
        code = -2
        msg = "Password error!"
        return jsonify(code=code, msg=msg)
    token_back = token.create_token(user[0].id)
    print(token_back)
    print(type(token_back))
    return jsonify(code=code, msg=msg, data=token_back)


@app.route('/getUser', methods=['GET'])
def getUser():
    token_received = request.args.get('token')
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")
    return jsonify(code=0, msg="getSuccess!", data=user.name)


@app.route('/alterPassword', methods=['POST'])
def alterPassword():
    data = json.loads(request.data)
    token_received = data["token"]
    old_password = data["oldPsw"]
    new_password = data["newPsw"]
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")
    if user.password != old_password:
        return jsonify(code=-2, msg="The old password is wrong!")
    user.password = new_password
    db.session.commit()
    return jsonify(code=0, msg="Alter Psw success!")


@app.route('/alterName', methods=['POST'])
def alterName():
    data = json.loads(request.data)
    token_received = data["token"]
    new_name = data["newName"]
    print(new_name)
    tmp = User.query.filter(User.name == new_name).all()
    if len(tmp) != 0:
        return jsonify(code=-1, msg="不能改成这个名字!")
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")

    # 对设备的主人名称也要进行修改
    devices = Device.query.filter(Device.user == user.name).all()
    for device in devices:
        device.user = new_name
    user.name = new_name
    db.session.commit()
    return jsonify(code=0, msg="更改名字成功!")


@app.route('/getDevice', methods=['GET', 'POST'])
def getDevice():
    if request.method == 'GET':
        token_received = request.args.get("token")
        user = token.verify_token(token_received)
        if user is None:
            return jsonify(code=-1, msg="Token has been 失效!")
        devices = Device.query.filter(Device.user == user.name).all()
        result = {
            "code": 0,
            "data": []
        }
        for device in devices:
            dev = {
                "id": device.id,
                "code": device.code,
                "name": device.name,
                "description": device.description,
                "create_time": device.create_time,
                "user": device.user,
            }
            result.get("data").append(dev)
            print(dev)
        return result
    # elif request.method == 'POST':


@app.route('/selectDevice', methods=['GET'])
def selectDevice():
    token_received = request.args.get("token")
    deviceName = request.args.get("name")
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")
    devices = Device.query.filter(Device.user == user.name).filter(Device.name.ilike("%" + deviceName + "%")).all()
    result = {
        "code": 0,
        "data": []
    }
    for device in devices:
        dev = {
            "id": device.id,
            "code": device.code,
            "name": device.name,
            "description": device.description,
            "create_time": device.create_time,
            "user": device.user,
        }
        result.get("data").append(dev)
    return result


@app.route('/alterDevice', methods=['POST'])
def alterDevice():
    data = json.loads(request.data)
    token_received = data["token"]
    deviceCode = data["code"]
    deviceOldName = data["oldName"]
    deviceNewName = data["newName"]
    deviceDescription = data["description"]
    deviceId = data["id"]
    new_device = Device.query.filter(Device.name == deviceNewName).all()
    if len(new_device)!=0:
        if len(new_device) == 1 and new_device[0].id == deviceId:
            pass
        else:
            return jsonify(code=-1, msg="The newName has existed and it cannot be the same!")
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")
    device = Device.query.filter(Device.name == deviceOldName).all()
    device[0].code = deviceCode
    device[0].name = deviceNewName
    device[0].description = deviceDescription
    db.session.commit()
    return jsonify(code=0, msg="修改成功!")


@app.route('/createDevice', methods=['POST'])
def createDevice():
    data = json.loads(request.data)
    token_received = data["token"]
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")

    deviceCode = data["code"]
    deviceName = data["name"]
    deviceDescription = data["description"]
    deviceUser = data["user"]
    result = {
        "code": 0,
        "msg": "create success!"
    }
    new_id = 0
    # 判断是否重名
    devices = Device.query.all()
    for device in devices:
        if deviceName == device.name:
            result['code'] = -1
            result['msg'] = "The deviceName has existed!"
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
    token_received = request.args.get("token")
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")

    deviceName = request.args.get("name")
    devices = Device.query.filter(Device.name == deviceName).all()
    for device in devices:
        db.session.delete(device)
    db.session.commit()
    return jsonify(code=0, msg="删除设备成功!")


@app.route('/getRecentDevice', methods=['GET'])
def getRecentDevice():
    day_return = []
    count = [0, 0, 0, 0, 0, 0, 0]
    token_received = request.args.get("token")
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")
    today = datetime.datetime.today()
    # 获取过去七天的日期并转化成字符串
    for i in range(0, 7):
        daytmp = today - datetime.timedelta(days=i)
        dayt = daytmp.replace(hour=0, minute=0, second=0, microsecond=0)
        dayt = datetime.datetime.date(dayt)
        day_return.append(str(dayt)[5:])
    day_return.reverse()
    # 获取设备中创造日期符合过去七天的
    devices = Device.query.filter(Device.user == user.name).all()
    for device in devices:
        device_day = str(datetime.datetime.date(device.create_time))[5:]
        for i in range(len(day_return)):
            if day_return[i] == device_day:
                count[i] += 1

    print(day_return, count)
    return jsonify(code=0, msg="getRDsuccess!", day=day_return, count=count)


@app.route("/getRecentMessage", methods=['GET'])
def getRecentMessage():
    day_return = []
    total = [0, 0, 0, 0, 0, 0, 0]
    normal = [0, 0, 0, 0, 0, 0, 0]
    alert = [0, 0, 0, 0, 0, 0, 0]
    token_received = request.args.get("token")
    user = token.verify_token(token_received)
    if user is None:
        return jsonify(code=-1, msg="Token has been 失效!")
    today = datetime.datetime.today()
    # 获取过去七天的日期并转化成字符串
    for i in range(0, 7):
        daytmp = today - datetime.timedelta(days=i)
        dayt = daytmp.replace(hour=0, minute=0, second=0, microsecond=0)
        dayt = datetime.datetime.date(dayt)
        day_return.append(str(dayt)[5:])
    day_return.reverse()

    messages = Message.query.filter().all()
    for message in messages:
        message_day = str(datetime.datetime.date(message.timestamp))[5:]
        for i in range(len(day_return)):
            if day_return[i] == message_day:
                total[i] += 1
                if message.alert == 0:
                    normal[i] += 1
                else:
                    alert[i] += 1
    print(day_return, total, normal, alert)
    return jsonify(code=0, msg="getRMsuccess!", day=day_return, total=total, alert=alert, normal=normal)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
