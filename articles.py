import requests
from bs4 import BeautifulSoup
import re

class Article:
    def __init__(self, url):
        self.article_url = url # Direct provided URL to article
        self.distance_to_target = float('inf') # Current shortest distance to target, positive inf if target not found
        self.next_article = None # Points to the next article in shortest sequence
        self.hyperlink_list = self.create_hyperlink_list() # List of article hyperlinks found in main article
        self.partial = self.create_partial_url(url) # Create partial tag of current article
        self.article_name = self.find_title() # Retrieves title of current article

    def create_partial_url(self, url):
        # Initial searching found %#\"?&;=/ symbols to indicators of non article pages, update as findings change
        # Symbols might not be useful as direct URLs should either be manually selected or previously filtered
        # TODO: Review need for symbol filtering as project progresses
        search_url = re.compile(r"wikipedia.org/wiki/[^%#\"?&;=/]+")
        partial = re.findall(search_url, url)[0][19:]
        return partial

    def create_partial_hyperlink(self, hyperlink):
        # Banned list filters common non article pages that make it through regex filtering, list is probably non
        # exhaustive and leaves rom for false positive bans
        # TODO: Review banned list and/or come up with more accurate alternatives
        banned_list = "Category, Wikipedia, Template, Template_talk, Help, commons, Talk"
        banned_list = banned_list.split(', ')
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
        page = requests.get(self.article_url)
        return BeautifulSoup(page.content, "html.parser")

    def find_title(self):
        soup = self.make_soup()
        results = soup.find(id='firstHeading')
        return results.text.strip()

    def create_hyperlink_list(self):
        soup = self.make_soup()
        body = soup.find(id='bodyContent')
        hyperlinks = body.find_all('a', href=True, class_=False)
        hyperlink_list = []
        for i in hyperlinks:
            holder = self.create_partial_hyperlink(i)
            if holder is None:
                continue
            hyperlink_list.append(holder)
        return hyperlink_list

def create_wiki_link(partial):
    return 'https://en.wikipedia.org/wiki/' + partial
