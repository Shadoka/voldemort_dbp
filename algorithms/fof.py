import voldemort
import sys
import time
from pprint import pprint

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])

# Returns a set containing the friends of all the friends the specified author has.
# author: The author to calculate the friends of his friends of
def friendsOfFriends(author):
	rootAuthor = authorStore.get(author)[0][0]
	result = set()
	for friend in rootAuthor["friends"]:
		friendAuthor = authorStore.get(str(friend))[0][0]
		for friendFriend in friendAuthor["friends"]:
			result.add(friendFriend)
	if author in result:
		result.remove(author)
	return result

if len(sys.argv) != 2:
	print("I need exactly one argument, which is the name of the author")
else:
	timer = time.time
	start = timer()
	result = friendsOfFriends(sys.argv[1])
	end = timer()
	print(sys.argv[1] + " hat folgende Freundesfreunde:")
	pprint(result)
	print("Laufzeit: " + str(end - start) + " Sekunden")