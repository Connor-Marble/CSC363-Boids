import json
from pythonosc import dispatcher, osc_server
from collections import NamedTuple

from random import random

Player = NamedTuple('Player', 'name color size goal')

DEFAULT_PORT=58274

class GameInstance():
    
    def __init__(self, max_players):
        self.max_players=max_players        
        self.players = []

    def register_display_server(self, addr, data):
        response = json.dumps(data)
        ip = response.ip
        if self.display_ip:
            respond("/Error/ExistingDisplayServer", "There is already a display server connected", ip)

        else:
            self.display_ip=ip
        
    def register_player(self, addr, data):
        response = json.dump(data)
        pass

    def start_session(self):
        self.started = True

    def remove_player(self, addr, playername):
        pass

    def update_parameter(self):
        pass

    def end_game(self):
        pass

def respond(address,value,ip,port=DEFAULT_PORT):
    client = udp_client.SimpleUDPClient(ip, port)
    client.send_message(adress, value)
    

def default_h(addr, value):
    print("[ERROR]Unknown addres:" + addr)
    
def main():
    game = GameInstance(1)
    
    dspt = dispatcher.Dispatcher()

    mappings = {
        "/register_player":game.register_player,
        "/remove_player":game.remove_player,
        "/register_display":game.register_display_server,
        "/start":game.start_session,
        "/update_param/player/*":game.update_parameter
    }

    for k, v in mappings:
        dspt.map(k, v)
    
    dspt.set_default_handler(default_h)
    
    server = osc_server.BlockingOSCUDPServer(('', 5005),dspt)
    server.serve_forever()
    
if __name__=='__main__':
    main()
