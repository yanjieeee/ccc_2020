import couchdb
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from urllib3.exceptions import ProtocolError

# Account information
Consumer_key = 'W225IVMaLWc3Cio8Y2ZwHmwXT'
Consumer_secret = 'D0Gebz3e1xqrSKKCNbQPCwLsjNdQVZxHguLekTU4zCavWysswy'
Access_token = '1121041186305630208-vVcpClv576aYx9OJjVaWJkYA89m7eI'
Access_token_secret = 'ZjUk3ppAaudL4KR3oDQo3K6lDMZRKrnGvj2wYRpzfx1uP'

# Connect to Twitter API
auth = OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_token_secret)


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

    # def on_data(self, data):
    #     try:
    #         print(data)
    #         # 'a' 附加方式打开 ， 'w' 写入方式打开
    #         # with open('Streaming.json', 'a') as tf:
    #         #     tf.write(data)
    #         return True
    #     except BaseException as e:
    #         print("Error on_data %s" % str(e))
    #     return True

    def on_status(self, status):
        tweet = status._json
        try:
            if Filter(tweet):
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
                print(Dict, '\n')
                db.save(Dict)
        except couchdb.http.ResourceConflict:
            pass

    def on_error(self, status):
        if status == 420:
            # return false on_status method in case rate limit occurs
            return False


if __name__ == '__main__':
    # ----------------------------------------------CloudDB-------------------------------------------------------------
    server = couchdb.Server('http://admin:admin@172.26.130.124:5984/')
    db_name = 'db_status_filter_test'

    try:
        db = server.create(db_name)
    except:
        db = server[db_name]

    print('-----------------------------------------CouchDB Connected-------------------------------------------------')

    # ----------------------------------------------Stream--------------------------------------------------------------

    # Searching tweets by keywords and save into CouchDB
    KeyWords = ['COV19', 'COV-19', 'cov19', 'cov-19', 'coronavirus',
                'virus', 'epidemic', 'covid19', 'covid_19']
    Stream = Stream(auth, MyListener())
    while True:
        try:
            Stream.filter(track=KeyWords, locations=[112, -45.5, 155.1, -9.1])
        except ProtocolError:
            continue
