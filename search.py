import articles

search_basket = set() # Global set that contains all previously searched articles to avoid loops
# and searching pages that have already not given any results

def depth_search(start, target, max_depth, current_depth=0):
    for i in start.hyperlink_list:
        current_link = articles.create_wiki_link(i)
        current_article = articles.Article(current_link) # Create article object for the next layer in the search
        print(' '*current_depth, current_article.article_name)
        if current_article.article_name == target.article_name: # If the current search object matches target return
            print('Target located, returning to surface')
            current_article.distance_to_target = current_depth
            return current_article
        elif current_depth >= max_depth: # If max depth is reached, return empty handed
            print(' '*current_depth, f'Can not dive deeper, {current_article.partial}')
            current_article.distance_to_target = float('inf')
            return
        if current_article.article_name in search_basket: #
            print('PING')
            return

        successor = depth_search(current_article, target, max_depth=max_depth, current_depth=current_depth+1) # Search continues, got to next deep link
        search_basket.add(current_article.article_name)

        if successor is None: # Search came back empty handed, go to next partial in list
            continue

        print(f'Surfacing, current article {current_article.article_name}')
        current_article.distance_to_target = current_depth
        current_article.next_article = successor
        return current_article
    return

def breadth_search(start, target):
    for i in range(8):
        check = depth_search(start, target, max_depth=i)
        if check is not None:
            return check
    return
