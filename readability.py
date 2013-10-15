from oauth import OAuth

class Readability(OAuth):

	def __init__(self, consumer_key, consumer_secret):
		self.request_token_url = "https://www.readability.com/api/rest/v1/oauth/request_token/"
		self.authorize_url = "https://www.readability.com/api/rest/v1/oauth/authorize/"
		self.access_token_url = "https://www.readability.com/api/rest/v1/oauth/access_token/"

		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
