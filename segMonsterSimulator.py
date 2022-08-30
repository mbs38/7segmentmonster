#!/usr/bin/env python3

if __name__ == "__main__":
   print("Just don't.")


def digitToMatrix(data, outdata, line, col):
    line-=1
    col-=1
    lineOffset=line*3
    coloffset=col*4
    
    if data[0]>0:
        outdata[coloffset+1+lineOffset*121]="_"
    if data[5]>0:
        outdata[coloffset+0+lineOffset*121+121]="|"
    if data[6]>0:
        outdata[coloffset+1+lineOffset*121+121]="_"
    if data[1]>0:
        outdata[coloffset+2+lineOffset*121+121]="|"
    if data[4]>0:
        outdata[coloffset+0+lineOffset*121+2*121]="|"
    if data[3]>0:
        outdata[coloffset+1+lineOffset*121+2*121]="_"
    if data[2]>0:
        outdata[coloffset+2+lineOffset*121+2*121]="|"
    if data[7]>0:
        outdata[coloffset+3+lineOffset*121+2*121]="."
    
    return outdata

def sendData(data):
    if len(data)!=(1152):
        print("Error input data length ist not 1152! (meaning: you f***ed up!)")
        return
    # create empty matrix
    outData=[]
    for y in range(0,18):
        for x in range(0,120):
            outData.append(" ")
        outData.append("\n")

    # rearrange data just like in the actual display matrix
    subdivision=3
    col=6
    line=6
    
    for x in range(0, int(len(data)/8)):
        outData=digitToMatrix(data[(0+8*x):(8+8*x)],outData,line,col+subdivision*6)  
        col-=1
        if col==0:
            col=6
            line-=1
            if line==0:
                line=6
                subdivision-=1
                  
    # finally print
    outstr=""
    for x in outData:
        outstr+=x
    
    print(outstr)
