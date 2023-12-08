from machine import UART,Pin
import sys
import time

rxData=bytes()
txData0= str()
txData1= str()
result=str()
strCommand =str()
strDigiR = str()
strDigiL = str()

BrightSet =int()
SelectedMeasure = int()

'''エラー処理'''
def DataProcessing():
    result=""
    BrightDat=""
    rxData=0

    #uart1.write(txData1)
    
    while result is not '\r':
        rxData = uart1.read(1)
        if rxData is not None:
            result = rxData.decode('utf-8')
            BrightDat += result
            print(str(result))

    uart0.write(BrightDat + '\r')
    print(BrightDat + '\r\n')

    
'''シリアル通信設定'''
uart0 = UART(0,115200,tx=Pin(12),rx=Pin(13))
uart0.init(115200, bits=8, parity=None, stop=1) 
txData0='Ver.2.0 SystemStartUp\r\n'
#print(txData0)
uart0.write(txData0)
print(txData0)

uart1 = UART(1,9600,tx=Pin(4),rx=Pin(5))
uart1.init(9600, bits=8, parity=None, stop=1) 

PICOLED = Pin(25,Pin.OUT)
PICOLED.value(1)

while True:
    result=""
    BrightDat=""
    rxData=0

    #while result is not '\n':
    while result is not '\r':
        #rxData = uart0.read(1)
        rxData = uart1.read(1)
        if rxData is not None:
            result = rxData.decode('utf-8')
            BrightDat += result
            #print(str(result))

    length = len(BrightDat)

    print(BrightDat)
    #print('Passing!')

    if BrightDat == 'S1\r':#\n':
        SelectedMeasure = 1
        print('SENDING FROM NOW ON!')
        #DataProcessing()
    elif BrightDat == 'S2\r':#\n':
        SelectedMeasure = 2
        print('SENDING FROM NOW ON!')
        #DataProcessing()
    elif BrightDat[0:2] == 'L1':
         SelectedMeasure = 3
         print(BrightDat[0:2])
    elif BrightDat[0:2] == 'L2':
         SelectedMeasure = 4
         print(BrightDat[0:2])
         
    print("DigiMicroNo."+str(SelectedMeasure))
        
    if length > 5 and SelectedMeasure == 1:
        '''
        #取得データを加工して高さ[um]へ変換
        flotedataR = float(BrightDat[-5:]) * 1000
        DigiR = str(flotedataR)
        print(DigiR)
        txData0=DigiR
        uart0.write("DigiR: " + txData0 + '\r\n')
        '''
        #取得データをそのまま使う
        txData0=BrightDat
        uart0.write('R' + txData0 + '\r\n')
    elif length > 5 and SelectedMeasure == 2:
        '''#取得データを加工して高さ[um]へ変換
        flotedataL = float(BrightDat[-5:]) * 1000
        DigiL = str(flotedataL)
        print(DigiL)
        txData0=DigiL
        uart0.write("DigiL: " + txData0 + '\r\n')
        '''
        #取得データをそのまま使う
        txData0=BrightDat
        uart0.write('L' + txData0 + '\r\n')
    elif length > 5 and SelectedMeasure == 3:
        '''#取得データを加工して高さ[um]へ変換
        flotedataL = float(BrightDat[-5:]) * 1000
        DigiL = str(flotedataL)
        print(DigiL)
        txData0=DigiL
        uart0.write("DigiL: " + txData0 + '\r\n')
        '''
        #取得データをそのまま使う
        txData0=BrightDat
        uart0.write('L' + txData0 + '\r\n')
    elif length > 5 and SelectedMeasure == 4:
        '''#取得データを加工して高さ[um]へ変換
        flotedataL = float(BrightDat[-5:]) * 1000
        DigiL = str(flotedataL)
        print(DigiL)
        txData0=DigiL
        uart0.write("DigiL: " + txData0 + '\r\n')
        '''
        #取得データをそのまま使う
        txData0=BrightDat
        uart0.write('L' + txData0 + '\r\n')
    


    #time.sleep(0.01) #0.08秒待機'''