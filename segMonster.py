import socket

# create empty matrix of seven segment digits
# using a grid starting upper left corner containing one digit per position
def createDigitMatrix():
    return [[[0 for s in range(8)] for x in range(24)] for y in range(6)]

#create matrix of pixels (32 rows with 96 pixels => 96x32) with brightness 0
def createPixelMatrix():
    return [[0 for x in range(96)] for y in range(36)]

#convert matrix of digits to the data structure of the display
# using a grid starting upper left corner containing one digit per position
def convertToDispLayout(matrix):
    out=[]
    for subdiv in range(3,-1,-1):
        for row in range(5,-1,-1):
            for dig in range(5,-1,-1):
                vals=matrix[row][subdiv*6+dig]
                for val in vals:
                    out.append(val)
    return out

# assume grid of digits and map 32 row of 96 pixels to it
def pixelsToDigitMatrix(pix,matrix):
    for x in range(96):
        digx=int(x/4)
        xindig=x-digx*4
        for y in range(36):
            digy=int(y/6)
            yindig=y-digy*6
            posindig=(xindig,yindig)
            if pix[y][x]>0:
                if posindig in [(0,0),(1,0),(2,0),(3,0)]: # a
                    matrix[digy][digx][0]=pix[y][x]
                if posindig in [(3,0),(3,1),(3,2),(2,1),(2,2)]: # b
                    matrix[digy][digx][1]=pix[y][x]
                if posindig in [(2,4),(3,3),(2,3),(3,4),(3,5)]: # c
                    matrix[digy][digx][2]=pix[y][x]
                if posindig in [(0,5),(1,5),(2,5),(3,5)]: # d
                    matrix[digy][digx][3]=pix[y][x]
                if posindig in [(0,5),(0,4),(0,3),(1,3),(1,4)]: # e
                    matrix[digy][digx][4]=pix[y][x]
                if posindig in [(0,1),(0,2),(0,0),(1,1),(1,2)]: # f
                    matrix[digy][digx][5]=pix[y][x]
                if posindig in [(2,2),(2,3),(1,2),(1,3)]: # g
                    matrix[digy][digx][6]=pix[y][x]
                if posindig in [(3,5)]: # DP
                    matrix[digy][digx][7]=pix[y][x]
    return matrix


# talk to actual display
sock = None
UDP_IP = None
UDP_PORT = None
MAX_CURRENT = 9000

def initSock(IP,port):
    global UDP_IP
    UDP_IP=IP
    global UDP_PORT
    UDP_PORT=port
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def sendData(rawdata):
    global sock
    digSum=0
    for x in rawdata:
        digSum+=x
  #  if digSum*20/63>MAX_CURRENT: #warn user that overcurrent protection will be triggered in the display
  #      current=digSum*20/63
  #      print("Overcurrent protection will be triggered! (maximum current is "+str(MAX_CURRENT)+"mA, estimated current for dataset is "+str(int(current))+"mA)")
    MESSAGE=b"D"+bytes(rawdata)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
