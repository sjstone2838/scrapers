import requests
from bs4 import BeautifulSoup
import pandas as pd

POSITIONS = ['P', 'C', 'SS', 'OF', '1B', '2B', '3B', 'INF']

position = 'P'
year = 1990
QUERY = '?query_type=pos_year&pos={}&year_ID={}&draft_type=junreg&'.format(position, year)
URL = 'http://www.baseball-reference.com/draft/' + QUERY

# print URL

r = requests.get(URL)
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
df.to_csv('draftees.csv', header=True)
