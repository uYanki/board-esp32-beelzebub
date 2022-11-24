## MQTT（网络通信协议）

每个客户端都可通过订阅主题以接收数据，也可以向指定主题发布消息。

每条消息有主题 topic 和 消息内容 data 组成。

收发流程：客户端向服务端的某主题发送消息，然后服务器向订阅了该主题的所有客户端转发该消息。

## EMQX（MQTT 服务器）

在 https://www.emqx.io/zh/downloads 下载压缩包，并进行解压。

![01](image\01.png)

然后进入`bin`目录，并使用命令行运行`emqx start`命令，以启动EMQX。

![02](image\02.png)

浏览器访问 http://localhost:18083/，看到以下界面则表示本地 MQTT 服务器搭建成功。

![03](image\03.png)

进行登录（默认账号`admin`，密码`public `）：

![02](image\02.png)

## MQTT X（MQTT客户端）

在 https://mqttx.app/zh 下载并安装程序。

命令行查看本机 IP：`ipconfig`

![04](image\04.png)

运行 MQTTX 创建链接。

![05](image\05.png) ![06](image\06.png)

![07](image\07.png)

在 http://localhost:18083/#/connections 中查看连接状态： ![08](image\08.png)

向主题发送消息：

![09](image\09.png)