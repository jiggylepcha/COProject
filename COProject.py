#CO Project
#Arm Simulator
# Vishaal Udandarao 2016119
# Suryatej Reddy 2016102
# JIgme Lobsang Lepcha 2016045

class Instruction:
	all_instructions = list()
	registers = dict()
	memory = list()

	TYPE_DATA_PROCESSING = 0
	TYPE_SINGLE_DATA_TRANSFER = 1

	def __init__(self,addr,inst):
		self.addressInHex = addr
		self.addressInInt = getIntFromHex(addr)
		self.instruction = inst
		self.instructionInBinary = getBinaryFromHex(inst)[2:]
		self.subInstruction = None
		Instruction.all_instructions.append(self)

	@staticmethod
	def getInstruction(address):
		return next((instruct for instruct in Instruction.all_instructions if instruct.addressInInt == address), None)

	def printFetchStatement(self):
		print ("Fetch instruction " + self.instruction + " from address " + self.addressInHex)

	def splitInstruction(self):
		instructionInBinary = self.instructionInBinary
		format_bits = instructionInBinary[4:6]  #27,26
		
		if format_bits == '00':
			#data processing instruction
			dataInstruction = DataProcessingInstruction(self)
			self.subInstruction = dataInstruction

		elif format_bits == '01':
			#single data transfer
			self.singleDataTransfer()


class DataProcessingInstruction:
	
	OPERAND_TYPE_REGISTER = '0'
	OPERAND_TYPE_IMMEDIATE = '1'

	def __init__(self,instruction):
		self.instruction = instruction
		self.condition = ""
		self.opcode = ""
		self.sourceRegister1 = None
		self.sourceRegister2 = None
		self.destinationRegister = None
		self.immediateValue = None
		self.typeOfOperand = ""
		self.operand_1 = 0
		self.operand_2 = 0
		self.shift = 0
		self.rotate = 0
		self.type = None
		self.assignValues()

	def assignValues(self):
		instructionInBinary = self.instruction.instructionInBinary
		condition = instructionInBinary[:4]  #31,30,29,28
		self.condition = condition
		self.type = Instruction.TYPE_DATA_PROCESSING
		self.typeOfOperand = instructionInBinary[6:7]
		self.opcode = instructionInBinary[7:11]
		self.sourceRegister1 = instructionInBinary[12:16]
		self.operand_1 = Instruction.registers[int(self.sourceRegister1,2)]

		self.destination_register = instructionInBinary[16:20]

		if self.typeOfOperand == DataProcessingInstruction.OPERAND_TYPE_REGISTER:
			self.shift = instructionInBinary[20:28]
			self.sourceRegister2 = instructionInBinary[28:]
			self.operand_2 = Instruction.registers[int(self.sourceRegister2,2)]

			#TODO - appply shift to second operand

		elif self.typeOfOperand == DataProcessingInstruction.OPERAND_TYPE_IMMEDIATE :
			self.rotate = instructionInBinary[20:24]
			self.immediateValue = instructionInBinary[24:]
			self.operand_2 = int(self.immediateValue,2)

			#TODO - apply rotate to second operand


class SingleDataTransferInstruction:


	def __init__(self,instruction):
		self.instruction = instruction
		


def getIntFromHex(hexValue):
	return int(hexValue,16)

def getBinaryFromHex(hexValue):
	b = bin(int(hexValue, 16))
	return b


#returns dictionary
def initRegisters(numberOfRegisters = 32):
	registers = dict()
	for reigsterId in range(0,32):
		registers[reigsterId] = 0
	Instruction.registers = registers

#returns List
def initMainMemory():
	memory = list()
	Instruction.memory = memory


#the dictionary contains {0:('0x0xE3A0200A',0x0),4:('0x0xE3A0200A',0x4)}
def loadFromFile(fileName):
	file = open(fileName,'r')
	allInstructions = file.readlines()
	for data in allInstructions:
		instruct = data.split()
		addressInHex = instruct[0].strip()
		instruction = instruct[1].strip()
		tempInstruction = Instruction(addressInHex,instruction)

#just prints instruction and returns the instruction
def fetchInstruction(instLocation):
	curInstruction = Instruction.getInstruction(instLocation)
	# curInstruction.printFetchStatement()
	return curInstruction

#takes the instruction object as a parameter
def decodeInstruction(instruction):
	pass

def main():
	loadFromFile("input.mem")
	initMainMemory()
	initRegisters()
	for i in range(0,13,4):
		currentInstruction = fetchInstruction(i)
		currentInstruction.splitInstruction()
		
if __name__=='__main__':
	main()
