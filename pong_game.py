import segMonster
import segMonsterSimulator
import time

class Game: # for change of speed increase Frame Rate
    def __init__(self):
        self.pos_1 = 0
        self.pos_2 = 0
        self.padel_len = 2
        self.last_pos_1 = 0
        self.last_pos_2 = 0

        self.height = 12
        self.width  = 24

        self.ball_position = [int(self.width/2),int(self.height/2)]
        self.ball_speed    = [1,1]

    def reset(self):
        self.__init__()

    def update(self):
        self.ball_position[0] += self.ball_speed[0]
        self.ball_position[1] += self.ball_speed[1]

        if not (0 <= self.ball_position[1] < self.height):
            self.ball_speed[1] = -self.ball_speed[1]
            self.ball_position[1] = self.height-1 if self.ball_position[1] >= self.height else 0
            self.update()

        if not (0 < self.ball_position[0] < self.width-1):
            if self.ball_position[1] in [(self.pos_1+i if self.ball_position[0] <= 0 else self.pos_2+i) for i in range(self.padel_len-1)]:
                self.ball_speed[0] = -self.ball_speed[0]
                self.ball_speed[1] += self.last_pos_1 - self.pos_1 if self.ball_position[0] <= 0 else self.last_pos_2 - self.pos_2

                self.ball_position[0] = 1 if self.ball_position[0] <= 0 else self.width-2
                self.update()
            else:
                self.reset()

        self.last_pos_1 = self.pos_1
        self.last_pos_2 = self.pos_2

    def draw_paddel(self, mat, x, y):
        for i in range(self.padel_len):
            mat[int((y+i)/2)][x][5-(y+i)%2] = 1

    def state_to_monster(self):
        mat = segMonster.createDigitMatrix()
        self.draw_paddel(mat, 0, self.pos_1)
        self.draw_paddel(mat, self.width-1, self.pos_2)
        mat[int(self.ball_position[1]/2)][self.ball_position[0]] = [0,0,1,1,1,0,1,0] if self.ball_position[1]%2 else [1,1,0,0,0,1,1,0]
        return mat
if __name__ == "__main__":
    FPS = 10
    game = Game()
    segMonster.initSock("10.24.200.22",7536) # set target display ip and port
    while True:
        game.update()
        time.sleep(FPS/60)
        rawdata = segMonster.convertToDispLayout(game.state_to_monster())
        segMonster.sendData(rawdata) # send to display
        segMonsterSimulator.sendData(rawdata) # send to display simulation
        FPS += 0.001 # exponential growth
