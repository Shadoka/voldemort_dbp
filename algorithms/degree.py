import voldemort
import sys
import time

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
usage = "Usage:\n<name>:\tCalculates the degree centrality of the given node\nmin:\tCalculates the minimal degree centrality of all the nodes in the graph\nmax:\tCalculates the maximal degree centrality of all the nodes in the graph\nin <name>:\tCalculates the ingoing degree of an author\nout <name>:\tCalculates the outgoing degree of an author"

# Calculates the degree centrality of the specified author.
# author: 			The author to calculate the degree centrality for
def degree(author):
	indeg = in_degree(author)
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
def in_degree(author):
	node = authorStore.get(author)[0][0]
	allAuthors = authorStore.get("_authors")[0][0]
	amountOfAllNodes = len(allAuthors["content"]) + 0.0
	result = len(node["ingoing"]) / (amountOfAllNodes - 1)
	return (author, result)

# Calculates the degree of all authors in the database and returns them.
def calculate_degree_of_all_authors():
	allAuthors = authorStore.get("_authors")[0][0]
	authorNames = allAuthors["content"]
	degree_results = {}
	for author in authorNames:
		author_degree = degree(str(author))
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

timer = time.time
if len(sys.argv) == 2:
	if sys.argv[1] == "min":
		start = timer()
		minimal = min_degree()
		end = timer()
		print("Die geringste Degree Centrality besitzt " + minimal[1] + " mit " + str(minimal[0]))
		print("Laufzeit: " + str(end - start) + " Sekunden")
	elif sys.argv[1] == "max":
		start = timer()
		maximal = max_degree()
		end = timer()
		print("Die maximale Degree Centrality besitzt " + maximal[1] + " mit " + str(maximal[0]))
		print("Laufzeit: " + str(end - start) + " Sekunden")
	else:
		start = timer()
		degree = degree(sys.argv[1])
		end = timer()
		print(degree[0] + " has a centrality of " + str(degree[1]))
		print("Laufzeit: " + str(end - start) + " Sekunden")
elif len(sys.argv) == 3:
	if sys.argv[1] == "in":
		start = timer()
		indeg = in_degree(sys.argv[2])
		end = timer()
		print(indeg[0] + " besitzt eine ingoing Degree Centrality von " + (str(indeg[1])))
		print("Laufzeit: " + str(end - start) + " Sekunden")
	elif sys.argv[1] == "out":
		start = timer()
		outdeg = out_degree(sys.argv[2])
		end = timer()
		print(outdeg[0] + " besitzt eine outgoing Degree Centrality von " + str(outdeg[1]))
		print("Laufzeit: " + str(end - start) + " Sekunden")
	else:
		print(usage)
else:
	print(usage)
