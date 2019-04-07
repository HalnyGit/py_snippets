
class Queue(object):
	"""
	Object that queues elements
	returning them on FIFO basis.
	"""
	def __init__(self):
		self.data = []
	def push(self, item):
		self.data.append(item)
	def pop(self):
		return self.data.pop(0)
	def isEmpty(self):
		return self.data is []

class Stack(object):
	"""
	Object that stacks elements
	returning them on LIFO basis.
	"""
	def __init__(self):
		self.data = []
	def push(self, item):
		self.data.append(item)
	def pop(self):
		return self.data.pop()
	def isEmpty(self):
		return self.data is []

class PriorityQueue(object):
	"""
	Object that queues elements
	the lowest valued entries are retrived first
	a typical pattern for entries is a tuple in the form: (priority_number, data)
	"""
	def __init__(self):
		self.data = []
	def push(self, item):
		self.data.append(item)
	def pop(self):
		self.data.sort()
		return self.data.pop(0)
	def isEmpty(self):
		return self.data is []

class SearchNode(object):
	def __init__(self, action, state, parent):
		self.action = action		
		self.state = state
		self.parent = parent		
	def path(self):
		if self.parent == None:
			return[(self.action, self.state)]
		else:
			return self.parent.path() + [(self.action, self.state)]		
	def inPath(self, s):
		if s == self.state:
			return True
		elif self.parent == None:
			return False
		else:
			return self.parent.inPath(s)
			
map1 = {'S':['A', 'B'],
		'A':['S', 'C', 'D'],
		'B':['S','D','E'],
		'C':['A', 'F'],
		'D':['A', 'B', 'F', 'H'],
		'E':['B', 'H'],
		'F':['C', 'D', 'G'],
		'G':['F', 'H'],
		'H':['D', 'E', 'G']}

def map1successors(s, a):
	"""
	Return the succesor of node
	accordint to the action taken
	s - string - node.state
	a - integer
	"""
	return map1[s][a]
	
def map1LegalActions(p):
	"""
	Return the list of possible actions
	for the node
	"""
	return range(len(map1[p]))

## depth-first-search	
def dfs(initialState, goalTest, actions, successor):
	agenda = Stack()
	if goalTest(initialState):
		return [(None, initialState)]
	agenda.push(SearchNode(None, initialState, None))
	while not agenda.isEmpty():
		parent = agenda.pop()
		newChildStates = []
		for a in actions(parent.state):
			newS = successor(parent.state, a)
			newN = SearchNode(a, newS, parent)
			if goalTest(newS):
				return newN.path()
			elif newS in newChildStates:
				pass
			# don't consider any path that visits the same state twice
			elif parent.inPath(newS):
				pass
			else:
				newChildStates.append(newS)
				agenda.push(newN)
	return None
	
print dfs('S', lambda x: x == 'F', map1LegalActions, map1successors)

## breadth-first-search
def bfs(initialState, goalTest, actions, successor):
	agenda = Queue()
	if goalTest(initialState):
		return [(None, initialState)]
	agenda.push(SearchNode(None, initialState, None))
	while not agenda.isEmpty():
		parent = agenda.pop()
		newChildStates = []
		for a in actions(parent.state):
			newS = successor(parent.state, a)
			newN = SearchNode(a, newS, parent)
			if goalTest(newS):
				return newN.path()
			elif newS in newChildStates:
				pass
			# don't consider any path that visits the same state twice
			elif parent.inPath(newS):
				pass
			else:
				newChildStates.append(newS)
				agenda.push(newN)
	return None

print bfs('S', lambda x: x == 'F', map1LegalActions, map1successors)

## dynamic programming depth/breadth-first-search
def dp_search(initialState, goalTest, actions, successor, depthFirst = False,
			maxNodes = 100000):
	"""
	depthFirst = False for breadth-first-search
	"""
	if depthFirst:
		agenda = Stack()
	else:
		agenda = Queue()
	
	if goalTest(initialState):
		return [(None, initialState)]
	agenda.push(SearchNode(None, initialState, None))
	visited = {initialState: True}
	count = 1
	while not agenda.isEmpty() and maxNodes > count:
		parent = agenda.pop()
		for a in actions(parent.state):
			newS = successor(parent.state, a)
			newN = SearchNode(a, newS, parent)
			if goalTest(newS):
				return newN.path()
			elif visited.has_key(newS):
				pass
			else:
				count += 1
				visited[newS] = True
				agenda.push(newN)
	return None

print dp_search('S', lambda x: x == 'F', map1LegalActions, map1successors, False)











