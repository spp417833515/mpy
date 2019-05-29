from machine import Timer
from machine import Pin 
import time

led = Pin(2, Pin.OUT, value=0)
led_value = 0
def ledkg(t):
    global led_value
    if led_value==0:
        led_value=1
    else:
        led_value=0
    led.value(led_value)
    print('LED%d'%led_value)
tim=Timer(1)
tim.init(period=2000, mode=Timer.PERIODIC, callback=ledkg)
time.sleep(10)#延迟10秒停用定时器
tim.deinit()
time.sleep(10)#延迟10秒重新配置定时器
tim.init(period=2000, mode=Timer.PERIODIC, callback=ledkg)
'''
tim=Timer(1)使用定时器1创建一个定时器对象
tim.init(period=2000, mode=Timer.PERIODIC, callback=ledkg)
#[period 定时器周期] [mode 定时器循环模式] [callback 定时器调用函数]
            
tim.init()           >>>初始化定时器
tim.callback(fun)    >>>设置定时器触发时所调用的函数。
tim.deinit()         >>>禁用停用定时器
'''
