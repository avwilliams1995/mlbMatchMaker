import requests
from bs4 import BeautifulSoup
from datetime import datetime
datetime.today().strftime('%Y-%m-%d')

# date = datetime.today().strftime('%Y%m%d')
# date = "20240712"
# # URL to scrape
# url = f"https://www.espn.com/mlb/scoreboard/_/date/{date}"

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
# }

# # Send a GET request to the URL
# response = requests.get(url, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     print('Successfully fetched the webpage.')
# else:
#     print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
#     exit()

# # Parse the HTML content using BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# #get daily urls
# scoreboard_elements = soup.find_all('section', class_='Scoreboard bg-clr-white flex flex-auto justify-between')

# game_urls = []
# for game in scoreboard_elements:
#     game_id = game.get('id')
#     if game_id:
#         game_urls.append(f"https://www.espn.com/mlb/game/_/gameId/{game_id}")
  
temp_url = "https://www.espn.com/mlb/game/_/gameId/401569882"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
def scrape_pitcher_splits(pitcher_url, i):
    if (i % 2 == 0):
        location = "away"
    else:
        location = "home"
    
    splits_url = pitcher_url.replace('/player/_/id/', '/player/splits/_/id/')
    print(splits_url)
    response = requests.get(splits_url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to retrieve the splits page. Status code: {response.status_code}')
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')

    breakdown_data = {}
    right_left_data = {}

    # Extract Breakdown section
    breakdown_section = soup.find('section', {'id': 'breakdown'})
    if breakdown_section:
        rows = breakdown_section.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:
                breakdown_data[cells[0].text.strip()] = cells[1].text.strip()

    # Extract RIGHT / LEFT section
    right_left_section = soup.find('section', {'id': 'right-left'})
    if right_left_section:
        rows = right_left_section.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:
                right_left_data[cells[0].text.strip()] = cells[1].text.strip()

    return {'Breakdown': breakdown_data, 'Right/Left': right_left_data}

# URL to scrape
game_url = "https://www.espn.com/mlb/game/_/gameId/401569882"

# Define headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Send a GET request to the game URL with headers
response = requests.get(game_url, headers=headers)
if response.status_code != 200:
    print(f'Failed to retrieve the game page. Status code: {response.status_code}')
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find pitcher URLs
pitchers = []
pitcher_links = soup.find_all('a', {'class': 'AnchorLink'})
for link in pitcher_links:
    if 'player/_/id' in link['href']:
        pitchers.append(link['href'])

# Print and scrape each pitcher's splits data
for i in range(1, 2):
    splits_data = scrape_pitcher_splits(pitchers[i], i)
    print(splits_data)


