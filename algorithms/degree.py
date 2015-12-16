import voldemort
import sys

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
usage = "Usage:\n<name>:\tCalculates the degree centrality of the given node\nmin:\tCalculates the minimal degree centrality of all the nodes in the graph\nmax:\tCalculates the maximal degree centrality of all the nodes in the graph"

# Calculates the degree centrality of the specified author.
# author: 			The author to calculate the degree centrality for
# allAuthorsMap: 	If degree is called from min or max a prefetched map is included for improved performance
def degree(author, allAuthorsMap=None):
	indeg = in_degree(author, allAuthorsMap)
	outdeg = out_degree(author)
	return (author, indeg[1] + outdeg[1])

# Calculates the outgoing degree of an author.
# author: The author to calculate the outgoing degree for
def out_degree(author):
	node = authorStore.get(author)[0][0]
	allAuthors = authorStore.get("_authors")[0][0]
	amountEdges = len(node["friends"]) + 0.0
	amountOfAllNodes = len(allAuthors["content"]) + 0.0
	result = amountEdges / (amountOfAllNodes - 1)
	return (author, result)

# Calculates the ingoing degree of an author.
# author: The author to calculate the ingoing degree for
# allAuthorsMap: 	If degree is called from min or max a prefetched map is included for improved performance
def in_degree(author, allAuthorsMap=None):
	node = authorStore.get(author)[0][0]
	allAuthors = authorStore.get("_authors")[0][0]
	incomingEdges = 0
	for currentName in allAuthors["content"]:
		currentAuthor = None
		if allAuthorsMap != None:
			currentAuthor = allAuthorsMap[currentName]
		else:
			currentAuthor = authorStore.get(str(currentName))[0][0]
		if author in currentAuthor.get("friends"):
			incomingEdges += 1
	amountOfAllNodes = len(allAuthors["content"]) + 0.0
	result = incomingEdges / (amountOfAllNodes - 1)
	return (author, result)

# Calculates the degree of all authors in the database and returns them.
def calculate_degree_of_all_authors():
	allAuthors = authorStore.get("_authors")[0][0]
	authorNames = allAuthors["content"]
	allAuthorsMap = {}
	for name in authorNames:
		allAuthorsMap[name] = authorStore.get(str(name))[0][0]
	degree_results = {}
	for author in authorNames:
		author_degree = degree(str(author), allAuthorsMap)
		degree_results[str(author)] = author_degree[1]
	return degree_results

# Calculates the minimal degree centrality of all nodes in the graph.
def min_degree():
	all_degrees = calculate_degree_of_all_authors()
	minimal = (1.0, "")
	for key in all_degrees:
		if all_degrees.get(key) < minimal[0]:
			minimal = (all_degrees.get(key), key)
	return minimal

# Calculates the maximal degree centrality of all nodes in the graph.
def max_degree():
	all_degrees = calculate_degree_of_all_authors()
	maximal = (0.0, "")
	for key in all_degrees:
		if all_degrees.get(key) > maximal[0]:
			maximal = (all_degrees.get(key), key)
	return maximal

if len(sys.argv) != 2:
	print(usage)
elif sys.argv[1] == "min":
	minimal = min_degree()
	print("Die geringste Degree Centrality besitzt " + minimal[1] + " mit " + str(minimal[0]))
elif sys.argv[1] == "max":
	maximal = max_degree()
	print("Die maximale Degree Centrality besitzt " + maximal[1] + " mit " + str(maximal[0]))
else:
	degree = degree(sys.argv[1])
	print(degree[0] + " has a centrality of " + str(degree[1]))
