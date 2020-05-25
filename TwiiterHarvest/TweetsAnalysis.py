import re
import couchdb
import json


def take1(elem):
    return elem[0]


def take2(elem):
    return elem[1]


def LD(str1, str2):
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                d = 0
            else:
                d = 1

            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    return matrix[len(str1)][len(str2)]


# 从已筛选后得到的 Dict.json 中读取， 并将地理信息整合到一个List中
def RankingList(FileName, mode):
    Cities_List = []

    if mode == 'Cloud':
        results = db.view('TestDesignDoc/TestView')
        # 从CouchDB读取数据
        for item in results:
            try:
                if 'location' in item.key:
                    Cities_List = CityCounter(item.key, Cities_List, 'CloudLocation')
                else:
                    Cities_List = CityCounter(item.key, Cities_List, 'CloudPlace')
            except TypeError as e:
                print(str(e))
                continue

    elif mode == 'Local':
        print('--------------------------Reading Tweets------------------------------')
        fileReader = open(FileName, 'r', encoding='utf-8')

        for line in fileReader:
            line = line.strip('\n, ')
            if line.startswith('{') and line.endswith('}'):
                try:
                    line = json.loads(line)
                    tweet = line

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
                    break
                elif i != len(list) - 1 and tweet['User']['location'] != list[i][0]:
                    i += 1
                elif i == len(list) - 1 and tweet['User']['location'] != list[i][0]:
                    list.append([tweet['User']['location'], 1])
                    i = 0

    elif mode == 'CloudLocation':
        if len(list) == 0:
            list.append([tweet['location'], 1])
        elif list is not None:
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
            list.append([tweet['name'], 1])
        elif list is not None:
            i = 0
            while i < len(list):
                if tweet['name'] == list[i][0]:
                    list[i][1] = list[i][1] + 1
                    break
                elif i != len(list) - 1 and tweet['name'] != list[i][0]:
                    i += 1
                elif i == len(list) - 1 and tweet['name'] != list[i][0]:
                    list.append([tweet['name'], 1])
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

    CityRank = cityRank

    for item in Target_Area:
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
    return Target_Area


def TargetMelSuburb(ranklist):
    # Extra Melbourne Suburb
    Target_Melbourne_Area = [
        ['Carlton', 0],
        ['Carlton North', 0],
        ['Docklands', 0],
        ['East Melbourne', 0],
        ['Flemington', 0],
        ['Kensington', 0],
        ['North Melbourne', 0],
        ['Parkville', 0],
        ['Port Melbourne', 0],
        ['Southbank', 0],
        ['South Wharf', 0],
        ['South Yarra', 0],
        ['West Melbourne', 0],
    ]

    Suburb_List = []
    for item in ranklist:
        Temp = False
        for extra_name in Target_Melbourne_Area:
            if extra_name[0].lower() in item[0].lower():
                Temp = True
                break
            else:
                Temp = False

        # 正则搜索所有 ', melbourne' 字段的元素
        YN = re.search('^.*, (m|M)elbourne$', item[0].lower())
        # 编剧距离不超过15，过滤较长干扰字符
        if 'australia' not in item[0].lower() \
                and (LD(item[0].lower(), 'melbourne') <= 15) \
                and YN:
            # or Temp:
            Suburb_List.append(item)
    # 按字母排序, 将相近的元素(设定ld<=11内为相近)，次数相加
    Suburb_List.sort(reverse=True, key=take1)

    pointer = 0
    while pointer < len(Suburb_List) - 1:
        if (LD(Suburb_List[pointer][0].lower(), Suburb_List[pointer + 1][0].lower()) <= 13) \
                and Suburb_List[pointer + 1][0].lower() in Suburb_List[pointer][0].lower():
            Suburb_List[pointer][1] = Suburb_List[pointer][1] + Suburb_List[pointer + 1][1]
            del Suburb_List[pointer + 1]
        pointer += 1

    # 按次数排序
    Suburb_List.sort(reverse=True, key=take2)
    return Suburb_List


if __name__ == '__main__':
    # ----------------------------------------------CloudDB-------------------------------------------------------------
    server = couchdb.Server('http://admin:admin@172.26.130.124:5984/')
    db_name = 'db_status_filter_test'

    try:
        db = server.create(db_name)
    except:
        db = server[db_name]

    print('----------------------------------------CouchDB Connected------------------------------------------------')

    # ----------------------------------------Data Visualisation--------------------------------------------------------
    mode = 'Local'  # Cloud or Local
    Ranking = RankingList('FullDict.json', mode)

    Ranking.sort(reverse=True, key=take2)
    # print(Ranking)
    # 读取澳洲主要城市，在list中出现的频数并排序
    Rank_City = TargetCityRanking(Ranking)
    # Melbourne Suburb Counting % Ranking
    Mel_Sub_List = TargetMelSuburb(Ranking)
    # 读取list中澳洲7个洲出现的频数，并将八大城市的数据加在对应的洲，再排序
    Target_Area = TargetAreaRanking(Ranking, Rank_City)
    Target_Area.sort(reverse=True, key=take2)

    print('\n--------------------------Start Ranking Area------------------------------')
    print('\n', 'AU Area Ranking:')
    for item in Target_Area:
        print('{0:30} : {1:10d}'.format(item[0], item[1]))

    print('\n--------------------------Start Ranking Cities----------------------------')
    print('\n', 'Top 10 Cities Ranking:')
    for item in Rank_City[:10]:
        print('{0:30} : {1:10d}'.format(item[0], item[1]))

    print('\n-------------------------Start Ranking Mel Suburb-------------------------')
    print('\n', 'Top 10 Melbourne Suburb Ranking:')
    for item in Mel_Sub_List[:10]:
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

    SuburbRank = {}
    for item in Mel_Sub_List:
        SuburbRank = {
            'AreaName': item[0],
            'Times': item[1],
            'Type': 'Suburb'
        }
        db.save(SuburbRank)
    print('\n-------------------------All Done-------------------------')
