import warnings
warnings.filterwarnings("ignore", category=Warning)

import requests
from scrapeFunc import scrape_urls
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime, timedelta
from scrapeCache import scrape_with_cache
import sys

# top batters in league based on batting avg
top_batters = [
    "Aaron Judge", "Freddie Freeman", "Jacob Wilson", "Paul Goldschmidt", "Manny Machado",
    "Jonathan Aranda", "Will Smith", "Steven Kwan", "CJ Abrams", "Alex Bregman", "Jeremy Pena",
    "Brendan Donovan", "Bobby Witt Jr.", "Pete Alonso", "Shohei Ohtani", "Fernando Tatis Jr.",
    "Josh Smith", "Kyle Stowers", "Trea Turner", "Josh Naylor", "Francisco Lindor", "Gavin Lux",
    "Maikel Garcia", "Kerry Carpenter", "Jose Ramirez", "Vladimir Guerrero Jr.", "Jake Meyers",
    "Rhys Hoskins", "Geraldo Perdomo", "Andy Pages", "Hunter Goodman", "Gavin Sheets",
    "Bo Bichette", "Brice Turang", "Gleyber Torres", "Heliot Ramos", "Austin Riley",
    "Luis Arraez", "Jung Hoo Lee", "Nick Castellanos", "Keibert Ruiz", "Zach McKinstry",
    "Corbin Carroll", "Pete Crow-Armstrong", "Joey Bart", "Tyler Soderstrom", "Mike Yastrzemski",
    "George Springer", "Wilyer Abreu", "Victor Scott II"
]

def find_urls(tomorrow=False):
    today = datetime.today()
    if tomorrow:
        today += timedelta(days=1)

    date = today.strftime('%Y%m%d')  
    # print(f"Scraping data for date: {date}")
    url = f"https://www.espn.com/mlb/scoreboard/_/date/{date}"

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != 200:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
        exit()

    soup = BeautifulSoup(response.content, 'html.parser')
    scoreboard_elements = soup.find_all('section', class_='Scoreboard bg-clr-white flex flex-auto justify-between')

    game_urls = []
    for game in scoreboard_elements:
        game_id = game.get('id')
        if game_id:
            game_urls.append(f"https://www.espn.com/mlb/game/_/gameId/{game_id}")
    
    return game_urls

def scale_score(type, value):
    if type == "avg_against":
        if value >= .6: return 10
        elif value >= .450: return 8.5
        elif value >= .325: return 7
        elif value >= .275: return 5
        elif value >= .25: return 3
        else: return 1
    elif type == "atbats":
        if value >= 30: return 10
        elif value >= 20: return 8.5
        elif value >= 15: return 7
        elif value >= 10: return 5
        elif value >= 5: return 3
        else: return 1
    elif type == "avg_ovr":
        if value >= .310: return 10
        elif value >= .3: return 9
        elif value >= .275: return 7
        elif value >= .25: return 5
        elif value >= .220: return 3
        else: return 1
    elif type == "hand_avg":
        if value >= .300: return 10
        elif value >= .28: return 8.5
        elif value >= .26: return 7
        elif value >= .24: return 5
        elif value >= .200: return 3
        else: return 1

def calculate_weighted_score(obj, type="top"):
    try:
        prev_hits = 3 if obj['prevHits'] == "-" else (10 if obj['prevHits'] == 0 else 5 if obj['prevHits'] == 1 else 1)
        avg = scale_score("avg_against", float(obj['avg']))
        at_bats = scale_score("atbats", float(obj['at_bats']))
        hand_avg = scale_score("hand_avg", convert_to_float(obj['hand_avg']))
        overall_avg = scale_score("avg_ovr", float(obj['overall_avg']))
        vs_hand = scale_score("avg_against", float(obj['vs_hand']))
        last_7 = scale_score("avg_against", float(obj['last_7']))

        if type == "top":
            return 0.3 * prev_hits + 0.2 * avg + 0.2 * at_bats + 0.05 * hand_avg + 0.15 * last_7
        else:
            return 0.2 * prev_hits + 0.2 * avg + 0.2 * at_bats + 0.1 * overall_avg + 0.05 * vs_hand + 0.25 * last_7
    except Exception as e:
        print(f"Error in calculate_weighted_score: {e}")
        print(f"Object causing error: {obj}")
        raise

def convert_to_float(value):
    if value == "HR": return .200
    try: return float(value)
    except ValueError: return .200

if __name__ == '__main__':
    clear = len(sys.argv) > 1 and sys.argv[1].lower() == 'true'
    tomorrow = len(sys.argv) > 2 and sys.argv[2].lower() == 'true'

    target_date = datetime.today()
    if tomorrow:
        target_date += timedelta(days=1)

    scrape_date = target_date.strftime('%Y-%m-%d')
    espn_url_date = target_date.strftime('%Y%m%d')

    urls = find_urls(tomorrow)
    scraped_data = scrape_with_cache(urls, clear, scrape_date)
    top_candidates = []
    flattened_data = []
    current_players = []

    for game in scraped_data:
        game_url = game['url']
        for pitcher in game['pitcher_data']:
            for batter in pitcher['batter_data']:
                stats = batter.get("prevStats", {})
                if "player_avg" in stats and "hits" in stats and "hand" in stats:
                    if float(batter['avg']) >= 0.2 and convert_to_float(stats["player_avg"]) >= .2:
                        stats["hits"] = int(stats["hits"]) if stats["hits"] != "-" else 1
                        hand = stats['hand']
                        hand_avg = pitcher['vs_right'] if hand == 'Right' else pitcher['vs_left'] if hand == 'Left' else max(pitcher['vs_right'], pitcher['vs_left'])
                        obj = {
                            'batter_name': batter['name'],
                            'team': stats['team'],
                            'overall_avg': f"{convert_to_float(stats['player_avg']):.3f}",
                            'avg': f"{float(batter['avg']):.3f}",
                            'hits': int(batter['hits']),
                            'at_bats': int(batter['at_bats']),
                            '2b': int(batter['2b']),
                            'home_runs': int(batter['home_runs']),
                            'prevHits': stats["hits"],
                            'game_url': game_url,
                            "opp_era": pitcher['era'],
                            "loc_era": pitcher['loc_era'],
                            "hand_avg": hand_avg,
                            "vs_hand": convert_to_float(stats["vs_hand"]),
                            "last_7": stats["last_7"] 
                        }

                        flattened_data.append(obj)

                        if batter['name'] in top_batters:
                            top_candidates.append(obj)
                            current_players.append(batter['name'])

    sorted_top = sorted(
        top_candidates,
        key=lambda x: calculate_weighted_score(x),
        reverse=True
    )[:10]
    sorted_flattened_data = sorted(flattened_data, key=lambda x: calculate_weighted_score(x, "others"), reverse=True)[:31]


    for idx, batter in enumerate(sorted_top, start=1):
        batter["rank"] = idx

    final_list = list(sorted_top)
    for item in sorted_flattened_data:
        if len(final_list) >= 31:
            break
        name = item["batter_name"]
        if name not in current_players:
            item["rank"] = len(final_list) + 1
            final_list.append(item)
            current_players.append(name)

    print(json.dumps(final_list))