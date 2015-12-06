import voldemort

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
stack = []
components = []
index = 0

def tarjan():
	voldemortResult = authorStore.get("_authors")
	allAuthors = voldemortResult[0][0]
	nodes = {}
	for author in allAuthors.get("content"):
		nodeKey = str(author)
		temp = authorStore.get(nodeKey)
		nodeValue = [temp[0][0], -1, -1, False, []]
		#node = Tupel aus den Autorendaten, index(int), lowlink(int), onStack(boolean)
		nodes[nodeKey] = nodeValue
	for nodeKey in nodes:
		node = nodes.get(nodeKey)
		if node[1] == -1:
			strongconnect(node, nodes)
	for scc in components:
		print("==> NEUE KOMPONENTE")
		for node in scc:
			print(node[2])
	print("Insgesamt sind es " + str(len(components)) + " Komponenten")

def strongconnect(node, allNodes, pre=None):
	global index
	if pre != None:
		node[4].append(pre)
	node[1] = index
	node[2] = index
	index += 1
	stack.append(node)
	node[3] = True
	for kanteKey in node[0].get("friends"):
		kanteNode = allNodes.get(str(kanteKey))
		if kanteNode not in node[4]:
			if kanteNode[1] == -1:
				strongconnect(kanteNode, allNodes, node)
				node[2] = min(node[2], kanteNode[2])
			elif kanteNode[3] == True:
				node[2] = min(node[2], kanteNode[1])
	if node[1] == node[2]:
		scc = []
		prevNode = None
		while prevNode != node:
			prevNode = stack.pop()
			prevNode[3] = False
			scc.append(prevNode)
		components.append(scc)

tarjan()