from .helpers import *

class EntityGlow():
    def __init__(self, socket, processID, classStart):
        self.socket = socket
        self.processID = processID
        self.classStart = classStart

    def enabled(self):
        return Data(self.socket, self.processID, self.classStart + 0x380, 1)

    def colours(self) -> Vector3Data:
        return Vector3Data(self.socket, self.processID, self.classStart + 0x1B8)

    def magic(self): #0x4D407D7E
        return Data(self.socket, self.processID, self.classStart + 0x278)

class C_BaseEntity:
    def __init__(self, socket, processID, pointer):
        self.socket = socket
        self.processID = processID
        self.classStart = self.socket.readProcessMemory(self.processID, pointer, 8)

    def glow(self):
        return EntityGlow(self.socket, self.processID, self.classStart)