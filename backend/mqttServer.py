import time
import paho.mqtt.client as mqtt
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/iot_app", encoding="utf-8")
# 格式说明：数据库类型 + 数据库驱动器://用户名:密码@地址:端口/数据库名
Session = sessionmaker(bind=engine)
session = Session()

# MQTT Settings
MQTT_Broker = "127.0.0.1"
MQTT_Port = 1883
Keep_Alive_Interval = 60
MQTT_Topic = "iotclient"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_Topic, 0)


def on_message(client, userdata, msg):
    # print(msg.topic+" " + ":" + str(msg.payload))
    var = str(msg.payload)
    n = re.findall(r":(.+?),", var)
    m = re.findall(r"\"value\":(.+?)}", var)
    print(var)
    # print(n)
    # print(m)
    n.append(m[0])
    # print(datetime.time())
    # print(n)
    stmt = f'insert into device_message(alert,clientId,info,lat,lng,timestamp,value) values ("{int(n[0])}", "{eval(n[1])}", "{eval(n[2])}", "{float(n[3])}", "{float(n[4])}", "{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(float(n[5]) / 1000)))}","{int(n[6])}")'
    session.execute(stmt)
    session.commit()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
client.loop_forever()
