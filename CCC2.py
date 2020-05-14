# -*- coding: UTF-8 -*-
import json
#import jsonpickle
import couchdb
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import tweepy
import datetime
#from twython import TwythonStreamer

# Account information
Consumer_key = 'A5lwUu9yqsv54TTv4uoCIUQXO'
Consumer_secret = 'rxuQ3ApIlLTGniLWIMDLmw2DLOsmQmGt3ZYcAtGCWgXtuRlPNj'
Access_token = '1252564827119030274-qJftxH0BF7PgBftPCJApzQCqZVjFQX'
Access_token_secret = 'lwJaxXvrZsoa0uV0hwv31jrZLy6Ishj0dPopY4dVaQjbE'

# Connect to Twitter API
auth = OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_token_secret)


def take2(elem):
    return elem[1]

"""
# 从已筛选后得到的 Dict.json 中读取， 并将地理信息整合到一个List中
def RankingList():
    Total_count = 0
    Cities_List = []

    fileReader = open('Dict.json', 'r', encoding='utf-8')

    for line in fileReader:
        line = line.strip('\n, ')
        if line.startswith('{') and line.endswith('}'):
            try:
                line = json.loads(line)
                tweet = line
                Total_count += 1

                if tweet['Coordinates'] is not None:
                    # print(tweet)
                    # Read_count += 1
                    continue

                elif tweet['Place'] is not None:
                    Cities_List = CityCounter(tweet, Cities_List, 'Place')

                elif tweet['User']['location'] is not None:
                    Cities_List = CityCounter(tweet, Cities_List, 'Location')

            except Exception as e:
                print('卧槽,报错啦 ', str(e))

    # print('\nThere are totally ', Total_count, ' tweets.\n')
    return Cities_List


# 生成一个二维列表， [ ['Name', number of times ], [...] ] 的格式
def CityCounter(tweet, list, mode):

    if mode == 'Place':
        if len(list) == 0:
            list.append([tweet['Place']['name'], 1])
        elif list is not None:
            i = 0
            while i < len(list):
                if tweet['Place']['name'] == list[i][0]:
                    list[i][1] = list[i][1] + 1
                    i = 0
                    break
                elif i != len(list) - 1 and tweet['Place']['name'] != list[i][0]:
                    i += 1
                elif i == len(list) - 1 and tweet['Place']['name'] != list[i][0]:
                    list.append([tweet['Place']['name'], 1])
                    i = 0

    elif mode == 'Location':
        if len(list) == 0:
            list.append([tweet['User']['location'], 1])
        elif list is not None:
            i = 0
            while i < len(list):
                if tweet['User']['location'] == list[i][0]:
                    list[i][1] = list[i][1] + 1
                    i = 0
                    break
                elif i != len(list) - 1 and tweet['User']['location'] != list[i][0]:
                    i += 1
                elif i == len(list) - 1 and tweet['User']['location'] != list[i][0]:
                    list.append([tweet['User']['location'], 1])
                    i = 0
    return list


def TargetCityRanking(RankList, TargetList):

    TargetCityList = TargetCounter(TargetList, RankList)
    TargetCityList.sort(reverse=True, key=take2)
    return TargetCityList


def TargetCounter(TargetList, ResultList):
    Tar_item = 0
    while Tar_item < len(TargetList):
        item = 0
        while item < len(ResultList):
            if TargetList[Tar_item][0].lower() in ResultList[item][0].lower():
                TargetList[Tar_item][1] = TargetList[Tar_item][1] + ResultList[item][1]
                item += 1
            else:
                item += 1
        Tar_item += 1
    return TargetList


def TargetAreaRanking(ranking, area, city, cityRank):
    for item in area:
        for name in ranking:
            Temp = True
            for target in city:
                if target[0] in name[0]:
                    Temp = False
                    break
                else:
                    Temp = True
            if item[0] in name[0] and Temp:
                item[1] = item[1] + name[1]

    CityRank = cityRank

    for item in area:
        for name in CityRank:
            if item[0] == 'Victoria' and name[0] == 'Melbourne':
                item[1] = item[1] + name[1]
            if item[0] == 'New South Wales' and name[0] == 'Sydney':
                item[1] = item[1] + name[1]
            if item[0] == 'Queensland' and name[0] == 'Brisbane':
                item[1] = item[1] + name[1]
            if item[0] == 'West Australia' and name[0] == 'Perth':
                item[1] = item[1] + name[1]
            if item[0] == 'South Australia' and name[0] == 'Adelaide':
                item[1] = item[1] + name[1]
            if item[0] == 'Northern Territory' and name[0] == 'Darwin':
                item[1] = item[1] + name[1]
            if item[0] == 'Tasmania' and name[0] == 'Hobart':
                item[1] = item[1] + name[1]
            if item[0] == 'New South Wales' and name[0] == 'Canberra':
                item[1] = item[1] + name[1]
            if item[0] == 'Queensland' and name[0] == 'Gold Coast':
                item[1] = item[1] + name[1]
            if item[0] == 'Victoria' and name[0] == 'Geelong':
                item[1] = item[1] + name[1]
            if item[0] == 'New South Wales' and name[0] == 'Newcastle':
                item[1] = item[1] + name[1]
            if item[0] == 'New South Wales' and name[0] == 'Wollongong':
                item[1] = item[1] + name[1]
            if item[0] == 'Queensland' and name[0] == 'Cairns':
                item[1] = item[1] + name[1]
            if item[0] == 'Queensland' and name[0] == 'Toowoomba':
                item[1] = item[1] + name[1]
            if item[0] == 'Queensland' and name[0] == 'Townsville':
                item[1] = item[1] + name[1]
            if item[0] == 'Victoria' and name[0] == 'Ballarat':
                item[1] = item[1] + name[1]
            if item[0] == 'Victoria' and name[0] == 'Bendigo':
                item[1] = item[1] + name[1]
            if item[0] == 'Queensland' and name[0] == 'Sunshine Coast':
                item[1] = item[1] + name[1]
            if item[0] == 'Tasmania' and name[0] == 'Launceston':
                item[1] = item[1] + name[1]
    return area

"""
# def Levenshtein_Distance(str1, str2):
#     matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
#
#     for i in range(1, len(str1) + 1):
#         for j in range(1, len(str2) + 1):
#             if (str1[i - 1] == str2[j - 1]):
#                 d = 0
#             else:
#                 d = 1
#
#             matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)
#
#     return matrix[len(str1)][len(str2)]


# 根据Tweets有无包含地理位置信息筛选, 配合status使用
def filter(tweets):
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


# 从本地读取未经处理的json文件，筛选后保存为既定格式的 Dict 并且存入 Dict.json
def getDict(FileName, mode):
    Dict = {}
    Num_tweets = 0
    fileReader = open(FileName, 'r', encoding='utf-8')
    for line in fileReader:
        line = line.strip('\n, ')
        if line.startswith('{') and line.endswith('}'):
            try:
                line = json.loads(line)
                tweet = line

                if filter(tweet):

                    if mode == 'Stream':
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

                    elif mode == 'Search':
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

                    Num_tweets += 1
                    print(Dict, '\n')

                    with open('Dict.json', 'a') as f:
                        f.write(jsonpickle.encode(Dict, unpicklable=False) + '\n')

                    db.save(Dict)
            except Exception as e:
                print('WoW! something happened: ', str(e))

    print('The number of tweets extracted: ', Num_tweets)
    
    return Dict


# Streaming
class MyListener(StreamListener):
    # On_data 速度快，但无法筛选，使用status时标记
    #def on_data(self, data):
    #    try:
    #        print(data)
    #        # 'a' 附加方式打开 ， 'w' 写入方式打开
    #        with open('Tweets_Stream.json', 'a') as tf:
    #            tf.write(data)
    #            return True
    #    except BaseException as e:
    #        print("Error on_data %s" % str(e))
    #    return True

    def on_status(self, status):
        tweets = status._json
    #
        Dict = {}
        if filter(tweets):
            Dict = {
                'ID': tweets['id_str'],
                'Create_Time': tweets['created_at'],
                'Text': tweets['text'],
                'Entities': tweets['entities'],
                'Source': tweets['source'],
                'User': tweets['user'],
                'Geo': tweets['geo'],
                'Coordinates': tweets['coordinates'],
                'Place': tweets['place'],
                'Lang': tweets['lang']
            }
            #print(Dict, '\n')
            # with open('Dict.json', 'a') as f:
            #    f.write(jsonpickle.encode(Dict, unpicklable=False) + '\n')
            db.save(Dict)

    def on_error(self, status):
        if status == 420:
            # return false on_status method in case rate limit occurs
            return False
        print(status)

"""
# Searching
def SearchTweets(DaysLength):
    api = tweepy.API(auth)
    Since_date = datetime.date.today() - datetime.timedelta(days=DaysLength)
    Until_date = datetime.date.today()

    # geocode: latitude, longitude, radius
    for tweets in tweepy.Cursor(api.search,
                                q=['coronavirus'],
                                since=Since_date,
                                until=Until_date,
                                geocode="%f,%f,%fkm" % (-26.9, 133, 2000),
                                count=1000,
                                tweet_mode='extended',
                                lang='en').items():
        tweets = tweets._json
        # print(tweets, '\n')
        Dict = {}
        if filter(tweets):
            Dict = {
                'ID': tweets['id_str'],
                'Create_Time': tweets['created_at'],
                'Text': tweets['full_text'],
                'Entities': tweets['entities'],
                'Source': tweets['source'],
                'User': tweets['user'],
                'Geo': tweets['geo'],
                'Coordinates': tweets['coordinates'],
                'Place': tweets['place'],
                'Lang': tweets['lang']
            }
            # db.save(Dict)
            print(Dict, '\n')
"""

# ---------------------------------------------Main Process-------------------------------------------------------------
if __name__ == '__main__':
    # ----------------------------------------------CloudDB-------------------------------------------------------------

    server = couchdb.Server("http://%s:%s@172.26.133.75:5984/" % ('admin', 'admin'))
    db_name = 'db_tweets_test'
    #
    try:
        db = server.create(db_name)
    except:
        db = server[db_name]

    # ----------------------------------------------Stream--------------------------------------------------------------

    # Searching tweets by keywords and save into a JSON file:

    KeyWords = ['#COV19', '#COV-19', '#cov19', '#cov-19', '#coronavirus',
               '#virus', '#epidemic', '#covid19', '#covid_19']
    Stream = Stream(auth, MyListener())
    Stream.filter(track=KeyWords, locations=[112, -45.5, 155.1, -9.1])

    # ----------------------------------------------Search--------------------------------------------------------------

    # Searching tweets by setting up 'length of days'
    # Updated 2020-04-28 - 2020-05-02
    #
    # Days = 1
    # SearchTweets(Days)

    # --------------------------------------------File Reader-----------------------------------------------------------

    # Reading file from hard-disk and upload to cloud.
    # FileName_St = 'Tweets_Stream.json'
    # mode = 'Stream'
    # Dic_Stream = getDict(FileName_St, mode)

    # ----------------------------------------Data Visualisation--------------------------------------------------------

    # 澳洲主要城市
    Target_Cities = [
        ['Melbourne', 0],
        ['Sydney', 0],
        ['Brisbane', 0],
        ['Perth', 0],
        ['Adelaide', 0],
        ['Darwin', 0],
        ['Canberra', 0],
        ['Hobart', 0],
        ['Gold Coast', 0],
        ['Geelong', 0],
        ['Newcastle', 0],
        ['Wollongong', 0],
        ['Cairns', 0],
        ['Toowoomba', 0],
        ['Townsville', 0],
        ['Ballarat', 0],
        ['Bendigo', 0],
        ['Sunshine Coast', 0],
        ['Launceston', 0],
    ]

    # 澳洲七大洲
    Target_Area = [
        ['Victoria', 0],
        ['New South Wales', 0],
        ['Queensland', 0],
        ['West Australia', 0],
        ['South Australia', 0],
        ['Northern Territory', 0],
        ['Tasmania', 0],
    ]

    # # 从place和location中的信息整合到一个list中
    # Ranking = RankingList()
    # # 读取澳洲八大城市，在list中出现的频数并排序
    # Rank_City = TargetCityRanking(Ranking, Target_Cities)
    # # 读取list中澳洲7个洲出现的频数，并将八大城市的数据加在对应的洲，再排序
    # TargetArea = TargetAreaRanking(Ranking, Target_Area, Target_Cities, Rank_City)
    # TargetArea.sort(reverse=True, key=take2)
    # print('\n', Rank_City, '\n')
    # print(TargetArea, '\n')



    

