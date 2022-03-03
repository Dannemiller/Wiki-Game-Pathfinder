# import articles
# import search
import cProfile
import pstats
# import requests
# import snakeviz
from GUI import gui_main


if __name__ == '__main__':
    with cProfile.Profile() as pr:
        gui_main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename='needs_profiling.prof')
