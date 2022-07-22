import os
from numpy import inner
import pandas as pd
import json
import requests
import time

# The data is refreshed once a day, 
# there is no reason to request the same information more than once every 24 hours.

def get_request(url, requests_para):
    """
    Args:
        page_num (int, optional): [Returns 1000 games per page with owners data sorted by owners (starts at 0 page)]. Defaults to 0.

    Returns:
        dictionary type 
    """
    response = requests.get(url, params = requests_para)

    if response:
        return json.loads(response.text)
    else:
        # response is none usually means too many requests. Wait and try again 
        print('No response, Retry After 10 seconds...')
        time.sleep(10)
        print('Retrying...')
        return get_request(url, requests_para)


def save_csv(dataframe,file_name):
    directort_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(directort_path, file_name)
    csv = dataframe.to_csv(csv_path, index=False)
    return csv

def get_steamspy_data(page_num):
    url = 'https://steamspy.com/api.php?'
    """
    # Returns all games with owners data sorted by owners. Returns 1,000 entries per page.
    # * page - page number for the list (starts at 0)
    ## Return format for an app: ##
    # * appid - Steam Application ID. If it's 999999, then data for this application is hidden on developer's request, sorry.
    # * name - game's name
    # * developer - comma separated list of the developers of the game
    # * publisher - comma separated list of the publishers of the game
    # * score_rank - score rank of the game based on user reviews
    # * owners - owners of this application on Steam as a range.
    # * average_forever - average playtime since March 2009. In minutes.
    # * average_2weeks - average playtime in the last two weeks. In minutes.
    # * median_forever - median playtime since March 2009. In minutes.
    # * median_2weeks - median playtime in the last two weeks. In minutes.
    # * ccu - peak CCU yesterday.
    # * price - current US price in cents.
    # * initialprice - original US price in cents.
    # * discount - current discount in percents.
    # * tags - game's tags with votes in JSON array.
    # * languages - list of supported languages.
    # * genre - list of genres.
    """

    for i in range(page_num + 1):
        requests_para = {
        'request' : 'all',
        'page' : i # defalut
        }

        dict_data = get_request(url, requests_para)
        dict_to_df = pd.DataFrame.from_dict(dict_data, orient='index')
        # streamspy data to Dataframe
        if i == 0:
            df_steamspy = dict_to_df
        else:
            df_steamspy = pd.concat([df_steamspy, dict_to_df], ignore_index=True, axis=0, join='outer')
            

    # generate sorted app_list from steamspy data
    df_app_list = df_steamspy[['appid', 'name']].sort_values('appid').reset_index(drop=True)
    save_csv(df_app_list, 'app_list.csv')



def get_steamspy_details(appid):
    url = 'https://steamspy.com/api.php?'
    requests_para = {
        'request' : 'appdetails',
        'appid' : appid # defalut
        }
    try:
        dict_data = get_request(url, requests_para)
        df_steamspy = pd.DataFrame.from_dict(dict_data, orient='index')
        return df_steamspy.T
        
    except:
        print('No response, Retry After 10 seconds...')
        time.sleep(10)
        print('Retrying...')
        return get_steamspy_details(appid)

    


def steam_request(appid, name):
    steam_URL = "https://store.steampowered.com/api/appdetails/?"
    requests_para = {
        'appids':appid,
        'name':name
        }

    response = requests.get(steam_URL, params = requests_para)

    if response:
        json_data= json.loads(response.text)
        json_app_data = json_data[str(appid)]

        if json_app_data['success'] is True:
            dict_data = json_app_data['data']
            data = pd.DataFrame.from_dict(dict_data, orient='index')
            return data.T
        else:
            dict_data = {'name': name, 'steam_appid': appid}
            data = pd.DataFrame.from_dict(dict_data, orient='index')
            return data.T
    else:
        # response is none usually means too many requests. Wait and try again 
        print('No response, loop pass')
        return None



get_steamspy_data(page_num=50) # 5만개의 데이터 반환 요청(page 1개당 1천개 데이터)

df_app_list = pd.read_csv('app_list.csv')
steam_appid = df_app_list['appid']
game_name = df_app_list['name']


for appid in steam_appid[:]:
    df = get_steamspy_details(appid)

    if appid == 10:
        df_steamspy = df
    else:
        df_steamspy = pd.concat([df_steamspy,df], ignore_index=True, axis=0, join='outer')

    save_csv(df_steamspy, 'steamspy_details.csv')

    print(f"Done Data - appid : {appid} ")
    print(df_steamspy.tail(1))
    print("**" * 20)

