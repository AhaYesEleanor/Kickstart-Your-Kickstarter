
# coding: utf-8

# In[30]:


import pandas as pd
import re
import datetime as dt
from currency_converter import CurrencyConverter


# In[33]:



def data_from_text(proj_series):
    #regexes to extract substrings from kicktraq text fields
    funding_regex = re.compile('Funding: (.*\d*.*\d*) of (.\d*.*\d*) ')
    backers_regex = re.compile('Backers: (\d*)')
    dates_regex = re.compile('Dates: (\w* \d*)\w* \-\> (\w* \d*)\w* \((\d*)\)')
    

    funding_match = re.search(funding_regex, str(proj_series.funding))
    funding_actual = re.sub('\D', '', funding_match.group(1).replace(',',''))
    funding_goal = re.sub('\D','', funding_match.group(2).replace(',',''))
    
    backers_match = re.search(backers_regex, str(proj_series.backers))
    n_backers = backers_match.group(1).replace(',','')
    
    dates_match = re.search(dates_regex, str(proj_series.campaign_dates))
    
    end_year = int(dates_match.group(3).strip())
    [start_month, start_day] = dates_match.group(1).split()
    [end_month, end_day] = dates_match.group(2).split()
    
    month_dict = {'January': 1, 'February': 2, 'March': 3,
                  'April': 4, 'May': 5, 'June': 6, 
                  'July': 7, 'August': 8, 'September': 9, 
                  'October': 10, 'November': 11, 'December': 12}
    start_month = month_dict[start_month]
    end_month = month_dict[end_month]
    
    #checking if project spanned Jan 01 and start year is different than end year
    if end_month - start_month < 0:
        start_year = end_year -1
    else:
        start_year = end_year
        
    start_date = dt.date(year=start_year, month=start_month, day=int(start_day))
    end_date = dt.date(year=end_year, month=end_month, day=int(end_day))
        
    duration = end_date - start_date
    
    #date_start = pd.to_datetime(dates_match.group(1) + ' ' + dates_match.group(3))
    #date_end = pd.to_datetime(dates_match.group(2) + ' ' + dates_match.group(3))
    
    proj_series.funding_actual = funding_actual
    proj_series.funding_goal = funding_goal
    proj_series.n_backers = n_backers
    proj_series.start_date = start_date
    proj_series.duration = duration.days
    
    
    return proj_series
    #return [funding_actual, funding_goal, n_backers]
    
    


# In[61]:


c = CurrencyConverter()

def currency_change(df_row):
    try:
        new_actual = c.convert(df_row.funding_actual,df_row.currency, 'USD', df_row.start_date)
        new_goal = c.convert(df_row.funding_goal,df_row.currency, 'USD', df_row.start_date)
        new_min = c.convert(df_row.pledge_level_min,df_row.currency, 'USD', df_row.start_date)
        new_max = c.convert(df_row.pledge_level_max,df_row.currency, 'USD', df_row.start_date)
        new_stddev = c.convert(df_row.pledge_level_stddev,df_row.currency, 'USD', df_row.start_date)
    except:
        new_actual = c.convert(df_row.funding_actual,df_row.currency, 'USD', dt.date(2014, 4, 1))
        new_goal = c.convert(df_row.funding_goal,df_row.currency, 'USD', dt.date(2014, 4, 1))
        new_min = c.convert(df_row.pledge_level_min,df_row.currency, 'USD', dt.date(2014, 4, 1))
        new_max = c.convert(df_row.pledge_level_max,df_row.currency, 'USD', dt.date(2014, 4, 1))
        new_stddev = c.convert(df_row.pledge_level_stddev,df_row.currency, 'USD', dt.date(2014, 4, 1))
    
    df_row.funding_actual = new_actual
    df_row.funding_goal = new_goal
    df_row.pledge_level_min = new_min
    df_row.pledge_level_max = new_max
    df_row.pledge_level_stddev = new_stddev
    return df_row

