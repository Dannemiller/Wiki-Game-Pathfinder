# Wiki-Game-Pathfinder
Program takes two wikipedia urls, a starting article and a target article. The program will jump from article to article via hyperlinks within the articles themselves until it finds the target.

Current state:

Article class is in a good place, but can be expanded on and optomized once full program gets to a rough finish.

Articles can be created individually, or asynchonously, very happy with how much asyncio sped things up.

Breadth first algorithm successfully finds target article as long as the computer running the pathfinder doesn't run out of memory.

Depth first algorithm works theoretically, however in tests it has yet to successfully find the target.

GUI basics have been started. Start and target URLs can be passed to program through GUI.

WIP List:

Scrap depth first search: Depth first is overly complicated, has several features that either don't work or actively fight against the overall success of the search. Either I need to abandon it (current top choice), or completely rebuild it from the ground up. For depth first to work I think some context would be needed since how far you want to search depends on how closely related the start and target are. 

**EDIT for section "Scrap depth first search": As noted in section "Comments and Documentation" I've forgotten a lot of details, includeing the fact that BREADTH SEARCH DEPENDS ON DEPTH SEARCH so scrapping it isn't an option until I remove that dependency.**

GUI expansion and refinement: Current GUI is a single static window, text can be entered but everything else besides input is handled in terminal. Need at least 3 more screens for GUI. Planned screens are: Input screen (rough draft), processing/searching screen (non existent), end screen (non existent), options screen (non existent)

Optomize memory usage: Storing all articles during search uses a lot of space (ex. wiki/World_War_II cointains 1,281 hyperlinks as of current scan) as number of children articles grow needed space grows. Plan on making a purpose built hash/set instead of relying on python built in set. Review article class to try and lessen the memory impact or storing so many article objects.

Processing speed: Biggest issue is GET requests are slow, even with the async function speeding things up. Multithreading/parallel processing is a potential solution, process GET requests on one thread/core, while scanning with another. Cython might have some solutions that python doesn't. Minor gains could be made with looping through NumPy arrays instead of python lists, but that would increase memory usage which is a bigger issue than speed as of current.

Comments and Documentation: Is currently non existent. I've currently forgotten most of the details about the article object and search algorithm. Need to go through each file and explain things. This proccess should help come up with solutions for some of the WIP items.

Update README more often: This is litterally the first update since I started this project, try to edit this with every update of the program.
