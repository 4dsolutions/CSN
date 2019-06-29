#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 16:45:56 2019

@author: Kirby Urner

Coffee Shops Network business model
For learning purposes.
"""
import numpy as np
import pandas as pd
import json
import hashlib
import random

#%%
# Create data section

def shazam(the_str):
    return hashlib.sha256(bytes(the_str, encoding='utf-8')).hexdigest()[:10]

def data():
    global hall_of_fame
    
    games = {"games":[ 
            
                {"gcode": "ASM",
                 "name": "Awesome Journey",
                 "rating": "hard",
                 "audience": "teen",
                 "theme": "theme park"},

                {"gcode": "TSH",
                 "name": "Treasure Hunt",
                 "rating": "hard",
                 "audience": "teen",
                 "theme": "VR"},
                
                {"gcode": "PPS",
                 "name": "Pilgrims Progress",
                 "rating": "easy",
                 "audience": "all",
                 "theme": "epic"},
                
                {"gcode": "WRR",
                 "name": "Writers Rock",
                 "rating": "medium",
                 "audience": "adult",
                 "theme": "quiz"}
            
            ]}
    
    # WARNING: destructive output, existing data will be overwritten
    with open("games.json", 'w') as outfile:
        json.dump(games, outfile)
        
    players = {"players":[
                  {'pcode':shazam('Gus'), 
                  'name': 'Gus',
                  'aliases': ['gustav', 'gus', 'the guster'],
                  'profile' : 'id-12345',
                  'account' : 200},
                  
                  {'pcode':shazam('Keela'), 
                  'name': 'Keela',
                  'aliases': ['keesha', 'pandabear', 'sloth'],
                  'profile' : 'id-54932',
                  'account' : 150},
                  
                  {'pcode':shazam('Tor'), 
                  'name': 'Tor',
                  'aliases': ['torror', 'torus', 'the tor'],
                  'profile' : 'id-94031',
                  'account' : 200},
                   
                  {'pcode':shazam('Mitsu'), 
                  'name': 'Mitsu',
                  'aliases': ['bishi', 'sitcom', 'vagrant'],
                  'profile' : 'id-88493',
                  'account' : 100}
                 ]
                }
    
    # WARNING: destructive output, existing data will be overwritten
    with open("players.json", 'w') as outfile:
        json.dump(players, outfile)
        
    causes = {"causes":[
                {'zcode': 'STB',
                 'name':'Save the Bees'},
                {'zcode': 'STW',
                 'name':'Save the Whales'},             
                {'zcode': 'STS',
                 'name':'Save the Seas'}             
                 ]}
     
    # WARNING: destructive output, existing data will be overwritten
    with open("causes.json", 'w') as outfile:
        json.dump(causes, outfile)

    # DataFrames
    hall_of_fame = pd.DataFrame({"pcode": pd.Series([], dtype=pd.np.unicode_),
                             "gcode": pd.Series([], dtype=pd.np.unicode_),
                             "zcode": pd.Series([], dtype=pd.np.unicode_),
                             "amnt" : pd.Series([], dtype=pd.np.int32),
                             "timestamp": pd.Series([], dtype='datetime64[ns]')})
 #%%
    
def make_players():
    pcode   = np.array([], dtype=np.unicode)
    name    = np.array([], dtype=np.unicode)
    aliases = np.array([], dtype=np.unicode)
    profile = np.array([], dtype=np.unicode) 
    account = np.array([], dtype=np.int32)
    
    with open('players.json') as target:
        players = json.load(target)
        
    for record in players['players']:
        pcode   = np.append(pcode,   record['pcode'])
        name    = np.append(name,    record['name'])
        aliases = np.append(aliases, ", ".join(record['aliases']))
        profile = np.append(profile, record['profile'])
        account = np.append(account, record['account'])
        
    return pd.DataFrame({'pcode'  : pcode,
                         'name'   : name,
                         'aliases': aliases,
                         'profile': profile,
                         'account': account})


def make_causes():
    zcode   = np.array([], dtype=np.unicode)
    name    = np.array([], dtype=np.unicode)
    
    with open('causes.json') as target:
        causes = json.load(target)
        
    for record in causes['causes']:
        zcode = np.append(zcode, record['zcode'])
        name  = np.append(name,  record['name'])
        
    return pd.DataFrame({'zcode': zcode,
                         'name': name})

def make_games():
    gcode    = np.array([], dtype=np.unicode)
    name     = np.array([], dtype=np.unicode)
    rating   = np.array([], dtype=np.unicode)    
    audience = np.array([], dtype=np.unicode)
    theme    = np.array([], dtype=np.unicode)
    
    with open('games.json') as target:
        games = json.load(target)
        
    for record in games['games']:
        gcode   = np.append(gcode,    record['gcode'])
        name    = np.append(name,     record['name'])
        rating  = np.append(rating,   record['rating'])
        audience= np.append(audience, record['audience'])
        theme   = np.append(theme,    record['theme'])
    
    #print(gcode)
    #print(name)
    #print(rating)
    #print(audience)
    #print(theme)

    return pd.DataFrame({'gcode'   : gcode,
                         'name'    : name,
                         'rating'  : rating,
                         'audience': audience,
                         'theme'   : theme})

class Cause:

    def __init__(self, **kwargs):
        self.name     = kwargs['name']
        self.zcode    = kwargs['zcode']

class Shop:

    def __init__(self):
        pass
    
    def play(self, the_player, prompting=False, **kwargs):
        the_game = None
        print("\nGreetings {}".format(the_player.name))
        if prompting:
            self.print_games()
            the_game      = input("What game (enter code)...? ")
            the_commit    = int(input("Commit how much? (1-10) "))
        else:
            the_game   = kwargs['the_game']
            the_commit = kwargs['the_commit']
            
        if not the_game:
            print("No game selected")
            return None
        
        the_player.the_game = load_game(gcode=the_game)
        the_player.commit   = the_commit
        print(the_player.the_game)
        print("Thank you for playing {}".format(the_player.the_game.name))
        the_player.account -= the_player.commit
        # OK, we're playing now...
        print("Action action, bling bling...")
        win = random.randint(0,10)/100 * the_player.commit + \
                        the_player.commit
        return win
    
    def commit(self, the_player, prompting=False, **kwargs):
        the_cause = None
        if prompting:
            self.print_causes()
            the_cause = input("You win! Commit {} to... ?".
                              format(the_player.winnings))
        else:
            the_cause = kwargs['the_cause']
        if not the_cause:
            print("No cause selected")
            return None
        
        the_player.the_cause = load_cause(zcode = the_cause)
        self.commit_winnings(the_player)
        the_player.update_profile()
    
    def commit_winnings(self, the_player):
        print("{} gets {}".format(the_player.the_cause.name, 
                                  the_player.winnings))

    def print_causes(self):
        print(causes)
        
    def print_games(self):
        print(games)

class Game:
    
    def __init__(self, **kwargs):
        self.name     = kwargs['name']
        self.gcode    = kwargs['gcode']
        self.rating   = kwargs['rating']
        self.audience = kwargs['audience']
        self.theme    = kwargs['theme']
        
    def __repr__(self):
        return "Game: {}, code: {}".format(self.name, self.gcode)
       
          
class Player:
    
    def __init__(self, pcode, nm, alias, profile, acct):
        self.pcode     = pcode # face recognition?  Welcome Real Player One
        self.name      = nm
        self.alias     = alias 
        self.profile   = profile
        self.account   = acct
        # decided during play
        self.commit    = 0
        self.winnings  = 0
        self.the_game  = None
        self.the_cause = None
        
    def play(self, the_shop, prompting=False, **kwargs):
        # play a game, donate winnings to the cause
        self.winnings  = the_shop.play(self, prompting, **kwargs)
        the_shop.commit(self, prompting, **kwargs)

    def update_profile(self):
        """
        Columns: [pcode, gcode, zcode, amnt, timestamp]
        """
        global hall_of_fame, new_rec
        # the_player.update_profile(the_cause, the_game, amount, table=None)
        print("{} gives {} to {}".format(self.name, 
                                         self.winnings, 
                                         self.the_cause.name))
        
        new_rec = pd.DataFrame( 
            [[self.pcode, self.the_game.gcode, self.the_cause.zcode,
             self.winnings, pd.datetime.now()]],    
            columns=['pcode', 'gcode', 'zcode', 'amnt', 'timestamp'])
        hall_of_fame = hall_of_fame.append(new_rec)
        hall_of_fame.index = pd.RangeIndex(0, hall_of_fame.shape[0])

def load_player(name=None, pcode=None):
    if name:
        the_player = players.query('name == "{}"'.format(name))
    if pcode:
        the_player = players.query('pcode == "{}"'.format(pcode))
        
    pcode   = the_player.pcode.values[0]
    name    = the_player.name.values[0]
    aliases = the_player.aliases.values[0]
    profile = the_player.profile.values[0]
    acct    = the_player.account.values[0]
    return Player(pcode, name, aliases, profile, acct)

def load_game(name=None, gcode=None):
    if name:
        the_game = games.query('name == "{}"'.format(name))
    if gcode:
        the_game = games.query('gcode == "{}"'.format(gcode))
        
    gcode   = the_game.gcode.values[0]
    name    = the_game.name.values[0]
    rating  = the_game.rating.values[0]
    audience= the_game.audience.values[0]
    theme   = the_game.theme.values[0]

    # all named arguments **kwargs
    return Game(gcode = gcode, 
                name = name, 
                rating = rating, 
                audience = audience, 
                theme = theme)

def load_cause(zcode=None, name=None):
    if name:
        the_cause = causes.query('name == "{}"'.format(name))
    if zcode:
        the_cause = causes.query('zcode == "{}"'.format(zcode))
        
    zcode   = the_cause.zcode.values[0]
    name    = the_cause.name.values[0]


    # all named arguments **kwargs
    return Cause(zcode = zcode, 
                 name = name)
    
def simulation1():
    the_shop = Shop()
    
    the_player = load_player(name = "Gus")
    the_player.play(the_shop, prompting=True)

    the_player = load_player(name = "Keela")
    the_player.play(the_shop, prompting=True)
    
def simulation2():
    the_shop = Shop()
    
    the_player = load_player(name = "Gus")
    the_player.play(the_shop, prompting=False, 
                    the_game="ASM",
                    the_cause='STB',
                    the_commit = 5)

    the_player = load_player(name = "Keela")
    the_player.play(the_shop, prompting=False,
                    the_game = 'TSH',
                    the_cause = 'STW',
                    the_commit = 9)
    
    
if __name__ == "__main__":
    data()
    causes  = make_causes()
    players = make_players()
    games   = make_games()
    # simulation1()
    simulation2()
    
