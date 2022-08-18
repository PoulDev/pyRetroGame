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

class Wall(pyRetroGame.objects.gameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.solid = True

    def __str__(self):
        return TextAssets.BlankSpace


game = pyRetroGame.game.Game(background=Background, size = Vector2(30, 15))
player = Player(
    Vector2(0, 0), # Define the initial position of the player
    game           # Pass the game object to the player
)
wall = Wall(position=Vector2(10, 10)) # It speaks for itself

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

@game.inputHandler('q')
def quit():
    game.quit()

@player.collisionHandler(wall)
def onPlayerCollision():
    game.printAnimatedText(f'Welcome to PyRetroGame!') # Print a message that has a duration of 2 seconds

"""
    NOTE: according to the order in which spawning objects will also be handled the Z Index
    for example:
        if your code is:
            game.spawn(wall)
            game.spawn(player)
        Z Index will be:
            wall -> 0
            player -> 1
        The wall will be on top of the player
"""
game.spawn(wall)
game.spawn(player)

game.start(fps = 60) # The argument fps is optional, it defaults to 60, and it defines the max refresh rate of the game.
