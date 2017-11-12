#CO Project
#Arm Simulator


class Instruction:
	all_instructions = list()
	def __init__(self,addr,inst):
		self.addressInHex = addr
		self.addressInInt = getIntFromHex(addr)
		self.instruction = inst
		Instruction.all_instructions.append(self)

	@staticmethod
	def getInstruction(address):
		return next((instruct for instruct in Instruction.all_instructions if instruct.addressInInt == address), None)

	def printFetchStatement(self):
		print "Fetch instruction " + self.instruction + " from address " + self.addressInHex

	def decodeInstruction(self):
		pass


def getIntFromHex(hexValue):
	return int(hexValue,16)


#returns dictionary
def initRegisters(numberOfRegisters = 32):
	registers = dict()
	for reigsterId in range(1,33):
		registers[reigsterId] = 0
	return registers

#returns List
def initMainMemory():
	memory = list()
	return memory


#the dictionary contains {0:('0x0xE3A0200A',0x0),4:('0x0xE3A0200A',0x4)}
def loadFromFile(fileName):
	file = open(fileName,'r')
	allInstructions = file.readlines()
	for data in allInstructions:
		instruct = data.split()
		addressInHex = instruct[0].strip()
		instruction = instruct[1].strip()
		tempInstruction = Instruction(addressInHex,instruction)

#just prints instruction
def fetchInstruction(instLocation):
	curInstruction = Instruction.getInstruction(instLocation)
	curInstruction.printFetchStatement()


#takes the instruction object as a parameter
def decodeInstruction(instruction):
	pass


def main():
	loadFromFile("input.mem")
	for i in range(0,13,4):
		fetchInstruction(i)

if __name__=='__main__':
	main()
