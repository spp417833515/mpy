#----------------------------------------------------------MQTT服务器连接数据配置
# MQTT服务器地址域名为：183.230.40.39,不变
SERVER = "183.230.40.39"
#设备ID
CLIENT_ID = "527663360"
#随便起个名字
TOPIC = b"ESP826601"
#产品ID
username='244930'
#产品APIKey:
password='faDcKIogViK5EJiWwJpSo1clWAc='
#----------------------------------------------------------MQTT服务器连接程序
def sub_cb(topic,msg):  #MQTT回调数据
    print('>'*50)
    print(topic,msg)

def mqqt_main(server=SERVER):        #初始化MQTT服务器
    c = MQTTClient('设备ID', '服务器地址','端口','产品ID','产品KEY')  #配置连接信息
    c.set_callback(sub_cb)                                           #设置回调函数
    c.connect()                                                      #连接
    print('='*50)
    c.subscribe(TOPIC)
    print('='*50)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))
    #publish报文上传数据点
    #c.publish('$dp',pubdata(message))
    while True:
        if True:
            c.wait_msg()
        else:
            c.check_msg()
            time.sleep(1)
    c.disconnect()


mqqt_main()
