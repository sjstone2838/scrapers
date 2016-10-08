import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

URL = 'http://www.baseball-reference.com'

DATA_TYPES = ['standard_pitching', 'standard_fielding', 'standard_batting']

def write_player_data(player_id):
    # Append player data to CSV.
    r = requests.get(URL + player_id)
    if not r.ok:
        raise RuntimeError("""Error connecting to %s;
                           "Make sure to add retries to code!""" % r.url)

    bs = BeautifulSoup(r.text, 'html.parser')

    draft_history = bs.find(string='Drafted').find_parent('p').text

    for data_type in DATA_TYPES:
        table = bs.find(id=data_type)

        # TODO: If no table, player probably didn't sign?
        # Ask Steven how to handle this situation
        if table:
            header, data = extract_table(table, player_id, draft_history)
            df = pd.DataFrame(data, columns=header)
            df.to_csv(data_type + '.csv', mode='a', header=True)

def extract_table(table, player_id, draft_history):
    # Return header (th) and data (td) from an html table.
    header = [th.text for th in table.thead.find_all('th')]
    header.insert(0, 'draft_history')
    header.insert(0, 'player_id')
    data = []
    for tr in table.tbody.find_all('tr'):
        record = [player_id, draft_history]
        tds = tr.find_all('td')
        for td in tds:
            record.append(td.text.encode('utf-8').strip())
        data.append(record)
    return header, data


start_time = datetime.datetime.now()

draftees = pd.read_csv('draftees.csv').values.tolist()

for draftee in draftees[100:]:
    player_id = draftee[1]
    write_player_data(player_id)
    end_time = datetime.datetime.now()
    delta = end_time - start_time
    print "Wrote {} in {}.{} seconds".format(player_id,
                                             delta.seconds,
                                             delta.microseconds)
    start_time = end_time
