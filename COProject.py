#CO Project
#Arm Simulator

def getIntFromHex(hexValue):
	return int(hexValue,16)

def loadFromFile(fileName):
	instructions = dict()
	file = open(fileName,'r')
	allInstructions = file.readlines()
	for data in allInstructions:
		instruct = data.split()
		addressInHex = instruct[0].strip()
		addressInInt = getIntFromHex(addressInHex)
		instruction = instruct[1].strip()
		instructions[addressInInt] = instruction
	print instructions


