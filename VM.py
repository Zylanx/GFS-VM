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
		
		self.stdoutBuffer = ""
		
		self.curAddr = 0
		self.curInstr = 0
		
	def reset(self):
		self.stack = deque()
		self.localVars = [None, None, None]
		self.curAddr = 0
		self.curInstr = 0
		self.stdoutBuffer = ""
	
	def exec(self):
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
				self.stdoutBuffer += str(self.stack.pop())
			elif self.curInstr == 8: # flush
				print(self.stdoutBuffer, end="")
				self.stdoutBuffer = ""
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
			print(self.stdoutBuffer, end="")
		
		if len(self.stack) > 0:
			return self.stack.pop()

def testFunc():
	for i in range(10):
		print("Bad VM. Iter Num: ", i+1)
		print("i: ", i)
		print("i + 3: ", i+3)

if __name__ == "__main__":
	testInstr = [0, 0, 2, 0, 0, 10, 2, 1, 3, 0, 3, 1, 9, 51, 1, "\n", 3, 0, 0, 3, 5, 1, "i + 3: ", 1, "\n", 3, 0, 1, "i: ", 1, "\n", 3, 0, 0, 1, 5, 1, "Bad VM. Iter Num: ", 7, 7, 7, 7, 7, 7, 7, 7, 7, 4, 0, 11, 8]
	testVM = VM(testInstr)
	
	timingResultsVM = []
	timingResultsPython = []
	for i in range(1000):
		testVM.reset()
		timingResultsVM.append(timeit(testVM.exec))
		
	for i in range(1000):
		timingResultsPython.append(timeit(testFunc))
		
	print("VM: " + str(sum(timingResultsVM)/len(timingResultsVM)))
	print("Pure Python: " + str(sum(timingResultsPython)/len(timingResultsPython)))