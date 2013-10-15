from oauth import OAuth

class Github(OAuth):

	def __init__(self, consumer_key, consumer_secret):
		self.request_token_url = "https://github.com/login/oauth/request_token"
		self.authorize_url = "https://github.com/login/oauth/authorize"
		self.access_token_url = "https://github.com/login/oauth/access_token"

		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
