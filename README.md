# Wiki-Game-Pathfinder
Program takes two wikipedia urls, a starting article and a target article. The program will jump from article to article via hyperlinks within the articles themselves until it finds the target.
Current state creates an Article object that will be used during search for target
WIP List:
  Create depth first search: Set initial depth that updates if path shorter than current depth is found. Execpted best use for loosely connected start and end
  Create breadth first search. Expected best use for strongly connected start and end
  Optomize memory usage: Storing all articles during search will use waste a lot of space (ex. wiki/World_War_II cointains 1,281 hyperlinks as of current scan) as number of children articles grow needed space will grow
  GUI: Once program is able to reliably find target articles create UI outside of terminal for ease of use
