import ctypes, socket
from .vectors import *

class Packet(ctypes.Structure):
    _fields_ = [('processID', ctypes.c_uint), ('address', ctypes.c_ulonglong), ('mode', ctypes.c_ubyte), ('size', ctypes.c_ubyte), ('result', ctypes.c_longlong)]

class Socket:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 6000))

    def getProcessBaseAddress(self, processID):
        self.socket.send(Packet(processID, 0, 0, 0, 0))
        return Packet.from_buffer_copy(self.socket.recv(ctypes.sizeof(Packet))).result

    def readProcessMemory(self, processID, address, size):
        self.socket.send(Packet(processID, address, 1, size, 0))
        return Packet.from_buffer_copy(self.socket.recv(ctypes.sizeof(Packet))).result

    def writeProcessMemory(self, processID, address, size, value):
        self.socket.send(Packet(processID, address, 2, size, value))
        return Packet.from_buffer_copy(self.socket.recv(ctypes.sizeof(Packet))).result == value

class Data:
    def __init__(self, socket: Socket, processID, address, size = 4):
        self.socket = socket
        self.processID = processID
        self.address = address
        self.size = size

    def get(self):
        return self.socket.readProcessMemory(self.processID, self.address, self.size)

    def set(self, value):
        self.socket.writeProcessMemory(self.processID, self.address, self.size, value)

class FloatData(Data):
    def get(self):
        longlong = self.socket.readProcessMemory(self.processID, self.address, self.size)
        return ctypes.cast(ctypes.pointer(ctypes.c_longlong(longlong)), ctypes.POINTER(ctypes.c_float)).contents.value

    def set(self, value):
        value = ctypes.cast(ctypes.pointer(ctypes.c_float(value)), ctypes.POINTER(ctypes.c_longlong)).contents
        self.socket.writeProcessMemory(self.processID, self.address, self.size, value)

class Vector3Data(Data):
    def get(self) -> Vector3:
        x = FloatData(self.socket, self.processID, self.address).get()
        y = FloatData(self.socket, self.processID, self.address + 0x4).get()
        z = FloatData(self.socket, self.processID, self.address + 0x8).get()
        return Vector3(x, y, z)

    def set(self, vector3: Vector3):
        FloatData(self.socket, self.processID, self.address).set(vector3.x)
        FloatData(self.socket, self.processID, self.address + 0x4).set(vector3.y)
        FloatData(self.socket, self.processID, self.address + 0x8).set(vector3.z)

class Vector2Data(Data):
    def get(self) -> Vector2:
        y = FloatData(self.socket, self.processID, self.address).get()
        x = FloatData(self.socket, self.processID, self.address + 0x4).get()
        return Vector2(x, y)

    def set(self, vector2: Vector2):
        FloatData(self.socket, self.processID, self.address).set(vector2.y)
        FloatData(self.socket, self.processID, self.address + 0x4).set(vector2.x)

class BoneData(Data):
    def get(self) -> Vector3:
        x = FloatData(self.socket, self.processID, self.address + 0xC).get()
        y = FloatData(self.socket, self.processID, self.address + 0x1C).get()
        z = FloatData(self.socket, self.processID, self.address + 0x2C).get()
        return Vector3(x, y, z)

    def set(self, vector3: Vector3):
        FloatData(self.socket, self.processID, self.address + 0xC).set(vector3.x)
        FloatData(self.socket, self.processID, self.address + 0x1C).set(vector3.y)
        FloatData(self.socket, self.processID, self.address + 0x2C).set(vector3.z)