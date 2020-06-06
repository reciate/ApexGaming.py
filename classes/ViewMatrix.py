from .helpers import *

class ViewMatrix:
    def __init__(self, socket, processID, pointer):
        self.socket = socket
        self.processID = processID
        self.classStart = self.socket.readProcessMemory(self.processID, pointer, 8)

    def array(self):
        viewMatrix = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                viewMatrix[i].append(FloatData(self.socket, self.processID, self.classStart + (i * 0x10 + j * 0x4)).get())
        return viewMatrix