import tweepy
#import jsonpickle
import couchdb
import datetime
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError

# Account information
Consumer_key = 'A5lwUu9yqsv54TTv4uoCIUQXO'
Consumer_secret = 'rxuQ3ApIlLTGniLWIMDLmw2DLOsmQmGt3ZYcAtGCWgXtuRlPNj'
Access_token = '1252564827119030274-qJftxH0BF7PgBftPCJApzQCqZVjFQX'
Access_token_secret = 'lwJaxXvrZsoa0uV0hwv31jrZLy6Ishj0dPopY4dVaQjbE'

# Connect to Twitter API
auth = OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_token_secret)


# 根据Tweets有无包含地理位置信息筛选
def Filter(tweets):
    # Geo: 纬度，经度  Coordinates： 经度，纬度
    # 澳大利亚纬度范围：南纬10°41'-43°39'之间； 东经112°-154°之间。
    # 筛选条件： 'user' 中'location'为'Australia' 'Geo' 'Coordinates' 'Place' 属于'Australia' 的Tweets
    # AuCities = ['Australia', 'Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Canberra',
    #             'Newcastle', 'Wollongong', 'Logan City', 'Geelong', 'Hobart']

    AuCities = ['australia', 'sydney', 'melbourne', 'brisbane', 'perth', 'adelaide', 'gold coast', 'canberra',
                'newcastle', 'wollongong', 'geelong', 'hobart', 'new south wales', 'victoria',
                'queensland', 'tasmania']

    SameNameList = ['newcastle upon tyne', 'nigeria', 'florida', 'scotland', 'south africa', 'canada',
                    'california', 'mexico', 'oklahoma', 'england', 'melbourne,fl', 'island lagos',
                    'tamaulipas', 'cd victoria', 'melbourne, fl', 'newcastle, uk', 'british', 'columbia',
                    'córdoba', 'la victoria', 'glasgow', 'morthumbria', 'hervey bay', 'leeds', 'méxico',
                    'newcastle-under-lyme', 'ontario']

    # 防止出现别国重名城市
    Temp = False
    if tweets['user']['location'] is not None:
        for item in AuCities:
            if item in tweets['user']['location'].lower():
                for name in SameNameList:
                    if name in tweets['user']['location'].lower():
                        Temp = False
                        break
                    else:
                        Temp = True

    if (tweets['user']['location'] is not None and Temp) \
            or (tweets['geo'] is not None
                and -10.41 <= tweets['geo']['coordinates'][0] <= -43.39
                and 112 <= tweets['geo']['coordinates'][1] <= 154) \
            or (tweets['coordinates'] is not None
                and 112 <= tweets['coordinates']['coordinates'][0] <= 154
                and -10.41 <= tweets['coordinates']['coordinates'][1] <= -43.39) \
            or (tweets['place'] is not None
                and tweets['place']['country_code'] == 'AU'):
        return True
    else:
        return False


# Streaming
class MyListener(StreamListener):

    #def on_data(self, data):
    #    try:
    #        print(data)
    #        # 'a' 附加方式打开 ， 'w' 写入方式打开
    #        with open('Streaming.json', 'a') as tf:
    #            tf.write(data)
    #            return True
    #    except BaseException as e:
    #        print("Error on_data %s" % str(e))
    #    return True

    def on_status(self, status):
        tweet = status._json
        Dict = {}
        if Filter(tweet):
            # print(tweet)
            try:
                Dict = {
                    'ID': tweet['id_str'],
                    'Create_Time': tweet['created_at'],
                    'Text': tweet['text'],
                    'Entities': tweet['entities'],
                    'Source': tweet['source'],
                    'User': tweet['user'],
                    'Geo': tweet['geo'],
                    'Coordinates': tweet['coordinates'],
                    'Place': tweet['place'],
                    'Lang': tweet['lang']
                }
                db.save(Dict)
                #print(Dict, '\n')
            except couchdb.http.ResourceConflict:
                pass
            #with open('Streaming.json', 'a') as f:
            #    f.write(jsonpickle.encode(Dict, unpicklable=False) + '\n')

    def on_error(self, status):
        if status == 420:
            # return false on_status method in case rate limit occurs
            return False

"""
# Searching
def SearchTweets(Keyword, DaysLength, Geocode):
    # geocode: latitude, longitude, radius
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    key = Keyword
    Since_date = datetime.date.today() - datetime.timedelta(days=DaysLength)
    Until_date = datetime.date.today()
    geocode = Geocode
    # geocode: latitude, longitude, radius
    while True:
        try:
            for tweets in tweepy.Cursor(api.search, query=key, since=Since_date, until=Until_date,
                                        geocode=geocode, tweet_mode='extended').items():
                tweet = tweets._json
                # print(tweets, '\n')
                Dict = {}
                if Filter(tweet):
                    try:
                        Dict = {
                            'ID': tweet['id_str'],
                            'Create_Time': tweet['created_at'],
                            'Text': tweet['full_text'],
                            'Entities': tweet['entities'],
                            'Source': tweet['source'],
                            'User': tweet['user'],
                            'Geo': tweet['geo'],
                            'Coordinates': tweet['coordinates'],
                            'Place': tweet['place'],
                            'Lang': tweet['lang']
                        }
                        print(Dict, '\n')
                        # db.save(Dict)
                        with open('Searching.json', 'a') as f:
                            f.write(jsonpickle.encode(Dict, unpicklable=False) + '\n')
                    except couchdb.http.ResourceConflict:
                        pass
        #except ProtocolError:
        #    continue
"""

if __name__ == '__main__':
    # ----------------------------------------------CloudDB-------------------------------------------------------------
    server = couchdb.Server('http://admin:admin@172.26.130.124:5984/')
    db_name = 'db_status_filter_test'

    try:
        db = server.create(db_name)
    except:
        db = server[db_name]

    print('-----------------------------------------CouchDB Connected-------------------------------------------------')

    # ----------------------------------------------Search--------------------------------------------------------------

    # Searching tweets by setting up 'length of days', save into a json file.
    # Output file name: Searching.json
    #key = 'COV19'
    #days = 7
    #geocode = "%f,%f,%fkm" % (-26.9, 133, 2000)
    #SearchTweets(key, days, geocode)
    #print('------------------------------------------End of Searching-------------------------------------------------')

    # ----------------------------------------------Stream--------------------------------------------------------------

    # Searching tweets by keywords and save into a JSON file.
    # Output file name: Streaming.json
    KeyWords = ['COV19', 'COV-19', 'cov19', 'cov-19', 'coronavirus',
                'virus', 'epidemic', 'covid19', 'covid_19']
    Stream = Stream(auth, MyListener())
    while True:
        try:
            Stream.filter(track=KeyWords)
        except ProtocolError:
            continue
