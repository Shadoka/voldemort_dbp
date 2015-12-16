import voldemort
import praw
import sys

user_agent = "keyvalue_graphdata by u/theshadoka ver 0.1"
# reddit connection
r = praw.Reddit(user_agent)
# database connections
authorStore = voldemort.StoreClient('authorStore', [{'0', 6666}])
contentStore = voldemort.StoreClient('contentStore', [{'0', 6666}])
usage = "<subreddit>:\tImports the hottest thread in the specified subreddit\n<subreddit> <amount>:\tImports the the specified amount of hottest threads of the specified subreddit"

# This function returns "hottest" threads in a specific subreddit.
# subreddit: The subreddit to fetch threads from
# amount: 	 The amount of threads to fetch
def getHottestInSubreddit(subreddit, amount):
	subs = r.get_subreddit(subreddit).get_hot(limit=amount)
	return subs

# This function traverses recursively through all given comments and their subcomments.
# It extracts the neccessary information into the structures used to persist the data into the database.
# authors: 				Set of all authors encountered during the import
# content_per_author: 	Map: author -> data of the author
# content:				Map: content -> data of the content
# prevAuthor:			The author on whose comment is commented on by the current comments
# subTitle:				The title of the thread this comment is placed in
# comments:				The comments to iterate over 
def traverseComments(authors, content_per_author, content, prevAuthor, subTitle, comments):
	if comments != None:
		for c in comments:
			created = c.created
			commentAuthor = str(c.author)
			commentId = str(c.id)
			authors.add(commentAuthor)
			content[commentId] = {"title":subTitle, "date":created}
			cpa = content_per_author.get(commentAuthor)
			if cpa == None:
				content_per_author[commentAuthor] = {"lastActivity":created, "content":[commentId], "friends":[prevAuthor], "name":commentAuthor}
			else:
				cpa.get('content').append(commentId)
				cpa.get('friends').append(prevAuthor)
				if cpa.get('lastActivity') < created:
					cpa['lastActivity'] = created
				content_per_author[commentAuthor] = cpa
			traverseComments(authors, content_per_author, content, commentAuthor, subTitle, c.replies)

# Persists all authors it is given into the database.
# authors: 					Set of all authors
# content_per_author: Map: 	author -> data of the author
def persistAuthors(authors, content_per_author):
	# little hack to know which authors are stored in the database
	authorStore.put("_authors", {"lastActivity":None, "content":authors, "friends":None, "name":"_authors"})
	for author in authors:
		content = content_per_author.get(author)
		# make the list of friends of an author unique
		content['friends'] = list(set(content.get('friends')))
		authorStore.put(author, content)
	print("==> authoren sind persistiert")

# Persists all comments and submissions into the database.
# content: Map: content -> data of the content
def persistContent(content):
	for key in content:
		contentStore.put(key, content.get(key))
	print("==> content ist persistiert")

# Persists all data into the database.
# authors: 					Set of all authors
# content_per_author: Map: 	author -> data of the author
# content: 					Map: content -> data of the content
def persist(authors, content_per_author, content):
	persistAuthors(authors, content_per_author)
	persistContent(content)
	print("==> persistierung ist abgeschlossen")

# Imports the specified amount of threads from the specified subreddit into the database, following these steps:
# 1. Fetch data from reddit
# 2. Extract the required information from the reddit data structure
# 3. Persist into the database
# subreddit: The subreddit to fetch the data from
# amount: 	 The amount of threads to fetch
def importData(subreddit, amount=1):
	print("==> import gestartet")
	print(amount)
	submissions = getHottestInSubreddit(subreddit, amount)
	authors = set()
	content_per_author = {}
	content = {}
	for sub in submissions:
		subAuthor = str(sub.author)
		subTitle = sub.title
		subId = str(sub.id)
		sub.replace_more_comments(limit=None, threshold=0)
		authors.add(subAuthor)
		content[subId] = {"title":subTitle, "date":sub.created}
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

if len(sys.argv) == 1:
	print(usage)
elif len(sys.argv) == 2:
	importData(sys.argv[1])
elif len(sys.argv) == 3:
	importData(sys.argv[1], sys.argv[2])
else:
	print(usage)