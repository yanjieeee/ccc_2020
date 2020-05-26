import json
import jsonpickle
import couchdb


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
                # print(tweet)
                if len(tweet) != 1 and Filter(tweet):

                    if mode == 'Stream':

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
                            print(Dict, '\n')
                        except couchdb.http.ResourceConflict:
                            pass

                    elif mode == 'Search':

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
                            db.save(Dict)
                            print(Dict, '\n')
                        except couchdb.http.ResourceConflict:
                            pass

                    Num_tweets += 1

            except Exception as e:
                print('WoW! something happened: ', str(e))

    print('The number of tweets extracted: ', Num_tweets)


if __name__ == '__main__':
    # ----------------------------------------------CloudDB-------------------------------------------------------------
    server = couchdb.Server('http://admin:admin@172.26.130.124:5984/')
    db_name = 'db_status_filter_test'

    try:
        db = server.create(db_name)
    except:
        db = server[db_name]
    print('----------------------------------------CouchDB Connected------------------------------------------------')

    # # Reading tweets from hard-disk and upload to cloud.
    FileName_St = 'Data_Stream0507.json'
    mode = 'Stream'  # Stream or Search
    getDict(FileName_St, mode)

    # Reading pre-process data from Dict.json
    fileReader = open('FullDict.json', 'r', encoding='utf-8')
    for line in fileReader:
        line = line.strip('\n, ')
        if line.startswith('{') and line.endswith('}'):
            try:
                line = json.loads(line)
                tweet = line
                # with open('FullDict.json', 'a') as f:
                #     f.write(jsonpickle.encode(Dict, unpicklable=False) + '\n')
                db.save(tweet)
            except Exception as e:
                print('WoW! something happened in Dict: ', str(e))

