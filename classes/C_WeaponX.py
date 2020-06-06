from .helpers import *

class C_WeaponX:
    def __init__(self, socket, processID, pointer):
        self.socket = socket
        self.processID = processID
        self.classStart = self.socket.readProcessMemory(self.processID, pointer, 8)

    def speed(self):
        return FloatData(self.socket, self.processID, self.classStart + 0x1D48)

    def gravity(self):
        return FloatData(self.socket, self.processID, self.classStart + 0x1D50)