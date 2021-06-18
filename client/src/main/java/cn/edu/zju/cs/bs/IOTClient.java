package cn.edu.zju.cs.bs;

import java.io.FileInputStream;
import java.util.Properties;
import java.util.Vector;

public class IOTClient {
    public static void main(String[] args) {
        MQTTPublisher mqttPublisher = MQTTPublisher.getInstance();
        mqttPublisher.publishMessageSimulation();
    }
}
