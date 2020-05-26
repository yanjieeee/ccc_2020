import couchdb
import json
import re
import jsonpickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def NoDuplicate(tweetID, tw):
    if tw['ID'] not in tweetID:
        tweetID.append(tw['ID'])
        return True
    else:
        return False


def ssCounter(Sentence, ScoreList):
    ss = sid.polarity_scores(Sentence)
    if ss['neu'] == 1:
        ScoreList[1][1] += 1
        return ScoreList
    elif ss['neg'] < ss['pos']:
        ScoreList[0][1] += 1
        return ScoreList
    else:
        ScoreList[2][1] += 1
        return ScoreList


def printer(List, Name):
    name = Name
    print('----', name, '----')
    for item in List:
        print(item[0], ': ', item[1])
    print('----', name, '----', '\n')


def Text_Normalize(tweets):
    # remove URLs
    text_noURL = re.sub(r"http\S+", "", tweets['Text'])
    # remove username
    Text = re.sub(r"@\w+", "", text_noURL).lstrip()
    return Text


def Text_Collection(tweets):

    # Area
    VIC_City = ['Victoria', 'Melbourne', 'Ballarat', 'Bendigo', 'Geelong', 'Melton']
    QSL_City = ['Queensland', 'Gold Coast', 'Cairns', 'Toowoomba', 'Townsville', 'Sunshine Coast', 'Brisbane']
    NSW_City = ['New South Wales', 'Canberra', 'Newcastle', 'Wollongong', 'Sydney', 'Central Coast', 'Maitland']
    WAU_City = ['Western Australia', 'Perth', 'Bunbury', 'Geraldton', 'Albany', 'Busselton', 'Kalgoorlie']
    SAU_City = ['South Australia', 'Adelaide', 'Gawler', 'Mount Gambier', 'Whyalla']
    TAS_City = ['Tasmania', 'Hobart', 'Launceston', 'Katherine']
    NOT_City = ['Northern Territory', 'Darwin', 'Alice Springs']

    text = tweets
    AU__Text.append(text)
    if tweet['Place'] is not None:
        # Area Text Collection
        if 'victoria' in tweet['Place']['full_name'].lower():
            if 'melbourne' in tweet['Place']['full_name'].lower():
                Melbourne_Text.append(text)
                VIC_Text.append(text)
                return
            else:
                VIC_Text.append(text)
                return
        elif 'new south wales' in tweet['Place']['full_name'].lower():
            if 'sydney' in tweet['Place']['full_name'].lower():
                Sydney_Text.append(text)
                NSW_Text.append(text)
                return
            else:
                NSW_Text.append(text)
                return
        elif 'queensland' in tweet['Place']['full_name'].lower():
            if 'brisbane' in tweet['Place']['full_name'].lower():
                Brisbane_Text.append(text)
                QSL_Text.append(text)
                return
            else:
                QSL_Text.append(text)
                return
        elif 'tasmania' in tweet['Place']['full_name'].lower():
            if 'hobart' in tweet['Place']['full_name'].lower():
                Hobart_Text.append(text)
                TAS_Text.append(text)
                return
            else:
                TAS_Text.append(text)
                return
        elif 'western australia' in tweet['Place']['full_name'].lower():
            if 'perth' in tweet['Place']['full_name'].lower():
                Perth_Text.append(text)
                WAU_Text.append(text)
                return
            else:
                WAU_Text.append(text)
                return
        elif 'south australia' in tweet['Place']['full_name'].lower():
            if 'adelaide' in tweet['Place']['full_name'].lower():
                Adelaide_Text.append(text)
                SAU_Text.append(text)
                return
            else:
                SAU_Text.append(text)
                return
        elif 'northern territory' in tweet['Place']['full_name'].lower():
            if 'darwin' in tweet['Place']['full_name'].lower():
                Drawin_Text.append(text)
                NOT_Text.append(text)
                return
            else:
                NOT_Text.append(text)
                return

    elif tweet['User']['location'] is not None:
        for item in VIC_City:
            if item.lower() in tweet['User']['location'].lower():
                if 'melbourne' in tweet['User']['location'].lower():
                    Melbourne_Text.append(text)
                    VIC_Text.append(text)
                    return
                else:
                    VIC_Text.append(text)
                    return
        for item in NSW_City:
            if item.lower() in tweet['User']['location'].lower():
                if 'sydney' in tweet['User']['location'].lower():
                    Sydney_Text.append(text)
                    NSW_Text.append(text)
                    return
                else:
                    NSW_Text.append(text)
                    return
        for item in QSL_City:
            if item.lower() in tweet['User']['location'].lower():
                if 'brisbane' in tweet['User']['location'].lower():
                    Brisbane_Text.append(text)
                    QSL_Text.append(text)
                    return
                else:
                    QSL_Text.append(text)
                    return
        for item in TAS_City:
            if item.lower() in tweet['User']['location'].lower():
                if 'hobart' in tweet['User']['location'].lower():
                    Hobart_Text.append(text)
                    TAS_Text.append(text)
                    return
                else:
                    TAS_Text.append(text)
                    return
        for item in WAU_City:
            if item.lower() in tweet['User']['location'].lower():
                if 'perth' in tweet['User']['location'].lower():
                    Perth_Text.append(text)
                    WAU_Text.append(text)
                    return
                else:
                    WAU_Text.append(text)
                    return
        for item in SAU_City:
            if item.lower() in tweet['User']['location'].lower():
                if 'adelaide' in tweet['User']['location'].lower():
                    Adelaide_Text.append(text)
                    SAU_Text.append(text)
                    return
                else:
                    SAU_Text.append(text)
                    return
        for item in NOT_City:
            if item.lower() in tweet['User']['location'].lower():
                if 'darwin' in tweet['User']['location'].lower():
                    Drawin_Text.append(text)
                    NOT_Text.append(text)
                    return
                else:
                    NOT_Text.append(text)
                    return


if __name__ == '__main__':
    # # ---------------------------------------------CloudDB------------------------------------------------------------
    # server = couchdb.Server('http://admin:admin@172.26.130.124:5984/')
    # db_name = 'db_status_filter_test'
    #
    # try:
    #     db = server.create(db_name)
    # except:
    #     db = server[db_name]

    # print('----------------------------------------CouchDB Connected------------------------------------------------')

    # ---------------------------------------Sentiments Analysis--------------------------------------------------------
    # nltk.download('vader_lexicon')

    # Tweet ID list, is used to avoid duplication.
    Tweets_ID = []

    # Saving Text for greater city
    Melbourne_Text = []
    Sydney_Text = []
    Brisbane_Text = []
    Perth_Text = []
    Adelaide_Text = []
    Drawin_Text = []
    Hobart_Text = []

    # Saving Sentiments Score for each city
    Mel_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    Syd_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    Bri_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    Per_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    Ade_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    Dra_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    Hob_Score = [['pos', 0], ['neg', 0], ['neu', 0]]

    # Saving Text for each Area
    AU__Text = []
    VIC_Text = []
    NSW_Text = []
    QSL_Text = []
    TAS_Text = []
    WAU_Text = []
    SAU_Text = []
    NOT_Text = []  # Northern Territory

    # Saving Sentiments Score for each Area
    AU__Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    VIC_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    NSW_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    QSL_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    TAS_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    WAU_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    SAU_Score = [['pos', 0], ['neg', 0], ['neu', 0]]
    NOT_Score = [['pos', 0], ['neg', 0], ['neu', 0]]

    print('-----------------------------Reading Tweets---------------------------------\n')

    FileName = 'FullDict.json'
    fileReader = open(FileName, 'r', encoding='utf-8')
    for line in fileReader:
        line = line.strip('\n, ')
        if line.startswith('{') and line.endswith('}'):
            line = json.loads(line)
            tweet = line
            if NoDuplicate(Tweets_ID, tweet):
                TEXT = Text_Normalize(tweet)
                Text_Collection(TEXT)

    sid = SentimentIntensityAnalyzer()
    print('Totally, there are ', len(AU__Text), ' tweets.\n')
    print('-----------------------Start Printing Area Result-------------------------------\n')

    for sentence in AU__Text:
        ssCounter(sentence, AU__Score)
    printer(AU__Score, 'Australia')

    for sentence in VIC_Text:
        ssCounter(sentence, VIC_Score)
    printer(VIC_Score, 'Victoria')

    for sentence in NSW_Text:
        ssCounter(sentence, NSW_Score)
    printer(NSW_Score, 'New South Wales')

    for sentence in QSL_Text:
        ssCounter(sentence, QSL_Score)
    printer(QSL_Score, 'Queensland')

    for sentence in SAU_Text:
        ssCounter(sentence, SAU_Score)
    printer(SAU_Score, 'South Australia')

    for sentence in WAU_Text:
        ssCounter(sentence, WAU_Score)
    printer(WAU_Score, 'Western Australia')

    for sentence in TAS_Text:
        ssCounter(sentence, TAS_Score)
    printer(TAS_Score, 'Tasmania')

    for sentence in NOT_Text:
        ssCounter(sentence, NOT_Score)
    printer(NOT_Score, 'Northern Territory')

    print('-----------------------Start Printing City Result-------------------------------\n')

    for sentence in Melbourne_Text:
        ssCounter(sentence, Mel_Score)
    printer(Mel_Score, 'Melbourne')

    for sentence in Sydney_Text:
        ssCounter(sentence, Syd_Score)
    printer(Syd_Score, 'Sydney')

    for sentence in Brisbane_Text:
        ssCounter(sentence, Bri_Score)
    printer(Bri_Score, 'Brisbane')

    for sentence in Perth_Text:
        ssCounter(sentence, Per_Score)
    printer(Per_Score, 'Perth')

    for sentence in Adelaide_Text:
        ssCounter(sentence, Ade_Score)
    printer(Ade_Score, 'Adelaide')

    for sentence in Drawin_Text:
        ssCounter(sentence, Dra_Score)
    printer(Dra_Score, 'Drawin')

    for sentence in Hobart_Text:
        ssCounter(sentence, Hob_Score)
    printer(Hob_Score, 'Hobart')

    print('\n-------------------------Uploading-------------------------')
    # Upload to Cloud
    # Area
    Au_Sem = {
        'Name': 'Australia',
        'pos': AU__Score[0][1],
        'neg': AU__Score[1][1],
        'neu': AU__Score[2][1],
        'type': 'SemArea',
    }
    print(Au_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(Au_Sem, unpicklable=False) + '\n')
    # db.save(Au_Sem)

    VIC_Sem = {
        'Name': 'Victoria',
        'pos': VIC_Score[0][1],
        'neg': VIC_Score[1][1],
        'neu': VIC_Score[2][1],
        'type': 'SemArea',
    }
    print(VIC_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(VIC_Sem, unpicklable=False) + '\n')
    # db.save(VIC_Sem)

    NSW_Sem = {
        'Name': 'New South Wales',
        'pos': NSW_Score[0][1],
        'neg': NSW_Score[1][1],
        'neu': NSW_Score[2][1],
        'type': 'SemArea',
    }
    # db.save(NSW_Sem)
    print(NSW_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(NSW_Sem, unpicklable=False) + '\n')

    QSL_Sem = {
        'Name': 'Queensland',
        'pos': QSL_Score[0][1],
        'neg': QSL_Score[1][1],
        'neu': QSL_Score[2][1],
        'type': 'SemArea',
    }
    # db.save(QSL_Sem)
    print(QSL_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(QSL_Sem, unpicklable=False) + '\n')

    SAU_Sem = {
        'Name': 'South Australia',
        'pos': SAU_Score[0][1],
        'neg': SAU_Score[1][1],
        'neu': SAU_Score[2][1],
        'type': 'SemArea',
    }
    # db.save(SAU_Sem)
    print(SAU_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(SAU_Sem, unpicklable=False) + '\n')

    WAU_Sem = {
        'Name': 'Western Australia',
        'pos': WAU_Score[0][1],
        'neg': WAU_Score[1][1],
        'neu': WAU_Score[2][1],
        'type': 'SemArea',
    }
    # db.save(WAU_Sem)
    print(WAU_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(WAU_Sem, unpicklable=False) + '\n')

    TAS_Sem = {
        'Name': 'Tasmania',
        'pos': TAS_Score[0][1],
        'neg': TAS_Score[1][1],
        'neu': TAS_Score[2][1],
        'type': 'SemArea',
    }
    # db.save(TAS_Sem)
    print(TAS_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(TAS_Sem, unpicklable=False) + '\n')

    NOT_Sem = {
        'Name': 'Northern Territory',
        'pos': NOT_Score[0][1],
        'neg': NOT_Score[1][1],
        'neu': NOT_Score[2][1],
        'type': 'SemArea',
    }
    # db.save(NOT_Sem)
    print(NOT_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(NOT_Sem, unpicklable=False) + '\n')

    # City
    Mel_Sem = {
        'Name': 'Melbourne',
        'pos': Mel_Score[0][1],
        'neg': Mel_Score[1][1],
        'neu': Mel_Score[2][1],
        'type': 'SemCity',
    }
    # db.save(Mel_Sem)
    print(Mel_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(Mel_Sem, unpicklable=False) + '\n')

    Syd_Sem = {
        'Name': 'Sydney',
        'pos': Syd_Score[0][1],
        'neg': Syd_Score[1][1],
        'neu': Syd_Score[2][1],
        'type': 'SemCity',
    }
    # db.save(Syd_Sem)
    print(Syd_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(Syd_Sem, unpicklable=False) + '\n')

    Per_Sem = {
        'Name': 'Perth',
        'pos': Per_Score[0][1],
        'neg': Per_Score[1][1],
        'neu': Per_Score[2][1],
        'type': 'SemCity',
    }
    # db.save(Per_Sem)
    print(Per_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(Per_Sem, unpicklable=False) + '\n')

    Bri_Sem = {
        'Name': 'Brisbane',
        'pos': Bri_Score[0][1],
        'neg': Bri_Score[1][1],
        'neu': Bri_Score[2][1],
        'type': 'SemCity',
    }
    # db.save(Bri_Sem)
    print(Bri_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(Bri_Sem, unpicklable=False) + '\n')

    Ade_Sem = {
        'Name': 'Adelaide',
        'pos': Ade_Score[0][1],
        'neg': Ade_Score[1][1],
        'neu': Ade_Score[2][1],
        'type': 'SemCity',
    }
    # db.save(Ade_Sem)
    print(Ade_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(Ade_Sem, unpicklable=False) + '\n')

    Hob_Sem = {
        'Name': 'Hobart',
        'pos': Hob_Score[0][1],
        'neg': Hob_Score[1][1],
        'neu': Hob_Score[2][1],
        'type': 'SemCity',
    }
    # db.save(Hob_Sem)
    print(Hob_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(Hob_Sem, unpicklable=False) + '\n')

    Dra_Sem = {
        'Name': 'Drawin',
        'pos': Dra_Score[0][1],
        'neg': Dra_Score[1][1],
        'neu': Dra_Score[2][1],
        'type': 'SemCity',
    }
    # db.save(Dra_Sem)
    print(Dra_Sem)
    with open('Sentiments.json', 'a') as f:
        f.write(jsonpickle.encode(Dra_Sem, unpicklable=False) + '\n')
    print('-----------------------ALL    DONE-------------------------------\n')
