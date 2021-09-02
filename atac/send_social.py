from twilio.rest import Client
import facebook
import tweepy

class FromRuXiaWithLove2:

    def send_facebook(self):
        status = 0
        msg = "Hello, world!"
        graph = facebook.GraphAPI(self.config['facebook']['access_token'])
        link = 'https://www.jcchouinard.com/'
        groups = ['744128789503859']
        for group in groups:
            graph.put_object(group, 'feed', message=msg, link=link)
            print(graph.get_connections(group, 'feed'))
        return status

    def send_twitter(self):
        status = 0
        CONSUMER_KEY = self.config['twitter']['consumer_key']
        CONSUMER_SECRET = self.config['twitter']['consumer_secret']
        ACCESS_TOKEN = self.config['twitter']['access_token']
        ACCESS_TOKEN_SECRET = self.config['twitter']['access_token_secret']
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        handles = sys.argv[1]
        f = open(handles, "r")
        h = f.readlines()
        f.close()
        for i in h:
            i = i.rstrip()
            m = i + " " + sys.argv[2]
            s = api.update_status(m)
            nap = randint(1, 60)
            time.sleep(nap)
        return status
        