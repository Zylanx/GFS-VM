__author__ = 'Zylanx'

from collections import deque
from time import time

def timeit(func, *args, **kwargs):
	start = time()
	func(*args, **kwargs)
	return time() - start


class VM:
	def __init__(self, instr = None):
		if not instr:
			instr = []
		
		self.stack = deque()
		self.localVars = [None, None, None]
		self.instrList = instr
		
		self.stdoutBuffer = deque()
		
		self.curAddr = 0
		self.curInstr = 0
		
	def reset(self):
		self.stack = deque()
		self.localVars = [None, None, None]
		self.curAddr = 0
		self.curInstr = 0
		self.stdoutBuffer = deque()
	
	def exec(self):
		self.curAddr = 0
		
		while self.curAddr < len(self.instrList):
			self.curInstr = self.instrList[self.curAddr]
			self.curAddr += 1
			
			if self.curInstr == 0: # push int
				val = self.instrList[self.curAddr]
				self.curAddr += 1
				
				self.stack.append(val)
			elif self.curInstr == 1: # push string
				val = self.instrList[self.curAddr]
				self.curAddr += 1
				
				self.stack.append(val)
			elif self.curInstr == 2: # store
				index = self.instrList[self.curAddr]
				self.curAddr += 1
				
				self.localVars[index] = self.stack.pop()
			elif self.curInstr == 3: # load
				index = self.instrList[self.curAddr]
				self.curAddr += 1
				
				self.stack.append(self.localVars[index])
			elif self.curInstr == 4: # inc
				index = self.instrList[self.curAddr]
				self.curAddr += 1
				
				self.localVars[index] += 1
			elif self.curInstr == 5: # add
				opand2 = self.stack.pop()
				opand1 = self.stack.pop()
				
				self.stack.append(opand1 + opand2)
			elif self.curInstr == 6: # dup
				self.stack.append(self.stack[-1])
			elif self.curInstr == 7: # print
				self.stdoutBuffer.append(str(self.stack.pop()))
			elif self.curInstr == 8: # flush
				print("".join(self.stdoutBuffer), end="")
				self.stdoutBuffer = deque()
			elif self.curInstr == 9: # jge
				addr = self.instrList[self.curAddr]
				self.curAddr += 1
				val2 = self.stack.pop()
				val1 = self.stack.pop()
				
				if val1 >= val2:
					self.curAddr = addr
			elif self.curInstr == 10: # jle
				addr = self.instrList[self.curAddr]
				self.curAddr += 1
				val2 = self.stack.pop()
				val1 = self.stack.pop()
				
				if val1 <= val2:
					self.curAddr = addr
			elif self.curInstr == 11: # jmp
				self.curAddr = self.instrList[self.curAddr]
		
		if len(self.stdoutBuffer) > 0:
			print("".join(self.stdoutBuffer), end="")
			self.stdoutBuffer = deque()
		
		if len(self.stack) > 0:
			return self.stack.pop()

if __name__ == "__main__":
	def timingtype1(pythonFunc, vm, numTests):
		timingResultsPython = []
		for i in range(numTests):
			timingResultsPython.append(timeit(pythonFunc))
		pythonDuration = sum(timingResultsPython)/len(timingResultsPython)
	
		timingResultsVM = []
		for i in range(numTests):
			# testVM.reset()
			timingResultsVM.append(timeit(vm.exec))
		vmDuration = sum(timingResultsVM)/len(timingResultsVM)
		
		return (pythonDuration, vmDuration)
	
	def timingtype2(pythonFunc, vm, numTests):
		pythonStartTime = time()
		for i in range(numTests):
			pythonFunc()
		pythonEndTime = time()
		pythonDuration = (pythonEndTime - pythonStartTime)/numTests
		
		vmStartTime = time()
		for i in range(numTests):
			vm.exec()
		vmEndTime = time()
		vmDuration = (vmEndTime - vmStartTime)/numTests
		
		return (pythonDuration, vmDuration)
	
	def testcase1(numTests):
		def testFunc():
			for i in range(10000):
				print("Bad VM. Iter Num: ", i + 1)
				print("i: ", i)
				print("i + 3: ", i + 3)
				
		testInstr = [0, 0, 2, 0, 0, 10000, 2, 1, 3, 0, 3, 1, 9, 51, 1, "\n", 3, 0, 0, 3, 5, 1, "i + 3: ", 1, "\n", 3, 0, 1, "i: ", 1, "\n", 3, 0, 0, 1, 5, 1, "Bad VM. Iter Num: ", 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 0, 11, 8]
		testVM = VM(testInstr)
		
		pythonDuration1, vmDuration1 = timingtype1(testFunc, testVM, numTests)
		pythonDuration2, vmDuration2 = timingtype2(testFunc, testVM, numTests)
		
		strBuf = ""
		strBuf += "---Test Case 1---\n"
		strBuf += "- Python Duration 1: " + str(pythonDuration1) + "\n"
		strBuf += "- VM Duration 1: " + str(vmDuration1) + "\n"
		strBuf += "- Python Duration 2: " + str(pythonDuration2) + "\n"
		strBuf += "- VM Duration 2: " + str(vmDuration2) + "\n"
		return strBuf
		
	def testcase2(numTests):
		def testFunc():
			for i in range(20000):
				print(str(i) + "\n", end="")
		
		testInstr = [0, 0, 0, 20000, 2, 1, 2, 0, 3, 0, 3, 1, 9, 25, 3, 0, 7, 1, "\n", 7, 4, 0, 11, 8]
		testVM = VM(testInstr)
		
		pythonDuration1, vmDuration1 = timingtype1(testFunc, testVM, numTests)
		pythonDuration2, vmDuration2 = timingtype2(testFunc, testVM, numTests)
		
		strBuf = ""
		strBuf += "---Test Case 2---\n"
		strBuf += "- Python Duration 1: " + str(pythonDuration1) + "\n"
		strBuf += "- VM Duration 1: " + str(vmDuration1) + "\n"
		strBuf += "- Python Duration 2: " + str(pythonDuration2) + "\n"
		strBuf += "- VM Duration 2: " + str(vmDuration2) + "\n"
		return strBuf
		
	
	strBuf = "\n\n----------------\n\n---Results---\n"
	strBuf += testcase1(25)
	strBuf += testcase2(25)
	print(strBuf)
	
	with open("TimingTests.txt", "w") as f:
		f.write(strBuf)