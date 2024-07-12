# coding: utf-8

import datetime
import logging
import os, sys
import collections

import requests

skip_request = True

start_date = datetime.datetime(2023, 5, 17)
end_date = datetime.datetime(2024, 5, 17)

def generate_dates():
    d = start_date
    delta = datetime.timedelta(days=3)
    while d <= end_date:
        yield d  #won't break the loop
        d += delta


def process_file(filepath):
    with open(filepath, 'r') as f:
        header = next(f)
        dates = header.strip().split(',')[6:]
        data = collections.defaultdict(int)
        for line in f:
            line = line.strip().split(',')
            country, o, d = line[1], line[4], line[5]
            for i, value in enumerate(line[6:]):
                value = int(value)
                if not value:
                    continue  #skip 0 
                date = dates[i]
                data[f'{date},{country},{o},{d}'] += value    
        return data



def download_file(url, filepath):
    if skip_request:
        return
    if os.path.exists(filepath):
        return
    response = requests.get(url, headers={'X-FilesAPI-Key': 'XXX'})
    response.raise_for_status()
    response = response.json()
    response = requests.get(response['download_uri'])
    with open(filepath, 'wb') as f:
        f.write(response.content)


def main():
    result = {}
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    for d in generate_dates():
        d = d.strftime('%Y_%m_%d')
        logging.info(f'Downloading {d}')
        try:
            download_file(f'https://app.files.com/api/rest/v1/files/Jetcost/Partners_report/CTRIP/Clicks/clicks_{d}.csv', f'temp/{d}.csv')
            result.update(process_file(f'temp/{d}.csv'))
        except Exception as e:
            logging.error(f'Error downloading {d}: {e}')
    with open('temp/result3.csv', 'w') as f:
        f.write('date,country,from,to,clicks\n')
        for key, clicks in sorted(result.items()):
            f.write(f'{key},{clicks}\n')


if __name__ == '__main__':
    main()

#a common Python idiom used to ensure that certain code only runs when the script is executed directly, and not when it is imported as a module in another script. 