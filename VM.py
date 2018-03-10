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
		
		self.curAddr = 0
		self.curInstr = 0
		
	def exec(self):
		self.curAddr = 0
		
		while self.curAddr < len(self.instrList):
			self.curInstr = self.instrList[self.curAddr]
			self.curAddr += 1
			
			self.execInstr()
		
		if len(self.stack) > 0:
			return self.stack.pop()
	
	def execInstr(self):
		if self.curInstr == 0: # push int
			val = self.instrList[self.curAddr]
			self.curAddr += 1
			
			self.stack.append(val)
		elif self.curInstr == 1: # push string
			val = self.instrList[self.curAddr]
			self.curAddr += 1
			
			self.stack.append(val)
		elif self.curInstr == 2: # store
			# index = self.instrList[self.curAddr]
			# self.curAddr += 1
			#
			# self.localVars[index] = self.stack.pop()
			
			index = self.stack.pop()
			val = self.stack.pop()
			self.localVars[index] = val
		elif self.curInstr == 3: # load
			# index = self.instrList[self.curAddr]
			# self.curAddr += 1
			#
			# self.append(self.localVars[index])
			
			index = self.stack.pop()
			self.stack.append(self.localVars[index])
		elif self.curInstr == 4: # inc
			# index = self.instrList[self.curAddr]
			# self.curAddr += 1
			#
			# self.localVars[index] += 1
			
			index = self.stack.pop()
			self.localVars[index] += 1
		elif self.curInstr == 5: # add
			opand2 = self.stack.pop()
			opand1 = self.stack.pop()
			
			self.stack.append(opand1 + opand2)
		elif self.curInstr == 6: # dup
			self.stack.append(self.stack[-1])
		elif self.curInstr == 7: # print
			print(str(self.stack.pop()), end="")
		elif self.curInstr == 8: # jge
			# addr = self.instrList[self.curAddr]
			# self.curAddr += 1
			#
			# if self.stack.pop() >= self.stack.pop():
			# 	self.curInstr = addr
			
			addr = self.stack.pop()
			val2 = self.stack.pop()
			val1 = self.stack.pop()
			
			if val1 >= val2:
				self.curAddr = addr
		elif self.curInstr == 9: # jle
			# addr = self.instrList[self.curAddr]
			# self.curAddr += 1
			#
			# if self.stack.pop() <= self.stack.pop():
			# 	self.curInstr = addr
		
			addr = self.stack.pop()
			val2 = self.stack.pop()
			val1 = self.stack.pop()
			if val1 <= val2:
				self.curAddr = addr
		elif self.curInstr == 10: # jmp
			self.curAddr = self.stack.pop()
		
"""
for i in range(10):
	print("Bad VM. Iter num: ", i + 1)
	print("i: ", i)
	print("i + 3: ", i+3)

---

push 0
store 0
push 10
store 1

loop:
load 0
load 1
jge end
push "\n"
load 0
push 3
add
push "i + 3: "
push "\n"
load 0
push "i: "
push "\n"
load 0
push 1
add
push "Bad VM. Iter Num: "
print
print
print
print
print
print
print
print
print
inc 0
jmp start
end:

[0, 0, 0, 0, 2, 0, 10, 0, 1, 2, 0, 0, 3, 0, 1, 3, 0, 51, 8, 1, "\n", 0, 0, 3, 0, 3, 5, 1, "i + 3: ", 1, "\n", 0, 0, 3, 1, "i: ", 1, "\n", 0, 0, 3, 0, 1, 5, 1, "Bad VM. Iter Num: ", 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 4, 0, 10, 10]

---

0: # push int
1: # push string
2: # store
3: # load
4: # inc
5: # add
6: # dup
7: # print
8: # jge
9: # jle
10: # jmp
"""

def testFunc():
	for i in range(10):
		print("Bad VM. Iter Num: ", i+1)
		print("i: ", i)
		print("i + 3", i+3)

testInstr = [0, 0, 0, 0, 2, 0, 10, 0, 1, 2, 0, 0, 3, 0, 1, 3, 0, 61, 8, 1, "\n", 0, 0, 3, 0, 3, 5, 1, "i + 3: ", 1, "\n", 0, 0, 3, 1, "i: ", 1, "\n", 0, 0, 3, 0, 1, 5, 1, "Bad VM. Iter Num: ", 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 4, 0, 10, 10]
testVM = VM(testInstr)
print("Return result: " + str(testVM.exec()))

timingResultsVM = []
timingResultsPython = []
for i in range(1000):
	timingResultsVM.append(timeit(testVM.exec))
	timingResultsPython.append(timeit(testFunc))
	
print("VM: " + str(sum(timingResultsVM)/len(timingResultsVM)))
print("Pure Python: " + str(sum(timingResultsPython)/len(timingResultsPython)))