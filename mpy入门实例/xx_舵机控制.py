from machine import Pin,PWM
#D6   12




dqjd=10

def djkz(_jd):
    global dqjd
    jd=int(_jd)
    djkz=jd
    if jd<10:
        jd=10
    elif jd>50:
        jd=50
    PWM(Pin(12),freq=20,duty=jd)      #频率20赫兹    占空比: 10-50 (角度调整)


PWM(Pin(12),freq=1000,duty=1000) 