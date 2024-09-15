import os
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from utils.const import *
from utils.func import prep_for_rec, create_recommender, recommend_based_on_champion, display_most_popular

def main():
    if os.path.exists(os.path.join('data', 'matches_data_prepped.csv')):
        df = pd.read_csv(os.path.join('data', 'matches_data_prepped.csv'))
    elif os.path.exists(os.path.join('data', 'matches_data.csv')):
        df = pd.read_csv(os.path.join('data', 'matches_data.csv'))
        df = prep_for_rec(df, item_columns, finished_items, columns_to_keep)

        os.makedirs('data', exist_ok=True)
        df.to_csv(os.path.join('data', 'matches_data_prepped.csv'), index=False)
    else:
        raise FileNotFoundError('Neither matches_data_prepped.csv nor matches_data.csv exist in the data folder.')

    champion_names = sorted([champion for champion in df['Champion Name'].unique()])
    roles = [role for role in df['Role'].unique()]

    create_recommender(df, champion_names, roles, rune_section_map, sec_rune_section_map, stat_section_map, num_items=10)

if __name__ == '__main__':
    main()