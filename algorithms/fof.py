import voldemort
import sys

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])

def friendsOfFriends(author):
	voldemortResult = authorStore.get(author)
	rootAuthor = voldemortResult[0][0]
	result = set()
	for friend in rootAuthor["friends"]:
		fofHelper(str(friend), result)
	if author in result:
		result.remove(author)
	print(result)

def fofHelper(name, result):
	voldemortResult = authorStore.get(name)
	friendAuthor = voldemortResult[0][0]
	for friend in friendAuthor["friends"]:
		result.add(friend)

if len(sys.argv) != 2:
	print("I need exactly one argument, which is the name of the author")
else:
	friendsOfFriends(sys.argv[1])