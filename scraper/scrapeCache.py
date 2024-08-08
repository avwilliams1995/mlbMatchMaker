import os
import pickle
import json
from datetime import datetime, timedelta
import pytz
from scrapeFunc import scrape_urls

CACHE_FILE = "mlb_data_cache.pkl"
CACHE_DATE_FILE = "cache_date.json"

def get_today_date():
    """Returns today's date as a string in the format YYYY-MM-DD."""
    return datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')

def load_json_data(file_path):
    """Load data from a JSON file and return it."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                return data
        except json.JSONDecodeError:
            print(f"Error: The file {file_path} contains invalid JSON.")
            return None
    else:
        print(f"Error: The file {file_path} does not exist.")
        return None

def save_json_data(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(data, file)

def is_cache_valid():
    """Check if the cache is valid based on the date stored in cache_date.json."""
    cache_date_data = load_json_data(CACHE_DATE_FILE)
    if cache_date_data:
        cache_date = cache_date_data.get("date")
        today_date = get_today_date()
        return cache_date == today_date
    return False

def load_cache():
    """Load the cache data from the pickle file."""
    try:
        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        print("Cache file is corrupted or empty. Fetching fresh data.")
        return None

def save_cache(data):
    """Save the cache data and update the cache date."""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE) 
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(data, f)

    # Update cache date in cache_date.json
    save_json_data(CACHE_DATE_FILE, {"date": get_today_date()})

def scrape_with_cache(urls, clear=False):
    """Scrape data with cache functionality."""
    if is_cache_valid() and not clear:
        cached_data = load_cache()
        if cached_data is not None:
            # print("Using cached data")
            return cached_data
    
    # print("Fetching fresh data")
    scraped_data = scrape_urls(urls)
    save_cache(scraped_data)
    return scraped_data