from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

# Access Basketball Reference to get league leaders in win shares for each season
#specify the url
site = "https://www.basketball-reference.com/leaders/hof_prob.html"
#Query the website and return the html to the variable 'page'
page = urllib.request.urlopen(site)
#Parse the html in the 'page' variable and store it in Beautiful Soup format
soup = BeautifulSoup(page, 'lxml')
hof_prob_table = soup.table

#create list tuples of players and href 
player_list = []
for line in hof_prob_table('td'):
    try:
        player_list.append((str(line.a.string), str(line.a.get('href'))))
    except:
        print('could not do it for', line)
        

all_seasons = [] 
for player in player_list[:10]:
    reference_site = 'https://www.basketball-reference.com'
    page = urllib.request.urlopen(reference_site + player[1])
    #Parse the html in the 'page' variable and store it in Beautiful Soup format
    soup = BeautifulSoup(page, 'lxml')
    # Assign 
    per_game_table = soup.table
    height = str(soup.find_all('div', {'id':'info'})[0].find_all('span', {'itemprop':'height'})[0].string)

    # this gets category values for a single season and makes a single list
    values = []
    length = 0
    for row in (per_game_table('tr')):
        for num, column in enumerate(row):
            # Players from different decades have different
            # available stats, but PTS is always the last column
            if column.string == 'PTS':
                length = int((num+1) / 2)
            if column != '\n':
                values.append(str(column.string))
    categories = values[:length]
    # Ignores category names
    values = values[length:]

    # Create list of individual season stats lists
    player_career = [['Player', 'href', 'Height'] + categories]
    season = [player[0], player[1], height]
    for value in values:
        season.append(str(value))
        #added and (season[3] != None)
        if (len(season) == length+3) and (season[4] != 'None'):
            player_career.append(season)
            season = [player[0], player[1], height]
        # Player must have played at least 12 seasons
    if (len(player_career) > 12):# and (len(player_career[0]) == 33):
        all_seasons.append(player_career)
        print(str((len(player_career)-1)), ' seasons of ', player[0], 'added')



# Create pandas DataFrame of all data
master_cat_dict_ls = []
for ind, lab in enumerate(['Player', 'href', 'Height', 'Season', 'Age', 'Tm', 'Lg', 'Pos', 'G',
                           'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2PA%',
                           'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV',
                           'PF', 'PTS']):
        cat_dict = {lab:ind}    
        master_cat_dict_ls.append(cat_dict)     
        
test_careers = all_seasons[:4]
for career in test_careers:
    labels = career[0]
    for season in career[0:]:
        for num, cat in enumerate(season):
            print(labels[num], cat)
            
            
# does not work
#for career in test_careers[0]:
#    labels=career[0]
#    career_df = pd.DataFrame(columns=labels)
#    for season in career[0:]:
#        season= pd.Series(data=season)
#        pd.concat([career_df, season], ignore_index=True, join='outer')