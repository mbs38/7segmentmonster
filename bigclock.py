import segMonster
import segMonsterSimulator
import threading

from PIL import Image, ImageFont, ImageDraw 
import time

# some helper functions
def setTextCapsLgse(text):
    text=text.upper()
    my_image = Image.new('RGB', (760,180), color='white')
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 255)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((0,-40), text, (0, 0, 0), font=title_font)
    return my_image.resize((96,36))




def setText(text):
    my_image = Image.new('RGB', (480,180), color='white')
    title_font = ImageFont.truetype("Pillow/Tests/fonts/NotoSans-Regular.ttf", 400)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((0,-40), text, (0, 0, 0), font=title_font)
    return my_image.resize((96,36))

def testpixel_lo(x):
    if x[len(x)-1]<100:
        return True
    return False


def drawRect(segmatrix, pos_x, pos_y, sz_x, sz_y, brightness=32):
    for x in range(pos_x,pos_x+sz_x): # draw top and bot
        if x > 95:
            pass
        else:
            segmatrix[pos_y][x]=brightness
        
        if x > 95 or (pos_y+sz_y)>35:
            pass
        else:
            segmatrix[pos_y+sz_y][x]=brightness

    for y in range(pos_y,pos_y+sz_y): # draw left and right side
        if y < 36 and pos_x<96:
            segmatrix[y][pos_x]=brightness
            if (pos_x+sz_x)<96:
                segmatrix[y][pos_x+sz_x]=brightness
    return segmatrix




segMonster.initSock("172.29.7.102",7536) # set target display ip and port

text_brightness=63



def thread_worker():
    from datetime import datetime
    someInt=0
    for u in range(0,9999):
        x=0      
        someInt+=1
        if someInt==60:
            someInt=0
        matrix=segMonster.createDigitMatrix() # create new empty matrix of digits
        test=str(someInt)
        test=str(someInt)+":"+str(someInt)
        now = datetime.now()
        test = now.strftime("%H:%M")
        img=setTextCapsLgse(test[x:x+7]) # create image containing text
        img_pix=img.load() # load pixels of image
        pix=segMonster.createPixelMatrix() # create empty matrix of pixels 
    
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if testpixel_lo(img_pix[x,y]): # parse pixels to see if they are black
                    pix[y][x]=text_brightness
    
        matrix=segMonster.pixelsToDigitMatrix(pix, matrix) # convert matrix of pixels to a matrix of digits
        rawdata=segMonster.convertToDispLayout(matrix) # convert matrix of digits to display data format
        segMonster.sendData(rawdata) # send to display
        segMonsterSimulator.sendData(rawdata) # send to display simulation     
        time.sleep(0.1)
    return   
    

t = threading.Thread(target=thread_worker)
t.start()
t.join()

