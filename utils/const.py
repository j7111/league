item_columns = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6']

columns_to_keep = [
    'Champion Name', 'Role',
    'Rune 1', 'Rune 2', 'Rune 3', 'Rune 4', 'Sec Rune 1', 'Sec Rune 2', 'Stat 1', 'Stat 2', 'Stat 3',
    'Summ 1', 'Summ 2',
    'Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6'
]

finished_items = [
    'Berserker\'s Greaves', 'Boots of Swiftness', 'Ionian Boots of Lucidity', 'Mercury\'s Treads', 'Plated Steelcaps', 'Sorcerer\'s Shoes', 'Symbiotic Soles', 'Synchronized Souls', 'Zephyr',
    'Abyssal Mask', 'Archangel\'s Staff', 'Ardent Censer', 'Axiom Arc', 'Banshee\'s Veil', 'Black Cleaver', 'Blackfire Torch', 'Blade of The Ruined King',
    'Bloodsong', 'Bloodthirster', 'Bounty of Worlds', 'Celestial Opposition', 'Chempunk Chainsword', 'Cosmic Drive', 'Cryptbloom', 'Dawncore',
    'Dead Man\'s Plate', 'Death\'s Dance', 'Dream Maker', 'Echoes of Helia', 'Eclipse', 'Edge of Night', 'Essence Reaver', 'Experimental Hexplate',
    'Fimbulwinter', 'Force of Nature', 'Frozen Heart', 'Guardian Angel', 'Guinsoo\'s Rageblade', 'Heartsteel', 'Hextech Rocketbelt', 'Hollow Radiance',
    'Horizon Focus', 'Hubris', 'Hullbreaker', 'Iceborn Gauntlet', 'Immortal Shieldbow', 'Imperial Mandate', 'Infinity Edge', 'Jak\'Sho, The Protean',
    'Kaenic Rookern', 'Knight\'s Vow', 'Kraken Slayer', 'Liandry\'s Torment', 'Lich Bane', 'Locket of the Iron Solari', 'Lord Dominik\'s Regards', 'Luden\'s Companion',
    'Malignance', 'Manamune', 'Maw of Malmortius', 'Mejai\'s Soulstealer', 'Mercurial Scimitar', 'Mikael\'s Blessing', 'Moonstone Renewer', 'Morellonomicon',
    'Mortal Reminder', 'Muramana', 'Nashor\'s Tooth', 'Navori Flickerblade', 'Opportunity', 'Overlord\'s Bloodmail', 'Phantom Dancer', 'Profane Hydra',
    'Rabadon\'s Deathcap', 'Randuin\'s Omen', 'Rapid Firecannon', 'Ravenous Hydra', 'Redemption', 'Riftmaker', 'Rod of Ages', 'Runaan\'s Hurricane',
    'Rylai\'s Crystal Scepter', 'Seraph\'s Embrace', 'Serpent\'s Fang', 'Serylda\'s Grudge', 'Shadowflame', 'Shurelya\'s Battlesong', 'Solstice Sleigh', 'Spear of Shojin',
    'Spirit Visage', 'Staff of Flowing Water', 'Statikk Shiv', 'Sterak\'s Gage', 'Stormsurge', 'Stridebreaker', 'Sundered Sky', 'Sunfire Aegis',
    'Terminus', 'The Collector', 'Thornmail', 'Titanic Hydra', 'Trailblazer', 'Trinity Force', 'Umbral Glaive', 'Unending Despair',
    'Vigilant Wardstone', 'Void Staff', 'Voltaic Cyclosword', 'Warmog\'s Armor', 'Winter\'s Approach', 'Wit\'s End', 'Youmuu\'s Ghostblade', 'Yun Tal Wildarrows',
    'Zaz\'Zak\'s Realmspike', 'Zeke\'s Convergence', 'Zhonya\'s Hourglass'
]

rune_section_map = {
    'Precision': {
        'Keystone': ['Press the Attack', 'Fleet Footwork', 'Conqueror'],
        'Slot 1': ['Absorb Life', 'Triumph', 'Presence of Mind'],
        'Slot 2': ['Legend: Alacrity', 'Legend: Haste', 'Legend: Bloodline'],
        'Slot 3': ['Coup de Grace', 'Cut Down', 'Last Stand']
    },
    'Domination': {
        'Keystone': ['Electrocute', 'Dark Harvest', 'Hail of Blades'],
        'Slot 1': ['Cheap Shot', 'Taste of Blood', 'Sudden Impact'],
        'Slot 2': ['Zombie Ward', 'Ghost Poro', 'Eyeball Collection'],
        'Slot 3': ['Treasure Hunter', 'Relentless Hunter', 'Ultimate Hunter']
    },
    'Sorcery': {
        'Keystone': ['Summon Aery', 'Arcane Comet', 'Phase Rush'],
        'Slot 1': ['Nullifying Orb', 'Manaflow Band', 'Nimbus Cloak'],
        'Slot 2': ['Transcendence', 'Celerity', 'Absolute Focus'],
        'Slot 3': ['Scorch', 'Waterwalking', 'Gathering Storm']
    },
    'Resolve': {
        'Keystone': ['Grasp of the Undying', 'Aftershock', 'Guardian'],
        'Slot 1': ['Demolish', 'Font of Life', 'Shield Bash'],
        'Slot 2': ['Conditioning', 'Second Wind', 'Bone Plating'],
        'Slot 3': ['Overgrowth', 'Revitalize', 'Unflinching']
    },
    'Inspiration': {
        'Keystone': ['Glacial Augment', 'Unsealed Spellbook', 'First Strike'],
        'Slot 1': ['Hextech Flashtraption', 'Magical Footwear', 'Cash Back'],
        'Slot 2': ['Triple Tonic', 'Time Warp Tonic', 'Biscuit Delivery'],
        'Slot 3': ['Cosmic Insight', 'Approach Velocity', 'Jack of All Trades']
    }
}

sec_rune_section_map = {
    section: {slot: runes for slot, runes in slots.items() if slot != 'Keystone'}
    for section, slots in rune_section_map.items()
}

stat_section_map = {
    'Offense': ['Adaptive Force', 'Attack Speed', 'Ability Haste'],
    'Flex': ['Adaptive Force', 'Move Speed', 'Health Scaling'],
    'Defense': ['Health', 'Tenacity and Slow Resist', 'Health Scaling']
}