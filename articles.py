# import requests
from bs4 import BeautifulSoup
import re
# import httpx
# import asyncio


def create_wiki_link(partial):
    return 'https://en.wikipedia.org/wiki/' + partial


def make_soup(page):
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def create_partial_hyperlink(hyperlink):
    # banned_list contains common terms that indicate a non article link
    banned_list = {'Category', 'Wikipedia', 'Template', 'Template_talk', 'Help', 'commons', 'Talk', 'Special'}
    # search is a regex that filters special characters that tend to indicate irrelevant information
    search = re.compile(r"a href=\"/wiki/[^%#\"?&;=/:]+")

    link_match = re.findall(search, str(hyperlink))
    length = len(link_match)

    if length == 1:
        # TODO: WHAT DOES THIS DO? FIGURE IT OUT
        link_match = list(link_match)[0]
        # [14:] strips link_match down to just the partial tag that can be used in creating links
        # TODO: Is this actually necessary? Can I use the whole thing?
        link_match = list(link_match)[14:]

        final = ''.join(link_match)
        if final in banned_list:
            return
        return final


''' 
Article Async is the class object that contains all relevant information scraped from wikipedia articles

 All methods and functions except dunders server the collection of the data.

 soup is a BeautifulSoup object and contains all data from the wikipedia article and methods for extracting information

 next_article is a "pointer" that remains empty until the target article is found.
 When the target is found, next_article points to the next object in the shortest chain leading to the target.
 For example my goto test is getting from start "Atomic Age" to target "Black Holes". The final chain goes:
 Atomic_Age.next_article-> Albert_Einstein, Albert_Einstein.next_article-> Black_Holes, Black_Holes.next_article->None

 distance_to_target indicates the number hops to reach the target article. It is given a value once article is found

 article_list is a python list that contains the article objects created from hyperlinks found in the current article

 article_name is the title of article on wikipedia page.
 Since one article can have multiple valid URLs, redirects, and other variables that make url comparison annoying
 Using the article title is the most accurate way to compare the target and the current

 hyperlink_set is a python set that contains all the urls found in the article.
 A set it used instead of a list to prevent duplicates.
 The hyperlink_set is a weird middle man, I don't actually care about the hyperlinks themselves, and they take space
 but the hyperlink_set is crucial to building the article list during the search.
'''


# TODO: Evaluate the need for next_article and distance_to_target since every dead end article contains them
# TODO: Look into alternatives to current hyperlink_set to article_list process
class ArticleAsync:
    def __init__(self, page):
        self.soup = make_soup(page)
        self.next_article = None
        self.distance_to_target = float('inf')
        self.article_list = []
        self.article_name = self.find_title()
        self.hyperlink_set = set()
        self.create_hyperlink_set()
        del self.soup

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

    def find_title(self):
        results = self.soup.find(id='firstHeading')
        return results.text.strip()

    def create_hyperlink_set(self):
        body = self.soup.find(id='bodyContent')
        hyperlinks = body.find_all('a', href=True, class_=False)
        for i in hyperlinks:
            holder = create_partial_hyperlink(i)
            if holder is not None:
                self.hyperlink_set.add(create_wiki_link(holder))
