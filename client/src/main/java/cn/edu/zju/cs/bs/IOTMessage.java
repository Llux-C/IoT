package cn.edu.zju.cs.bs;

public class IOTMessage {

    // 设备ID
    private String clientId;

    // 上报信息
    private String info;

    //设备数据
    private int value;

    //是否告警，0-正常，1-告警
    private int alert;

    //设备位置，经度
    private double lng;

    //设备位置，纬度
    private double lat;

    //上报时间，ms
    private long timestamp;

    public String getClientId() {
        return clientId;
    }

    public void setClientId(String clientId) {
        this.clientId = clientId;
    }

    public String getInfo() {
        return info;
    }

    public void setInfo(String info) {
        this.info = info;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }

    public int getAlert() {
        return alert;
    }

    public void setAlert(int alert) {
        this.alert = alert;
    }

    public double getLng() {
        return lng;
    }

    public void setLng(double lng) {
        this.lng = lng;
    }

    public double getLat() {
        return lat;
    }

    public void setLat(double lat) {
        this.lat = lat;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }
}
