# BGG_fetch
BGG_fetch is a simple, custom-tailored Python script to fetch data from BoardGameGeek.
BGG_fetch is written in Python3. Usage:

python BGG_fetch.py [--steps 100 -p 0 --no-clean -o fileout]

BGG_fetch will connect to https://boardgamegeek.com/browse/boardgame and download data from available boardgames, writing output to a table-formatted plaintext file.

--steps      This flag controls how often the percentage progress is printed to screen. The default means that progress is printed 100 times, i.e. approximately every 1% progress.

-p           This flag allows the user to specify how many pages should be fetched. The default (0) means to fetch all the pages of the BGG database (ranked). Otherwise,
             only the first p pages will be fetched (ranked).

--clean      Remove temporary files (default)

--no-clean   Do not remove temporary files.

-o           Print results to fileout file. The default is game_<date>.out.

BGG_fecth will print an output table and a logfile. Currently, only major features are supported, but more may come.

1. Game title
2. Year
3. Minimum players
4. Maximum players
5. Minimum player age
6. Average rating
7. Average Geek rating
8. Average weight
9. Number of weight voters
10. Number of voters
11. Game categories
12. Game mechanics
13. Other game features ("families")
