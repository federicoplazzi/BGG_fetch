# BGG_fetch
BGG_fetch is a simple, custom-tailored Python script to fetch data from BoardGameGeek.
BGG_fetch is written in Python3. Usage:

python BGG_fetch.py [--steps 100 -p 0 --clean False]

BGG_fetch will connect to https://boardgamegeek.com/browse/boardgame and download data from available boardgames, writing output to a table-formatted plaintext file.

--steps   This flag controls how often the percentage progress is printed to screen. The default means that progress is printed 100 times, i.e. approximately every 1% progress.

-p        This flag allows the user to specify how many pages should be fetched. The default (0) means to fetch all the pages of the BGG database (ranked). Otherwise,
          only the first p pages will be fetched (ranked).

--clean   If this is set to something different from 'False', temporary files are deleted.

BGG_fecth will print an output table and a logfile. Currently, only some features are supported, but more are to come.

-> Game title
-> Year
-> Average rating
-> Average Geek rating
-> Average weight
-> Minimum players
-> Maximum players
-> Game categories
-> Game mechanics
