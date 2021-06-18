package cn.edu.zju.cs.bs;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.Vector;

public class MQTTPublisher {

    public static Logger logger = LoggerFactory.getLogger(MQTTPublisher.class);

    final private String clientId = "mqtt_server_pub";

    private String serverUrl;

    private static MQTTPublisher mqttPublisher;

    private static MqttClient mqttClient;

    private static MqttConnectOptions connectOptions;

    private static MemoryPersistence memoryPersistence;

    public MQTTPublisher() {
        this.config();
    }

    protected void finalize() throws Throwable {
        try {
            mqttClient.disconnect();
        }
        catch(MqttException e) {
            logger.error(e.getMessage(), e);
        }
    }

    synchronized public static MQTTPublisher getInstance() {
        if(mqttPublisher == null) {
            mqttPublisher = new MQTTPublisher();
        }
        return mqttPublisher;
    }

    private void config() {
        this.serverUrl = MQTTConfig.SERVER;
        memoryPersistence = new MemoryPersistence();
        connectOptions = new MqttConnectOptions();

        try {
            mqttClient = new MqttClient(serverUrl, clientId, memoryPersistence);
            connectOptions.setCleanSession(true);
            connectOptions.setUserName(MQTTConfig.USER_NAME);
            connectOptions.setPassword(MQTTConfig.USER_PASSWORD.toCharArray());
            mqttClient.connect(connectOptions);
        } catch (MqttException e) {
            logger.warn(e.getMessage(), e);
        }
    }

    public void publishMessageSimulation() {
        try {
            int devices = MQTTConfig.DEVICE_NUM;
            String topic = MQTTConfig.TOPIC;
            String deviceIdPrefix = MQTTConfig.DEVICE_ID_PREFIX;

            Vector<WorkerThread> threadVector = new Vector<>();
            for (int i = 0; i < devices; i++) {
                WorkerThread thread = new WorkerThread();
                thread.setDeviceId(i + 1);
                thread.setMqttServer(serverUrl);
                thread.setTopic(topic);
                thread.setClientPrefix(deviceIdPrefix);
                threadVector.add(thread);
                thread.start();
            }
            for (WorkerThread thread : threadVector) { thread.join(); }
        } catch (Exception e) {
            logger.error(e.getMessage(), e);
        }
    }

    public void disconnect() {
        try {
            mqttClient.disconnect();
        } catch (MqttException me) {
            logger.error("ERROR", me);
        }
    }
}
