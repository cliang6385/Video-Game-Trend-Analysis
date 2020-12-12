#!/usr/bin/env python
# coding: utf-8

# In[4]:


import json
import pandas as pd
import requests


# In[1]:


#Part III: Steam API
#In order to search for specific info about each game, we need to maintain a list of games and their corresponding steam app id
#to do so, we use the steam_app_id() which returns a list of ids of the desired games from the input dataframe

def steam_appid(df):
    url1='http://api.steampowered.com/ISteamApps/GetAppList/v0001/'
    url2='http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    response = requests.get(url1)
    game_lst1 = response.json()['applist']['apps']['app']
    response = requests.get(url2)
    game_lst2 = response.json()['applist']['apps']
    game_lst = game_lst1 + game_lst2
    appid_table = pd.DataFrame(game_lst)
    appid_table = appid_table.rename(columns = {"name":"Name"})
    appid_table = pd.merge(appid_table, df, on = "Name")
    return appid_table


# In[2]:


#use steam_reviews() to return a table of steam game reviews

def steam_reviews(appid_table):
    steam_reviews=[]
    for ID in list(appid_table['appid']):
        appid=ID
        url=f'https://store.steampowered.com/appreviews/{appid}?json=1'
        response = requests.get(url)
        review = response.json()
        steam_reviews.append(review['query_summary'])
    steam_review_table = pd.DataFrame(steam_reviews)
    return steam_review_table


# In[ ]:




