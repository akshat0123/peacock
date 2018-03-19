# Peacock
Twitter popularity gaining agent

## Dependencies
[tweepy](https://github.com/tweepy/tweepy) - `pip3 install tweepy`

## Running instructions
1. Fill in the relevant credential fields in the 'credentials.py' document using your Twitter API key information

	```
	credentials = {
		'username': '[the twitter username for the agent's account]',
		'consumer_key': '[twitter API consumer key]',
		'consumer_secret': '[twitter API consumer secret]',
		'access_token': '[twitter API access token]',
		'access_token_secret': '[twitter API access token secret]'
	}
	```

2. Fill in list of initial influencers by twitter username in 'influencers.py'

	```
	influencers = ['[username]', '[username 2]', '[username 3']]
	```

3. Run with `python3 main.py`
