#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import pandas as pd
import requests


# In[3]:


#Part I: Metacritics
#the web page displays 100 games per page by default
#use apply_filters_metacritics() function to generate the url with desired filters applied:
    #default: descending order, with details information applied
    #time frame: game of all time? last 90 days? By year?
    #platform avaliability: pc? ps4? xbox?
    #sort by: metascore? userscore?

def apply_filters_metacritics():
    
    time=input('Time Frame(Last90days/AllTime/ByYear)\nPlease type in only one answer, exactly  as shown in the brackets: ')
    print('\n')
    platform=input('Avaliable Platform(AllPlatform/PC/PS4/XboxOne)\nPlease type in only one answer, exactly as shown in the brackets: ')
    print('\n')
    sort=input('Sort By(metascore/userscore)\nPlease type in only one answer, exactly as shown in the brackets: ')
    print('\n')
    
    if (time=='Last90days'):
        time='/90day'
        year=None
    elif (time=='AllTime'):
        time='/all'
        year=None
    elif (time=='ByYear'):
        time='/year'
        year=input('Which year? (Only avaliable between 1916 to 2020): ')
    else:
        print('Invalid time input!')
        exit()
    
    if (platform=='AllPlatform'):
        platform='/all'
    elif (platform=='PC'):
        platform='/pc'
    elif (platform=='PS4'):
        platform='/ps4'
    elif (platform=='XboxOne'):
        platform='/xboxone'
    else:
        print('Invalid platform input!')
        exit()
    if (sort=='metascore'):
        sort='/metascore'
    elif (sort=='userscore'):
        sort='/userscore'
    else:
        print('Invalid sort input!')
        exit()
   
    if (year!=None):
        try:
            year=int(year)
            if (year in range(1916,2021)):
                url_filters=sort+time+platform+'/filtered?sort=desc&view=detailed&year_selected='+str(year)
            else:
                print('Invalid year input!')
                exit()
        except ValueError:
            print('Invalid year input!')
            exit()
    else:
        url_filters=sort+time+platform+'/filtered?sort=desc&view=detailed'
    
    return url_filters


# In[4]:


#use game_info() to scrape the desired information
#for the purpose of this project, the url_tail is set to '/metascore/all/pc/filtered?sort=desc&view=detailed'

def game_info(top_x_games, url_tail='/metascore/all/pc/filtered?sort=desc&view=detailed'):
    num=int(top_x_games/100)+1
    game_name=[]
    release_date=[]
    metascore=[]
    userscore=[]
    url_head='https://www.metacritic.com/browse/games/score'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    for i in range(num+1):
        page='&page='+str(i)
        url=url_head+url_tail+page
        response = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(response.text, 'html.parser')

        for items in soup.find_all('a',{'class':'title'}):
            game_name.append(items.find('h3').string)

        for items in soup.find_all('div', {'class':'clamp-details'}):
            release_date.append(items.find('span',{'class':None}).string)

        for clamp in soup.find_all('table',{'class':'clamp-list'}):
            clamps=clamp.find_all('div', {'class':['metascore_w large game positive','metascore_w large game mixed','metascore_w large game negative','metascore_w medium game positive','metascore_w medium game mixed','metascore_w medium game negative','metascore_w large game tbd','metascore_w medium game tbd']})
            for items in clamps:
                metascore+=items.contents
        for clamp in soup.find_all('table',{'class':'clamp-list'}):
            clamps=clamp.find_all('div', {'class':['metascore_w user large game positive','metascore_w user large game mixed','metascore_w user large game negative','metascore_w user medium game positive','metascore_w user medium game mixed','metascore_w user medium game negative','metascore_w user large game tbd','metascore_w user medium game tbd']})
            for items in clamps:
                userscore+=items.contents

    del metascore[1::2]   
    table=pd.DataFrame.from_dict({'Name':game_name,'Release Date':release_date,'Metascore':metascore,'Userscore':userscore})
    result=table[:top_x_games]
    return result

