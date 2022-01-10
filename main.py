import articles
import search


if __name__ == '__main__':
    url_list = ['https://en.wikipedia.org/wiki/World_War_II', 'https://en.wikipedia.org/wiki/Associated_Press',
                'https://en.wikipedia.org/wiki/Christian_Gow',
                'https://en.wikipedia.org/wiki/Bradie_Tennell', 'https://en.wikipedia.org/wiki/Fame_for_15',
                'https://en.wikipedia.org/wiki/Bali_tiger']
    start = articles.Article('https://en.wikipedia.org/wiki/Atomic_Age')
    intermediate = articles.Article('https://en.wikipedia.org/wiki/Albert_Einstein')
    target = articles.Article('https://en.wikipedia.org/wiki/Black_hole')


start.next_article = search.depth_search(start, target, max_depth=4)
current = start
while current is not None:
    print(current.partial, current.distance_to_target, '->')
    current = current.next_article

start.next_article = search.breadth_search(start, target)
current = start
while current is not None:
    print(current.partial, current.distance_to_target, '->')
    current = current.next_article