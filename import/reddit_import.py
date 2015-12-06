import voldemort
import praw
import datetime

user_agent = "keyvalue_graphdata by u/theshadoka ver 0.1"
r = praw.Reddit(user_agent)
authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
contentStore = voldemort.StoreClient('contentStore', [{'0', 6666}])

def getHottestInSubreddit(subreddit, amount=1):
	subs = r.get_subreddit(subreddit).get_hot(limit=amount)
	return subs

def traverseComments(authors, content_per_author, content, prevAuthor, subTitle, comments):
	if comments != None:
		for c in comments:
			created = c.created
			commentAuthor = str(c.author)
			content_per_author.get(prevAuthor).get('friends').append(commentAuthor)
			commentId = str(c.id)
			authors.add(commentAuthor)
			content[commentId] = {"title":subTitle, "date":created}
			cpa = content_per_author.get(commentAuthor)
			if cpa == None:
				content_per_author[commentAuthor] = {"lastActivity":created, "content":[commentId], "friends":[prevAuthor], "name":commentAuthor}
			else:
				cpa.get('content').append(commentId)
				cpa.get('content').append(prevAuthor)
				if cpa.get('lastActivity') < created:
					cpa['lastActivity'] = created
				content_per_author[commentAuthor] = cpa
			traverseComments(authors, content_per_author, content, commentAuthor, subTitle, c.replies)

def persistAuthors(authors, content_per_author):
	authorStore.put("_authors", {"lastActivity":None, "content":authors, "friends":None, "name":"_authors"})
	for author in authors:
		content = content_per_author.get(author)
		content['friends'] = list(set(content.get('friends')))
		authorStore.put(author, content)
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
	submissions = getHottestInSubreddit("leagueoflegends", 2)
	authors = set() #brauche ich das set wirklich? hab doch content_per_author
	content_per_author = {}
	content = {}
	for sub in submissions:
		subAuthor = str(sub.author)
		subTitle = str(sub.title)
		subId = str(sub.id)
		sub.replace_more_comments(limit=None, threshold=0)
		authors.add(subAuthor)
		content[subId] = {"title":subTitle, "date":sub.created}
		# jetzt nicht nur die contentIds, sondern lastActivity+friends
		current = content_per_author.get(subAuthor)
		if current == None:
			content_per_author[subAuthor] = {"lastActivity":sub.created, "content":[subId], "friends":[], "name":subAuthor}
		else:
			current.get('content').append(subId)
			if current.get('lastActivity') < sub.created:
				current['lastActivity'] = sub.created
			content_per_author[subAuthor] = current
		traverseComments(authors, content_per_author, content, subAuthor, subTitle, sub.comments)
	persist(list(authors), content_per_author, content)
	print("==> import abgeschlossen")

importData()