import feedparser

feed = feedparser.parse( "https://www.reddit.com/r/Python/.rss?limit=100" )
for post in feed.entries:
	print("{0},0".format(post.title.replace(',', ' ')))
