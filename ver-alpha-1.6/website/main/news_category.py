import nltk
from nltk.stem import PorterStemmer
from newsapi import NewsApiClient
stemmer = PorterStemmer()

newsapi = NewsApiClient(api_key='42d68d8ee37146a6a61827e76d46f1c3')

def news_category(sport):
    sport_category = stemmer.stem(sport)
    return sport_category

def get_news(sport):
    sport=news_category(sport)
    top_headlines = newsapi.get_top_headlines(q=sport,
                                            category='sports',
                                            language='en',
                                            country='in')

    if top_headlines["totalResults"] <10 :
        top_headlines = newsapi.get_everything(q=sport,
                                                language='en')
    return top_headlines

if __name__ == '__main__':
    news=(get_news('volleyball'))
    for i in news:
        print(i)
        print()
        