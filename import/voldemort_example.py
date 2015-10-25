import voldemort
from pprint import pprint

# verbindungen zu den stores aufbauen
authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
contentStore = voldemort.StoreClient('contentStore', [{'0', 6666}])
# author
authorKey = "shadoka"
authorValue = ["qwert", "asdf"]
# vom author verfasster inhalt, also submissions + comments
contentKey1 = "qwert"
contentValue1 = {"author":"shadoka", "prev":None}
contentKey2 = "asdf"
contentValue2 = {"author":"shadoka", "prev":"qwert"}
# daten in die stores schreiben
authorStore.put(authorKey, authorValue)
contentStore.put(contentKey1, contentValue1)
contentStore.put(contentKey2, contentValue2)
# lesen der daten
authorResponse = authorStore.get("shadoka")
contentsOfShadoka = authorResponse[0][0] # das wirkliche ergebnis steht halt an der stelle

print("contents von shadoka:")
for content in contentsOfShadoka:
    x = contentStore.get(str(content))
    pprint(x[0][0])

authorStore.delete(authorKey)
contentStore.delete(contentKey1)
contentStore.delete(contentKey2)
