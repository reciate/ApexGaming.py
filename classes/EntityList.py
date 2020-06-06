from .C_Player import C_Player
from .C_WeaponX import C_WeaponX
from .C_EntInfo import C_EntInfo

class EntityList:
    def __init__(self, socket, processID, entityListStart):
        self.socket = socket
        self.processID = processID
        self.entityListStart = entityListStart

    def players(self):
        playerList = []
        for i in range(60):
            player = C_Player(self.socket, self.processID, self.entityListStart + ((i + 1) * 0x20))
            if player.classStart == 0: continue
            playerList.append(player)
        return playerList

    def validEntities(self):
        validEntites = []
        currentEntInfo = C_EntInfo(self.socket, self.processID, self.entityListStart + 0x18)
        while currentEntInfo != None:
            validEntites.append(currentEntInfo)
            currentEntInfo = currentEntInfo.forwardPointer()
        return validEntites

    def findWeapon(self, offset) -> C_WeaponX:
        return C_WeaponX(self.socket, self.processID, self.entityListStart + offset)