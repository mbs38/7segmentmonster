#!/usr/bin/env python3

from argparse import ArgumentParser
import socket
import time
import curses


def digitToMatrix(data, outdata, line, col):
    line-=1
    col-=1
    lineOffset=line*3
    coloffset=col*4
    
    if data[0]>0:
        outdata[coloffset+1+lineOffset*97]="_"
    if data[5]>0:
        outdata[coloffset+0+lineOffset*97+97]="|"
    if data[6]>0:
        outdata[coloffset+1+lineOffset*97+97]="_"
    if data[1]>0:
        outdata[coloffset+2+lineOffset*97+97]="|"
    if data[4]>0:
        outdata[coloffset+0+lineOffset*97+2*97]="|"
    if data[3]>0:
        outdata[coloffset+1+lineOffset*97+2*97]="_"
    if data[2]>0:
        outdata[coloffset+2+lineOffset*97+2*97]="|"
    if data[7]>0:
        outdata[coloffset+3+lineOffset*97+2*97]="."
    
    return outdata

def sendData(data, scr=None):
    if len(data)!=(1152):
        print("Error input data length ist not 1152! (meaning: you f***ed up!)")
        return
    # create empty matrix
    outData=[]
    for y in range(0,18):
        for x in range(0,96):
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
    
    if scr:
        scr.addstr(0,0,outstr)
        scr.refresh()
    else:
        print(outstr)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
            '--listen-port', '-l',
            required=True,
            type=int,
            help="Port to listen for UDP data packets.",
            )

    parser.add_argument(
            '--bind-address', '-b',
            required=False,
            type=str,
            default="0.0.0.0",
            help="Address to listen on for UPD data packets.",
            )

    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.bind_address, args.listen_port))

    data_length = 1+(144*8)

    scr = curses.initscr()

    init_data = b''
    for _ in range(0,144*8):
        init_data = init_data + b'\xff'

    sendData(init_data, scr)

    try:
        while True:
            data, address = sock.recvfrom(data_length)
            if data[0] != 0x44:
                print(data[0])
                print("ignored Packet")
            else:
                sendData(data[1:], scr)
    except KeyboardInterrupt:
        curses.endwin()
        print('Bye')
