
# coding: utf-8

# In[ ]:


import requests
import time
import re
import numpy as np
import os

from bs4 import BeautifulSoup


# In[ ]:


def get_kickstarter_data(proj_series):
    url = 'https://www.kickstarter.com/' + proj_series.kickstarter_page
    #print(url)    
    
    #define filename for where to store html txt file
    page_id_regex = re.compile('projects\/.*\/(.*)\/')
    match = re.search(page_id_regex, proj_series.kickstarter_page)
    page_id = match.group(1)
    filename = r"kickstarter_files/{}.txt".format(page_id)
    
    #check if html txt file exists already
    if os.path.isfile(filename):
        with open( filename, "r") as f:
            page_text = f.read()
        soup = BeautifulSoup(page_text,'lxml')
        
    else:
        response = requests.get(url)
        #print(url)

        # dealing with 404s 
        for i in range (1,10):
            if response.status_code == 200:
                break
            else:
                time.sleep(5)
                response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page,'lxml')

        # save soup as txt file
        with open( filename, "w") as f:
            f.write(str(soup.html))
            
    pledges = soup.find_all(class_='pledge__info')

    n_pledges = len(pledges)
    
    # extract currency characters from pledge rewards levels
    pledge_amounts=[]
    for pledge in pledges:
        
        #strip out $ because it seems to be the wrong kind of unicode
        pledge_amount = str(pledge.find(class_='money').text.replace('$',''))
        currency = ''
        
        #while the first character in pledge_amount is not an integer, add that character to currency string
        while not (re.match('\d',pledge_amount[0])):
            currency = currency + (pledge_amount[0])
            pledge_amount = pledge_amount[1:]
        if currency == '':
            currency = '$'
        proj_series['currency'] = currency
        pledge_amounts.append(int(pledge_amount.replace(',','')))

    #if page does not contain the expected information, move on to the next page
    try:
        descript_paragraphs = soup.find(class_="full-description js-full-description responsive-media formatted-lists").find_all('p')
        description_words = 0
        for par in descript_paragraphs:
            description_words += len(str(par.text).split())

        proj_series.description_length = description_words
        proj_series.n_pledges = n_pledges
        proj_series.pledge_level_min = min(pledge_amounts)
        proj_series.pledge_level_max = max(pledge_amounts)
        proj_series.pledge_level_stddev = np.std(pledge_amounts)
    except:
        print('unable to scrape data from ' + filename)
        pass

    time.sleep(2)
        
    return proj_series

