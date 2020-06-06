from .helpers import *
from .ViewMatrix import ViewMatrix

class C_ViewRender:
    def __init__(self, socket, processID, pointer):
        self.socket = socket
        self.processID = processID
        self.classStart = self.socket.readProcessMemory(self.processID, pointer, 8)

    def viewMatrix(self) -> ViewMatrix:
        return ViewMatrix(self.socket, self.processID, self.classStart + 0x1b3bd0)