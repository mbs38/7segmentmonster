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

# convert rawdata with display data structure back to a matrix
def rawdataToMatrix(matrix,rawdata):
    digcount=0
    for subdiv in range(3,-1,-1):
        for row in range(5,-1,-1):
            for dig in range(5,-1,-1):
                for seg in range(8):
                    matrix[row][subdiv*6+dig]=rawdata[(0+8*digcount):(8+8*digcount)]
                digcount+=1
    return matrix

# erzeuge matrix wie oben jedoch mit positionen der mittelpunkte der segmente bezogen auf
# ein bild mit 3166 x 1068 pixeln
def createCenterPosMatrix():
    xdifrow=32
    ydifrow=184
    xdifcol=126
    posmatrix = [[[[0,0] for s in range(8)] for x in range(24)] for y in range(6)]
    for y in range(6):
        for x in range(24): # [y,x] in 1068 by 3166
            posmatrix[y][x][0] = [7+ydifrow*y,  226+xdifcol*x-y*xdifrow]  # a
            posmatrix[y][x][1] = [40+ydifrow*y, 251+xdifcol*x-y*xdifrow] # b
            posmatrix[y][x][2] = [110+ydifrow*y,239+xdifcol*x-y*xdifrow] # c
            posmatrix[y][x][3] = [141+ydifrow*y,203+xdifcol*x-y*xdifrow] # d
            posmatrix[y][x][4] = [108+ydifrow*y,169+xdifcol*x-y*xdifrow] # e
            posmatrix[y][x][5] = [36+ydifrow*y,183+xdifcol*x-y*xdifrow] # f
            posmatrix[y][x][6] = [74+ydifrow*y,200+xdifcol*x-y*xdifrow] # g
            posmatrix[y][x][7] = [141+ydifrow*y,257+xdifcol*x-y*xdifrow] # dp
    return posmatrix

posmatrix=createCenterPosMatrix()

## betrachtet nur die Position, an der der Mittelpunkt eines jeden Segmentes liegt.
def maskToDigitMatrix(pix,matrix):
    posmatrix=createCenterPosMatrix()
    for y in range(6):
        for x in range(24):
            for s in range(8):
                if pix[posmatrix[y][x][s][0]][posmatrix[y][x][s][1]]>0:
                    matrix[y][x][s]=pix[posmatrix[y][x][s][0]][posmatrix[y][x][s][1]]
    return matrix

# legacy compatibility wrapper with sane values
def pixelsToDigitMatrix(pix,matrix):
    return pixelsToDigitMatrixParametric(pix,matrix,10,1)

# assume grid of digits and map 32 row of 96 pixels to it
def pixelsToDigitMatrixParametric(pix,matrix,threshold,contrast):
    for x in range(96):
        digx=int(x/4)
        xindig=x-digx*4
        for y in range(36):
            digy=int(y/6)
            yindig=y-digy*6
            posindig=(xindig,yindig)
            if pix[y][x]>threshold:
                val=pix[y][x]
                if contrast>0:
                    val=val*contrast
                if val>63:
                    val=63
                if posindig in [(0,0),(1,0),(2,0),(3,0)]: # a
                    matrix[digy][digx][0]=val
                if posindig in [(3,0),(3,1),(3,2),(2,1),(2,2)]: # b
                    matrix[digy][digx][1]=val
                if posindig in [(2,4),(3,3),(2,3),(3,4),(3,5)]: # c
                    matrix[digy][digx][2]=val
                if posindig in [(0,5),(1,5),(2,5),(3,5)]: # d
                    matrix[digy][digx][3]=val
                if posindig in [(0,5),(0,4),(0,3),(1,3),(1,4)]: # e
                    matrix[digy][digx][4]=val
                if posindig in [(0,1),(0,2),(0,0),(1,1),(1,2)]: # f
                    matrix[digy][digx][5]=val
                if posindig in [(2,2),(2,3),(1,2),(1,3)]: # g
                    matrix[digy][digx][6]=val
                if posindig in [(3,5)]: # DP
                    matrix[digy][digx][7]=val
    return matrix

# talk to actual display
sock = None
UDP_IP = None
UDP_PORT = None

def initSock(IP,port):
    global UDP_IP
    UDP_IP=IP
    global UDP_PORT
    UDP_PORT=port
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

gammaTable=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 34, 35, 37, 38, 40, 41, 43, 45, 46, 48, 50, 52, 53, 55, 57, 59, 61, 63]

def sendData(rawdata):
    global sock
    digSum=0
    outdata=[]
    for x in rawdata:
        digSum+=x
    for pos in rawdata:
        outdata.append(gammaTable[int(pos)])
    MESSAGE=b"D"+bytes(outdata)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

# safe to 7sg files and read from 7sg files
filename=""
f=None

def openFile(filename):
    global f
    f = open(filename, "wb")

def sendToFile(rawdata,delay):
    chunk=delay.to_bytes(2, 'big')+bytes(rawdata)
    f.write(chunk)

def closeFile():
    global f
    f.close()

def playFile(filename,repeat):
    import segMonsterSimulator
    import time
    f = open(filename, 'rb')
    for t in range(repeat):
        f.seek(0)
        while(True):
            content = f.read(1154)
            if not content:
                break
            #sendData(content[2:])
            #segMonsterSimulator.sendData(content[2:]) # send to display simulation
            sendData(content[2:]) # send to display simulation
            time.sleep(int.from_bytes(content[0:2], 'big')*0.001)
    f.close()
