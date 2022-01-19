import articles
import search
import cProfile
import pstats

if __name__ == '__main__':
    url_list = ['https://en.wikipedia.org/wiki/World_War_II', 'https://en.wikipedia.org/wiki/Associated_Press',
                'https://en.wikipedia.org/wiki/Christian_Gow',
                'https://en.wikipedia.org/wiki/Bradie_Tennell', 'https://en.wikipedia.org/wiki/Fame_for_15',
                'https://en.wikipedia.org/wiki/Bali_tiger']
    start = articles.Article_Async('https://en.wikipedia.org/wiki/Atomic_Age')
    intermediate = articles.Article('https://en.wikipedia.org/wiki/Albert_Einstein')
    target = articles.Article('https://en.wikipedia.org/wiki/Black_hole')
    #start.create_sub_articles_list()

    start.create_article_list()