import pyRetroGame
from pyRetroGame.mathematics.vector import Vector2
from pyRetroGame.assets import *


# Define all the game objects
class Background:
    def __str__(self): return TextAssets.FilledBlock # White background

class Player(pyRetroGame.objects.gameEntity):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return TextAssets.BlankSpace # Black player


game = pyRetroGame.game.Game(
    background=Background,
    size = Vector2(30, 15) # Size of the game (width, height)
)
player = Player(
    Vector2(0, 0), # Define the initial position of the player
    game           # Pass the game object to the player
)


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

@player.gameLimitCollisionHandler()
def Eiei(side):
    game.printAnimatedText(f'Touched {side}')

game.spawn(player)
game.start(fps = 60, debugging=False)