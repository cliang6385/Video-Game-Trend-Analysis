#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import requests


# In[1]:


#Part II: Vgchartz
#We aim to maintain games with highest shipped records from this website, as well as informations about game developer and publisher
#the web page is set to display 200 games per page

def game_sale(top_x_sales,url_tail='&results=200&console=PC&order=Sales&ownership=Both&direction=DESC&showtotalsales=1&shownasales=0&showpalsales=0&showjapansales=0&showothersales=0&showpublisher=1&showdeveloper=1&showreleasedate=0&showlastupdate=0&showvgchartzscore=0&showcriticscore=0&showuserscore=0&showshipped=1&showmultiplat=Yes'):
    game_name=[]
    sale=[]
    manufacture=[]
    num=int(top_x_sales/200)+1
    url_head='https://www.vgchartz.com/games/games.php?'
    for i in range(num+1):
        page='page='+str(i)
        url=url_head+page+url_tail
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        game_lst=soup.find_all('a', href=True)

        for games in game_lst:
            if games['href'].startswith('https://www.vgchartz.com/game/'):
                game_name.append(games.text.strip(' '))
        sales_lst=soup.find_all('td', {'align':'center'})

        for sales in sales_lst:
            if sales.text != None:
                sale.append(sales.text)
        sale=list(filter(lambda a: a != '\n\n', sale))
        len(sale)

        manufacture_lst=soup.find_all('td', {'width':'100'})

        for manufactures in manufacture_lst:
            manufacture.append(manufactures.text)
        
    publisher=manufacture[::2]
    developer=manufacture[1::2]
    total_shipped=sale[::2]
    total_sale=sale[1::2]

    
    sales_table=pd.DataFrame.from_dict({'Name':game_name,'Publisher':publisher,'Developer':developer,'Total Shipped':total_shipped,'Total Sales':total_sale})
    result=sales_table[:top_x_sales]
    return result

