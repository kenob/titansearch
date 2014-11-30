import oauth2
import urllib2 as urllib
import json
from apikeys import Keys 
api_key = Keys.api_key
api_secret = Keys.api_secret
access_token_key = Keys.access_token_key
access_token_secret = Keys.access_token_secret

oauth_token = oauth2.Token(key=access_token_key, secret=access_token_secret )
oauth_consumer = oauth2.Consumer(key=api_key, secret = api_secret)

http_method = "GET"

_debug = 0

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

signature_method_hmac_sha1 = oauth2.SignatureMethod_HMAC_SHA1()
def twitterRequest(url, method, parameters):
    request = oauth2.Request.from_consumer_and_token(oauth_consumer, token=oauth_token, http_method=method, http_url=url, parameters=parameters)
    request.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    if http_method == "POST":
        encoded_post_data = request.to_postdata()
    else:
        encoded_post_data = None
        url = request.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

def search_twitter(search_term):
    url = "https://api.twitter.com/1.1/search/tweets.json?language=en&q="+search_term

    print "search term : " + search_term
    parameters = []
    response = twitterRequest(url, "GET", parameters)
    jsonresponse = json.load(response)

    print "keys" + str(jsonresponse.keys())
    results = []
    if (u'statuses' in jsonresponse):
        statuses = jsonresponse[u'statuses']
        tweet_count = len(statuses);
        if(len(statuses) > 3):
            tweet_count = 3;
        else:
            tweet_count = len(statuses);
        for i in xrange(tweet_count):
            results.append(statuses[i][u'text'])  

        # for result in results:
        #     print result
        return results
    return results;

def main():
    search_term = str(raw_input("Enter the search term : "))
    search_twitter(search_term);



if (__name__ == "__main__"):
    main()