import win32api
import threading
from .viritualKeys import virtual_keys

class Event:
    def __init__(self, vkey) -> None:
        self.vkey = vkey
        self.string = virtual_keys[vkey]

    def __str__(self) -> str:
        return self.string

class Listener:
    def __init__(self,  eventHandler=None, args: list=[]) -> None:
        self.listening = False
        self.listener = None
        self.eventHandler = eventHandler
        self.handlerArgs = args
        self.keystates = {vkey:False for vkey in virtual_keys.keys()}

    def isPressed(self, key:int):
        return win32api.GetAsyncKeyState(key)

    def listen(self):
        if (not self.listening):
            self.listening = True
            self.listenerThread = threading.Thread(target=self._start)
            self.listenerThread.start()

    def stop(self):
        if (self.listening):
            self.listening = False
            self.listenerThread.join()

    def _start(self):
        while (self.listening):
            self._updateKeystates()

    def _updateKeystates(self):
        keystates = self.keystates
        newDict = keystates.copy()
        for key in keystates.keys():
            if (self.isPressed(key)):

                if (newDict[key]):
                    continue

                if (not self.eventHandler):
                    continue

                event = Event(key)
                self.eventHandler(event, *self.handlerArgs)

                newDict[key] = True
            else:
                newDict[key] = False

        self.keystates = newDict
