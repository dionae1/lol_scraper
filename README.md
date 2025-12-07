# League of Graphs Scraper

A Scrapy project designed to extract League of Legends games data from [LeagueOfGraphs](https://www.leagueofgraphs.com).
The first idea is to use the data collected to train ML models to predicts a winner given 2 compositions.

- **Profile Scraping**: Extracts summoner names from ranking pages, collecting better ranked matches.

## Installation

1. Clone the repository.
2. Install the required dependencies:

```bash
pip install scrapy
```

## Usage

Navigate to the project directory and run the spider:

The following code will create a sqlite database.

```bash
cd lol_scraper
scrapy crawl leagueofgraphs
```

To save the scraped data to a JSON file:

```bash
scrapy crawl leagueofgraphs -o games.json
```

