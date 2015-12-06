import voldemort
import sys
from pprint import pprint

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
usage = "Usage:\n<show>:\tShows all authors stored in the database\n<show> <name>:\tShows details of an author"

def show(author="_authors"):
	result = authorStore.get(author)
	pprint(result[0][0])

if len(sys.argv) == 1:
	print(usage)
elif len(sys.argv) == 2:
	if sys.argv[1] == "show":
		show()
	else:
		print(usage)
elif len(sys.argv) == 3:
	if sys.argv[1] == "show":
		show(sys.argv[2])
	else:
		print(usage)
else:
	print(usage)