import requests
from bs4 import BeautifulSoup
import re
import httpx
import asyncio


def create_wiki_link(partial):
    return 'https://en.wikipedia.org/wiki/' + partial


class ArticleAsync:
    def __init__(self, page):
        self.page = page
        self.soup = self.make_soup()
        self.next_article = None  # Points to the next article in shortest sequence
        self.distance_to_target = float('inf')
        self.article_list = []  # List of article hyperlinks found in main article, start blank to avoid infinite recursion
        self.article_name = self.find_title()  # Retrieves title of current article
        self.hyperlink_set = set()
        self.create_hyperlink_set()
        del self.soup
        del self.page

    def __gt__(self, other):
        if type(other) is ArticleAsync:
            return self.article_name > other.article_name
        elif type(other) is str:
            return self.article_name > other
        else:
            raise TypeError

    def __ge__(self, other):
        if type(other) is ArticleAsync:
            return self.article_name >= other.article_name
        elif type(other) is str:
            return self.article_name >= other
        else:
            raise TypeError

    def __lt__(self, other):
        if type(other) is ArticleAsync:
            return self.article_name < other.article_name
        elif type(other) is str:
            return self.article_name < other
        else:
            raise TypeError

    def __le__(self, other):
        if type(other) is ArticleAsync:
            return self.article_name <= other.article_name
        elif type(other) is str:
            return self.article_name <= other
        else:
            raise TypeError

    def __eq__(self, other):
        if type(other) is ArticleAsync:
            return self.article_name == other.article_name
        elif type(other) is str:
            return self.article_name == other
        else:
            raise TypeError

    def __ne__(self, other):
        if type(other) is ArticleAsync:
            return self.article_name != other.article_name
        elif type(other) is str:
            return self.article_name != other
        else:
            raise TypeError

    def create_partial_hyperlink(self, hyperlink):
        # Banned list filters common non article pages that make it through regex filtering, list is probably non
        # exhaustive and leaves rom for false positive bans
        # TODO: Review banned list and/or come up with more accurate alternatives
        banned_list = {'Category', 'Wikipedia', 'Template', 'Template_talk', 'Help', 'commons', 'Talk'}
        # Initial searching found %#\"?&;=/ symbols to indicators of non article pages, update as findings change
        # Regex strips partial tags of banned pages down to a recognizable form
        # combine with banned list and only article links should pass all checks
        # Regex search sometimes removes needed URL information so final partial tag does not use the filter
        search = re.compile(r"a href=\"/wiki/[^%#\"?&;=/:]+")
        link_match = re.findall(search, str(hyperlink))
        length = len(link_match)
        if length == 1:
            link_match = list(link_match)[0]
            # [14:] strips link_match down to just the partial tag that can be used in creating links
            link_match = list(link_match)[14:]
            final = ''
            for j in link_match:
                final += j
            if final in banned_list:
                return
            holder = ''
            for letter in link_match:
                holder += letter
            return holder

    def make_soup(self):
        soup = BeautifulSoup(self.page.content, "html.parser")
        return soup

    def find_title(self):
        results = self.soup.find(id='firstHeading')
        return results.text.strip()

    def create_hyperlink_set(self):
        body = self.soup.find(id='bodyContent')
        hyperlinks = body.find_all('a', href=True, class_=False)
        for i in hyperlinks:
            holder = self.create_partial_hyperlink(i)
            if holder is not None:
                self.hyperlink_set.add(create_wiki_link(holder))
