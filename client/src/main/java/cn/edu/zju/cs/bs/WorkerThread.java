package cn.edu.zju.cs.bs;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Random;
import com.alibaba.fastjson.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class WorkerThread extends Thread {

    public static Logger logger = LoggerFactory.getLogger(MQTTPublisher.class);

    private Integer deviceId;

    private String mqttServer;

    private String topic;

    private String clientPrefix;

    private Boolean RUNNING = true;

    public Integer getDeviceId() {
        return deviceId;
    }

    public void setDeviceId(Integer deviceId) {
        this.deviceId = deviceId;
    }

    public String getMqttServer() {
        return mqttServer;
    }

    public void setMqttServer(String mqttServer) {
        this.mqttServer = mqttServer;
    }

    public String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public String getClientPrefix() {
        return clientPrefix;
    }

    public void setClientPrefix(String clientPrefix) {
        this.clientPrefix = clientPrefix;
    }

    public void run() {
        try {
            String clientId;
            String content;
            MemoryPersistence memoryPersistence = new MemoryPersistence();

            Random rand = new Random();

            clientId = clientPrefix + String.format("%04d", deviceId);
            MqttClient mqttClient = new MqttClient(mqttServer, clientId, memoryPersistence);
            MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
            mqttConnectOptions.setCleanSession(true);
            mqttConnectOptions.setUserName(MQTTConfig.USER_NAME);
            mqttConnectOptions.setPassword(MQTTConfig.USER_PASSWORD.toCharArray());
            mqttClient.connect(mqttConnectOptions);

            while (RUNNING) {
                // 随机等待
                int interval = rand.nextInt(10);
                Thread.sleep(interval * 1000);

                IOTMessage msg = new IOTMessage();

                // 设定信息和时间
                Date now = new Date();
                msg.setClientId(clientId);

                msg.setInfo("Device Data " + new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(now));
                // 生成时间戳
                msg.setTimestamp(now.getTime());

                // 随机生成数字
                int value = rand.nextInt(100);
                msg.setValue(value);
                // 超过80告警
                msg.setAlert(value > 80 ? 1 : 0);

                // 根据杭州经纬度随机生成设备位置信息
                msg.setLng(119.9 + rand.nextFloat() * 0.6);
                msg.setLat(30.1 + rand.nextFloat() * 0.4);

                // 格式化
                content = JSONObject.toJSONString(msg);
                System.out.println("Publishing message: " + content);

                // 生成MQTT消息并发布
                MqttMessage message = new MqttMessage(content.getBytes());
                message.setQos(MQTTConfig.QoS);
                mqttClient.publish(topic, message);
                System.out.println("Message published");
            }

            mqttClient.disconnect();
            System.out.println("Disconnected.");
        } catch (MqttException | InterruptedException e) {
            logger.error(e.getMessage(), e);
        }
    }
}
