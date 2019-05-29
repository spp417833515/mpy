import usocket,time,ure
from machine import Pin,PWM
#D6   12


str="wd50>sd20>kqq10>dd50"
#texts=ure.match("(.*?)(\d+)>","wd50>sd20>kqq10>dd50")
#print(texts.start)
#
def zz(xx,str):
    print(str)
    nn =ure.match("(%s)(\d+)+"%xx, str)
    if nn:
        return nn.group(2)
    else:
        return 0
print(zz('wdx','wd50'))
