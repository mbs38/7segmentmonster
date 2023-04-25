import segMonster
import segMonsterSimulator
import threading
import time

class textLine():
    alphabet={
            '.': [["","",""],["gcde","",""]],
            '0': [["aef","abc",""],["def","bcd",""]],
            '1': [["","fe",""],["","fe",""]],
            '2': [["fa","abcd",""],["afed","d",""]],
            '3': [["a","abcd",""],["d","abcd",""]],
            '4': [["def","bcd",""],["","bc",""]],
            '5': [["afed","a",""],["d","abcd",""]],
            '6': [["afe","a",""],["afed","abcd",""]],
            '7': [["a","abc",""],["","bc",""]],
            '8': [["adef","abcd",""],["adef","abcd",""]],
            '9': [["afed","abcd",""],["d","bcd",""]],
            ':': [["b","f",""],["c","e",""]],
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
            'I': [["bc","fe",""],["bc","fe",""]],
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
            '}': [["","",""],["","",""]]
    }

    segmentMap={
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'dp': 7
    }

    def __init__(self,text,origin,brightness):
        if brightness>63 or brightness<1:
            brightness=63
        self.brightness=brightness
        self.origin=origin # top left corner
        self.text=text.upper()
        self.pos=0
        if len(text)>8: # no scrolling 
            self.text="        "+self.text+"        "
        self.scrollMatrix=[[[0 for s in range(8)] for x in range(3*len(self.text))] for y in range(2)]
        self.setText(self.scrollMatrix,self.text)

    def setText(self,matrix,text):
        for x in range(0,len(text)):
            self.setChar(matrix,text[x],x,0)
    
    def scrollText(self,matrix,pos):
        for x in range(0,24):
            for y in range(0,2):
                if (x+self.origin[0])<24 and (y+self.origin[1])<6 and (x+pos)<len(self.scrollMatrix[0]):
                    matrix[y+self.origin[1]][self.origin[0]+x]=self.scrollMatrix[y][x+pos]
    
    def pasteCurrent(self,matrix):
        if len(self.text)<=8:
            self.scrollText(matrix,0)
        else:
            self.scrollText(matrix,self.pos)
            self.pos+=1
            if self.pos==len(self.text)*3:
                self.pos=0   
        return matrix

        

    def setChar(self,matrix,char,posx,posy):
        ## position range: x: 0 to 8, y:0 to 2a
        try:
            self.alphabet[char]
        except:
            return
        for x in range(0,3):
            for y in range(0,2):
                for bit in range(0, 8):
                    for seg in self.segmentMap:
                        if str(seg) in self.alphabet[char][y][x]:
                            matrix[posy*3+y][posx*3+x][self.segmentMap[seg]]=self.brightness
                    

