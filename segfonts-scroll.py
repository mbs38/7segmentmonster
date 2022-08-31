import segMonster
import segMonsterSimulator
import threading

from PIL import Image, ImageFont, ImageDraw 
import time

class textLine():
#    char48=[[[0,0,1,1,0,0,0,1],[0,0,0,0,0,1,1,1],[0,0,0,0,0,0,0,0]],[[0,0,1,1,1,0,0,0],[0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0]]]
    alphabet={
            '0': [["aef","abc",""],["def","bcd",""]],
            '1': [["bc","fe",""],["bc","fe",""]],
            '2': [["fa","abcd",""],["afed","d",""]],
            '3': [["a","abcd",""],["d","abcd",""]],
            '4': [["def","bcd",""],["","bc",""]],
            '5': [["afed","a",""],["d","abcd",""]],
            '6': [["afe","a",""],["afed","abcd",""]],
            '7': [["a","abc",""],["","bc",""]],
            '8': [["adef","abcd",""],["adef","abcd",""]],
            '9': [["afed","abcd",""],["d","bcd",""]],
            ':': [["b","f",""],["c","e",""]],
            '.': [["","",""],["c","e",""]],
            '*': [["","fg",""],["","",""]],
            '!': [["bc","ef",""],["c","e",""]],
            '?': [["af","abcd",""],["bc","",""]],
            '@': [["afec","abce",""],["fedb","bgd",""]],
            'A': [["afed","abcd",""],["afe","abc",""]],
            'B': [["adef","abcd",""],["adef","abcd",""]],
            'C': [["afe","a",""],["fed","d",""]],
            'D': [["aef","abc",""],["def","bcd",""]],
            'E': [["afed","a",""],["afed","d",""]],
            'F': [["afed","a",""],["afe","",""]],
            'G': [["afe","a",""],["fed","abcd",""]],
            'H': [["fed","bcd",""],["afe","abc",""]],
            'I': [["abc","afe",""],["bcd","fed",""]],
            'J': [["","bc",""],["ed","dcb",""]],
            'K': [["fedc","gb",""],["bafe","gc",""]],
            'L': [["fe","",""],["fed","d",""]],
            'M': [["efabc","efabc",""],["fe","bc",""]],
            'N': [["feabc","bc",""],["fe","fedcb",""]],
            'O': [["afe","abgc",""],["fged","dcb",""]],
            'P': [["afed","abcd",""],["fe","",""]],
            'Q': [["afe","abc",""],["fed","edcb",""]],
            'R': [["afed","abcd",""],["afe","afgc",""]],
            'S': [["afed","ab",""],["ed","abcd",""]],
            'T': [["abc","afe",""],["bc","fe",""]],
            'U': [["fe","bc",""],["fed","bcd",""]],
            'V': [["fe","bc",""],["fgc","egb",""]],
            'W': [["fe","bc",""],["fedcb","fedcb",""]],
            'X': [["fgc","egb",""],["egb","fgc",""]],
            'Y': [["fed","dcb",""],["bc","fe",""]],
            'Z': [["a","abge",""],["bged","d",""]],
            '(': [["afe","",""],["fed","",""]],
            ')': [["","abc",""],["","bcd",""]],
            '-': [["d","d",""],["a","a",""]],
            '\\': [["bc","",""],["","fe",""]],
            '=': [["g","g",""],["g","g",""]],
            '/': [["","fe",""],["bc","",""]],
            '{': [["afe","",""],["fed","",""]],
            '}': [["","abc",""],["","bcd",""]],
            '[': [["afe","",""],["fed","",""]],
            ']': [["","abc",""],["","bcd",""]]
    }

    segmentMap={
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'dp': 7
    }

    def __init__(self,text,origin,matrix):
        self.origin=origin # top left corner
        self.text=text
        if len(text)<=8: # no scrolling 
            self.setText(matrix,self.text) 
            #self.setText(text[0:8])
        else:
            self.text="        "+self.text
            self.scrollMatrix=[[[0 for s in range(8)] for x in range(3*len(self.text))] for y in range(2)]
            self.setText(self.scrollMatrix,self.text)
            print(self.scrollMatrix)

    def setText(self,matrix,text):
        print(text)
        for x in range(0,len(text)):
            self.setChar(matrix,text[x],x,0)
    
    def scrollText(self,matrix,pos):
        if len(self.text)<=8:
            return
        for x in range(0,24):
            for y in range(0,2):
                matrix[y][x]=self.scrollMatrix[y][x+pos]


        

    def setChar(self,matrix,char,posx,posy):
        ## position range: x: 0 to 8, y:0 to 2a
        try:
            self.alphabet[char]
        except:
            return
        for x in range(0,3):
            for y in range(0,2):
                for bit in range(0, 8):
                    #self.matrix[posy*3+y][posx*3+x][bit]=self.alphabet[char][y][x][bit]*20
                    for seg in self.segmentMap:
                        if str(seg) in self.alphabet[char][y][x]:
                            matrix[posy*3+y][posx*3+x][self.segmentMap[seg]]=63
                    

segMonster.initSock("172.29.7.102",7536) # set target display ip and port

test="Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
test=test.upper()
text_brightness=63

matrix=segMonster.createDigitMatrix() # create new empty matrix of digits
textline=textLine(test.upper(),[0,0],matrix)
def thread_worker():
    pos=0
    for x in range(0,100000):
        time.sleep(0.055)
        matrix=segMonster.createDigitMatrix() # create new empty matrix of digits
        textline.scrollText(matrix,pos)
        pos+=1
        rawdata=segMonster.convertToDispLayout(matrix) # convert matrix of digits to display data format
        segMonster.sendData(rawdata) # send to display
        segMonsterSimulator.sendData(rawdata) # send to display simulation
        if pos==len(test)*3:
            exit()
    return
    

t = threading.Thread(target=thread_worker)
t.start()
t.join()

