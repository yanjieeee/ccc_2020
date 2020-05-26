import couchdb
import json


def NoDuplicate(tweetID, tw):
    if tw['ID'] not in tweetID:
        tweetID.append(tw['ID'])
        return True
    else:
        return False


def take1(elem):
    return elem[0]


def take2(elem):
    return elem[1]


# 从已筛选后得到的 Dict.json 中读取， 并将地理信息整合到一个List中
def RankingList(FileName, mode):
    Cities_List = []
    Tweets_Num_Count = 0
    if mode == 'Cloud':
        print('-----------------------------Reading Tweets---------------------------------')
        results = db.view('TestDesignDoc/TestView')
        # 从CouchDB读取数据
        for item in results:
            try:
                if 'location' in item.key:
                    Cities_List = CityCounter(item.key, Cities_List, 'CloudLocation')
                    Tweets_Num_Count += 1
                else:
                    Cities_List = CityCounter(item.key, Cities_List, 'CloudPlace')
                    Tweets_Num_Count += 1
            except TypeError as e:
                print(str(e))
                continue

    elif mode == 'Local':
        Tw_ID = []
        print('-----------------------------Reading Tweets---------------------------------')
        fileReader = open(FileName, 'r', encoding='utf-8')
        for line in fileReader:
            line = line.strip('\n, ')
            if line.startswith('{') and line.endswith('}'):
                try:
                    line = json.loads(line)
                    tweet = line
                    if NoDuplicate(Tw_ID, tweet):
                        if tweet['Place'] is not None:
                            Cities_List = CityCounter(tweet, Cities_List, 'Place')
                            Tweets_Num_Count += 1

                        elif tweet['User']['location'] is not None:
                            Cities_List = CityCounter(tweet, Cities_List, 'Location')
                            Tweets_Num_Count += 1

                except Exception as e:
                    print('卧槽,报错啦 ', str(e))

    print('\nThere are totally ', Tweets_Num_Count, ' tweets.\n')

    return Cities_List


# 生成一个二维列表， [ ['Name', number of times ], [...] ] 的格式
def CityCounter(tweet, list, mode):
    if mode == 'Place':
        if len(list) == 0:
            list.append([tweet['Place']['name'], 0])
        elif len(list) != 0:
            i = 0
            while i < len(list):
                if tweet['Place']['name'] == list[i][0]:
                    list[i][1] = list[i][1] + 1
                    break
                elif i != len(list) - 1 and tweet['Place']['name'] != list[i][0]:
                    i += 1
                elif i == len(list) - 1 and tweet['Place']['name'] != list[i][0]:
                    list.append([tweet['Place']['name'], 0])
                    i = 0

    elif mode == 'Location':
        if len(list) == 0:
            list.append([tweet['User']['location'], 0])
        elif len(list) != 0:
            i = 0
            while i < len(list):
                if tweet['User']['location'] == list[i][0]:
                    list[i][1] = list[i][1] + 1
                    break
                elif i != len(list) - 1 and tweet['User']['location'] != list[i][0]:
                    i += 1
                elif i == len(list) - 1 and tweet['User']['location'] != list[i][0]:
                    list.append([tweet['User']['location'], 0])
                    i = 0

    elif mode == 'CloudLocation':
        if len(list) == 0:
            list.append([tweet['location'], 1])
        elif len(list) != 0:
            i = 0
            while i < len(list):
                if tweet['location'] == list[i][0]:
                    list[i][1] = list[i][1] + 1
                    break
                elif i != len(list) - 1 and tweet['location'] != list[i][0]:
                    i += 1
                elif i == len(list) - 1 and tweet['location'] != list[i][0]:
                    list.append([tweet['location'], 1])
                    i = 0

    elif mode == 'CloudPlace':
        if len(list) == 0:
            list.append([tweet['name'], 0])
        elif len(list) != 0:
            i = 0
            while i < len(list):
                if tweet['name'] == list[i][0]:
                    list[i][1] = list[i][1] + 1
                    break
                elif i != len(list) - 1 and tweet['name'] != list[i][0]:
                    i += 1
                elif i == len(list) - 1 and tweet['name'] != list[i][0]:
                    list.append([tweet['name'], 0])
                    i = 0

    return list


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


def TargetCityRanking(RankList):
    # 澳洲主要城市
    TargetList = [
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
        ['Melton', 0],
        ['Central Coast', 0],
        ['Maitland', 0],
        ['Bunbury', 0],
        ['Geraldton', 0],
        ['Albany', 0],
        ['Busselton', 0],
        ['Kalgoorlie', 0],
        ['Gawler', 0],
        ['Mount Gambier', 0],
        ['Whyalla', 0],
        ['Alice Springs', 0],
        ['Launceston', 0],
        ['Katherine', 0],
    ]
    TargetCityList = TargetCounter(TargetList, RankList)
    TargetCityList.sort(reverse=True, key=take2)
    return TargetCityList


def TargetAreaRanking(ranking, cityRank):
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

    for item in Target_Area:
        for name in ranking:
            Temp = True
            for target in cityRank:
                if target[0] in name[0]:
                    Temp = False
                    break
                else:
                    Temp = True
            if item[0] in name[0] and Temp:
                item[1] = item[1] + name[1]

    # 将城市的统计也加入各自州的统计中：
    CityRank = cityRank
    for item in Target_Area:
        for name in CityRank:
            if item[0] == 'Victoria' and (name[0] == 'Melbourne'
                                          or name[0] == 'Ballarat'
                                          or name[0] == 'Bendigo'
                                          or name[0] == 'Geelong'
                                          or name[0] == 'Melton'):
                item[1] = item[1] + name[1]
            if item[0] == 'Queensland' and (name[0] == 'Gold Coast'
                                            or name[0] == 'Cairns'
                                            or name[0] == 'Toowoomba'
                                            or name[0] == 'Townsville'
                                            or name[0] == 'Sunshine Coast'
                                            or name[0] == 'Brisbane'):
                item[1] = item[1] + name[1]
            if item[0] == 'New South Wales' and (name[0] == 'Canberra'
                                                 or name[0] == 'Newcastle'
                                                 or name[0] == 'Wollongong'
                                                 or name[0] == 'Sydney'
                                                 or name[0] == 'Central Coast'
                                                 or name[0] == 'Maitland'):
                item[1] = item[1] + name[1]
            if item[0] == 'West Australia' and (name[0] == 'Perth'
                                                or name[0] == 'Bunbury'
                                                or name[0] == 'Geraldton'
                                                or name[0] == 'Albany'
                                                or name[0] == 'Busselton'
                                                or name[0] == 'Kalgoorlie'):
                item[1] = item[1] + name[1]
            if item[0] == 'South Australia' and (name[0] == 'Adelaide'
                                                 or name[0] == 'Gawler'
                                                 or name[0] == 'Mount Gambier'
                                                 or name[0] == 'Whyalla'):
                item[1] = item[1] + name[1]
            if item[0] == 'Northern Territory' and (name[0] == 'Darwin'
                                                    or name[0] == 'Alice Springs'):
                item[1] = item[1] + name[1]
            if item[0] == 'Tasmania' and (name[0] == 'Hobart'
                                          or name[0] == 'Launceston'
                                          or name[0] == 'Katherine'):
                item[1] = item[1] + name[1]

    return Target_Area


if __name__ == '__main__':
    # --------------------------------------------CloudDB-----------------------------------------------------------
    server = couchdb.Server('http://admin:admin@172.26.130.124:5984/')
    db_name = 'db_status_filter_test'

    try:
        db = server.create(db_name)
    except:
        db = server[db_name]

    print('----------------------------------------CouchDB Connected------------------------------------------------')

    # ----------------------------------------Data Visualisation--------------------------------------------------------
    mode = 'Cloud'  # Cloud or Local
    Ranking = RankingList('FullDict.json', mode)
    Ranking.sort(reverse=True, key=take2)
    # print(Ranking)

    # 读取澳洲主要城市，在list中出现的频数并排序
    Rank_City = TargetCityRanking(Ranking)
    # 读取list中澳洲7个洲出现的频数，并将八大城市的数据加在对应的洲，再排序
    Target_Area = TargetAreaRanking(Ranking, Rank_City)
    Target_Area.sort(reverse=True, key=take2)

    print('--------------------------Start Ranking Area------------------------------')
    print('\n', 'AU Area Ranking:')
    for item in Target_Area:
        print('{0:30} : {1:10d}'.format(item[0], item[1]))

    print('\n--------------------------Start Ranking Cities----------------------------')
    print('\n', 'Top 10 Cities Ranking:')
    for item in Rank_City[:10]:
        print('{0:30} : {1:10d}'.format(item[0], item[1]))

    print('\n-------------------------Uploading-------------------------')
    # Upload to Cloud
    AreaRank = {}
    for item in Target_Area:
        AreaRank = {
            'AreaName': item[0],
            'Times': item[1],
            'Type': 'Area'
        }
        db.save(AreaRank)

    CityRank = {}
    for item in Rank_City:
        CityRank = {
            'AreaName': item[0],
            'Times': item[1],
            'Type': 'City'
        }
        db.save(CityRank)

    print('\n-----------------------ALL    DONE-------------------------------\n')
