import articles
import search
import cProfile
import pstats
import requests
from GUI import gui_main


def test_main():
    start = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Karla_Ratnagiri'))
    search.create_article_list(start)
    for i in start.article_list:
        print(i.article_name)


if __name__ == '__main__':
    gui_main()