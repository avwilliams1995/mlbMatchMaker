# MLB Daily Batter Analyzer

This project is a web scraping tool designed to collect and analyze Major League Baseball (MLB) player statistics for a specific date. It is designed to fetch daily data from ESPN's MLB scoreboard and provide a weighted score analysis for top batters based on various statistical parameters. The project is built using Python, utilizing libraries such as `requests`, `BeautifulSoup`, and `datetime`.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Processing](#data-processing)
- [Scoring System](#scoring-system)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Web Scraping**: Fetches daily MLB scoreboard data and retrieves URLs for individual games.
- **Data Analysis**: Extracts and processes statistics for pitchers and batters.
- **Weighted Scoring**: Calculates a weighted score for each batter based on specific criteria such as batting average, hits, at-bats, previous game at bats, and more.
- **Top Batters List**: Generates a sorted list of top batters in the league.
- **Caching**: Uses a caching mechanism to avoid redundant data scraping.


## Project still in early stages, notes on why I started this:
  - Gain more knowledge on scraping data
  - Keep enhancing skills on frontend development
  - Have fun betting $5 a day on the top players each day/testing the calculation algo
  Things I want to try:
  - Implementing ML to check if bets are working and what trends it finds. Definitely want to expand my knowledge on this subject


## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/mlb-daily-batter-analyzer.git
    cd scraper
    ```

2. **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Create the required directories for caching (if not already present):**
    ```bash
    touch mlb_data_cache.pkl
    ```

## Usage

1. **Run the scraper:**
    ```bash
    python scraper.py
    ```
   This will scrape the data for today or tomorrow's  MLB games and generate a list of top batters based on their weighted scores. Cache resets will reset after 5am

2. **View the results:**
   The script will output a sorted list of top batters along with their statistics directly to the console.

## Project Structure

- `scraper.py`: The main script that handles the scraping, data processing, and scoring of batters.
- `scrapeFunc.py`: Contains functions that perform the web scraping, including extracting and processing data for individual players and pitchers.
- `scrapeCache.py`: Implements caching to store and reuse scraped data.
- `requirements.txt`: Lists the required Python libraries to run the project.

## Data Processing

The scraper collects data from ESPN's MLB scoreboard for a specified date. The data includes information about games, pitchers, and batters. The collected data is then processed to calculate various statistical metrics such as batting average, hits, at-bats, etc.

## Scoring System

The project uses a weighted scoring system to evaluate batters. The score is calculated based on the following parameters:
- **Previous Hits**: Assigns a score based on the number of hits in previous games.
- **Batting Average**: Considers both overall batting average and average against specific pitcher handedness.
- **At-bats**: Rewards batters who have had more at-bats.
- **Recent Performance**: Evaluates a player's performance in prev game and last 15 days.

### Example Scoring Calculation:

```python
weighted_score = (0.3 * prev_hits) + (0.15 * avg) + (0.2 * at_bats) + 
                 (0.10 * hand_avg) + (0.1 * overall_avg) + (0.05 * vs_hand) + 
                 (0.10 * last_15)

