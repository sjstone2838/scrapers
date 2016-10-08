import requests
from bs4 import BeautifulSoup
import pandas as pd

# Ignore INF (Infielder); only 3 in 1990 and none after
POSITIONS = ['P', 'C', 'SS', 'OF', '1B', '2B', '3B']
# POSITIONS = ['P', 'C', 'SS']

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

    header = [th.text for th in table.thead.find_all('th')]
    header.insert(0, 'player_link')
    if position != 'P' and position != 'OF':
        header.insert(10, 'position')

    data = []
    for tr in table.tbody.find_all('tr'):
        player_link = get_player_link(tr)
        record = [player_link]

        tds = tr.find_all('td')
        for td in tds:
            record.append(td.text.encode('utf-8').strip())

        if position != 'P' and position != 'OF':
            record.insert(10, position)

        data.append(record)

    df = pd.DataFrame(data, columns=header)
    df.to_csv('draftees.csv', mode='a', header=True)
    print "Wrote {} from {}".format(position, year)

def get_player_link(row):
    for a in row.find_all('a'):
        link = a.get('href')
        if link[0:23] == '/register/player.cgi?id':
            return link
    return ''

for year in range(1990, 1992):
    write_players_by_year(year)
