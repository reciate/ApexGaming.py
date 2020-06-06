from .helpers import *
from .C_WeaponX import *

class PlayerGlow:
    def __init__(self, socket: Socket, processID, classStart):
        self.socket = socket
        self.processID = processID
        self.classStart = classStart

    def enabled(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x390, 1)

    def context(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x310, 4)

    def range(self) -> FloatData:
        return FloatData(self.socket, self.processID, self.classStart + 0x2FC)

    def colours(self) -> Vector3Data:
        return Vector3Data(self.socket, self.processID, self.classStart + 0x1D0)

    def fade(self) -> Vector2Data:
        return Vector2Data(self.socket, self.processID, self.classStart + 0x2D0)

    def enable(self, red, green, blue):
        self.enabled().set(1)
        self.context().set(1)
        self.fade().set(Vector2(1, 1))
        self.colours().set(Vector3(red, green, blue))

class C_Player:
    def __init__(self, socket: Socket, processID, pointer):
        self.socket = socket
        self.processID = processID
        self.classStart = self.socket.readProcessMemory(self.processID, pointer, 8)

    def health(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x3E0)

    def shield(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x170)

    def maxShield(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x174)

    def helmetType(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x41C4)

    def shieldType(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x41C8)

    def team(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x3F0)

    def zooming(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x1AC1, 1)

    def lifeState(self) -> Data:
        return Data(self.socket, self.processID, self.classStart + 0x758, 1)

    def viewAngles(self) -> Vector2Data:
        return Vector2Data(self.socket, self.processID, self.classStart + 0x23C8)

    def swayAngles(self) -> Vector2Data:
        return Vector2Data(self.socket, self.processID, self.classStart + 0x23B8)

    def aimPunch(self) -> Vector2Data:
        return Vector2Data(self.socket, self.processID, self.classStart + 0x2300)

    def origin(self) -> Vector3Data:
        return Vector3Data(self.socket, self.processID, self.classStart + 0x14C)

    def boneOffsets(self, boneID) -> BoneData:
        boneMatrix = self.socket.readProcessMemory(self.processID, self.classStart + 0xED8, 8) + 0x30 * boneID
        return BoneData(self.socket, self.processID, boneMatrix)

    def bonePosition(self, boneID) -> Vector3:
        origin = self.origin().get()
        origin.add(self.boneOffsets(boneID).get())
        return origin

    def cameraPosition(self) -> Vector3Data:
        return Vector3Data(self.socket, self.processID, self.classStart + 0x1DA4)

    def vectorVelocity(self) -> Vector3Data:
        return Vector3Data(self.socket, self.processID, self.classStart + 0x420)

    def relativeOrigin(self, target) -> Vector3:
        relativeOrigin = target.origin().get()
        relativeOrigin.subtract(self.origin().get())
        return relativeOrigin

    def glow(self) -> PlayerGlow:
        return PlayerGlow(self.socket, self.processID, self.classStart)

    def currentWeapon(self, entityList) -> C_WeaponX:
        currentWeaponOffset = (Data(self.socket, self.processID, self.classStart + 0x1944).get() & 0xFFFF) * 32
        return entityList.findWeapon(currentWeaponOffset)

    def distanceTo(self, target) -> float:
        return self.relativeOrigin(target).magnitude()

    def boneDistanceToCrosshair(self, target, bone):
        relativePos = target.bonePosition(8)
        relativePos.subtract(self.cameraPosition().get())
        aimbotAngles = Vector2(math.degrees(math.atan2(relativePos.y, relativePos.x)), -math.degrees(math.asin(relativePos.z / relativePos.magnitude())))
        aimbotAngles.subtract(self.viewAngles().get())
        magnitude = aimbotAngles.magnitude()
        if magnitude > 180: magnitude = 360 - magnitude
        return magnitude

    def doAimbot(self, entityList, target, boneID, smoothing):
        targetPosition = target.bonePosition(boneID)
        targetPosition.subtract(self.cameraPosition().get()) #Relative angles
        
        currentWeapon = self.currentWeapon(entityList)
        bulletTime = targetPosition.magnitude() / currentWeapon.speed().get()
        velocity = target.vectorVelocity().get()
        velocity.multiply(Vector3(bulletTime, bulletTime, bulletTime)) #Movement prediction
        if velocity.z < 0: velocity.z *= 1.5

        velocity.z +=  (2 - currentWeapon.gravity().get()) * 375 * bulletTime * bulletTime #Bullet drop prediction

        targetPosition.add(velocity)
        aimbotAngles = Vector2(math.degrees(math.atan2(targetPosition.y, targetPosition.x)), -math.degrees(math.asin(targetPosition.z / targetPosition.magnitude())))

        swayAngles = self.swayAngles().get()
        viewAngles = self.viewAngles().get()
        swayAngles.subtract(viewAngles)

        aimbotAngles.subtract(swayAngles)

        aimbotAngles.subtract(viewAngles)
        if aimbotAngles.x < -180: aimbotAngles.x += 360
        if aimbotAngles.x > 180: aimbotAngles.x -= 360
        aimbotAngles.multiply(Vector2(smoothing, smoothing))
        aimbotAngles.add(viewAngles)
        
        self.viewAngles().set(aimbotAngles)