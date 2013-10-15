from oauth import OAuth

class Fitbit(OAuth):

	def __init__(self, consumer_key, consumer_secret):
		self.request_token_url = "http://api.fitbit.com/oauth/request_token"
		self.authorize_url = "http://www.fitbit.com/oauth/authorize"
		self.access_token_url = "http://api.fitbit.com/oauth/access_token"

		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
