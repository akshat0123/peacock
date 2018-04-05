
def process_tweet(raw):
	""" Takes in raw tweet text and returns cleaned text
	"""
	# 1. replace the url with single space
	rm_urls = re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'," ",raw)

	# 2. removing the RT
	# rm_RT = if this tweet contains RT then remove the whole tweet

	# 3. remove the @ # ??
	letters_only = re.sub("[^a-zA-Z]"," ",rm_RT)
	# 4. Find out how the picture
	# 5. emoji
	pass
