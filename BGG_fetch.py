from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import os
import datetime
import time

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--disable-gpu')

base_URL = 'https://boardgamegeek.com'

# Arguments parsing.
parser = argparse.ArgumentParser()

# Change the optional title.
parser._optionals.title = "Arguments"

# Verbosity.
parser.add_argument('--steps', dest='steps',required=False,help='How many times should process be printed (number of maximum screen messages)?',default=100)

# Number of games to include.
parser.add_argument('-p', dest='max_pages',required=False,help='Number of game pages to be parsed from BGG',default=150)

# Remove temporary files.
parser.add_argument('--clean',dest='clean',required=False,help='Remove temporary files',action='store_true')
parser.add_argument('--no-clean',dest='clean',required=False,help='Do not remove temporary files',action='store_false')
parser.set_defaults(clean=True)

# Output file
current_date = datetime.date.today()
current_date = current_date.strftime("%y%m%d")
parser.add_argument('-o', dest='outfile',required=False,help='Output file name',default='game_'+current_date+'.out')

# Argument list.
args = parser.parse_args()

# Open a headless Chrome browser (ensure that the browser and the drivers match!) and start counting elapsed time.

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
browser.get(base_URL)
start_time = time.monotonic()

print('Connected to site '+base_URL+'/browse/boardgame...')

log_file = open('BGG_log.txt','w')
log_file.write('Connected to site '+base_URL+'/browse/boardgame...\n')
log_file.close()

# If a maximum number of pages was specified via the -p flag, it is printed; otherwise, read the number of pages and write into _last_page_.

if args.max_pages == 0:

# Download the first page of boardgame list; pour into a file; read the file to a list and delete the file.

    try:
        browser.get(base_URL+'/browse/boardgame')
    except:
        print('Error while downloading the first BGG page. Exiting...')
        exit()
    try:
        first_page = browser.page_source
    except:
        print('Error while downloading the first BGG page. Exiting...')
        exit()
    first_file = open('first_file.txt','w')
    first_file.writelines(first_page)
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
    log_file = open('BGG_log.txt','a')
    log_file.write('Last page found: '+last_page+'!\n')
    log_file.close()
else:
    last_page = args.max_pages
    if int(last_page) == 1:
        print('Start fetching the first page...')
        log_file = open('BGG_log.txt','a')
        log_file.write('Start fetching the first page...\n')
        log_file.close()
    else:
        print('Start fetching '+str(last_page)+' pages...')
        log_file = open('BGG_log.txt','a')
        log_file.write('Start fetching '+str(last_page)+' pages...\n')
        log_file.close()

# Compute _steps_ steps to monitor the whole process.

game_print_step = float(last_page)/int(args.steps)
step_list = []
for s in range(int(args.steps)):
    step_list.append(int(round(game_print_step*(s+1),0)))

# Set up empty lists for the final table.

max_ID = 0

# Start the final output.

game_out = open(args.outfile,'w')
game_out.write("ID\tGame\tDesigner\tYear\tMin_players\tMax_players\tMin_player_age\tRating\tGeekRating\tWeight\tWeight_voters\tVoters\tCategories\tMechanisms\tFamilies\n")
game_out.close()

# Let's start! Calling _p_ the number of pages (last_page), start a cycle with p repetitions, opening the page starting with the p*100-99-esime game (since from page 21 the site works differently).

for p in range(int(last_page)):
    p_game = str((p+1)*100-99)

# Open and read page number p.

    try:
        browser.get(base_URL+'/browse/boardgame?sort=rank&rankobjecttype=subtype&rankobjectid=1&rank='+p_game+'#'+p_game)
    except:
        print('Error while downloading page #'+str(p+1)+'. Skipping...')
        log_file = open('BGG_log.txt','a')
        log_file.write('Error while downloading page #'+str(p+1)+'. Skipping...\n')
        log_file.close()
        continue
    try:
        current_page = browser.page_source
    except:
        print('Error while downloading page #'+str(p+1)+'. Skipping...')
        log_file = open('BGG_log.txt','a')
        log_file.write('Error while downloading page #'+str(p+1)+'. Skipping...\n')
        log_file.close()
        continue
    current_file = open('current_file.txt','w')
    current_file.writelines(current_page)
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
            current_name = current_list[HTML_line+9].split('class="primary">')[1].split('</a>')[0].replace('\t','')
            if '<span class="smallerfont dull">(' in current_list[HTML_line+11].strip():
                current_year = current_list[HTML_line+11].strip().split('(')[1].split(')')[0]
                m = 1
            else:
                current_year = "NA"
                m = 0
            if '<p class="smallefont dull"' in current_list[HTML_line+14+m].strip():
                n = 3
            else:
                n = 0
            current_rating = current_list[HTML_line+22+m+n].strip().split('\t')[0]
            current_geek_rating = current_list[HTML_line+19+m+n].strip().split('\t')[0]
            current_voters = current_list[HTML_line+25+m+n].strip().split('\t')[0]

# Open the game's page.

            game_URL = base_URL+line.split('href="')[1].split('"')[0]
            try:
                browser.get(game_URL)
            except:
                print('Error while downloading the game '+current_name+'. Skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Error while downloading the game '+current_name+'. Skipping...\n')
                log_file.close()
                HTML_line = HTML_line+1
                continue
            try:
                current_game_page = browser.page_source
            except:
                print('Error while downloading the game '+current_name+'. Skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Error while downloading the game '+current_name+'. Skipping...\n')
                log_file.close()
                HTML_line = HTML_line+1
                continue
            current_game = open('current_game.txt','w')
            current_game.writelines(current_game_page)
            current_game.close()

            current_game = open('current_game.txt','r')
            current_game_list = current_game.readlines()
            current_game.close()
            if args.clean:
                os.remove('current_game.txt')

            if '<h1>Error: Server Error</h1>\n' in current_game_list:
                print('Error while downloading the game '+current_name+'. Skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Error while downloading the game '+current_name+'. Skipping...\n')
                log_file.close()
                HTML_line = HTML_line+1
                continue

# Look for the stats line, where some pieces of information are written.

            stats_line_found = False
            game_line = 0
            while stats_line_found == False:
                stats_line = current_game_list[game_line].strip()
                if 'GEEK.geekitemPreload' in stats_line:
                    if 'avgweight":"' in stats_line:
                        current_weight = stats_line.split('avgweight":"')[1].split('"')[0]
                    else:
                        current_weight = "NA"
                    if 'numweights":"' in stats_line:
                        current_num_weights = stats_line.split('numweights":"')[1].split('"')[0]
                    else:
                        current_num_weights = "NA"
                    if 'minplayers":"' in stats_line:
                        current_min_players = stats_line.split('minplayers":"')[1].split('"')[0]
                    else:
                        current_min_players = "NA"
                    if 'maxplayers":"' in stats_line:
                        current_max_players = stats_line.split('maxplayers":"')[1].split('"')[0]
                    else:
                        current_max_players = "NA"
                    if 'playerage":"' in stats_line:
                        current_player_age = stats_line.split('playerage":"')[1].split('"')[0]
                        if current_player_age == '(no votes)':
                            current_min_player_age = "NA"
                        elif current_player_age.count('\\u2013') == 1:
                            try:
                                current_min_min_player_age = current_player_age.split('\\u2013')[0]
                                current_max_min_player_age = current_player_age.split('\\u2013')[1]
                                current_min_player_age = str((int(current_min_min_player_age)+int(current_max_min_player_age))/2)
                            except:
                                print('Uncommonly formatted age for the game '+current_name+'. Reporting...')
                                log_file = open('BGG_log.txt','a')
                                log_file.write('Uncommonly formatted age for the game '+current_name+'. Reporting...\n')
                                log_file.close()
                                current_min_player_age = current_player_age
                        elif current_player_age[-1] == '+':
                            try:
                                current_player_age_int = int(current_player_age[:-1])
                                current_min_player_age = str(current_player_age_int)
                            except:
                                print('Uncommonly formatted age for the game '+current_name+'. Reporting...')
                                log_file = open('BGG_log.txt','a')
                                log_file.write('Uncommonly formatted age for the game '+current_name+'. Reporting...\n')
                                log_file.close()
                                current_min_player_age = current_player_age
                        else:
                            try:
                                current_player_age_int = int(current_player_age)
                                current_min_player_age = str(current_player_age_int)
                            except:
                                print('Uncommonly formatted age for the game '+current_name+'. Reporting...')
                                log_file = open('BGG_log.txt','a')
                                log_file.write('Uncommonly formatted age for the game '+current_name+'. Reporting...\n')
                                log_file.close()
                                current_min_player_age = current_player_age
                    else:
                        current_min_player_age = "NA"
                    stats_line_found = True
                game_line = game_line+1

# Connects to the 'credits' page, where complete information about designers, categories, mechanisms, and families is available.

            try:
                browser.get(game_URL+'/credits')
            except:
                print('Error while rendering credits of the game '+current_name+'. Setting to NA and skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Error while rendering credits of the game '+current_name+'. Setting to NA and skipping...\n')
                log_file.close()
                current_designers = "NA"
                current_categories = "NA"
                current_mechanisms = "NA"
                current_families = "NA"
                HTML_line = HTML_line+1
                continue
            try:
                game_session = browser.page_source
            except:
                print('Error while rendering credits of the game '+current_name+'. Setting to NA and skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Error while rendering credits of the game '+current_name+'. Setting to NA and skipping...\n')
                log_file.close()
                current_designers = "NA"
                current_categories = "NA"
                current_mechanisms = "NA"
                current_families = "NA"
                HTML_line = HTML_line+1
                continue
            current_credits = open('current_credits.txt','w')
            current_credits.writelines(game_session)
            current_credits.close()
            current_credits = open('current_credits.txt','r')
            current_credits_list = current_credits.readlines()
            current_credits.close()
            if args.clean:
                os.remove('current_credits.txt')

            if '<h1>Error: Server Error</h1>\n' in current_credits_list:
                print('Error while rendering credits of the game '+current_name+'. Setting to NA and skipping...')
                log_file = open('BGG_log.txt','a')
                log_file.write('Error while rendering credits of the game '+current_name+'. Setting to NA and skipping...\n')
                log_file.close()
                current_designers = "NA"
                current_categories = "NA"
                current_mechanisms = "NA"
                current_families = "NA"
                HTML_line = HTML_line+1
                continue

            string_line_found = False
            game_end_found = False
            game_line = 0
            while string_line_found == False and game_end_found == False:
                if game_line+1 == len(current_credits_list):
                    game_end_found = True
                    current_designers = "NA"
                    current_categories = "NA"
                    current_mechanisms = "NA"
                    current_families = "NA"

                string_line = current_credits_list[game_line].strip()

# The line with 'GEEK.geekitemPreload' is the second choice: this is because 'Preload' may imply that the page has not been fully rendered.

                if 'GEEK.geekitemPreload' in string_line:
                    if '"boardgamedesigner":[' in string_line:
                        raw_designers = string_line.split('"boardgamedesigner":[')[1].split(']')[0]
                        designer_number = raw_designers.count('"name":')
                        if designer_number == 0:
                            current_designers_worse = "NA"
                        else:
                            current_designers_worse = raw_designers.split('"name":"')[1].split('",')[0]
                            if designer_number > 1:
                                for c in range(1,designer_number):
                                    current_designers_worse = current_designers_worse+'|'+raw_designers.split('"name":"')[c+1].split('",')[0]
                    if '"boardgamecategory":[' in string_line:
                        raw_categories = string_line.split('"boardgamecategory":[')[1].split(']')[0]
                        category_number = raw_categories.count('"name":')
                        if category_number == 0:
                            current_categories_worse = "NA"
                        else:
                            current_categories_worse = raw_categories.split('"name":"')[1].split('",')[0]
                            if category_number > 1:
                                for c in range(1,category_number):
                                    current_categories_worse = current_categories_worse+'|'+raw_categories.split('"name":"')[c+1].split('",')[0]
                    if '"boardgamemechanic":[' in string_line:
                        raw_mechanisms = string_line.split('"boardgamemechanic":[')[1].split(']')[0]
                        mechanism_number = raw_mechanisms.count('"name":')
                        if mechanism_number == 0:
                            current_mechanisms_worse = "NA"
                        else:
                            current_mechanisms_worse = raw_mechanisms.split('"name":"')[1].split('",')[0]
                            if mechanism_number > 1:
                                for c in range(1,mechanism_number):
                                    current_mechanisms_worse = current_mechanisms_worse+'|'+raw_mechanisms.split('"name":"')[c+1].split('",')[0]
                    if '"boardgamefamily":[' in string_line:
                        raw_families = string_line.split('"boardgamefamily":[')[1].split(']')[0]
                        family_number = raw_families.count('"name":')
                        if family_number == 0:
                            current_families_worse = "NA"
                        else:
                            current_families_worse = raw_families.split('"name":"')[1].split('",')[0]
                            if family_number > 1:
                                for c in range(1,family_number):
                                    current_families_worse = current_families_worse+'|'+raw_families.split('"name":"')[c+1].split('",')[0]

# The page with '<span class="rating-stars-secondary">' is the first choice (on empirical bases!).

                if '<span class="rating-stars-secondary">' in string_line:
                    designer_number = string_line.count(' href="/boardgamedesigner/')
                    if designer_number == 0:
                        current_designers = "NA"
                    else:
                        current_designers = string_line.split(' href="/boardgamedesigner/')[1].split('</a>')[0].split('>')[1]
                        if designer_number > 1:
                            for c in range(1,designer_number):
                                current_designers = current_designers+'|'+string_line.split(' href="/boardgamedesigner/')[c+1].split('</a>')[0].split('>')[1]
                    category_number = string_line.count(' href="/boardgamecategory/')
                    if category_number == 0:
                        current_categories = "NA"
                    else:
                        current_categories = string_line.split(' href="/boardgamecategory/')[1].split('</a>')[0].split('>')[1]
                        if category_number > 1:
                            for c in range(1,category_number):
                                current_categories = current_categories+'|'+string_line.split(' href="/boardgamecategory/')[c+1].split('</a>')[0].split('>')[1]
                    mechanism_number = string_line.count(' href="/boardgamemechanic/')
                    if mechanism_number == 0:
                        current_mechanisms = "NA"
                    else:
                        current_mechanisms = string_line.split(' href="/boardgamemechanic/')[1].split('</a>')[0].split('>')[1]
                        if mechanism_number > 1:
                            for m in range(1,mechanism_number):
                                current_mechanisms = current_mechanisms+'|'+string_line.split(' href="/boardgamemechanic/')[m+1].split('</a>')[0].split('>')[1]
                    family_number = string_line.count(' href="/boardgamefamily/')
                    if family_number == 0:
                        current_families = "NA"
                    else:
                        current_families = string_line.split(' href="/boardgamefamily/')[1].split('</a>')[0].split('>')[1]
                        if family_number > 1:
                            for f in range(1,family_number):
                                current_families = current_families+'|'+string_line.split(' href="/boardgamefamily/')[f+1].split('</a>')[0].split('>')[1]
                    string_line_found = True
                game_line = game_line+1

# If the first choices for categories, mechanisms, and famililes are 'NA', they are replaced with second choices (until they are not 'NA', too).

            if current_designers == 'NA' and current_designers_worse != 'NA':
                current_designers = current_designers_worse
            if current_categories == 'NA' and current_categories_worse != 'NA':
                current_categories = current_categories_worse
            if current_mechanisms == 'NA' and current_mechanisms_worse != 'NA':
                current_mechanisms = current_mechanisms_worse
            if current_families == 'NA' and current_families_worse != 'NA':
                current_families = current_families_worse

# Write a line of the final table-formatted file.

            game_out = open(args.outfile,'a')
            current_stats = str(current_ID)+"\t"+current_name+"\t"+current_designers+"\t"+current_year+"\t"+current_min_players+"\t"+current_max_players+"\t"+current_min_player_age+"\t"+current_rating+"\t"+current_geek_rating+"\t"+current_weight+"\t"+current_num_weights+"\t"+current_voters+"\t"+current_categories+"\t"+current_mechanisms+"\t"+current_families+"\n"
            current_stats = current_stats.replace('\"','^^')
            current_stats = current_stats.replace('\'','^')
            current_stats = current_stats.replace('#','')
            current_stats = current_stats.replace("N/A","NA")
            current_stats = current_stats.replace('\/','/')
            current_stats = current_stats.replace(' / ','/')
            current_stats = current_stats.replace('&amp;','&')
            game_out.write(current_stats)
            game_out.close()
        HTML_line = HTML_line+1

# Check if progress should be printed.

    if p+1 in step_list and p+1 != int(last_page):
        now_time = time.monotonic()
        elapsed_time = now_time-start_time
        if elapsed_time > 86400:
            elapsed_days = elapsed_time // 86400
            if elapsed_days == 1:
                elapsed_days = 'one day, '
            else:
                elapsed_days = str(int(elapsed_days))+' days, '
            elapsed_time = elapsed_time % 86400
        else:
            elapsed_days = ''
        predicted_remaining_time = ((elapsed_time/(p+1))*int(last_page))-elapsed_time
        if predicted_remaining_time > 86400:
            predicted_remaining_days = predicted_remaining_time // 86400
            if predicted_remaining_days == 1:
                predicted_remaining_days = 'one day, '
            else:
                predicted_remaining_days = str(int(predicted_remaining_days))+' days, '
            predicted_remaining_time = predicted_remaining_time % 86400
        else:
            predicted_remaining_days = ''
        print('Fetching boardgame #'+str(max_ID)+' ('+current_name+'), '+str(round(float((p+1)/int(last_page)*100),2))+'% completed! Elapsed time: '+elapsed_days+time.strftime("%H:%M:%S",time.gmtime(elapsed_time))+'. Predicted remaining time: '+predicted_remaining_days+time.strftime("%H:%M:%S",time.gmtime(predicted_remaining_time))+'.')
        log_file = open('BGG_log.txt','a')
        log_file.write('Fetching boardgame #'+str(max_ID)+' ('+current_name+'), '+str(round(float((p+1)/int(last_page)*100),2))+'% completed! Elapsed time: '+elapsed_days+time.strftime("%H:%M:%S",time.gmtime(elapsed_time))+'. Predicted remaining time: '+predicted_remaining_days+time.strftime("%H:%M:%S",time.gmtime(predicted_remaining_time))+'.\n')
        log_file.close()

browser.close()
now_time = time.monotonic()
elapsed_time = now_time-start_time
if elapsed_time > 86400:
    elapsed_days = elapsed_time // 86400
    if elapsed_days == 1:
        elapsed_days = 'one day, '
    else:
        elapsed_days = str(int(elapsed_days))+' days, '
        elapsed_time = elapsed_time % 86400
else:
    elapsed_days = ''
print('End. '+str(max_ID)+' games fetched from BGG. Elapsed time: '+elapsed_days+time.strftime("%H:%M:%S",time.gmtime(elapsed_time))+'.')
log_file = open('BGG_log.txt','a')
log_file.write('End. '+str(max_ID)+' games fetched from BGG. Elapsed time: '+elapsed_days+time.strftime("%H:%M:%S",time.gmtime(elapsed_time))+'.')
log_file.close()
