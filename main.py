import requests
from bs4 import BeautifulSoup
import re
import articles

if __name__ == '__main__':
    url_list = ['https://en.wikipedia.org/wiki/World_War_II', 'https://en.wikipedia.org/wiki/Associated_Press',
                'https://en.wikipedia.org/wiki/Christian_Gow',
                'https://en.wikipedia.org/wiki/Bradie_Tennell', 'https://en.wikipedia.org/wiki/Fame_for_15',
                'https://en.wikipedia.org/wiki/Bali_tiger']
    start = articles.Article(url_list[0])