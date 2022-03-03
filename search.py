import articles
import httpx
import asyncio
import requests
# import sys

previously_found = set()
total_prev_fnd_hits = 0


# book_keeping is my lazy way of keeping tabs on various interesting data points.
# TODO: I should really make a proper stat tracking system that writes to a file and compiles a running history
def book_keeping(size, exceptions, prev_hits):
    global total_prev_fnd_hits
    total_prev_fnd_hits += prev_hits
    print(f'\nNumber of articles to be processed: {size}\nNumber of timeouts: {exceptions}'
          f'\nNumber of articles successfully processed: {size - exceptions}'
          f'\nNumber of previous hits: {prev_hits}'
          f'\nTotal number of appended articles: {size - exceptions - prev_hits}'
          f'\nNumber of previously found articles: {len(previously_found)}'
          f'\nNumber of objects avoided due to set: {total_prev_fnd_hits}\n')


# confirmation is a function that checks for the existence and location known intermediate hops
# so that I can estimate how long the program will need to run, and so I know for sure there is a valid path
# TODO: Review implementation, if the known hops are missing maybe end program.
def confirmation(current):
    intermediate = [articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Albert_Einstein')),
                    articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Atomic_Age'))]
    # Sorting the article list speeds things up since Albert Einstein is fairly early in alphabetical order
    # TODO: Move sort function to the building of article list
    # TODO: Create a sorting algo that would put target article and similar titles at beginning of list
    current.article_list.sort()

    for spot, item in enumerate(current.article_list):
        if intermediate[0].article_name == item.article_name or intermediate[1].article_name == item.article_name:
            print(f'Confirmation at spot: {spot}')
            return


# Asynchronously makes GET requests for the hyperlinks found within current article
# TODO: Review exception handling. It works as is, but I don't want to lose potential paths from an unlucky time out
async def articles_batch(hyperlink_list):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = (client.get(url) for url in hyperlink_list)
        pages = await asyncio.gather(*tasks, return_exceptions=True)
        return pages


def create_article_list(current):
    # The slices were originally implemented when GET response timeouts where causing crashes
    # I mistakenly thought that the timeouts were from async processing instead of the GET request
    # TODO: Review need for batching async.
    slice_size = 1000
    size = len(current.hyperlink_set)

    # exceptions and prev_hits are used for tracking performance
    # TODO: Remove once satisfied with performance
    exceptions = 0
    prev_hits = 0

    # hundred_holder is part of the batch system
    hundred_holder = []

    hyperlinks = list(current.hyperlink_set)
    for item in range(size // slice_size):
        hundred_holder.append(hyperlinks[:slice_size * (item + 1)])

    hundred_holder.append(hyperlinks[-1 * (size % slice_size):])
    for hundred_links in hundred_holder:
        pages = asyncio.run(articles_batch(hundred_links))
        for page in pages:
            # If an article times out during GET an exception object is put in place of the page object
            if not issubclass(type(page), Exception):
                check = articles.ArticleAsync(page)
                ''' 
                previously_found is a global set that should contain the name of every article we have found
                Since the breadth searches all articles in a hop distance before moving forward the first time
                an article is found we know it is the closest instance and all future findings are irrelevant
                '''
                if check.article_name not in previously_found:
                    current.article_list.append(check)
                    previously_found.add(check.article_name)
                else:
                    prev_hits += 1
            else:
                exceptions += 1
    book_keeping(size, exceptions, prev_hits)


# TODO: Change this function to be a component of breadth search rather than an independent search algo
def layer_search_async(current, target, max_depth, current_depth=0):
    # TODO: This is only needed the first time an article is passed, global set catches the repeats but they are still
    #  subjected to costly processes
    create_article_list(current)
    for spot, item in enumerate(current.article_list):
        found = None
        # Keeps track of how many hops from start. When search is recursively called this is the depth passed
        next_depth = current_depth + 1

        if item.article_name == target.article_name:
            print('Target found rising')
            return item
        elif next_depth <= max_depth:
            print(f'Diving {item.article_name}')
            found = layer_search_async(item, target, max_depth, next_depth)

        # TODO: This block might no longer be useful since the breadth search doesn't backtrack in the same way as depth
        if found is not None:
            # Checks if the current path takes fewer hops than the previously found path.
            if next_depth < current.distance_to_target:
                current.distance_to_target = next_depth
                current.next_article = found
        # Program is memory intensive, need to free up as much as possible during runtime
        current.article_list[spot] = None
    return


# TODO: Review breadth search; Remove debugging print eventually; Optimize if possible; REMOVE DEPTH SEARCH DEPENDENCY!
def breadth_search_async(current, target, max_depth=0, current_depth=0):
    create_article_list(current)
    confirmation(current)

    # TODO: Implement an adjustable max hops because infinite loops are scary
    while True:
        for spot, item in enumerate(current.article_list):
            found = None

            next_depth = current_depth + 1

            # This block of code mimics the depth search and is a holdover from when they were "separate" functions
            # TODO: Figure out how to merge this section of code and the similar section in layer_search
            if item.article_name == target.article_name:
                previously_found.clear()
                item.distance_to_target = 0
                return item
            elif next_depth <= max_depth:
                print(f'Diving {item.article_name}')
                found = layer_search_async(item, target, max_depth, next_depth)

            if found is not None:
                item.distance_to_target = next_depth
                item.next_article = found
                return item
        max_depth += 1
