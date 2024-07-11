import requests

def scrape_data():
    # Your scraping logic here
    data = {
        'playerName': 'John Doe',
        'oppPitcher': 'Jane Smith',
        'oppPitcherERASplit': 3.45,
        'oppAB': 25,
        'oppHits': 10,
        'last7': 0.345,
        'last15': 0.290,
        'yesterdayBA': 0.300,
        'homeAwaySplit': 0.310,
        'dayNightSplit': 0.295
    }
    return data

def send_data_to_server(data):
    url = 'http://localhost:3000/api/scraper'
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Data sent successfully')
        print(response.json())
    else:
        print('Failed to send data:', response.status_code, response.text)

if __name__ == '__main__':
    scraped_data = scrape_data()
    send_data_to_server(scraped_data)