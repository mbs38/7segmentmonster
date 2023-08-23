import segMonster
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('filename')           # positional argument
parser.add_argument('-c', '--count')  
args = parser.parse_args()

segMonster.initSock("172.29.110.211",7536)
#segMonster.initSock("10.24.100.81",7536)

count=1
if args.count:
    count = int(args.count)
segMonster.playFile(args.filename,count)
