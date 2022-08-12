import pyRetroGame
from pyRetroGame.mathematics.vector import Vector2
from pyRetroGame.assets import *

import json
import socket
import threading
import string
import hashlib

def pack(data : dict) -> bytes:
    return json.dumps(data).encode()

def unpack(data : bytes) -> dict:
    return json.loads(data.decode())

# Initialize the connection to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))
initialPacket = unpack(client.recv(1024))

username = ''
skin = ''

while len(username) < 3:
    username = input('Enter your username (min 3 digits): ')

while len(skin) != 1:
    skin = input('Enter your one char skin (allowed: a-z, A-Z, 0-9): ')

client.send(pack({'action': 'IDENTIFY', 'username': username, 'skin': skin}))


serverInformations = unpack(client.recv(1024))
SESSION_ID = serverInformations['session_id']
sessionIDs = serverInformations['session_ids']
PUBLIC_SESSION_ID = hashlib.sha256(SESSION_ID.encode()).hexdigest()

def packet_handler():
    while True:
        packet = unpack(client.recv(1024))
        if packet['session_id'] == PUBLIC_SESSION_ID:
            continue

        if packet['action'] == 'CONNECT':
            entity = Player(Vector2(0, 0), game, skin = packet['skin'])
            sessionIDs[packet['session_id']] = {
                'username': packet['username'],
                'skin': packet['skin'],
                'entity': entity
            }
            game.spawn(entity)
            game.printText(f'{packet["username"]} joined the game!', 4)

        elif packet['action'] == 'DISCONNECT':
            game.printText(f'{sessionIDs[packet["session_id"]]["username"]} left the game.', 4)
            game.despawn(sessionIDs[packet["session_id"]]["entity"])
            del sessionIDs[packet['session_id']]


        elif packet['action'] == 'MOVE':
            sessionIDs[packet['session_id']]['entity'].move(Vector2(*packet['direction']))


# Define all the game objects
class Background:
    def __str__(self): return TextAssets.FilledBlock

class Player(pyRetroGame.objects.gameEntity):
    def __init__(self, *args, skin = TextAssets.BlankSpace):
        super().__init__(*args)
        self.skin = skin

    def __str__(self):
        return self.skin

class Wall(pyRetroGame.objects.gameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.solid = True

    def __str__(self):
        return TextAssets.BlankSpace


game = pyRetroGame.game.Game(background=Background, size = Vector2(30, 15))
player = Player(Vector2(0, 0), game, skin = skin)

#Movement
@game.inputHandler(['w', 'a', 's', 'd'])
def movement(key):
    direction = Vector2(0, 0)
    if key == 'w':
        direction.y -= 1
    if key == 's':
        direction.y += 1
    if key == 'a':
        direction.x -= 1
    if key == 'd':
        direction.x += 1
    player.move(direction) # Move the player at X: playerPosition.x + direction.x; Y: playerPosition.y + direction.y
    client.send(pack({'action': 'MOVE', 'direction': direction.__list__(), 'pos': player.position.__list__(), 'session_id': SESSION_ID}))

@game.inputHandler('q')
def quit():
    game.quit()


game.spawn(player)
for onlinePlayer in sessionIDs:
    entity = Player(Vector2(*sessionIDs[onlinePlayer]['pos']), game, skin = sessionIDs[onlinePlayer]['skin'])
    sessionIDs[onlinePlayer]['entity'] = entity
    game.spawn(entity)

threading.Thread(target=packet_handler).start()
game.start(fps = 60) # The argument fps is optional, it defaults to 60, and it defines the max refresh rate of the game.