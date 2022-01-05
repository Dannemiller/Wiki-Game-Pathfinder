import requests
from bs4 import BeautifulSoup
import re

class Article:
    def __init__(self, url):
        self.article_url = url
        self.distance_to_target = 0
        self.next_article = None
        self.hyperlink_list = []
        f = open('banned_list.txt', 'r')
        banned_list = f.read()
        banned_list = banned_list.split(', ')
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id='firstHeading')
        self.article_name = results.text.strip()
        body = soup.find(id='bodyContent')
        hyperlinks = body.find_all('a', href=True, class_=False)
        search = re.compile(r"a href=\"/wiki/[^%#\"?&;=/:]+")
        for i in hyperlinks:
            link_match = re.findall(search, str(i))
            length = len(link_match)
            if length == 1:
                link_match = list(link_match)[0]
                link_match = list(link_match)[14:]
                final = ''
                for j in link_match:
                    final += j
                if final in banned_list:
                    continue
                holder = ''
                for letter in link_match:
                    holder += letter
                self.hyperlink_list.append(holder)