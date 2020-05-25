import nltk
import couchdb
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer


if __name__ == '__main__':
    # ----------------------------------------------CloudDB-------------------------------------------------------------
    server = couchdb.Server('http://admin:admin@172.26.130.124:5984/')
    db_name = 'db_status_filter_test'

    try:
        db = server.create(db_name)
    except:
        db = server[db_name]

    print('-----------------------------------------CouchDB Connected-------------------------------------------------')

    # ---------------------------------------Sentiments Analysis--------------------------------------------------------
    # nltk.download('vader_lexicon')
    Text = []
    Sen = 'Love'
    # remove URLs
    text_noURL = re.sub(r"http\S+", "", Sen)
    # remove username
    text = re.sub(r"@\w+", "", text_noURL).lstrip()
    Text.append(text)
    print(Text)

    sid = SentimentIntensityAnalyzer()
    for sentence in Text:
        print(sentence)
        ss = sid.polarity_scores(sentence)
        for k in ss:
            print('{0}: {1}, '.format(k, ss[k]), end="")
