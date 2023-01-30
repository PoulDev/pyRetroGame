from pyRetroGame.crossPlatform import osApi
from .mathematics.vector import Vector2
from .crossPlatform.osApi import *
import threading
import time
import curses
from pyRetroGame import assets

class GameBackground:
    def __init__(self): pass
    def __str__(self): return ' '

class Game:
    def __init__(self, background = GameBackground, size : Vector2 = Vector2(40, 20)):
        self.background = background()
        self.emptyMap = [[self.background for _ in range(size.x)] for _ in range(size.y)]
        self.objects = []
        self.size = size
        self.handlers = {}
        self.printedBefore = []
        self.texts = {}

        self.stopGame = False # Set this variable to True to stop the game.

    def start(self, fps = 30, debugging = False):
        self.fps = fps
        self.debugging = debugging
        self.stdscr = curses.initscr()
        #self.__set_pairs__()

        self.keyboardThread = threading.Thread(target=self.__key_handler__)
        self.keyboardThread.setDaemon(True)
        self.keyboardThread.start()
        self.__update_screen__()

    def quit(self):
        self.stopGame = True

    def getMapArray(self):
        gameMap = [[self.background for _ in range(self.size.x)] for _ in range(self.size.y)]
        for obj in self.objects:
            gameMap[obj.position.y][obj.position.x] = obj
        return gameMap

    def getMap(self):
        gameMap = self.getMapArray()
        rawMap = ''
        for line in gameMap:
            for obj in line:
                rawMap += str(obj)
            rawMap += '\n'

        now = time.time()
        for textIdentifier in self.texts.copy():
            if now - textIdentifier > self.texts[textIdentifier]['maxtime']:
                del self.texts[textIdentifier]
                continue
            rawMap += f'{self.texts[textIdentifier]["txt"]}'

        if self.debugging:
            for obj in self.objects:
                rawMap += f'{obj.__class__}: ({obj.position}), ({obj.limitCollisionHandlerFunction})\n'


        return rawMap
    
    def spawn(self, obj):
        if type(obj) == list:
            for o in obj:
                self.spawn(o)
            return
        self.objects.append(obj)

    def despawn(self, obj):
        self.objects.remove(obj)

    def despawnAll(self):
        self.objects = []

    def inputHandler(self, key):
        def inner(func):
            if not type(key) == list:
                self.handlers[ord(key)] = {'func': func, 'passKey': False}
            else:
                for ky in key:
                    self.handlers[ord(ky)] = {'func': func, 'passKey': True}
            return func
        return inner

    def __set_pairs__(self):
        """
            In development
            Ignore this.
        """
        curses.init_pair(1, 1, assets.colors['black'])
        curses.init_pair(2, 1, assets.colors['yellow'])
        curses.init_pair(3, 1, assets.colors['white'])
        curses.init_pair(4, 1, assets.colors['red'])
        curses.init_pair(5, assets.colors['black'], 1)
        curses.init_pair(6, assets.colors['yellow'], 1)
        curses.init_pair(7, assets.colors['white'], 1)
        curses.init_pair(8, assets.colors['red'], 1)

    def __key_handler__(self):
        while not self.stopGame:
            key = waitKey()
            if key in self.handlers:
                if self.handlers[key]['passKey']:
                    subthread = threading.Thread(target=self.handlers[key]['func'], args=(chr(key),))
                else:
                    subthread = threading.Thread(target=self.handlers[key]['func'])
                subthread.setDaemon(True)
                subthread.start()

    def __update_screen__(self):
        while not self.stopGame:
            time.sleep(1 / self.fps)
            num = 0
            self.stdscr.clear()
            for line in self.getMap().splitlines():
                try:
                    self.stdscr.addstr(num, 0, line.center(terminalSize().x))
                except: continue
                num += 1

            self.stdscr.refresh()

        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def printText(self, text, timeout = 2):
        self.texts[time.time()] = {'txt': '\n' + str(text), 'maxtime': timeout}


    def printAnimatedText(self, text, animationTimeout = 0.05, timeout = 2):
        now = time.time()
        current = '\n'
        for char in text:
            if char == ' ':
                current += char
                continue
            current += char
            self.texts[now] = {'txt': current, 'maxtime': timeout}
            time.sleep(animationTimeout)
