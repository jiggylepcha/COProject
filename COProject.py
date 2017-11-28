#CO Project
#Arm Simulator


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

		if (format_bits == '00'):
			#data processing instruction
			dataInstruction = DataProcessingInstruction(self)
			self.subInstruction=dataInstruction

		elif (format_bits == '01'):
			#single data transfer
			self.singleDataTransfer()


class DataProcessingInstruction:



	OPERAND_TYPE_REGISTER = '0'
	OPERAND_TYPE_IMMEDIATE = '1'
	SHIFT_TYPE_LOGICAL_LEFT = "00"
	SHIFT_TYPE_LOGICAL_RIGHT = "01"
	SHIFT_TYPE_ARITHMETIC_RIGHT = "10"
	SHIFT_TYPE_ROTATE_RIGHT = "11"

	OPCODE_AND = '0000'
	OPCODE_EOR = '0001'
	OPCODE_SUB = '0010'
	OPCODE_RSB = '0011'
	OPCODE_ADD = '0100'
	OPCODE_ORR = '1100'
	OPCODE_MOV = '1101'
	OPCODE_BIC = '1110'
	OPCODE_MVN = '1111'


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

		if str(self.typeOfOperand) == str(DataProcessingInstruction.OPERAND_TYPE_REGISTER):
			self.shift = instructionInBinary[20:28]
			self.sourceRegister2 = instructionInBinary[28:]
			self.operand_2 = Instruction.registers[int(self.sourceRegister2,2)]
			


			shiftOperation = self.shift[7]
			if (str(shiftOperation) == "0"):
				#instruction specified shift amount
				shiftAmount = self.shift[:5]
				shiftAmount = int(shiftAmount,2)
				shiftType = self.shift[5:7]
				if (str(shiftType) == SHIFT_TYPE_LOGICAL_LEFT):
					self.operand_2 = self.operand_2 << shiftAmount
				elif (str(shiftType) == SHIFT_TYPE_LOGICAL_RIGHT):
					self.operand_2 = self.operand_2 >> shiftAmount



				#TODO Apply ASR and ROR

			elif (str(shiftOperation) == "1"):
				#register specified shift amount

				#TODO


		elif str(self.typeOfOperand) == str(DataProcessingInstruction.OPERAND_TYPE_IMMEDIATE) :
			self.rotate = instructionInBinary[20:24]
			self.immediateValue = instructionInBinary[24:]
			self.operand_2 = int(self.immediateValue,2)
			

			#TODO - apply rotate to second operation



	def executeInstruction(self):
		if self.opcode == OPCODE_AND:
				res = self.operand_1 & self.operand_2
				Instruction.registers[int(self.destination_register,2)] = res
		elif self.opcode == OPCODE_EOR:
				res = self.operand_1 ^ self.operand_2
				Instruction.registers[int(self.destination_register,2)] = res
		elif self.opcode == OPCODE_SUB:
				res = self.operand_1 - self.operand_2
				Instruction.registers[int(self.destination_register,2)] = res
		elif self.opcode == OPCODE_RSB:
				res = self.operand_2 - self.operand_1
				Instruction.registers[int(self.destination_register,2)] = res
		elif self.opcode == OPCODE_ADD:
				res = self.operand_1 + self.operand_2
				Instruction.registers[int(self.destination_register,2)] = res
		elif self.opcode == OPCODE_ORR:
				res = self.operand_1 | self.operand_2
				Instruction.registers[int(self.destination_register,2)] = res
		elif self.opcode == OPCODE_MOV:
				res = self.operand_2
				Instruction.registers[int(self.destination_register,2)] = res
		elif self.opcode == OPCODE_BIC:
				res = self.operand_1 & (!self.operand_2)
				Instruction.registers[int(self.destination_register,2)] = res
		elif self.opcode == OPCODE_MVN:
				res = !self.operand_2
				Instruction.registers[int(self.destination_register,2)] = res



class SingleDataTransferInstruction:


	def __init__(self,instruction):
		self.instruction = instruction

		self.condition = ""
		self.immediateOffset = ""
		self.indexingBit = ""
		self.upDownBit = ""
		self.byteWordBit = ""
		self.writeBackBit = ""
		self.loadStoreBit = ""
		self.baseRegister = None
		self.destinationRegister = None
		self.offset = None

	def assignValues(self):
		instructionInBinary = self.instruction.instructionInBinary
		condition = instructionInBinary[:4]  #31,30,29,28
		self.condition = condition
		self.immediateOffset = instructionInBinary[6:7] #25
		self.indexingBit = instructionInBinary[7:8] #24
		self.upDownBit = instructionInBinary[8:9] #23
		self.byteWordBit = instructionInBinary[9:10] #22
		self.writeBackBit = instructionInBinary[10:11] #21
		self.loadStoreBit = instructionInBinary[11:12] #20
		self.baseRegister = instructionInBinary[12:16] #19,18,17,16
		self.destinationRegister = instructionInBinary[16:20] #15,14,13,12		



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
