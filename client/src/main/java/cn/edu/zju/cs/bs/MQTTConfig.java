package cn.edu.zju.cs.bs;

public class MQTTConfig {
    // 监听端口，一般就是1883
    public final static String SERVER = "tcp://localhost:1883";
    // mosquitto设置的用户名和密码，这里用户名设置成username，密码设置成password
    public final static String USER_NAME = "username";
    public final static String USER_PASSWORD = "password";

    public final static Integer DEVICE_NUM = 5;
    // 订阅主题，与mqttServer中一致就行
    public final static String TOPIC = "iotclient";

    public final static String DEVICE_ID_PREFIX = "device";

    public final static Integer QoS = 2;
}
