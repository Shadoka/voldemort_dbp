import voldemort
import praw

user_agent = "keyvalue_graphdata by u/theshadoka ver 0.1"
r = praw.Reddit(user_agent)
authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
contentStore = voldemort.StoreClient('contentStore', [{'0', 6666}])

def getHottestInSubreddit(subreddit, amount=1):
	subs = r.get_subreddit(subreddit).get_hot(limit=amount)
	return subs

def traverseComments(authors, content_per_author, content, prevId, comments):
	if comments != None:
		for c in comments:
			commentAuthor = str(c.author)
			commentId = str(c.id)
			authors.add(commentAuthor)
			content[commentId] = {"author":commentAuthor, "prev":prevId}
			cpa = content_per_author.get(commentAuthor)
			if cpa == None:
				content_per_author[commentAuthor] = [commentId]
			else:
				cpa.append(commentId)
				content_per_author[commentAuthor] = cpa
			traverseComments(authors, content_per_author, content, commentId, c.replies)

def persistAuthors(authors, content_per_author):
	authorStore.put("_authors", authors)
	for author in authors:
		authorStore.put(author, content_per_author.get(author))
	print("==> authoren sind persistiert")

def persistContent(content):
	for key in content:
		contentStore.put(key, content.get(key))
	print("==> content ist persistiert")

def persist(authors, content_per_author, content):
	persistAuthors(authors, content_per_author)
	persistContent(content)
	print("==> persistierung ist abgeschlossen")

def importData():
	print("==> import gestartet")
	submissions = getHottestInSubreddit("leagueoflegends")
	authors = set() #brauche ich das set wirklich? hab doch content_per_author
	content_per_author = {}
	content = {}
	for sub in submissions:
		subAuthor = str(sub.author)
		subId = str(sub.id)
		sub.replace_more_comments(limit=None, threshold=0)
		authors.add(subAuthor)
		content[subId] = {"author":subAuthor, "prev":None}
		current = content_per_author.get(subAuthor)
		if current == None:
			content_per_author[subAuthor] = [subId]
		else:
			current.append(subId)
			content_per_author[subAuthor] = current
		traverseComments(authors, content_per_author, content, subId, sub.comments)
	persist(list(authors), content_per_author, content)
	print("==> import abgeschlossen")

importData()