import voldemort
import sys

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
usage = "Usage:\n<name>:\tCalculates the degree centrality of the given node\nmin:\tCalculates the minimal degree centrality of all the nodes in the graph"

def degree_internal(author):
	voldemortResultAuthor = authorStore.get(author)
	voldemortResultAllAuthors = authorStore.get("_authors")
	allAuthors = voldemortResultAllAuthors[0][0]
	node = voldemortResultAuthor[0][0]
	amountEdges = len(node["friends"]) + 0.0
	amountOfAllNodes = len(allAuthors["content"]) + 0.0
	result = amountEdges / amountOfAllNodes
	return (author, result)

def degree(author):
	result = degree_internal(author)
	print(result[0] + " has a centrality of " + str(result[1]))

def min_degree():
	voldemortResultAllAuthors = authorStore.get("_authors")
	allAuthors = voldemortResultAllAuthors[0][0]
	authorNames = allAuthors["content"]
	degree_results = {}
	for author in authorNames:
		author_degree = degree_internal(str(author))
		degree_results[str(author)] = author_degree[1]
	minimal = (1.0, "")
	for key in degree_results:
		if degree_results.get(key) < minimal[0]:
			minimal = (degree_results.get(key), key)
	print("Die geringste Degree Centrality besitzt " + minimal[1] + " mit " + str(minimal[0]))
	return minimal

def max_degree():
	voldemortResultAllAuthors = authorStore.get("_authors")
	allAuthors = voldemortResultAllAuthors[0][0]
	authorNames = allAuthors["content"]
	degree_results = {}
	for author in authorNames:
		author_degree = degree_internal(str(author))
		degree_results[str(author)] = author_degree[1]
	maximal = (0.0, "")
	for key in degree_results:
		if degree_results.get(key) > maximal[0]:
			maximal = (degree_results.get(key), key)
	print("Die maximale Degree Centrality besitzt " + maximal[1] + " mit " + str(maximal[0]))
	return maximal

if len(sys.argv) != 2:
	print(usage)
elif sys.argv[1] == "min":
	min_degree()
elif sys.argv[1] == "max":
	max_degree()
else:
	degree(sys.argv[1])
