from oauth import OAuth, OAuthUrl

class Twitter(OAuth):

	def __init__(self, consumer_key, consumer_secret):
		self.request_token_url = "https://api.twitter.com/oauth/request_token"
		self.authorize_url = "https://api.twitter.com/oauth/authorize"
		self.access_token_url = "https://api.twitter.com/oauth/access_token"

		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
