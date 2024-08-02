import os
import pickle
from datetime import datetime, timedelta
import pytz
from scrapeFunc import scrape_urls

CACHE_FILE = "mlb_data_cache.pkl"

def get_expiration_time():
    now = datetime.now(pytz.timezone('US/Eastern'))
    tomorrow_5am = (now + timedelta(days=1)).replace(hour=5, minute=0, second=0, microsecond=0)
    return tomorrow_5am

def is_cache_valid():
    if os.path.exists(CACHE_FILE):
        cache_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE), pytz.timezone('US/Eastern'))
        expiration_time = get_expiration_time()
        return cache_time < expiration_time
    return False

def load_cache():
    try:
        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        print("Cache file is corrupted or empty. Fetching fresh data.")
        return None

def save_cache(data):
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(data, f)

def scrape_with_cache(urls):
    if is_cache_valid():
        print("Using cached data")
        cached_data = load_cache()
        if cached_data is not None:
            return cached_data
    
    print("Fetching fresh data")
    scraped_data = scrape_urls(urls)
    save_cache(scraped_data)
    return scraped_data