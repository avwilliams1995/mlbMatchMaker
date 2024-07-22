import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

def scrape_batter_splits(pitcher_url):
    
    splits_url = pitcher_url.replace('/player/_/id/', '/player/batvspitch/_/id/')
    print('pitcher url ------',splits_url)
    response = requests.get(splits_url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to retrieve the splits page. Status code: {response.status_code}')
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')

    breakdown_data = []

    # Extract Breakdown section
    # breakdown_section = soup.select("tbody.Table__TBODY")
    # print('breakdown section ------',breakdown_section)
    tbodies = soup.find_all('tbody', class_='Table__TBODY')

   

    # Iterate over each 'tr' in the 'tbody'
    for row in tbodies[1].find_all('tr', class_='Table__TR Table__TR--sm Table__even'):
        cells = row.find_all('td')
        print(cells[9])

        if len(cells) > 1 and cells[9] and cells[0]:
            breakdown_data.append({
            "name": cells[0].text.strip(),
            "hits": cells[2].text.strip(),
            "at_bats": cells[1].text.strip(),
            "2b": cells[3].text.strip(),
            "home_runs": cells[5].text.strip(),
            "avg": cells[9].text.strip()
            })
                            
    return breakdown_data

           
    


# '-----------------------------------------------------------------------------'





def scrape_pitcher_splits(pitcher_url, i):
    if (i % 2 == 0):
        location = "away"
    else:
        location = "home"
    
    locStr = location + "_era"
    
    splits_url = pitcher_url.replace('/player/_/id/', '/player/splits/_/id/')
    
    
    
    # print(splits_url)
    response = requests.get(splits_url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to retrieve the splits page. Status code: {response.status_code}')
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')

    breakdown_data = {
        "era": "0.00",
        locStr: "0.00"
    }
    right_left_data = {
        "vs_right": "0.00",
        "vs_left": "0.00"
    }


    # Extract Breakdown section
    if (location == "home"):
        breakdown_section = soup.select('tr.Table__TR.Table__TR--sm.Table__even[data-idx="5"]')
    else:  
        breakdown_section = soup.select('tr.Table__TR.Table__TR--sm.Table__even[data-idx="6"]')

    all_section = soup.select('tr.Table__TR.Table__TR--sm.Table__even[data-idx="1"]')
    
    firstName = soup.find('span', class_='truncate min-w-0 fw-light')
    lastName = soup.find('span', class_='truncate min-w-0')
    
    first = firstName.text.strip()
    last = lastName.text.strip()
    name = first + " " + last


# Iterate over the found elements to locate and extract the specific value
    for section in breakdown_section:
        cells = section.find_all('td')
        if cells and len(cells) > 1:  # Ensure there are multiple cells and not just a header or single-cell row
            breakdown_data['loc_era'] = cells[0].text.strip()  # Assuming '1.24' is in the first cell
            break

    for section in all_section:
        cells = section.find_all('td')
        if cells and len(cells) > 1:  # Ensure there are multiple cells and not just a header or single-cell row
            breakdown_data['era'] = cells[0].text.strip()  # Assuming '1.24' is in the first cell
            break
    
    left_section = soup.select('tr.Table__TR.Table__TR--sm.Table__even[data-idx="10"]')
    right_section = soup.select('tr.Table__TR.Table__TR--sm.Table__even[data-idx="11"]')


    for section in left_section:
        cells = section.find_all('td')
        if cells and len(cells) > 1:  # Ensure there are multiple cells and not just a header or single-cell row
            right_left_data["vs_left"] = cells[12].text.strip()  # Assuming '1.24' is in the first cell
            break
    for section in right_section:
        cells = section.find_all('td')
        if cells and len(cells) > 1:  # Ensure there are multiple cells and not just a header or single-cell row
            right_left_data["vs_right"] = cells[12].text.strip()  # Assuming '1.24' is in the first cell
            break

    final = {
        "name": name,
        "era": breakdown_data['era'],
        locStr: breakdown_data[locStr],
        "vs_right": right_left_data['vs_right'],
        "vs_left": right_left_data['vs_left']
    }
    return final


# '-----------------------------------------------------------------------------'



def scrape_urls(urls):
    
    final_data = []
    for game_url in urls:
        # Send a GET request to the game URL with headers
        response = requests.get(game_url, headers=headers)
        if response.status_code != 200:
            print(f'Failed to retrieve the game page. Status code: {response.status_code}')
            exit()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find pitcher URLs

        
        pitcher_elements = soup.select('div.Pitchers__Athlete a')

        # Extract URLs
        pitcher_urls = [a['href'] for a in pitcher_elements]

        #   Print the extracted URLs      
            
        
        # Print and scrape each pitcher's splits data
        pitcher_data = []
        print('fetching pitchers for game', urls.index(game_url) + 1  , "...")
        for i in range(0, len(pitcher_urls)):
            
            splits_data = scrape_pitcher_splits(pitcher_urls[i], i)
            batter_data = scrape_batter_splits(pitcher_urls[i])
            splits_data["batter_data"] = batter_data
            pitcher_data.append(splits_data)
        
        final_data.append({"url": game_url, "pitcher_data": pitcher_data})


    return final_data



        




