class ARMSim:

	def fetch():
		with open("input.mem","r") as f:
			for line in f:
				decode(line)


	def decode(self, instruction):
		print ("This function decodes an")