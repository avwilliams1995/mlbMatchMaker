import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define headers as a global constant since it's used multiple times
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def scrape_urls(urls):
    final_data = []
    
    for idx, game_url in enumerate(urls, 1):
        response = requests.get(game_url, headers=HEADERS)
        if response.status_code != 200:
            print(f'Failed to retrieve the game page. Status code: {response.status_code}')
            exit()

        soup = BeautifulSoup(response.content, 'html.parser')
        pitcher_elements = soup.select('div.Pitchers__Athlete a')
        pitcher_urls = [a['href'] for a in pitcher_elements]

        # print(f'Fetching pitchers for game {idx}/{len(urls)}...')

        pitcher_data = []
        for i, pitcher_url in enumerate(pitcher_urls):
            splits_data = scrape_pitcher_splits(pitcher_url, i)
            splits_data['batter_data'] = scrape_batter_splits(pitcher_url, splits_data["handedness"])
            pitcher_data.append(splits_data)
        
        final_data.append({"url": game_url, "pitcher_data": pitcher_data})

    return final_data

def get_hand_avg(player_url, handedness):
    splits_url = player_url.replace('/player/_/id/', '/player/splits/_/id/')
    response = requests.get(splits_url, headers=HEADERS)
    if response.status_code != 200:
        print(f'Failed to retrieve the get_hand_avg url. Status code: {response.status_code}')
        return 0.0  # Default to 0.0 if the request fails

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'Table Table--align-right'})
    if not table:
        print('Could not find the relevant table.')
        return 0.0  # Default to 0.0 if the table is not found

    rows = table.find_all('tr')
    scrape_row = rows[4] if handedness == "Right" else rows[3]
    rows_15 = soup.find_all('tr', class_='Table__TR Table__TR--sm Table__even')
    index = 0
    for row in rows_15:
        if row.find('td', class_='Table__TD').text.strip() == "Last 15 Days":
            index = int(row['data-idx'])
            break

    if index != 0:
        cells_15 = rows[index].find_all('td')  
    cells = scrape_row.find_all('td')
    
    if cells:
        value = cells[12].text.strip()
        if index!= 0:
            last_15_avg = cells_15[12].text.strip()
        else:
            last_15_avg = 0.0
        finalValue = 0.2 if value == "HR" or value == "AVG" else float(value)        
        final_15 = 0.2 if last_15_avg == "HR" else float(last_15_avg)
        return [finalValue, final_15]
    else:
        return [0.0, 0.0]  # Default to 0.0 if cells are empty


def batter_previous_games(player_url, pitcher_hand):
    response = requests.get(player_url, headers=HEADERS)
    if response.status_code != 200:
        print(f'Failed to retrieve the batter_previous_games url. Status code: {response.status_code}')
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    avg_element = soup.select_one('li.flex-expand .StatBlockInner__Value')
    batting_average = avg_element.get_text(strip=True) if avg_element else '0'

    bio_list_items = soup.select('.PlayerHeader__Bio_List li')
    handedness = next(
        (item.find('div', class_='fw-medium clr-black').get_text(strip=True).split('/')[0]
         for item in bio_list_items if item.find('div', class_='ttu').get_text() == 'BAT/THR'), None)

    rows = soup.find_all('tr', class_='Table__TR Table__TR--sm Table__even')
    game_stats = {}

    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 4 and '/' in cells[0].text.strip():
            game_stats = {
                "player_avg": batting_average,
                "date": cells[0].text.strip(),
                "at_bats": cells[3].text.strip(),
                "hits": cells[5].text.strip(),
                "hand": handedness,
                "vs_hand": get_hand_avg(player_url, pitcher_hand)[0],
                "last_15": get_hand_avg(player_url, pitcher_hand)[1]
            }
            break
    
    return game_stats

def scrape_batter_splits(pitcher_url, handedness):
    splits_url = pitcher_url.replace('/player/_/id/', '/player/batvspitch/_/id/')
    response = requests.get(splits_url, headers=HEADERS)
    if response.status_code != 200:
        print(f'Failed to retrieve the splits page. Status code: {response.status_code}')
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    tbodies = soup.find_all('tbody', class_='Table__TBODY')
    breakdown_data = []

    if len(tbodies) > 1:
        for row in tbodies[1].find_all('tr', class_='Table__TR Table__TR--sm Table__even'):
            cells = row.find_all('td')
            if len(cells) == 13 and cells[0].text.strip() != "Totals" and float(cells[9].text.strip()) >= .230:
                player_url = cells[0].find('a')['href']
                prev_stats = batter_previous_games(player_url, handedness)
                breakdown_data.append({
                    "name": cells[0].text.strip(),
                    "hits": cells[2].text.strip(),
                    "at_bats": cells[1].text.strip(),
                    "2b": cells[3].text.strip(),
                    "home_runs": cells[5].text.strip(),
                    "avg": cells[9].text.strip(),
                    "prevStats": prev_stats
                })
                
    
    return breakdown_data

def scrape_pitcher_splits(pitcher_url, i):
    location = "away" if i % 2 == 0 else "home"
    splits_url = pitcher_url.replace('/player/_/id/', '/player/splits/_/id/')
    response = requests.get(splits_url, headers=HEADERS)
    if response.status_code != 200:
        print(f'Failed to retrieve the splits page. Status code: {response.status_code}')
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    
    name = ' '.join([soup.find('span', class_='truncate min-w-0 fw-light').text.strip(),
                     soup.find('span', class_='truncate min-w-0').text.strip()])
    
    bio_list_items = soup.select('.PlayerHeader__Bio_List li')
    handedness = next(
        (item.find('div', class_='fw-medium clr-black').get_text(strip=True).split('/')[1]
         for item in bio_list_items if item.find('div', class_='ttu').get_text() == 'BAT/THR'), None)
    
    breakdown_data = {
        "era": extract_table_data(soup, '1'),
        "loc_era": extract_table_data(soup, '5' if location == "home" else '6')
    }

    right_left_data = {
        "vs_right": extract_table_data(soup, '11', True),
        "vs_left": extract_table_data(soup, '10', True)
    }

    return {
        "name": name,
        "era": breakdown_data['era'],
        "loc_era": breakdown_data["loc_era"],
        "vs_right": right_left_data['vs_right'],
        "vs_left": right_left_data['vs_left'],
        "handedness": handedness
    }

def extract_table_data(soup, idx, avg=False):
    section = soup.select(f'tr.Table__TR.Table__TR--sm.Table__even[data-idx="{idx}"]')
    for row in section:
        cells = row.find_all('td')
        if cells and len(cells) > 1:
            if avg:
                return cells[12].text.strip()
            else: 
                return cells[0].text.strip()
    return "0.00"