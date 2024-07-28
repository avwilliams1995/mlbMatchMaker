import requests
from scrapeFunc import scrape_urls
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime, timedelta




def find_urls():
    today = datetime.today()

    tomorrow = today + timedelta(days=1)

    date = tomorrow.strftime('%Y%m%d')  
    
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

    
    

# def send_data_to_server(data):
#     url = 'http://localhost:3000/api/scraper'
#     response = requests.post(url, json=data)
#     if response.status_code == 200:
#         print('Data sent successfully')
#         print(response.json())
#     else:
#         print('Failed to send data:', response.status_code, response.text)
top_batters  = [
    "Bobby Witt Jr.",
    "Steven Kwan",
    "Shohei Ohtani",
    "Luis Arraez",
    "Juan Soto",
    "Carlos Correa",
    "Jose Altuve",
    "Aaron Judge",
    "Marcell Ozuna",
    "Mookie Betts",
    "Yordan Alvarez",
    "Jurickson Profar",
    "Alec Bohm",
    "Vladimir Guerrero Jr.",
    "Ketel Marte",
    "Rafael Devers",
    "Jarren Duran",
    "Bryce Harper",
    "Alec Burleson",
    "Brent Rooker",
    "Bryan Reynolds",
    "Freddie Freeman",
    "Josh Smith",
    "William Contreras",
    "Gunnar Henderson",
    "Ezequiel Tovar",
    "Masyn Winn",
    "Jeremy Pena",
    "Jackson Merrill",
    "Yainer Diaz",
    "Fernando Tatis Jr.",
    "Brenton Doyle",
    "Salvador Perez",
    "Logan O'Hoppe",
    "Luis Garcia Jr.",
    "Yandy Diaz",
    "Jose Ramirez",
    "Jonathan India",
    "Ryan Mountcastle",
    "Nathaniel Lowe",
    "Corey Seager",
    "Brendan Rodgers",
    "Brice Turang",
    "Ryan McMahon",
    "Cody Bellinger",
    "Adley Rutschman",
    "Teoscar Hernandez",
    "Brendan Donovan",
    "Sal Frelick",
    "Jordan Westburg"
]
DATA_FILE = 'flattened_data.json'
DATA_TIMESTAMP_FILE = 'data_timestamp.json'
DATA_EXPIRY_DAYS = 1  # Data is valid for 1 day

def save_data(data, timestamp):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)
    with open(DATA_TIMESTAMP_FILE, 'w') as f:
        json.dump({'timestamp': timestamp}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def load_timestamp():
    if os.path.exists(DATA_TIMESTAMP_FILE):
        with open(DATA_TIMESTAMP_FILE, 'r') as f:
            return json.load(f).get('timestamp')
    return None

def is_data_stale(timestamp):
    if timestamp:
        file_date = datetime.fromisoformat(timestamp)
        return datetime.now() - file_date > timedelta(days=DATA_EXPIRY_DAYS)
    return True

def calculate_weighted_score(obj, type="top"):
    try:
        # Convert values to float for calculations
        prev_hits = float(obj['prevHits'])
        avg = float(obj['avg'])
        at_bats = float(obj['at_bats'])
        
        overall_avg = float(obj['overall_avg'])
        
        # Calculate the weighted score. Will adjust later when we have individual batters' averages
        if type == "top":
            weighted_score = (0.25 * prev_hits) + (0.50 * avg) + (0.25 * at_bats)
        else:
            weighted_score = (0.10 * prev_hits) + (0.60 * avg) + (0.05 * at_bats) + (0.25 * overall_avg)
        
        return weighted_score
    except Exception as e:
        print(f"Error in calculate_weighted_score: {e}")
        print(f"Object causing error: {obj}")
        raise

def convert_to_float(value):
        try:
            return float(value)
        except ValueError:
            if '-' in value:
                numerator, denominator = value.split('-')
                try:
                    return float(numerator) / float(denominator)
                except ValueError:
                    print(f"Cannot convert {value} to float.")
                    return None
            else:
                print(f"Cannot convert {value} to float.")
                return None

if __name__ == '__main__':
    scraped_data = find_urls()
    top_candidates = []
    flattened_data = []
    current_players = []
    
    
    for game in scraped_data:
        game_url = game['url']
        for pitcher in game['pitcher_data']:
            pitcher_name = pitcher['name']
            era = pitcher['era']
            loc_era = pitcher['loc_era']
            vs_right = pitcher['vs_right']
            vs_left = pitcher['vs_left']

            for batter in pitcher['batter_data']:
                if float(batter['avg']) > 0.3:
                    if batter["prevStats"]["hits"] != "-":
                        batter["prevStats"]["hits"] = int(batter["prevStats"]["hits"])
                    else:
                        batter["prevStats"]["hits"] = 2
                    
                    avg = float(batter['avg'])
                    formatted_avg = f"{avg:.3f}"
                    
                    ovr_avg = convert_to_float(batter["prevStats"]["player_avg"])
                    formatted_ovr_avg = f"{ovr_avg:.3f}" if ovr_avg is not None else "N/A"
                    
                    obj = {
                        'batter_name': batter['name'],
                        'overall_avg': formatted_ovr_avg,
                        'avg': formatted_avg,
                        'hits': int(batter['hits']),
                        'at_bats': int(batter['at_bats']),
                        '2b': int(batter['2b']),
                        'home_runs': int(batter['home_runs']),
                        'prevHits': batter["prevStats"]["hits"],
                        'game_url': game_url,
                    }

                    flattened_data.append(obj)

                    if batter['name'] in top_batters:
                        top_candidates.append(obj)
                        current_players.append(batter['name'])

    print('sorting data')
    sorted_data = sorted(top_candidates, key=lambda x: calculate_weighted_score(x), reverse=True)
    sorted_flattened_data = sorted(flattened_data, key=lambda x: calculate_weighted_score(x, "others"), reverse=True)
    
    for item in sorted_flattened_data[:15]:
        player_name = item['batter_name']
        if player_name not in current_players:
            sorted_data.append(item)
            current_players.append(player_name)

    # Print the sorted top candidates
    print("Top batters sorted:")
    headers = ['Batter Name', 'Overall Avg', 'Avg', 'Hits', 'At Bats', '2B', 'Home Runs', 'Prev Game Hits', 'Game URL']
    header_row = "{:<20} {:<15} {:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<30}".format(*headers)
    print(header_row)
    print("-" * len(header_row))

    # Print each row of data
    for item in sorted_data:
        print("{:<20} {:<15} {:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<30}".format(
            item['batter_name'],
            item['overall_avg'],
            item['avg'],
            item['hits'],
            item['at_bats'],
            item['2b'],
            item['home_runs'],
            item['prevHits'],
            item['game_url']
        ))