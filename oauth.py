import time
import urllib2
from urlparse import parse_qs
import urllib
from hashlib import sha1
import hmac
import binascii

class OAuth(object):

	consumer_key = ""
	consumer_secret = ""

	request_token = ""
	request_secret = ""

	token = ""
	secret = ""

	request_token_url = ""
	authorize_url = ""
	access_token_url = ""

	def getRequestToken(self):
		url = OAuthUrl()
		url.flush()
		url.setMethod("GET")
		url.setBaseUrl(self.request_token_url)
		url.addParam("oauth_version", "1.0")
		url.addParam("oauth_nonce", str(int(int(time.time()))))
		url.addParam("oauth_timestamp", str(int(int(time.time()))))
		url.addParam("oauth_consumer_key", self.consumer_key)
		url.addParam("oauth_signature_method", "HMAC-SHA1")
		url.addParam("oauth_callback", "oob")
		url.sortParams()
		response = self.executeRequest(url.signRequest(self.consumer_secret))
		self.request_token = response["oauth_token"][0]
		self.request_secret = response["oauth_token_secret"][0]

	def getAuthorizeUrl(self):
		url = OAuthUrl()
		url.flush()
		url.setMethod("GET")
		url.setBaseUrl(self.authorize_url)
		url.addParam("oauth_consumer_key", self.consumer_key)
		url.addParam("oauth_token", self.request_token)
		url.sortParams()
		return url.getRequestUrl()

	def getAccessToken(self, verifier):
		url = OAuthUrl()
		url.flush()
		url.setMethod("GET")
		url.setBaseUrl(self.access_token_url)
		url.addParam("oauth_version", "1.0")
		url.addParam("oauth_nonce", str(int(int(time.time()))))
		url.addParam("oauth_timestamp", str(int(int(time.time()))))
		url.addParam("oauth_consumer_key", self.consumer_key)
		url.addParam("oauth_signature_method", "HMAC-SHA1")
		url.addParam("oauth_token", self.request_token)
		url.addParam("oauth_verifier", verifier)
		url.sortParams()
		
		path = url.signRequest(self.consumer_secret, self.request_secret)
		response = self.executeRequest(path)
		self.token = response["oauth_token"][0]
		self.secret = response["oauth_token_secret"][0]

	def get(self, method, path):
		url = OAuthUrl()
		url.flush()
		url.setMethod(method)
		url.setBaseUrl(path)
		url.addParam("oauth_version", "1.0")
		url.addParam("oauth_nonce", str(int(int(time.time()))))
		url.addParam("oauth_timestamp", str(int(int(time.time()))))
		url.addParam("oauth_consumer_key", self.consumer_key)
		url.addParam("oauth_signature_method", "HMAC-SHA1")
		url.addParam("oauth_token", self.token)
		url.sortParams()
		return url.signRequest(self.consumer_secret, self.secret)

	def executeRequest(self, url):
		response = urllib2.urlopen(url)
		data = response.read()
		return parse_qs(data)

class OAuthUrl(object):

	params = []
	method = ""
	base_url = ""

	def addParam(self,name,value):
		self.params.append(
			{
				"name":name,
				"value":value
			}
		)

	def flush(self):
		del self.params[:]

	def setMethod(self,method):
		self.method = method

	def setBaseUrl(self, url):
		self.base_url = url

	def sortParams(self):
		self.params.sort(key=lambda x: x["name"])

	def getRequestUrl(self):
		params = []

		for param in self.params:
			params.append(param["name"] + "=" + urllib.quote(param["value"],''))

		paramstring = "&".join(params)

		output = []

		for param in self.params:
			output.append(param["name"] + "=" + param["value"])

		return self.base_url + "?" + "&".join(output)

	def signRequest(self, consumer_secret = "", token_secret = ""):
		params = []

		for param in self.params:
			params.append(param["name"] + "=" + urllib.quote(param["value"],''))

		paramstring = "&".join(params)

		baseString = self.method + "&" + urllib.quote(self.base_url,'') + "&" + urllib.quote(paramstring, '')

		signature = self.sign(baseString, consumer_secret + "&" + token_secret)

		self.addParam("oauth_signature", urllib.quote(signature,''))

		output = []

		for param in self.params:
			output.append(param["name"] + "=" + param["value"])

		return self.base_url + "?" + "&".join(output)

	def sign(self, baseString, password):
		hashed = hmac.new(password, baseString, sha1)
		return binascii.b2a_base64(hashed.digest())[:-1]
