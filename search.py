import articles
import httpx
import asyncio
import requests
import sys

previously_found = set()


async def articles_batch(hyperlink_list):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = (client.get(url) for url in hyperlink_list)
        pages = await asyncio.gather(*tasks, return_exceptions=True)
        return pages


def create_article_list(current):
    slice_size = 1000
    size = len(current.hyperlink_set)
    hundred_holder = []
    hyperlinks = list(current.hyperlink_set)
    for item in range(size // slice_size):
        hundred_holder.append(hyperlinks[:slice_size * (item + 1)])
    hundred_holder.append(hyperlinks[-1 * (size % slice_size):])
    for hundred_links in hundred_holder:
        pages = asyncio.run(articles_batch(hundred_links))
        for page in pages:
            if not issubclass(type(page), Exception):
                check = articles.ArticleAsync(page)
                if check.article_name not in previously_found:
                    current.article_list.append(check)
                    previously_found.add(check.article_name)
    print(size, len(previously_found))


def confirmation(current):
    intermediate = articles.ArticleAsync(requests.get('https://en.wikipedia.org/wiki/Albert_Einstein'))
    current.article_list.sort()
    for spot, i in enumerate(current.article_list):
        if intermediate.article_name == i.article_name:
            print(f'Confirmation at spot: {spot}')
            return


def depth_search_async(current, target, max_depth, current_depth=0):
    create_article_list(current)
    for spot, item in enumerate(current.article_list):
        found = None
        next_depth = current_depth + 1
        print(f'Current depth: {current_depth}, spot: {spot}')
        if item.article_name == target.article_name:
            print('Target found rising')
            return item
        elif next_depth <= max_depth:
            print(f'Diving {item.article_name}')
            found = depth_search_async(item, target, max_depth, next_depth)

        if found is not None:
            if next_depth < current.distance_to_target:
                current.distance_to_target = next_depth
                current.next_article = found
        # Program is memory intensive, need to free up as much as possible during runtime
        current.article_list[spot] = None
    return


def breadth_search_async(current, target, max_depth=0, current_depth=0):
    create_article_list(current)
    confirmation(current)

    while True:
        for spot, item in enumerate(current.article_list):
            found = None

            next_depth = current_depth + 1
            print(f'Current depth: {current_depth}, spot: {spot}')

            if item.article_name == target.article_name:
                previously_found.clear()
                print(f'Target found rising: {item.article_name}')
                item.distance_to_target = 0
                return item
            elif next_depth <= max_depth:
                print(f'Diving {item.article_name}')
                found = depth_search_async(item, target, max_depth, next_depth)

            if found is not None:
                item.distance_to_target = next_depth
                item.next_article = found
                print(f'Target found rising: {item.article_name}')
                return item
        max_depth += 1
