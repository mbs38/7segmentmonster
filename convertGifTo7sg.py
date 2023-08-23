import segMonster
import segMonsterSimulator
import argparse


from PIL import Image, ImageFont, ImageDraw, ImageChops
import time

parser = argparse.ArgumentParser(prog='convertGif', description='Converts gif files to 7sg files. All resolutions and aspect ratios are accepted. For best results your images shoud have an aspect ratio of 9.6 by 3.6 and they should be grayscale only. DO NOT USE STACKED GIFS! BACKGROUND HAS TO BE PRESENT IN ALL FRAMES!')
parser.add_argument('inputfile')
parser.add_argument('outputfile')
parser.add_argument('-t', '--threshold', help='Threshold at which a pixel is considered to be on')  
parser.add_argument('-b', '--brightness', help='Brightness of each pixel is multiplied by this value (to enhance contrast/brightness)')
parser.add_argument('-i', '--invert', help='We assume a black background. Sometimes it helps to invert the image.')  

args = parser.parse_args()
if args.threshold:
    threshold = int(args.threshold)
else:
    threshold = 0
if args.brightness:
    brightness = int(args.brightness)
else:
    brightness = 1


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
    gifimg  = Image.open(args.inputfile) 

def testpixel_lo(x):
    if x<21:
        return True
    return False

segMonster.openFile(args.outputfile)
loadGIF()
maxframe=getFrameAmount(gifimg)
frame = 0
for t in range(0,maxframe+1):
    pix=segMonster.createPixelMatrix() # create empty matrix of pixels 
    img=gifimg

    if frame>maxframe:
        frame=0
    img.seek(frame)
    
    if args.invert:
        img=ImageChops.invert(img)

    frame+=1

    img=img.resize((96,36))
    print(frame)
    print(maxframe)
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
    matrix=segMonster.pixelsToDigitMatrixParametric(pix,matrix,threshold,brightness)
    rawdata=segMonster.convertToDispLayout(matrix) # convert matrix of digits to display data format
    segMonsterSimulator.sendData(rawdata) # send to display simulation
    print(int(img.info['duration']))
    segMonster.sendToFile(rawdata,int(img.info['duration']))

segMonster.closeFile()
