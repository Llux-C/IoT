windows下mosquitto安装（x64）

https://mosquitto.org/download/



https://www.cnblogs.com/dissun/p/10505007.html
打开windows“服务”应用，启动mosquito服务
mosquitto下载后需要配置的，参考上面这个连接，用户名和密码设置成username和password
看到第四章结束就行
记得网站里面操作的是cmd，用powershell的话要变成./balabala什么的，就用cmd吧


然后client文件夹，首先要用idea打开，然后maven如果没下载要下，然后mvn clean install，然后就生成一个target文件夹
cd到：
project\client\target
输入
java -jar iotclient-1.0.0.jar
就可以看到message出来了

可以先在cmd配置一下用户名、密码、topic看看能不能接受到java发送的消息

如果可以，就可以进行建库操作然后进行后端编写了，如果没有mysql赶紧下一个
