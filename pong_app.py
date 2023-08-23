from flask import Flask, render_template, request, jsonify
import pong_game
import segMonster, segMonsterSimulator
import threading, time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    state = app.config['STATE']

    if request.method == 'POST':
        # Get the slider value and radio selection from the form
        if request.form['radio'] == 'L':
            state.set("pos_1", int(request.form['slider']))
        else:
            state.set("pos_2", int(request.form['slider']))
        return jsonify(success=True)

    return render_template('../pong_index.html', slider_value=0, radio_selection='L')

def webserver(state):
    app.config['STATE'] = state
    app.run(host='0.0.0.0', use_reloader=False, debug=True)

def run_game():
    state.set("pos_2", 0)
    state.set("pos_1", 0)
    g = pong_game.Game()
    FPS = 5
    segMonster.initSock("10.24.200.22", 7536)
    while True:
        time.sleep(1/FPS)
        g.pos_1 = state.get("pos_1")
        g.pos_2 = state.get("pos_2")
        g.update()
        rawdata = segMonster.convertToDispLayout(g.state_to_monster())
        segMonster.sendData(rawdata) # send to display
        segMonsterSimulator.sendData(rawdata) # send to display simulation
        #FPS += 0.001 # exponential growth

class SharedState():
    def __init__(self):
        self.lock = threading.Lock()
        self.state = dict()

    def get(self, key):
        with self.lock:
            return self.state.get(key)

    def set(self, key, value):
        with self.lock:
            self.state[key] = value

if __name__ == '__main__':
    state = SharedState()
    web_thread = threading.Thread(target=webserver, args=(state,))
    web_thread.start()
    run_game()
