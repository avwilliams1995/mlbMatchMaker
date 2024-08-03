import requests
from scrapeFunc import scrape_urls
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime, timedelta
from scrapeCache import scrape_with_cache


def find_urls():
    today = datetime.today()

    # Uncomment the following line to scrape data for tomorrow
    # today = today + timedelta(days=1)

    date = today.strftime('%Y%m%d')  
    
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
    
    return game_urls

    
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

    


def scale_score(type, value):
    if type == "avg_against":
        if value>=.7:
            return 10
        elif value>=.6:
            return 8.5
        elif value>=.4:
            return 7
        elif value>=.333:
            return 5
        elif value>=.27:
            return 3
        else:
            return 1
    elif type == "atbats":
        if value>=25:
            return 10
        elif value>=20:
            return 8.5
        elif value>=15:
            return 7
        elif value>=10:
            return 5
        elif value>=5:
            return 4
        else:
            return 0
    elif type == "avg_ovr":
        if value>=.310:
            return 10
        elif value>=.3:
            return 9
        elif value>=.275:
            return 7
        elif value>=.25:
            return 5
        elif value>=.220:
            return 3
        else:
            return 1
    elif type == "hand_avg":
        if value>=.300:
            return 10
        elif value>=.28:
            return 8.5
        elif value>=.26:
            return 7
        elif value>=.24:
            return 5
        elif value>=.200:
            return 3
        else:
            return 1


def calculate_weighted_score(obj, type="top"):
    try:
        # Convert values to float for calculations
        if obj['prevHits'] == "-":
            prev_hits = 3
        elif obj['prevHits'] == 0:
            prev_hits = 10
        elif obj['prevHits'] == 1: 
            prev_hits = 5
        else:
            prev_hits = 2
        avg = scale_score("avg_against", float(obj['avg']))
        at_bats = scale_score("atbats", float(obj['at_bats']))
        hand_avg = scale_score("hand_avg", convert_to_float(obj['hand_avg']))
        overall_avg = scale_score("avg_ovr", float(obj['overall_avg']))
        vs_hand = scale_score("avg_against", float(obj['vs_hand']))
        last_15 = scale_score("avg_against", float(obj['last_15']))

        
        # Calculate the weighted score. Will adjust later when we have individual batters' averages
        if type == "top":
            weighted_score = (0.3 * prev_hits) + (0.15 * avg) + (0.2 * at_bats) + (0.10 * hand_avg) + (0.1 * overall_avg) + (0.05 * vs_hand) + (0.10 * last_15)
        else:
            weighted_score = (0.2 * prev_hits) + (0.2 * avg) + (0.2 * at_bats) + (0.15 * overall_avg) + (0.05 * vs_hand) + (0.15 * last_15)
        
        return weighted_score
    except Exception as e:
        print(f"Error in calculate_weighted_score: {e}")
        print(f"Object causing error: {obj}")
        raise

def convert_to_float(value):
        if value == "HR":
            return .2
        try:
            return float(value)
        except ValueError:
            return .2



if __name__ == '__main__':
    urls = find_urls()
    scraped_data = scrape_with_cache(urls)
    # scraped_data = scrape_with_cache(urls, True)
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
                if ("player_avg" in batter["prevStats"] and "hits" in batter["prevStats"] and "hand" in batter["prevStats"]):
                    if float(batter['avg']) >= 0.25 and convert_to_float(batter["prevStats"]["player_avg"]) >= .23:
                        if batter["prevStats"]["hits"] != "-":
                            batter["prevStats"]["hits"] = int(batter["prevStats"]["hits"])
                        else:
                            batter["prevStats"]["hits"] = 1
                        
                        avg = float(batter['avg'])
                        formatted_avg = f"{avg:.3f}"
                        
                        ovr_avg = convert_to_float(batter["prevStats"]["player_avg"])
                        formatted_ovr_avg = f"{ovr_avg:.3f}" if ovr_avg is not None else "N/A"
                        
                        vs_hand = convert_to_float(batter["prevStats"]["vs_hand"])
                        formatted_hand_avg = f"{vs_hand:.3f}" 


                        if batter["prevStats"]['hand'] == 'Right':
                            hand_avg = vs_right
                        elif batter["prevStats"]['hand'] == 'Left':
                            hand_avg = vs_left
                        elif batter["prevStats"]['hand'] == 'Both':
                            if vs_right > vs_left:
                                hand_avg = vs_right
                            else:
                                hand_avg = vs_left
                        
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
                            "opp_era": pitcher['era'],
                            "loc_era": pitcher['loc_era'],
                            "hand_avg": hand_avg,
                            "vs_hand": vs_hand,
                            "last_15": batter["prevStats"]["last_15"]
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
    headers = ['Batter Name', 'Ovr Avg', 'Pitcher vs_hand',  "vs_hand", "last_15", 'vs pitcher', 'Hits', 'At Bats', '2B', 'HR', 'Prev Hits', 'Game URL']
    header_row = "{:<20} {:<15} {:<15} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<30}".format(*headers)
    print(header_row)
    print("-" * len(header_row))

    # Print each row of data
    found = False
    for item in sorted_data:
        if item['batter_name'] not in top_batters and not found:
            print(" ")
            print('---------------------------------')
            print(" ")
            found = True
            
        print("{:<20} {:<15} {:<15} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<30}".format(
            item['batter_name'][0:18],
            item['overall_avg'],
            item['hand_avg'],
            item["vs_hand"], 
            item["last_15"],
            item['avg'],
            item['hits'],
            item['at_bats'],
            item['2b'],
            item['home_runs'],
            item['prevHits'],
            item['game_url']
))