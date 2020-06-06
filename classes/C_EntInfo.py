from __future__ import annotations
from .C_BaseEntity import C_BaseEntity

class C_EntInfo:
    def __init__(self, socket, processID, pointer):
        self.socket = socket
        self.processID = processID
        self.classStart = self.socket.readProcessMemory(self.processID, pointer, 8)

    def entity(self) -> C_BaseEntity:
        entity = C_BaseEntity(self.socket, self.processID, self.classStart)
        if entity.classStart == 0: return None
        return entity

    def backPointer(self) -> C_EntInfo:
        backPointer = C_EntInfo(self.socket, self.processID, self.classStart + 0x10)
        if backPointer.classStart == 0: return None
        return backPointer

    def forwardPointer(self) -> C_EntInfo:
        forwardPointer = C_EntInfo(self.socket, self.processID, self.classStart + 0x18)
        if forwardPointer.classStart == 0: return None
        return forwardPointer