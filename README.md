# BGG_fetch
BGG_fetch is a simple, custom-tailored Python script to fetch data from BoardGameGeek.
BGG_fetch is written in Python3. Usage:

python BGG_fetch.py [--steps 100 -p 0 --no-clean -o fileout]

BGG_fetch will connect to https://boardgamegeek.com/browse/boardgame and download data from available boardgames, writing output to a table-formatted plaintext file.

--steps      This flag controls how often the percentage progress is printed to screen. The default means that progress is printed 100 times, i.e. approximately every 1% progress.

-p           This flag allows the user to specify how many pages should be fetched. The default (0) means to fetch all the pages of the BGG database (ranked). Otherwise,
             only the first p pages will be fetched (ranked).

--no-clean   Do not remove temporary files.

-o           Print results to fileout file. The default is game.out.

BGG_fecth will print an output table and a logfile. Currently, only some features are supported, but more are to come.

1. Game title
2. Year
3. Minimum players
4. Maximum players
5. Average rating
6. Average Geek rating
7. Average weight
8. Number of voters
9. Game categories
10. Game mechanics
