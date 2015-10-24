import praw

r = praw.Reddit('keyvalue_graphdata by u/theshadoka ver 0.1')
submissions = r.get_subreddit('leagueoflegends').get_hot(limit=3)
for x in submissions:
    print(str(x))
