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
parser.add_argument('--clean',dest='clean',required=False,help='Remove temporary files',action='store_true')
parser.add_argument('--no-clean',dest='clean',required=False,help='Do not remove temporary files',action='store_false')
parser.set_defaults(clean=True)

# Output file
parser.add_argument('-o', dest='outfile',required=False,help='Output file name',default='game.out')

# Argument list.
args = parser.parse_args()

print('Connected to site '+base_URL+'/browse/boardgame...')

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
    if args.clean:
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
    if int(last_page) == 1:
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

max_ID = 0

# Calling _p_ the number of pages (last_page), start a cycle with p repetitions.

log_file = open('BGG_log.txt','a')
log_file.write('Connected to site '+base_URL+'/browse/boardgame...\n')
log_file.close()

# Start the final output.

game_out = open(args.outfile,'w')
game_out.write("ID\tGame\tYear\tMin_players\tMax_players\tRating\tGeekRating\tWeight\tVoters\tCategories\tMechanisms\tFamilies\n")
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
    except OSError:
        p = p-1
        continue
    except urllib.error.URLError:
        p = p-1
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
    if args.clean:
        os.remove('current_file.txt')

# Look for the board games.

    HTML_line = 0
    while HTML_line < len(current_list):
        line = current_list[HTML_line].strip()
        if '<img alt="Board Game: ' in line or 'From gallery of BoardGameGeek' in line:
            current_ID = max_ID+1
            max_ID = max_ID+1
            current_name = current_list[HTML_line+12].split('class=\'primary\' >')[1].split('</a>')[0]
            if "<span class='smallerfont dull'>(" in current_list[HTML_line+14].strip():
                current_year = current_list[HTML_line+14].strip().split('(')[1].split(')')[0]
                m = 1
            else:
                current_year = "NA"
                m = 0
            if '<p class="smallefont dull"' in current_list[HTML_line+17+m].strip():
                n = 3
            else:
                n = 0
            current_rating = current_list[HTML_line+25+m+n].strip().split('\t')[0]
            current_geek_rating = current_list[HTML_line+22+m+n].strip().split('\t')[0]
            current_voters = current_list[HTML_line+28+m+n].strip().split('\t')[0]

# Open the game's page.

            game_URL = base_URL+line.split('href="')[1].split('"')[0]
            HTML = urlopen(game_URL).read().decode('utf-8').encode('cp850','replace').decode('cp850')
            current_game = open('current_game.txt','w')
            try:
                current_game.writelines(HTML)
            except UnicodeEncodeError:
                print('Unicode error while downloading the game '+current_name+'. Maybe an uncommon character in the game name? Skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Unicode error while downloading the game '+current_name+'. Maybe an uncommon character in the game name? Skipping...\n')
                log_file.close()
                HTML_line = HTML_line+1
                continue
            except OSError:
                continue
            except urllib.error.URLError:
                continue
            except:
                print('Error while downloading the game '+current_name+'. Skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Error while downloading the game '+current_name+'. Skipping...\n')
                log_file.close()
                HTML_line = HTML_line+1
                continue
            current_game.close()
            current_game = open('current_game.txt','r')
            current_game_list = current_game.readlines()
            current_game.close()
            if args.clean:
                os.remove('current_game.txt')

# Look for the stats line, where most pieces of information are written.

            stats_line_found = False
            game_line = 0
            while stats_line_found == False:
                stats_line = current_game_list[game_line].strip()
                if 'GEEK.geekitemPreload' in stats_line:
                    if 'avgweight":"' in stats_line:
                        current_weight = stats_line.split('avgweight":"')[1].split('"')[0]
                    else:
                        current_weight = "NA"
                    if 'minplayers":"' in stats_line:
                        current_min_players = stats_line.split('minplayers":"')[1].split('"')[0]
                    else:
                        current_min_players = "NA"
                    if 'maxplayers":"' in stats_line:
                        current_max_players = stats_line.split('maxplayers":"')[1].split('"')[0]
                    else:
                        current_max_players = "NA"
                    if 'boardgamecategory":[' in stats_line:
                        raw_category_line = stats_line.split('boardgamecategory":[')[1].split(']')[0]
                        if raw_category_line == "":
                            current_categories = "NA"
                        else:
                            category_number = raw_category_line.count('"name":"')
                            category_list = raw_category_line.split('"name":"')[1].split('"')[0]
                            if category_number > 1:
                                for c in range (1,category_number):
                                    category_list = category_list+'|'+raw_category_line.split('"name":"')[c+1].split('"')[0]
                            current_categories = category_list
                    else:
                        current_categories = "NA"
                    if 'boardgamemechanic":[' in stats_line:
                        raw_mechanism_line = stats_line.split('boardgamemechanic":[')[1].split(']')[0]
                        if raw_mechanism_line == "":
                            current_mechanisms = "NA"
                        else:
                            mechanism_number = raw_mechanism_line.count('"name":"')
                            mechanism_list = raw_mechanism_line.split('"name":"')[1].split('"')[0]
                            if mechanism_number > 1:
                                for c in range (1,mechanism_number):
                                    mechanism_list = mechanism_list+'|'+raw_mechanism_line.split('"name":"')[c+1].split('"')[0]
                            current_mechanisms = mechanism_list
                    else:
                        current_mechanisms = "NA"
                    if 'boardgamefamily":[' in stats_line:
                        raw_family_line = stats_line.split('boardgamefamily":[')[1].split(']')[0]
                        if raw_family_line == "":
                            current_families = "NA"
                        else:
                            family_number = raw_family_line.count('"name":"')
                            family_list = raw_family_line.split('"name":"')[1].split('"')[0]
                            if family_number > 1:
                                for c in range (1,family_number):
                                    family_list = family_list+'|'+raw_family_line.split('"name":"')[c+1].split('"')[0]
                            current_families = family_list
                    else:
                        current_families = "NA"
                    stats_line_found = True
                game_line = game_line+1
            
# Write a line of the final table-formatted file.

            game_out = open(args.outfile,'a')
            current_stats = str(current_ID)+"\t"+current_name+"\t"+current_year+"\t"+current_min_players+"\t"+current_max_players+"\t"+current_rating+"\t"+current_geek_rating+"\t"+current_weight+"\t"+current_voters+"\t"+current_categories+"\t"+current_mechanisms+"\t"+current_families+"\n"
            game_out.write(current_stats.replace("N/A","NA").replace('\/','/').replace(' / ','/'))
            game_out.close()
        HTML_line = HTML_line+1

# Check if progress should be printed.

    if p+1 in step_list:
        print('Fetching boardgame #'+str(max_ID)+' ('+current_name+'). Approximately '+str(round(float((p+1)/int(last_page)*100),2))+'% completed!')
        log_file = open('BGG_log.txt','a')
        log_file.write('Fetching boardgame #'+str(max_ID)+' ('+current_name+'). Approximately '+str(round(float((p+1)/int(last_page)*100),2))+'% completed!\n')
        log_file.close()

print('End. '+str(max_ID)+' games fetched from BGG.')
log_file = open('BGG_log.txt','a')
log_file.write('End. '+str(max_ID)+' games fetched from BGG.')
log_file.close()
