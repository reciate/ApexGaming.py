import psutil
from classes import *
from classes.C_Player import *
from classes.EntityList import *

def getProcessID(processName):
	for process in psutil.process_iter():
		try:
			if process.name() == processName: return process.pid
		except: continue

def findApexProcess():
	processID = getProcessID('r5apex.exe')
	if processID == None: processID = getProcessID('EasyAntiCheat_launcher.exe')
	return processID

def cheatLoop(socket, apexPID, baseAddress):
	localPlayer = C_Player(socket, apexPID, baseAddress + 0x1CCDFF8)
	entityList = EntityList(socket, apexPID, baseAddress + 0x1767348)
	playerList = entityList.players()
	closest = [None, 180]
	for player in playerList:
		if player.classStart == localPlayer.classStart or player.health().get() == 0 or (localPlayer.distanceTo(player) / 40) > 300 or localPlayer.origin().get().z > 21000: continue
		if player.team().get() == localPlayer.team().get():
			player.glow().enable(0, 10, 0)
		else:
			player.glow().enable(10, 0, 0)
			cDistance = localPlayer.boneDistanceToCrosshair(player, 8)
			if cDistance < closest[1]:
				closest[0] = player
				closest[1] = cDistance
	if closest[0] and closest[1] < 10:
		closest[0].glow().enable(0, 10, 10)
		if localPlayer.zooming().get():
			localPlayer.doAimbot(entityList, closest[0], 12, 0.5)

def main():
	apexPID = findApexProcess()
	if apexPID == None: 
		print("Apex not open!")
		exit()
	socket = Socket()
	baseAddress = socket.getProcessBaseAddress(apexPID)
	while True: cheatLoop(socket, apexPID, baseAddress)

main()