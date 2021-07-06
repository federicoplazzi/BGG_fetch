from urllib.request import urlopen
import argparse
import os

base_URL = 'https://boardgamegeek.com'

# Arguments parsing.
parser = argparse.ArgumentParser()

# Change the optional title.
parser._optionals.title = "Arguments"

# Input file.
parser.add_argument('--steps', dest='steps',required=False,help='How often should process be printed (number of pages)?',default=100)

# Number of games to include.
parser.add_argument('-p', dest='max_pages',required=False,help='Number of games to be parsed from BGG',default=0)

# Remove temporary files.
parser.add_argument('--clean', dest='clean',required=False,help='Remove temporary files?',default=False)

# Argument list.
args = parser.parse_args()

# If a maximum number of pages was specified via the -p flag, it is printed; otherwise, read the number of pages and write into _last_page_.

if args.max_pages == 0:

# Download the first page of boardgame list; pour into a file; read the file to a list and delete the file.

    HTML = urlopen(base_URL+'/browse/boardgame').read().decode('utf-8').encode('cp850','replace').decode('cp850')
    first_file = open('first_file.txt','w')
    try:
        first_file.writelines(HTML)
    except UnicodeEncodeError:
        print('Unicode error while downloading the first BGG page. Maybe an uncommon character in a game name? Exiting...')
        exit()
    except:
        print('Error while downloading the first BGG page. Exiting...')
        exit()
    first_file.close()

    first_file = open('first_file.txt','r')
    first_list = first_file.readlines()
    first_file.close()
    if args.clean != False:
        os.remove('first_file.txt')

    HTML_line = 0
    last_page_found = False
    while last_page_found == False:
        if 'title="last page">[' in first_list[HTML_line].strip():
            last_page_found = True
            last_page = first_list[HTML_line].strip().split('title="last page">[')[1].split(']')[0]
        else:
            HTML_line = HTML_line+1
    print('Last page found: '+last_page+'!')
    log_file = open('BGG_log.txt','w')
    log_file.write('Last page found: '+last_page+'!\n')
    log_file.close()
else:
    last_page = args.max_pages
    if last_page == 1:
        print('Start fetching the first page...')
        log_file = open('BGG_log.txt','w')
        log_file.write('Start fetching the first page...\n')
        log_file.close()
    else:
        print('Start fetching '+str(last_page)+' pages...')
        log_file = open('BGG_log.txt','w')
        log_file.write('Start fetching '+str(last_page)+' pages...\n')
        log_file.close()


# Compute _steps_ steps to monitor the whole process.

game_print_step = float(last_page)/int(args.steps)
step_list = []
for s in range(int(args.steps)):
    step_list.append(int(round(game_print_step*(s+1),0)))

# Set up empty lists for the final table.

max_rank = 0
ranks = []
games = []
years = []
min_players = []
max_players = []
ratings = []
geek_ratings = []
weights = []
categories = []
mechanisms = []

# Calling _p_ the number of pages (last_page), start a cycle with p repetitions.

print('Connected to site '+base_URL+'/browse/boardgame...')
log_file = open('BGG_log.txt','a')
log_file.write('Connected to site '+base_URL+'/browse/boardgame...\n')
log_file.close()

# Start the final output.

game_out = open('game.out','w')
game_out.write("Rank\tGame\tYear\tMin_players\tMax_players\tRating\tGeekRating\tWeight\tCategories\tMechanisms\n")
game_out.close()

for p in range(int(last_page)):

# Open and read page number p.

    HTML = urlopen(base_URL+'/browse/boardgame/page/'+str(p+1)).read().decode('utf-8').encode('cp850','replace').decode('cp850')
    current_file = open('current_file.txt','w')
    try:
        current_file.writelines(HTML)
    except UnicodeEncodeError:
        print('Unicode error while downloading page #'+str(p+1)+'. Maybe an uncommon character in some game name? Skipping...')
        log_file = open('BGG_log.txt','a')
        log_file.write('Unicode error while downloading page #'+str(p+1)+'. Maybe an uncommon character in some game name? Skipping...\n')
        log_file.close()
        continue
    except:
        print('Error while downloading page #'+str(p+1)+'. Skipping...')
        log_file = open('BGG_log.txt','a')
        log_file.write('Error while downloading page #'+str(p+1)+'. Skipping...\n')
        log_file.close()
        continue
    current_file.close()
    current_file = open('current_file.txt','r')
    current_list = current_file.readlines()
    current_file.close()
    if args.clean != False:
        os.remove('current_file.txt')

# Look for the board games.

    HTML_line = 0
    while HTML_line < len(current_list):
        line = current_list[HTML_line].strip()
        if 'Board Game: ' in line:
            ranks.append(max_rank+1)
            max_rank = max_rank+1
            games.append(line.split('Board Game: ')[1].split('"')[0])
            if "<span class='smallerfont dull'>(" in current_list[HTML_line+14].strip():
                years.append(current_list[HTML_line+14].strip().split('(')[1].split(')')[0])
                m = 1
            else:
                years.append("NA")
                m = 0
            ratings.append(current_list[HTML_line+28+m].strip().split('\t')[0])
            geek_ratings.append(current_list[HTML_line+25+m].strip().split('\t')[0])

# Open the game's page.

            game_URL = base_URL+line.split('href="')[1].split('"')[0]
            HTML = urlopen(game_URL).read().decode('utf-8').encode('cp850','replace').decode('cp850')
            current_game = open('current_game.txt','w')
            try:
                current_game.writelines(HTML)
            except UnicodeEncodeError:
                print('Unicode error while downloading the game '+games[-1]+'. Maybe an uncommon character in the game name? Skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Unicode error while downloading the game '+games[-1]+'. Maybe an uncommon character in the game name? Skipping...\n')
                log_file.close()
                HTML_line = HTML_line+1
                continue
            except:
                print('Error while downloading the game '+games[-1]+'. Skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Error while downloading the game '+games[-1]+'. Skipping...\n')
                log_file.close()
                HTML_line = HTML_line+1
                continue
            current_game.close()
            current_game = open('current_game.txt','r')
            current_game_list = current_game.readlines()
            current_game.close()
            if args.clean != False:
                os.remove('current_game.txt')

# Look for the stats line, where most pieces of information are written.

            stats_line_found = False
            game_line = 0
            while stats_line_found == False:
                stats_line = current_game_list[game_line].strip()
                if 'GEEK.geekitemPreload' in stats_line:
                    if 'avgweight":"' in stats_line:
                        weights.append(stats_line.split('avgweight":"')[1].split('"')[0])
                    else:
                        weights.append("NA")
                    if 'minplayers":"' in stats_line:
                        min_players.append(stats_line.split('minplayers":"')[1].split('"')[0])
                    else:
                        min_players.append("NA")
                    if 'maxplayers":"' in stats_line:
                        max_players.append(stats_line.split('maxplayers":"')[1].split('"')[0])
                    else:
                        max_players.append("NA")
                    raw_category_line = stats_line.split('boardgamecategory":[')[1].split(']')[0]
                    if raw_category_line == "":
                        categories.append("NA")
                    else:
                        category_number = raw_category_line.count('"name":"')
                        category_list = raw_category_line.split('"name":"')[1].split('"')[0]
                        if category_number > 1:
                            for c in range (1,category_number):
                                category_list = category_list+'|'+raw_category_line.split('"name":"')[c+1].split('"')[0]
                        categories.append(category_list)
                    raw_mechanism_line = stats_line.split('boardgamemechanic":[')[1].split(']')[0]
                    if raw_mechanism_line == "":
                        mechanisms.append("NA")
                    else:
                        mechanism_number = raw_mechanism_line.count('"name":"')
                        mechanism_list = raw_mechanism_line.split('"name":"')[1].split('"')[0]
                        if mechanism_number > 1:
                            for c in range (1,mechanism_number):
                                mechanism_list = mechanism_list+'|'+raw_mechanism_line.split('"name":"')[c+1].split('"')[0]
                        mechanisms.append(mechanism_list)
                    stats_line_found = True
                game_line = game_line+1
            
# Write a line of the final table-formatted file.

            game_out = open('game.out','a')
            game_out.write(str(ranks[-1])+"\t"+games[-1]+"\t"+years[-1]+"\t"+min_players[-1]+"\t"+max_players[-1]+"\t"+ratings[-1]+"\t"+geek_ratings[-1]+"\t"+weights[-1]+"\t"+categories[-1]+"\t"+mechanisms[-1]+"\n")
            game_out.close()
        HTML_line = HTML_line+1

# Check if progress should be printed.

    if p+1 in step_list:
        print('Fetching boardgame #'+str(max_rank)+' ('+games[-1]+'). Approximately '+str(round(float((p+1)/int(last_page)*100),2))+'% completed!')
        log_file = open('BGG_log.txt','a')
        log_file.write('Fetching boardgame #'+str(max_rank)+' ('+games[-1]+'). Approximately '+str(round(float((p+1)/int(last_page)*100),2))+'% completed!\n')
        log_file.close()

print('End. '+str(max_rank)+' games fetched from BGG.')
log_file = open('BGG_log.txt','a')
log_file.write('End. '+str(max_rank)+' games fetched from BGG.')
log_file.close()