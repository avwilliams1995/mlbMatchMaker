import requests
from bs4 import BeautifulSoup
import sys
import json

def scrape_golf_scores():
    url = "https://www.espn.com/golf/leaderboard"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    teams = [
        {"name": "Harry", "golfer": "Xander Schauffele", "score": 0},
        {"name": "Topping", "golfer": "Brooks Koepka", "score": 0},
        {"name": "Wilson", "golfer": "Scottie Scheffler", "score": 0},
        {"name": "McGranahan", "golfer": "Tony Finau", "score": 0},
        {"name": "Drew", "golfer": "Collin Morikawa", "score": 0},
        {"name": "Nelson", "golfer": "Robert MacIntyre", "score": 0},
        {"name": "Sam", "golfer": "Tyrrell Hatton", "score": 0},
        {"name": "Addison", "golfer": "Ludvig Åberg", "score": 0},
        {"name": "2e", "golfer": "Viktor Hovland", "score": 0},
        {"name": "Reid", "golfer": "Bryson DeChambeau", "score": 0},
        {"name": "Bug", "golfer": "Tommy Fleetwood", "score": 0},
        {"name": "Topping", "golfer": "Rory McIlroy", "score": 0}
    ]

    response = requests.get(url, headers=headers)
    print(response.status_code, " ")
    if response.status_code != 200:
        return {"error": f'Failed to retrieve the golf stats page. Status code: {response.status_code}'}

    soup = BeautifulSoup(response.content, 'html.parser')
    leaderboard_entries = soup.find_all('tr', class_='PlayerRow__Overview')

    golfer_scores = {}
    for entry in leaderboard_entries:
        golfer_name_tag = entry.find('a', class_='leaderboard_player_name')
        score_tag = entry.find_all('td')[3]  # Assuming the score is in the 4th <td>
        
        if golfer_name_tag and score_tag:
            golfer_name = golfer_name_tag.text.strip()
            score = score_tag.text.strip()
            golfer_scores[golfer_name] = score

    for team in teams:
        golfer_name = team['golfer']
        if golfer_name in golfer_scores:
            team['score'] = golfer_scores[golfer_name]

    return teams

if __name__ == "__main__":
    result = scrape_golf_scores()
    print(json.dumps(result))
