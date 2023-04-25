import segMonster
import segMonsterSimulator
import segMonsterText
import time


segMonster.initSock("10.24.200.22",7536) # set target display ip and port

textline=segMonsterText.textLine("Text",[3,0],0)
textlineU=segMonsterText.textLine("A much longer text.",[0,3],63)

for x in range(0,100000):
    time.sleep(0.155)
    matrix=segMonster.createDigitMatrix() # create new empty matrix of digits
    matrix=textline.pasteCurrent(matrix) 
    matrix=textlineU.pasteCurrent(matrix)
    rawdata=segMonster.convertToDispLayout(matrix) # convert matrix of digits to display data format
    segMonster.sendData(rawdata) # send to display
    segMonsterSimulator.sendData(rawdata) # send to display simulation
