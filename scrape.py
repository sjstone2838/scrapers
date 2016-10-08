import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

URL = 'http://www.baseball-reference.com/register/player.cgi?id='

def write_player_data(player_id, start_time):
    # Append player data to CSV.
    r = requests.get(URL + player_id)
    if not r.ok:
        raise RuntimeError("""Error connecting to %s;
                           "Make sure to add retries to code!""" % r.url)

    bs = BeautifulSoup(r.text, 'html.parser')
    table = bs.find(id='standard_pitching')

    header, data = extract_table(table, player_id)

    df = pd.DataFrame(data, columns=header)
    # df.to_csv('baseball.csv')
    df.to_csv('baseball.csv', mode='a', header=False)

def extract_table(table, player_id):
    # Return header (th) and data (td) from an html table.
    header = [th.text for th in table.thead.find_all('th')]
    header.insert(0, 'player_id')
    data = []
    for tr in table.tbody.find_all('tr'):
        record = [player_id]
        tds = tr.find_all('td')
        for td in tds:
            record.append(td.text.encode('utf-8').strip())
        data.append(record)
    return header, data

start_time = datetime.datetime.now()

player_ids = [
    'osborn002don',
    'vanpop001tod',
    'smith-015dan'
]
for player_id in player_ids:
    write_player_data(player_id, start_time)
    end_time = datetime.datetime.now()
    delta = end_time - start_time
    print "Wrote {} in {}.{} seconds".format(player_id,
                                             delta.seconds,
                                             delta.microseconds)
    start_time = end_time
