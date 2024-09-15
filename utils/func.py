# Necessary imports
from dotenv import load_dotenv
import json
import os
import numpy as np
import pandas as pd
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import ttk



def get_ranked_players(tier, region='NA1', div_start=1, div_end=4, page_start=1, page_end=1):
    """
    Gets the encrypted summoner IDs of current ranked players of a single tier, all divisions.

    Args:
        tier (str): Tier of rankings to retrieve. Valid options are:
            - `CHALLENGER`
            - `GRANDMASTER`
            - `MASTER`
            - `DIAMOND`
            - `EMERALD`
            - `PLATINUM`
            - `GOLD`
            - `SILVER`
            - `BRONZE`
            - `IRON`
        region (str, optional): Region. Defaults to 'NA1'.
        div_start (int, optional): Only relevant for tiers `DIAMOND` and lower. Division to start retrieving on. Defaults to 1.
        div_end (int, optional): Only relevant for tiers `DIAMOND` and lower. Division to end retrieving on. Must be greater than or equal to div_start. Max of 4. Defaults to 4.
        page_start (int, optional): Only relevant for tiers `DIAMOND` and lower. Page to start retrieving on. Defaults to 1.
        page_end (int, optional): Only relevant for tiers `DIAMOND` and lower. Page to end retrieving on. Must be greater than or equal to page_start. Defaults to 1.

    Returns:
        list: Encrypted summoner IDs.

    Raises:
        ValueError: If `tier` is not valid.
        ValueError: If `div_end` is less than `div_start` or greater than 4.
        ValueError: If `page_end` is less than `page_start`.
        requests.exceptions.HTTPError: If an HTTP error occurs during the request.
        Exception: For other errors during the request.
    """

    # Validate tier
    valid_tiers = ['challenger', 'grandmaster', 'master', 'diamond', 'emerald', 'platinum', 'gold', 'silver', 'bronze', 'iron']
    if tier.lower() not in valid_tiers:
        raise ValueError('Invalid tier.')

    # Handle top 3 tiers with different URL
    if tier.lower() in ['challenger', 'grandmaster', 'master']:
        url = f'https://{region}.api.riotgames.com/lol/league/v4/{tier.lower()}leagues/by-queue/RANKED_SOLO_5x5?api_key={api_key}'
        try:
            print(f'Retrieving {tier.capitalize()}')
            response = requests.get(url)
            response.raise_for_status()             # Check if the request was successful
            return [entry['summonerId'] for entry in response.json()['entries']]

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Error occurred: {err}')
            raise

    # Validate divisions and pages
    if div_start > div_end or div_end > 4:
        raise ValueError('div_end must be greater than or equal to div_start and less than or equal to 4.')
    if page_start > page_end or page_start < 1:
        raise ValueError('page_start must be greater than 0 and less than or equal to page_end.')

    summoner_ids = []
    divisions = ['I', 'II', 'III', 'IV'][div_start - 1:div_end]

    # Loop through selected divisions
    for div in divisions:
        # Loop through selected pages
        for page in range(page_start, page_end + 1):
            url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier.upper()}/{div}?page={page}&api_key={api_key}'
            try:
                print(f'Retrieving {tier.capitalize()} {div} page {page}')
                api_response = requests.get(url)
                api_response.raise_for_status()     # Check if the request was successful
                data = api_response.json()
                summoner_ids.extend(entry['summonerId'] for entry in data)
                
                # To avoid hitting API limits. Do not run on final loop
                if not (div == divisions[-1] and page == page_end):
                    time.sleep(1.25)

            except requests.exceptions.HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                raise
            except Exception as err:
                print(f'Error occurred: {err}')
                raise

    return summoner_ids



def scrape_opgg():
    # YOU WILL NEED TO SPECIFY YOUR OWN CHROME EXECUTABLE PATH
    chrome_options = Options()
    chrome_options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

    # WebDriver path
    chromedriver_path = os.path.join('utils', 'chromedriver-win64', 'chromedriver.exe')

    # Set up the WebDriver with automatic ChromeDriver management
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    # Open the webpage
    driver.get("https://www.op.gg/statistics/tiers")

    # Wait for the table to load
    driver.implicitly_wait(2)

    # Find the table element
    table = driver.find_element(By.CSS_SELECTOR, "table")

    # Extract table rows
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Loop through the rows and columns to get the data
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)

    driver.quit()

    return data



def get_puuid(summonerId, region='NA1'):
    """
    Gets the PUUID from an encrypted summoner ID.

    Args:
        summonerId (str): Encrypted Summoner ID.
        region (str, optional): Region. Defaults to 'NA1'.

    Returns:
        str: puuid

    Raises:
        ValueError: If the summonerId is None.
        requests.exceptions.HTTPError: If an HTTP error occurs during the request.
        Exception: For other errors during the request.
    """

    if summonerId is None:
        raise ValueError('Empty summoner ID.')

    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['puuid']

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        print(f'Error occurred: {err}')
        raise



def get_match_history(puuid, region='americas', start=0, count=20):
    """
    Gets the match history of player from their PUUID.

    Args:
        puuid (str): PUUID of player.
        region (str, optional): Region. Defaults to 'americas'.
        start (int, optional): Start index of matches. Defaults to 0
        count (int, optional): Number of match IDs to return. Max 100. Defaults to 20.

    Returns:
        list: match IDs.

    Raises:
        ValueError: If the puuid is None.
        requests.exceptions.HTTPError: If an HTTP error occurs during the request.
        Exception: For other errors during the request.
    """

    if puuid is None:
        raise ValueError('Empty PUUID.')

    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}&api_key={api_key}'
    try:
        print(f'Retrieving last {count} matches for {puuid}')
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        print(f'Error occurred: {err}')
        raise



def get_match_details(matchId, region='americas'):
    """
    Gets the relevent details of a match from its ID.

    Args:
        matchId (str): ID of the match.
        region (str, optional): Region. Defaults to 'americas'.

    Returns:
        dict: All of the match details.

    Raises:
        ValueError: If the matchId is None.
        requests.exceptions.HTTPError: If an HTTP error occurs during the request.
        Exception: For other errors during the request.
    """

    if matchId is None:
        raise ValueError('Empty matchId.')

    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        print(f'Error occurred: {err}')
        raise



def json_extract(obj, key):
    def extract(obj, key):
        values = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    values.append(v)
                if isinstance(v, (dict, list)):
                    values.extend(extract(v, key))
        elif isinstance(obj, list):
            for item in obj:
                values.extend(extract(item, key))

        return values

    return extract(obj, key)



def process_match(match_json):
    """
    Processes the match via its JSON into a pandas DataFrame with the most relevant information.

    Args:
        match_json (dict): The JSON of match details.

    Returns:
        pd.DataFrame: A Dataframe containing the relevant match information.

    Raises:
        ValueError: If the match is not a ranked game or the game duration is less than 15 minutes.
    """

    info = match_json['info']
    players = info['participants']

    # Filter out non-ranked games and remakes
    if info['queueId'] != 420:
        raise ValueError('Not a ranked game.')
    if info['gameDuration'] < 900:
        raise ValueError('Game too short.')

    # Define columns of DataFrame
    match_data = {
        'Match ID': [match_json['metadata']['matchId']] * 10,
        'Game Duration': [info['gameDuration']] * 10,
        'Game Version': [info['gameVersion']] * 10,
        'Summoner Name': [player['riotIdGameName'] if 'riotIdGameName' in player else player['riotIdName'] for player in players],
        'Summoner Tag': [player['riotIdTagline'] for player in players],
        'Champion ID': [player['championId'] for player in players],
        'Champion Name': [player['championName'] for player in players],
        'Champion Level': [player['champLevel'] for player in players],
        'Team': [player['teamId'] for player in players],
        'Role': [player['teamPosition'] for player in players],
        'Kills': [player['kills'] for player in players],
        'Deaths': [player['challenges']['deathsByEnemyChamps'] for player in players],
        'Assists': [player['assists'] for player in players],
        'CS': [player['totalMinionsKilled']for player in players],
        'CS (Jungle)': [(player['totalAllyJungleMinionsKilled'] + player['totalEnemyJungleMinionsKilled']) for player in players],
        'First Blood': [player['firstBloodKill'] for player in players],
        'First Tower': [player['firstTowerKill'] for player in players],
        'Objective Stolen': [player['objectivesStolen'] for player in players],
        'Total Gold Earned': [player['goldEarned'] for player in players],
        'Gold Spent': [player['goldSpent'] for player in players],
        'Gold/Minute': [player['challenges']['goldPerMinute'] for player in players],
        'Damage Dealt': [player['totalDamageDealtToChampions'] for player in players],
        '% of Team\'s Damage': [player['challenges']['teamDamagePercentage'] for player in players],
        'Damage Taken': [player['totalDamageTaken'] for player in players],
        'Damage Mitigated': [player['damageSelfMitigated'] for player in players],
        'Heal and Shielding': [player['challenges']['effectiveHealAndShielding'] for player in players],
        'CC Time Dealt': [player['totalTimeCCDealt'] for player in players],
        'Turret Plates Taken': [player['challenges']['turretPlatesTaken'] for player in players],
        'Turret Takedowns': [player['turretTakedowns'] for player in players],
        'Vision Score': [player['visionScore'] for player in players],
        'Rune 1': [player['perks']['styles'][0]['selections'][0]['perk'] for player in players],
        'Rune 2': [player['perks']['styles'][0]['selections'][1]['perk'] for player in players],
        'Rune 3': [player['perks']['styles'][0]['selections'][2]['perk'] for player in players],
        'Rune 4': [player['perks']['styles'][0]['selections'][3]['perk'] for player in players],
        'Sec Rune 1': [player['perks']['styles'][1]['selections'][0]['perk'] for player in players],
        'Sec Rune 2': [player['perks']['styles'][1]['selections'][1]['perk'] for player in players],
        'Stat 1': [player['perks']['statPerks']['offense'] for player in players],
        'Stat 2': [player['perks']['statPerks']['flex'] for player in players],
        'Stat 3': [player['perks']['statPerks']['defense'] for player in players],
        'Summ 1': [player['summoner1Id'] for player in players],
        'Summ 2': [player['summoner2Id'] for player in players],
        'Item 1': [player['item0'] for player in players],
        'Item 2': [player['item1'] for player in players],
        'Item 3': [player['item2'] for player in players],
        'Item 4': [player['item3'] for player in players],
        'Item 5': [player['item4'] for player in players],
        'Item 6': [player['item5'] for player in players],
        #'Ward': [player['item6'] for player in players],
        'Triplekills': [player['tripleKills'] for player in players],
        'Quadrakills': [player['quadraKills'] for player in players],
        'Pentakills': [player['pentaKills'] for player in players],
        'Grubs Taken (Team)': [info['teams'][0]['objectives']['horde']['kills'] if player['teamId'] == 100
                          else info['teams'][1]['objectives']['horde']['kills'] for player in players],
        'Heralds Taken (Team)': [info['teams'][0]['objectives']['riftHerald']['kills'] if player['teamId'] == 100
                            else info['teams'][1]['objectives']['riftHerald']['kills'] for player in players],
        'Barons Taken (Team)': [info['teams'][0]['objectives']['baron']['kills'] if player['teamId'] == 100
                           else info['teams'][1]['objectives']['baron']['kills'] for player in players],
        'Dragons Taken (Team)': [info['teams'][0]['objectives']['dragon']['kills'] if player['teamId'] == 100
                            else info['teams'][1]['objectives']['dragon']['kills'] for player in players],
        'Game Ended in Surrender': [player['gameEndedInSurrender'] for player in players],
        'Win': [player['win'] for player in players]
    }

    match_df = pd.DataFrame(match_data)

    return match_df



def name_replace(df):
    # Lists of rune, summoner spell, and item IDs and names
    runes = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json'
    summs = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/summoner-spells.json'
    items = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json'

    # Getting the JSON data
    runes_json = requests.get(runes).json()
    summs_json = requests.get(summs).json()
    items_json = requests.get(items).json()

    # Extracting the IDs and names
    runes_id = json_extract(runes_json, 'id')
    runes_name = json_extract(runes_json, 'name')
    summs_id = json_extract(summs_json, 'id')
    summs_name = json_extract(summs_json, 'name')
    items_id = json_extract(items_json, 'id')
    items_name = json_extract(items_json, 'name')

    # Create dictionaries of IDs and names
    runes_dict = dict(map(lambda i, j: (i, j), runes_id, runes_name))
    summs_dict = dict(map(lambda i, j: (i, j), summs_id, summs_name))
    items_dict = dict(map(lambda i, j: (int(i), j), items_id, items_name))
    teams_dict = {100: 'Blue', 200: 'Red'}

    # Replace IDs with names in the DataFrame
    rune_columns = ['Rune 1', 'Rune 2', 'Rune 3', 'Rune 4', 'Sec Rune 1', 'Sec Rune 2', 'Stat 1', 'Stat 2', 'Stat 3']
    summ_columns = ['Summ 1', 'Summ 2']
    item_columns = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6']
    df[rune_columns] = df[rune_columns].replace(runes_dict)
    df[summ_columns] = df[summ_columns].replace(summs_dict)
    df[item_columns] = df[item_columns].replace(items_dict)
    df['Team'] = df['Team'].replace(teams_dict)

    return df



def classify_champions(version):
    # Fetch champion data from Riot's Data Dragon
    champion_url = f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json'
    response = requests.get(champion_url)

    if response.status_code != 200:
        raise Exception(f'Failed to fetch champion data: {response.status_code}')

    champion_data = response.json()
    champion_classes = {}

    for champ_name, champ_info in champion_data.get('data', {}).items():
        classes = champ_info.get('tags', [])      # Champion class (Mage, Support, Tank, etc.)

        champion_classes[champ_name] = {
            'classes': classes
        }

    return champion_classes



def filter_items(df, item_columns, finished_items):
    for col in item_columns:
        df[col] = df[col].apply(lambda x: x if x in finished_items else np.nan)
    return df



def filter_columns(df, columns_to_keep):
    return df[columns_to_keep]



def champ_name_upper(df):
    df['Champion Name'] = df['Champion Name'].str.upper()
    return df



def prep_for_rec(df, item_columns, finished_items, columns_to_keep):
    df_copy = df.copy()
    df_copy = name_replace(df_copy)
    df_copy = filter_items(df_copy, item_columns, finished_items)
    df_copy = filter_columns(df_copy, columns_to_keep)
    df_copy = champ_name_upper(df_copy)
    return df_copy



def aggregate_frequencies(df, column_list):
    combined_series = pd.concat([df[col] for col in column_list], ignore_index=True)
    frequencies = combined_series.dropna().value_counts()       # Drop NaN values before counting
    return frequencies



def aggregate_runes(df, primary_rune_columns, secondary_rune_columns, rune_section_map, sec_rune_section_map):
    # Initialize dictionaries to store rune counts
    rune_sections = {section: {slot: {rune: 0 for rune in runes} for slot, runes in slots.items()}
                     for section, slots in rune_section_map.items()}
    sec_rune_sections = {section: {slot: {rune: 0 for rune in runes} for slot, runes in slots.items()}
                         for section, slots in sec_rune_section_map.items()}

    # Count primary runes
    for column, slot in zip(primary_rune_columns, ['Keystone', 'Slot 1', 'Slot 2', 'Slot 3']):
        rune_counts = df[column].value_counts()

        for rune, count in rune_counts.items():
            for section, slots in rune_section_map.items():
                if rune in rune_sections[section][slot]:
                    rune_sections[section][slot][rune] += count
    
    # Combine counts from Sec Rune 1 and Sec Rune 2 for secondary runes
    combined_sec_runes = pd.concat([df['Sec Rune 1'], df['Sec Rune 2']])
    combined_sec_rune_counts = combined_sec_runes.value_counts()

    # Count secondary runes (excluding keystones) using combined counts
    for rune, count in combined_sec_rune_counts.items():
        for section, slots in sec_rune_section_map.items():
            for slot, runes in slots.items():
                if rune in runes:
                    sec_rune_sections[section][slot][rune] += count
    
    return rune_sections, sec_rune_sections



def aggregate_stats(df, stat_section_map):
    stat_sections = {category: {stat: 0 for stat in stats} for category, stats in stat_section_map.items()}

    for stat_column, category in zip(['Stat 1', 'Stat 2', 'Stat 3'], ['Offense', 'Flex', 'Defense']):
        stat_counts = df[stat_column].value_counts()

        for stat, count in stat_counts.items():
            if stat in stat_sections[category]:
                stat_sections[category][stat] += count
    
    return stat_sections



def recommend_based_on_champion(df, champion_name, role, rune_section_map, sec_rune_section_map, stat_section_map):
    # Filter data by role and champion
    df_filtered = df[(df['Champion Name'] == champion_name) & (df['Role'] == role)]
    
    if df_filtered.empty:
        return f'No data available for champion {champion_name} in role {role}.'
    
    item_columns = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6']
    rune_columns = ['Rune 1', 'Rune 2', 'Rune 3', 'Rune 4']
    sec_rune_columns = ['Sec Rune 1', 'Sec Rune 2']
    stat_columns = ['Stat 1', 'Stat 2', 'Stat 3']
    summoner_spell_columns = ['Summ 1', 'Summ 2']
    
    # Aggregating different data types
    item_frequencies = aggregate_frequencies(df_filtered, item_columns)
    rune_frequencies, sec_rune_frequencies = aggregate_runes(df_filtered, rune_columns, sec_rune_columns, rune_section_map, sec_rune_section_map)
    stat_frequencies = aggregate_stats(df_filtered, stat_section_map)
    summoner_spell_frequencies = aggregate_frequencies(df_filtered, summoner_spell_columns)
    
    return {
        'Items': item_frequencies,
        'Runes': rune_frequencies,
        'Secondary Runes': sec_rune_frequencies,
        'Stats': stat_frequencies,
        'Summoner Spells': summoner_spell_frequencies
    }



def display_most_popular(recommendations, num_items=10):

    if type(recommendations) == str:
        return recommendations

    def get_most_popular_runes(rune_sections):
        most_popular = {}
        max_count = 0
        for section, slots in rune_sections.items():
            section_count = sum(max(runes.values()) for slot, runes in slots.items())
            if section_count > max_count:
                max_count = section_count
                most_popular = {section: slots}
        return most_popular

    res = ''

    res += 'Most Popular Items:'
    res += f'\n{'-' * 20}'
    res += f'\n{recommendations['Items'].head(num_items).to_string()}'

    res += '\n\n\nMost Popular Runes:'
    res += f'\n{'-' * 20}'
    most_popular_runes = get_most_popular_runes(recommendations.get('Runes', {}))
    for section, slots in most_popular_runes.items():
        res += f'\n{section}:'
        for slot, runes in slots.items():
            res += f'\n  {slot}:'
            for rune, count in runes.items():
                res += f'\n    {rune}: {count}'

    res += '\n\n\nMost Popular Secondary Runes:'
    res += f'\n{'-' * 20}'
    most_popular_sec_runes = get_most_popular_runes(recommendations.get('Secondary Runes', {}))
    for section, slots in most_popular_sec_runes.items():
        res += f'\n{section}:'
        for slot, runes in slots.items():
            res += f'\n  {slot}:'
            for rune, count in runes.items():
                res += f'\n    {rune}: {count}'

    res += '\n\n\nMost Popular Stats:'
    res += f'\n{'-' * 20}'
    stat_sections = recommendations.get('Stats', {})
    for category, stats in stat_sections.items():
        res += f'\n{category}:'
        for stat, count in stats.items():
            res += f'\n  {stat}: {count}'

    res += '\n\n\nMost Popular Summoner Spells:'
    res += f'\n{'-' * 20}'
    res += f'\n{recommendations['Summoner Spells'].to_string()}'

    return res



def create_recommender(df, champion_names, roles, rune_section_map, sec_rune_section_map, stat_section_map, num_items=10):
    def on_button_click(event=None):
        champion = champion_combobox.get().upper()
        role = role_combobox.get().upper()
        recommendations = recommend_based_on_champion(df, champion, role, rune_section_map, sec_rune_section_map, stat_section_map)
        result = display_most_popular(recommendations, num_items)
        text_window.delete(1.0, tk.END)     # Clear previous text
        text_window.insert(tk.END, result)

    # Create the main window
    root = tk.Tk()
    root.title('Build Recommendation')

    # Create and place the Champion Name dropdown
    champion_label = tk.Label(root, text='Champion Name:')
    champion_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    champion_combobox = ttk.Combobox(root, values=champion_names)
    champion_combobox.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Create and place the Role dropdown
    role_label = tk.Label(root, text='Role:')
    role_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    role_combobox = ttk.Combobox(root, values=roles)
    role_combobox.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    role_combobox.set(roles[0])

    # Create and place the button
    recommendations_button = tk.Button(root, text='Get Recommendations', command=on_button_click)
    recommendations_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Bind Enter key to the button click event
    root.bind('<Return>', on_button_click)

    # Escape to close application
    root.bind('<Escape>', lambda event: root.destroy())

    # Create a frame to hold the text window and scrollbar
    text_frame = tk.Frame(root)
    text_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Create and place the text window
    text_window = tk.Text(text_frame, wrap=tk.WORD, height=50, width=50)
    text_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create and place the scrollbar
    scrollbar = tk.Scrollbar(text_frame, command=text_window.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the text window to use the scrollbar
    text_window.config(yscrollcommand=scrollbar.set)

    # Focus the main window
    root.after(50, root.focus_force())
    root.after(50, lambda: champion_combobox.focus_set())

    # Run the application
    root.mainloop()