import string
from turtle import position
from .mathematics.vector import Vector2
import threading

class gameObject:
    def __init__(self, position : Vector2,  game : bool = True, solid : bool = True):
        self.position = position
        self.game = game
        self.solid = solid
        

        self.collisionHandlers = { }


    def collisionHandler(self, collidedGameObject):
        def inner(func):
            
            self.collisionHandlers[collidedGameObject] = func
            
            return func
        return inner
    
    def __collision_handler__(self, collidedObject):
        if collidedObject in self.collisionHandlers:
            threading.Thread(target=self.collisionHandlers[collidedObject]).start()
    

    
    def move(self, direction : Vector2):
        self.position += direction


class gameEntity:
    def __init__(self, position : Vector2, game : bool = True, solid : bool = False):
        self.position = position
        self.game = game
        self.solid = solid
        self.onGround = False
        self.limitCollisionHandlerFunction = None
        self.collisionHandlers = { }



    def collisionHandler(self, collidedGameObject):
        def inner(func):
            if type(collidedGameObject) == list:
                for o in collidedGameObject:
                    self.collisionHandlers[o] = func
            else:
                self.collisionHandlers[collidedGameObject] = func
            return func
        return inner
    
    def __collision_handler__(self, collidedObject):
        if collidedObject in self.collisionHandlers:
            threading.Thread(target=self.collisionHandlers[collidedObject]).start()


    def gameLimitCollisionHandler(self):
        def inner(func):
            self.limitCollisionHandlerFunction = func
            return func
        return inner
    
    def __side_handler__(self, side):
        if self.limitCollisionHandlerFunction != None:
            threading.Thread(target=self.limitCollisionHandlerFunction, args=(side,)).start()



    def move(self, direction : Vector2):
        self.gameMap = self.game.getMapArray()
        newPos = Vector2(self.position.x, self.position.y)
        newPos.x += direction.x
        newPos.y += direction.y


        if newPos.x > self.game.size.x-1:
            return self.__side_handler__('right')

        if newPos.x < 0:
            return self.__side_handler__('left')

        if newPos.y > self.game.size.y-1:
            return self.__side_handler__('down')

        if newPos.y < 0:
            return self.__side_handler__('up')
        

        self.onGround = False

        if self.gameMap[newPos.y][newPos.x] in self.game.objects and self.gameMap[newPos.y][newPos.x].solid:
            self.onGround = True
            self.__collision_handler__(self.gameMap[newPos.y][newPos.x])
            return
        
        self.position = newPos

class gameScene:
    def __init__(self, objects = []):
        self.objects = objects

