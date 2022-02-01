import articles
import search
import cProfile
import pstats
import requests

if __name__ == '__main__':
    url_list = ['https://en.wikipedia.org/wiki/World_War_II', 'https://en.wikipedia.org/wiki/Associated_Press',
                'https://en.wikipedia.org/wiki/Christian_Gow',
                'https://en.wikipedia.org/wiki/Bradie_Tennell', 'https://en.wikipedia.org/wiki/Fame_for_15',
                'https://en.wikipedia.org/wiki/Bali_tiger']
    start = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Atomic_Age'))
    intermediate = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Atomic_Age'))
    target = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Black_hole'))
    #start.create_sub_articles_list()
    test = articles.ArticleAsync(requests.get(url_list[0]))
    start.next_article = search.depth_search_async(start, target, 1)
    print(start.next_article)