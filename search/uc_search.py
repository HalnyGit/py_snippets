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
			
class UCSNode(SearchNode):
	def __init__(self, action, state, parent, actionCost):
		self.action = action
		self.state = state
		self.parent = parent
		if self.parent:
			self.cost = self.parent.cost + actionCost
		else:
			self.cost = actionCost


def map1distsuccessors(s, a):
	"""
	Return the succesor of node
	accordint to the action taken
	s - string - node.state
	a - integer
	"""
	return map1dist[s][a]
	
def map1distLegalActions(p):
	"""
	Return the list of possible actions
	for the node
	"""
	return range(len(map1dist[p]))


## uniform cost search
map1dist = {'S':[('A', 2), ('B', 1)],
			'A':[('S', 2), ('C', 3), ('D', 2)],
			'B':[('S', 1), ('D', 2), ('E', 3)],
			'C':[('A', 2), ('F', 1)],
			'D':[('A', 2), ('B', 2), ('F', 4), ('H', 6)],
			'E':[('B', 3), ('H', 2)],
			'F':[('C', 1), ('D', 4), ('G', 1)],
			'G':[('F', 1), ('H', 4)],
			'H':[('D', 6), ('E', 2), ('G', 4)]}

def uc_search(initialState, goalTest, actions, successor):	
	if goalTest(initialState):
		return [(None, initialState)]
	startNode = UCSNode(None, initialState, None, 0)
	agenda = PriorityQueue()	
	agenda.push((0, startNode))
	expanded = {}
	while not agenda.isEmpty():
		n = agenda.pop()[1]
		if not expanded.has_key(n.state):
			expanded[n.state] = True
		if goalTest(n.state):
			return n.path()
		for a in actions(n.state):
			(newS, cost) = successor(n.state, a)
			if not expanded.has_key(newS):
				newN = UCSNode(a, newS, n, cost)
				agenda.push((newN.cost, newN))
	return None

print uc_search('S', lambda x: x == 'G', map1distLegalActions, map1distsuccessors)




