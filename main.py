from machine import UART,Pin
import sys
import time

rxData=bytes()
rxData2=bytes()
result=str()
strCommand =str()
strBrightDat=str()
DatSplit = list()
BrightSet =int()
SaveBrightSetting = int()

'''エラー処理'''
def DataProcessing():
    uart.write(txData)
    rxData=""
    strCommand =""
    strBrightDat=""
    
'''I/O設定'''
DIN = [0,1,2,3,4,5,6,7]
for d in DIN:
    DIN[d] = Pin(d, Pin.OUT)
    DIN[d].value(0)
    
CPIN = Pin(10,Pin.OUT)
CPIN.value(1)

PICOLED = Pin(25,Pin.OUT)
PICOLED.value(1)

SWITCHLED = Pin(18,Pin.OUT)
SWITCHLED.value(0)

'''シリアル通信設定'''
uart = UART(0,115200,tx=Pin(12),rx=Pin(13))
uart.init(115200, bits=8, parity=None, stop=1) 
txData='SystemStartUp\r\n'
uart.write(txData)

e=0
while True:
    result=""
    BrightDat=""

    while result is not '\n':
        rxData = uart.readline()
        if rxData is not None:
            result = rxData.decode('utf-8')
            BrightDat += result 

    DatSplit = BrightDat.split()
    print(DatSplit)
    try:
        count = 0 
        for row in DatSplit:
            row_str = []
            if count == 0:
                strCommand = row
            if count == 1:
                strBrightDat = row
            count += 1
    except:
        txData='NOP\r\n'
        uart.write(txData)
    print(strBrightDat)
    if strCommand == 'CTRLBRIGHT':
        if len(strBrightDat) != 4:
            if strBrightDat == 'ON':
                CPIN.value(1)
                txData='LEDON\r\n'
                DataProcessing()
            elif strBrightDat == 'OFF':
                CPIN.value(0)
                txData='LEDOFF\r\n'
                DataProcessing()
            elif strBrightDat == 'CHK':
                strBrightValue = str(SaveBrightSetting)
                txData= '0' + strBrightValue + '\r\n'
                uart.write(txData)
            else :
                txData='NOP\r\n'
                DataProcessing()
        elif len(strBrightDat) == 4:
            try:
                intBrightDat = int(strBrightDat)
                BinBrightDat =[]
                
                if intBrightDat > 255:
                    intBrightDat = 255
                    strBrightDat = str(intBrightDat)#"0255"
                
                while intBrightDat > 0:
                    if intBrightDat % 2 == 0:
                        intBrightDat = int(intBrightDat / 2)
                        BinBrightDat.append(0)
                    elif intBrightDat % 2 == 1:
                        BinBrightDat.append(intBrightDat % 2)
                        intBrightDat = int(intBrightDat / 2)
                
                BinBrightDat.reverse()
                if len(BinBrightDat) != 8:
                    ElementsNum = 8 - len(BinBrightDat)
                    for i in range(0,ElementsNum):
                        BinBrightDat.insert(0,0)

                CPIN.value(1)
                time.sleep(0.01)
                for j in range(0,8,1):
                    if BinBrightDat[7-j] ==1: 
                        DIN[j].value(1)
                    if BinBrightDat[7-j] ==0: 
                        DIN[j].value(0)
                
                BrightRate =round(float(strBrightDat) / 255 * 100,2)
                SaveBrightSetting = int(strBrightDat)
                print(BrightRate)
                strBrightRate = str(BrightRate)
                txData = strBrightRate + '%\r\n'
                DataProcessing()
            except:
                DataProcessing()
    elif strCommand == 'n':
        CPIN.value(1)
        uart.write('LEDON\r\n')
    elif strCommand == 'f':
        CPIN.value(0) 
        uart.write('LEDOFF\r\n')
    elif strCommand == 'SWITCHLED':
        if strBrightDat == '0': 
            CPIN.value(0)
            txData='LEDOFF\r\n'
            time.sleep(0.5)
            SWITCHLED.value(0) 
            uart.write('VISIBLE-LIGHT_LED\r\n')
        if strBrightDat == '1': 
            CPIN.value(0)
            txData='LEDOFF\r\n'
            time.sleep(0.5)
            SWITCHLED.value(1) 
            uart.write('NIR_LED\r\n')
    elif strCommand != 'CTRLBRIGHT':
        txData='NOP\r\n'
        DataProcessing()

time.sleep(0.08) #0.08秒待機