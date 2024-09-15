# A League of Legends Recommender System

## Project Description
This project is a personal endeavor aimed at building a recommender system for the popular game _League of Legends_It scrapes data from the Riot Games API and sites like [op.gg](https://op.gg/) to analyze popular in-game choices made by top players. The system provides recommendations for champion builds—items, runes, stats, and summoner spells—based on these choices. While similar to tools available for public use, this project serves as a learning experience in data collection, analysis, and system development, rather than being intended for widespread usage.

## Usage
To use the recommender system, run `recommender.py`.

## Outline
1. `Data Scraping and Cleaning` - We collect match data from the Riot API by scraping the summoner IDs from the top leaderboards. We then find account PUUIDS from these summoner IDs using the same API, and for each PUUID scrape the recent match history. Then the match details of each match is requested from the API. We also use the `selenium` library to gather the total number of players in a division from [op.gg](https://op.gg/).
2. `Data Analysis` - Using the data from the previous part, we perform an exploratory analysis of the data gathered. While some conclusions reached are obvious to one who has played the game, some may not be so obvious. This is not a complete analysis of the data. The match details retrieved from the API are so dense that one can probe much deeper should one wish.
3. `Recommender System` - We narrow the data down to Champions, Roles, Runes, Stats, Items, and Summoner Spells. We create a system where given a champion and role, the most popular items, rune pages and runes, stats, and summoner spells are returned. This works the same way as on [op.gg](https://op.gg/): the recommended items and runes are based off a count of the most popular choices made by top players. A simple GUI is created to interface with the system.# league
