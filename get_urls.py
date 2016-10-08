import requests
from bs4 import BeautifulSoup
import pandas as pd

# Ignore INF (Infielder); only 3 in 1990 and none after
POSITIONS = ['P', 'C', 'SS', 'OF', '1B', '2B', '3B']

def write_players_by_year(year):
    for position in POSITIONS:
        write_players_by_position(year, position)

def write_players_by_position(year, position):
    query = ('?query_type=pos_year&pos='
             '{}&year_ID={}&draft_type=junreg&'.format(position, year))
    url = 'http://www.baseball-reference.com/draft/' + query

    # print url

    r = requests.get(url)
    if not r.ok:
        raise RuntimeError('Error connecting to %s' % r.url)

    bs = BeautifulSoup(r.text, 'html.parser')

    table = bs.find(id='draft_stats')

    players = []

    for a in table.find_all('a'):
        link = a.get('href')
        if link[0:23] == '/register/player.cgi?id':
            players.append([year, position, link])

    # print len(links)
    # print links

    df = pd.DataFrame(players, columns=['Year', 'Position', 'Link'])
    df.to_csv('draftees.csv', mode='a', header=True)

for year in range(1990, 1991):
    write_players_by_year(year)
