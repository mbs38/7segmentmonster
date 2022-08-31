import segMonster
import segMonsterSimulator
import threading

from PIL import Image, ImageFont, ImageDraw 
import time

gifimg = None

def getFrameAmount(image):
    maxframe=0
    while(1):
        try:
            image.seek(maxframe)
            maxframe+=1
        except:
            maxframe-=1
            break
    return maxframe

def getRange():
    pass

def loadGIF():
    global gifimg
    gifimg  = Image.open("test.gif") 

def getFrame(step):
    global gifimg
    gifimg.seek(step)
    return gifimg.resize((96,36))
##

def testpixel_lo(x):
    if x<21:
        return True
    return False

segMonster.initSock("172.29.7.101",7536) # set target display ip and port

text_brightness=13

def thread_worker():
    loadGIF()
    maxframe=getFrameAmount(gifimg)
    frame = 0
    for y in range(0,10000):
        pix=segMonster.createPixelMatrix() # create empty matrix of pixels 
        img=gifimg
        
        frame+=1
        if frame>maxframe:
            frame=0
        gifimg.seek(frame)

        img=img.resize((96,36))
        print(frame)
        img=img.convert("L")
        img_pix=img.load() # load pixels of image
        for x in range(img.size[0]):
            for y in range(img.size[1]):

                tmp=img_pix[x,y]
                tmp=tmp/4
                if tmp>63:
                    tmp = 63
                if tmp<4:
                    tmp=0
                pix[y][x]=int(tmp)
     
        matrix=segMonster.createDigitMatrix() # create new empty matrix of digits
        matrix=segMonster.pixelsToDigitMatrix(pix,matrix)
        rawdata=segMonster.convertToDispLayout(matrix) # convert matrix of digits to display data format
        segMonster.sendData(rawdata) # send to display
        segMonsterSimulator.sendData(rawdata) # send to display simulation
        time.sleep(img.info['duration']*0.001)


    return   
    

t = threading.Thread(target=thread_worker)
t.start()
t.join()
