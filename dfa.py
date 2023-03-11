import random, sys, math
sys.setrecursionlimit(300)

class State:
	holds = ""
	def __init__(self, name = "", final :bool = False, next_0 = None, next_1 = None):
		self.next_0  = next_0
		self.next_1 = next_1
		self.final = final
		self.name = name

	def __repr__(self):
		return self.__class__.__name__ + ' -- ' + self.name + ' CURR STATE ->' + self.holds
	
	def __unicode__(self): return "State"

	def move_0(self): self.next_1.holds += "0"
	def move_1(self): self.next_0.holds += "1"
			

class DFA:
	def __init__(self, states): 
		self.states = states
		self.pointer = 0

	# def update(self):
	# 	self.states[self.pointer].update()
	# 	if self.states[self.pointer].final: print(self.states[self.pointer].holds)
	# 	self.pointer = (self.pointer + 1) % len(self.states)
	
	def string_assert(self, s: str):
		pointer = self.states[0]
		for i in s:
			if i == '0':
				pointer.move_0()
				pointer = pointer.next_0
			elif i == '1':
				pointer.move_1()
				pointer = pointer.next_1
			else:
				raise Exception('Value other than 0 or 1 given')
		# print(pointer)
		return True if pointer.final else False

		



zero = State("q0")
one = State("q1",True)
zero.next_0 = one 
zero.next_1 = zero
one.next_1 = zero
one.next_0 = one 

dfa = DFA([zero, one])

# print(dfa.string_assert(""))
# print(dfa.states[1].__repr__())
# assert dfa.string_assert("10111") == False


def builder(r : int) -> DFA:
	states = [State(f"q{i}") for i in range(r)]
	for state in states:
		state.next_0 = states[int(input(f"Enter next_0 for {state.name} : "))]
		state.next_1 = states[int(input(f"Enter next_1 for {state.name} : "))]
	# f = int(input("Final state : "))
	X = map(int, input(" finals :-> ").split())
	for f in X: states[f].final = True
	return DFA(states)

def mat_builder(mat: list) -> DFA:
	states = [State(f"q{i+1}") for i in range(len(mat) -1)]
	print(len(states))
	for i, state in enumerate(states):
		state.next_0 = states[mat[i][0] - 1]
		state.next_1 = states[mat[i][1] - 1]
		# print(i, state.next_1, state.next_0)

	for i in mat[-1]: 
		states[i - 1].final = True
	return DFA(states)

def dfa_dfs(state : State, string :str) -> str:
	try:
		key = {"0": "a", "1": "b"}
		if state.final:
			print("".join([key[a] for a in string]))
			yield string
		i  = random.randint(0, 100)
		if i&1:
			yield from dfa_dfs(state.next_0, string+"0")
			yield from dfa_dfs(state.next_1, string+"1")
		else:
			yield from dfa_dfs(state.next_1, string+"1")
			yield from dfa_dfs(state.next_0, string+"0")
	except RecursionError as e:
		# print("--------")
		raise Exception("RecursionDepthError")

D = mat_builder([[2, 2], 
				 [3, 3],
				 [4, 4],
				 [5, 4],
				 [5, 6], 
				 [5, 7], 
				 [8, 9],
				 [10, 11],
				 [12, 10], 
				 [5, 4], 
				 [5, 7], 
				 [5, 4], 
				 [7, 8, 9, 10, 11, 12]])


# ============================================================================#

def assert_function(string: str) -> bool: 
	def strStr(haystack, needle):
		if needle == "":
		    return 0
		for i in range(len(haystack)-len(needle)+1):
			    for j in range(len(needle)):
			    	if haystack[i+j] != needle[j]: 
			    		break
			    	if j == len(needle)-1:
			        	return i
		return -1

	i = strStr(string[::-1], "bba")
	if i == -1: return 0
	if i>2: return 0
	return 1


def run_dfs(n : int) -> None:
	p, assert_passes = 0, 0
	for _ in range(n):
		try:
			for i in dfa_dfs(D.states[0], ""): 
				key = {"0": "a", "1": "b"}
				j = "".join([key[a] for a in i])
				if not assert_function(j): 
					print("error -> ", j)
				else:
					assert_passes += 1
				p += 1
		except Exception as e:
			if e.args[0] == "RecursionDepthError":
				pass
			pass
	return (p, assert_passes)

p = run_dfs(1000)
print(f"rate -> {p[0]/p[0]*100} cases-> {p}")
# key = {"a": "0", "b": "1"}
# key2 = {"0": "a", "1": "b"}

# change = lambda s: "".join([key2[a] for a in s])
# # print(D.string_assert(change("aaaabbabba")))

		
# A="(a*bb*ab*)(a(a*bb*ab*)*)"  
# B="(a+bb*ab*a)*bb*ab*"
# print([key2[a] for a in A])
# print(change(A))