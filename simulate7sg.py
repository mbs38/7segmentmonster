import segMonster
import segMonsterSimulatorGui3
import segMonsterSimulator
import threading
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument('filename')           # positional argument
parser.add_argument('-c', '--count')  
args = parser.parse_args()


repeat=1
if args.count:
    repeat = int(args.count)

filename=args.filename
f=None

f = open(filename, 'rb')

for t in range(repeat):
    f.seek(0)
    while(True):
        content = f.read(1154)
        if not content:
            break
        rawdata=content[2:]
        segMonsterSimulator.sendData(rawdata) # send to display simulation
        time.sleep(int.from_bytes(content[0:2], 'big')*0.001)
f.close()
