import requests
from scrapeFunc import scrape_urls
from bs4 import BeautifulSoup
from datetime import datetime

import pandas as pd

def find_urls():
    # date = datetime.today.strftime('%Y%m%d')
    date = "20240723"

    url = f"https://www.espn.com/mlb/scoreboard/_/date/{date}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print('Successfully fetched the webpage.')
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        exit()

    # Parse the HTML content, then get the daily urls
    soup = BeautifulSoup(response.content, 'html.parser')
    scoreboard_elements = soup.find_all('section', class_='Scoreboard bg-clr-white flex flex-auto justify-between')

    game_urls = []
    for game in scoreboard_elements:
        game_id = game.get('id')
        if game_id:
            game_urls.append(f"https://www.espn.com/mlb/game/_/gameId/{game_id}")

    # Scrape the data from the URLs
    scraped_data = scrape_urls(game_urls)
    return scraped_data

    
    

def send_data_to_server(data):
    url = 'http://localhost:3000/api/scraper'
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Data sent successfully')
        print(response.json())
    else:
        print('Failed to send data:', response.status_code, response.text)

if __name__ == '__main__':
    scraped_data = find_urls()
    top_batters = []
    flattened_data = []
    for game in scraped_data:
        game_url = game['url']
        for pitcher in game['pitcher_data']:
            pitcher_name = pitcher['name']
            era = pitcher['era']
            loc_era = pitcher['loc_era']
            vs_right = pitcher['vs_right']
            vs_left = pitcher['vs_left']
            for batter in pitcher['batter_data']:
                batter_name = batter['name']
                hits = batter['hits']
                at_bats = batter['at_bats']
                doubles = batter['2b']
                home_runs = batter['home_runs']
                avg = batter['avg']
                prev_date = batter['prevStats']['date']
                prev_at_bats = batter['prevStats']['at_bats']
                prev_hits = batter['prevStats']['hits']
                
                
                flattened_data.append({
                    'game_url': game_url,
                    'pitcher_name': pitcher_name,
                    'era': era,
                    'loc_era': loc_era,
                    'vs_right': vs_right,
                    'vs_left': vs_left,
                    'batter_name': batter_name,
                    'hits': hits,
                    'at_bats': at_bats,
                    'doubles': doubles,
                    'home_runs': home_runs,
                    'avg': avg,
                    'prev_date': prev_date,
                    'prev_at_bats': prev_at_bats,
                    'prev_hits': prev_hits
                })

    print(flattened_data[0])

    print("Data has been exported to baseball_data.csv")

    # send_data_to_server(scraped_data)