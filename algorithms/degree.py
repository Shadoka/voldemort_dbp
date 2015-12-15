import voldemort
import sys

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
usage = "Usage:\n<name>:\tCalculates the degree centrality of the given node\nmin:\tCalculates the minimal degree centrality of all the nodes in the graph\nmax:\tCalculates the maximal degree centrality of all the nodes in the graph"

# Calculates the degree centrality of the specified author.
# author: The author to calculate the degree centrality for
def degree(author):
	voldemortResultAuthor = authorStore.get(author)
	voldemortResultAllAuthors = authorStore.get("_authors")
	allAuthors = voldemortResultAllAuthors[0][0]
	node = voldemortResultAuthor[0][0]
	amountEdges = len(node["friends"]) + 0.0
	amountOfAllNodes = len(allAuthors["content"]) + 0.0
	result = amountEdges / amountOfAllNodes
	return (author, result)

# Calculates the degree of all authors in the database and returns them.
def calculate_degree_of_all_authors():
	voldemortResultAllAuthors = authorStore.get("_authors")
	allAuthors = voldemortResultAllAuthors[0][0]
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
