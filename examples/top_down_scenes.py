import time
import pyRetroGame
from pyRetroGame.mathematics.vector import Vector2
from pyRetroGame.assets import *

# Define all the game objects
class Background:
    def __str__(self): return TextAssets.FilledBlock

class Player(pyRetroGame.objects.gameEntity):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return TextAssets.BlankSpace

class Door(pyRetroGame.objects.gameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.solid = True

    def __str__(self):
        return TextAssets.BlankSpace

class Door(pyRetroGame.objects.gameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.solid = True

    def __str__(self):
        return TextAssets.BlankSpace

class EmojiBlock(pyRetroGame.objects.gameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.solid = True

    def __str__(self):
        return TextAssets.BlankSpace

game = pyRetroGame.game.Game(background=Background, size = Vector2(30, 15))
player = Player(
    Vector2(0, 0),
    game
)
door = Door(position=Vector2(10, 10)) # It speaks for itself

scene1 = [
    player,
    door
]

scene2 = [
    player,
    emoji1 := EmojiBlock(position=Vector2(5, 5)),
    emoji2 := EmojiBlock(position=Vector2(8, 5)),
    emoji3 := EmojiBlock(position=Vector2(5, 7)),
    emoji4 := EmojiBlock(position=Vector2(6, 7)),
    emoji5 := EmojiBlock(position=Vector2(7, 7)),
    emoji6 := EmojiBlock(position=Vector2(8, 7)),
]

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
    
    player.move(direction)

@game.inputHandler('q')
def quit():
    game.quit()

@player.collisionHandler(door)
def onPlayerCollision():
    game.despawnAll()
    game.spawn(scene2)
    game.printAnimatedText("Congratulations, you have found the door!", timeout=3)
    time.sleep(1)
    game.printAnimatedText("Now you are in the.. emoji scene...", timeout=4)
    time.sleep(2)
    game.printAnimatedText("There's nothing to do here..", timeout=4)

@player.collisionHandler([emoji1, emoji2, emoji3, emoji4, emoji5, emoji6])
def onPlayerCollisionsWithEmoji():
    game.printAnimatedText('Ehy, don\'t touch the emoji!', timeout=3)


game.spawn(scene1)
game.start(fps = 60) # The argument fps is optional, it defaults to 60, and it defines the max refresh rate of the game.