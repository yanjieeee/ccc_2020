import tweepy
from tweepy import OAuthHandler
import couchdb
import datetime
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
            for tweets in tweepy.Cursor(api.search, query=key,  geocode=geocode,
                                        since=Since_date, until=Until_date,
                                        tweet_mode='extended', language='en').items():
                tweet = tweets._json
                # if Filter(tweet):
                try:
                    if Filter(tweet):
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
                        db.save(Dict)
                except couchdb.http.ResourceConflict:
                    pass
        except ProtocolError:
            continue


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
    key = 'virus'
    days = 7
    geocode = "%f,%f,%fkm" % (-26.9, 133, 2000)
    SearchTweets(key, days, geocode)
    print('------------------------------------------End of Searching-------------------------------------------------')