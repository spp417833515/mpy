import usocket,time
from machine import Timer
'''
-----------------------------------------------------地址簇
usocket.AF_INET             = 2 - TCP / IP - IPv4
usocket.AF_INET6            = 10 - TCP / IP - IPv6
-----------------------------------------------------套接字类型
usocket.SOCK_STREAM         = 1 - TCP流
usocket.SOCK_DGRAM          = 2 - UDP数据报
usocket.SOCK_RAW            = 3 - 原始套接字
usocket.SO_REUSEADDR        = 4 - socket可重用
-----------------------------------------------------套接字选项级别
usocket.SOL_SOCKET = 4095
-----------------------------------------------------函数
'''
#设置连接属性

def tlc_msg(msg):
    print(msg)
    
while True:
    try:
        print('start...')
        s = usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
        s.connect(("10.0.0.81",6000))                         #连接服务器
        print('>'*30,s)
        s.send("micropython")                                  #向服务器传输信息
        while True:
            data=s.recv(1024)
            if data:
                tlc_msg(data)
            else:
                print('TLC over!')
                break;
    except:
        print('TCL ing.....')
        time.sleep(5)