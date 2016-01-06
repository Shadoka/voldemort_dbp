import voldemort

authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
contentStore = voldemort.StoreClient('contentStore', [{'0', 6666}])

# {"lastActivity":created, "content":[commentId], "friends":[prevAuthor], "name":commentAuthor}

def data():
	nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
	created = 0.0
	authorStore.put('_authors', {"lastActivity":None, "content":nodes, "friends":None, "name":"_authors"});
	authorStore.put('A', {"lastActivity":created, "content":[], "friends":['B'], "name":'A'})
	authorStore.put('B', {"lastActivity":created, "content":[], "friends":['C'], "name":'B'})
	authorStore.put('C', {"lastActivity":created, "content":[], "friends":['D', 'E'], "name":'C'})
	authorStore.put('D', {"lastActivity":created, "content":[], "friends":['A', 'E'], "name":'D'})
	authorStore.put('E', {"lastActivity":created, "content":[], "friends":['C', 'F'], "name":'E'})
	authorStore.put('F', {"lastActivity":created, "content":[], "friends":['G', 'I'], "name":'F'})
	authorStore.put('G', {"lastActivity":created, "content":[], "friends":['F', 'H'], "name":'G'})
	authorStore.put('H', {"lastActivity":created, "content":[], "friends":['J'], "name":'H'})
	authorStore.put('I', {"lastActivity":created, "content":[], "friends":['G', 'F'], "name":'I'})
	authorStore.put('J', {"lastActivity":created, "content":[], "friends":['I'], "name":'J'})

data()