import network,usocket,time,machine,ure
from machine import Timer
from machine import Pin,PWM
from dht import DHT11
#----------------------------------------------------------全局变量>>上传数据使用
wd=0                 #温度数据
sd=0                 #湿度数据
TLC=0                #连接状态 0未连接 1已连接
timer_1=0            #定时器1状态
timer_2=0            #定时器2状态
timer_3=0            #定时器2状态
jdq1=0               #继电器1
jdq2=0               #继电器2
hw = 0               #红外模块当前状态
djjd = 10            #舵机当前角度
cm1=0                #触摸按钮1    0未按下 1按下
cm2=0                #触摸按钮2

#----------------------------------------------------------针脚初始化
PWM(Pin(2),freq=0,duty=700)     #TCP连接灯 闪光未未连接
led = Pin(16, Pin.OUT, value=1) #主板LED灯
tcpled=Pin(2, Pin.OUT, value=1) #ESP8266 WIFI芯片LED灯
cm_1=Pin(15,Pin.IN)
cm_2=Pin(16,Pin.IN)
led2 = Pin(4, Pin.OUT, value=0) #LED针脚2  (D4) 初始化为输出模式 默认输出 0 低电平
jdq1_pin=Pin(4,Pin.OUT,value=1)
jdq2_pin=Pin(13,Pin.OUT,value=1)
p5  = Pin(14,Pin.IN)           #红外针脚14(D5) 初始化为输入模式
dht11_wsd=DHT11(Pin(5))        #HDT 传感器针脚
#----------------------------------------------------------连接WIFI
def wifi_main():
    wifi=network.WLAN(network.STA_IF)        #WIFI模式
    if not wifi.isconnected():
        print('wifi  ing......')
        wifi.active(True)
        wifi.connect('ioT2.4G','407440523')  #连接WIFI
        while not wifi.isconnected():
            pass
    print('wifi   ok......')
wifi_main()
#----------------------------------------------------------正则命令数据分离 失败返回0
def zz(xx,str):
    nn =ure.match("(%s)(\d+)+"%xx, str)
    if nn:
        return int(nn.group(2))
    else:
        return 0
#----------------------------------------------------------触摸按钮
def cman(f):
    global cm1,cm2,cm_1,cm_2
    print('cm_1.value()',cm_1.value())
    print('cm_2.value()',cm_2.value())
    if cm_1.value()==1 and cm1==0:
        cm1=1
        print('cm1111   _________')
        #执行按钮1按下命令
    elif cm_1.value()==0 and cm1==1:
        cm1=0
    
    if cm_2.value()==1 and cm2==1:
        cm2=1
        print('cm2222   _________')
        #执行按钮2按下命令
    elif cm_2.value()==0 and  cm2==1:
        cm2=0
    

jk_cman=Timer(1)
jk_cman.init(period=500,mode=Timer.PERIODIC,callback=cman)
#----------------------------------------------------------传感器系列  --定时获取数据
def dht11_gx(f):
    global wd,sd
    dht11_wsd.measure()  #调用DHT类库中测量数据的函数 
    wd = str(dht11_wsd.temperature())#读取measure()函数中的温度数据
    sd = str(dht11_wsd.humidity())  #读取measure()函数中的湿度数据
    #------------------# 判断红外信号
    if p5.value():     #
        hw=1           #
    #------------------#
timer_dht11=Timer(2)
timer_dht11.init(period=2000, mode=Timer.PERIODIC, callback=dht11_gx)

    

#----------------------------------------------------------主动控制模块
#---------------[舵机控制]
def djkz(_jd):
    global dqjd
    jd=int(_jd)
    djkz=jd
    if jd<10:
        jd=10
    elif jd>50:
        jd=50
    PWM(Pin(12),freq=20,duty=jd)

#----------------------------------------------------------定时器变量

#----------------------------------------------------------定时上传数据
s = usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
def tlc_up(f): 
    global TLC,s,wd,sd,jdq1,jdq2,hw,djjd
    if TLC==1:
        try:
          s.send('wd%d>sd%d>jdq1%d>jdq2%d>sw%d>djjd%d>'%(int(wd),int(sd),jdq1,jdq2,hw,djjd))
        except:
          pass
  
timer_up=Timer(3)
timer_up.init(period=10000,mode=Timer.PERIODIC,callback=tlc_up)
def upmsg(str='sc'):
    global TLC,s,wd,sd,jdq1,jdq2,hw,djjd
    if TLC==1:
        try:
            if str=='sc':
                s.send('wd%d>sd%d>jdq1%d>jdq2%d>sw%d>djjd%d>'%(int(wd),int(sd),jdq1,jdq2,hw,djjd))
            else:
                s.send(str)
        except:
          pass
#----------------------------------------------------------TCL直连
def tlc_msg(msg):
    global wd,sd,led1,jdq1,jdq2,hw,djjd,led,timer_1
    if msg==b"pass":
        pass
    elif msg==b"pass":
       pass
    elif msg==b"jdq1k":
        jdq1_pin.value(0)
        jdq1=1
        upmsg()
    elif msg==b'jdq1g':
        jdq1_pin.value(1)
        jdq1=0
        upmsg()
    elif msg==b'jdq2k':
        jdq2_pin.value(0)
        jdq2=1
        upmsg()
    elif msg==b'jdq2g':
        jdq2=0
        jdq2_pin.value(1)
        upmsg()
    elif zz('djjd',msg)!=0:
        djjd=zz('djjd',msg)
        djkz(djjd)
        upmsg()
    print(msg)

while True:
    try:
        print('start...')
        s = usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
        s.connect(("10.0.0.81",6000))                         #连接服务器
        print('>'*30,s)
        s.send("%1%1")                                  #向服务器传输信息
        s.send('wd%d>sd%d>jdq1%d>jdq2%d>sw%d>djjd%d>'%(int(wd),int(sd),jdq1,jdq2,hw,djjd))
        PWM(Pin(2),freq=1000,duty=1023) #关闭主板LED
        TLC=1
        while True:
            try:
                data=s.recv(1024)
                if data:
                    tlc_msg(data)
                else:
                    TLC=0
                    print('TCP over!')
                    PWM(Pin(2),freq=0,duty=700)     #闪烁主板LED
                    break;
            except:
                print('TCP  except over !')
                TLC=0
                PWM(Pin(2),freq=0,duty=700)     #闪烁主板LED
    except:
        print('TCP ing.....')
        time.sleep(5)






















