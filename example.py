from twitter import *

o = Twitter("your-consumer-key","your-consumer-secret")
o.getRequestToken()
print o.getAuthorizeUrl()
verifier = raw_input("Verifier:")
o.getAccessToken(verifier)

while(1 == 1):
	m = raw_input("Method:")
	u = raw_input("URL:")
	print o.get(m,u)
