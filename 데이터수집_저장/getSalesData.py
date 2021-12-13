import os
from numpy import inner
import pandas as pd
import json
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler

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


    for i in range(page_num + 1):
        requests_para = {
        'request' : 'all',
        'page' : i # defalut
        }

        dict_data = get_request(url, requests_para)
        # streamspy data to Dataframe
        if i == 0:
            df_steamspy = pd.DataFrame.from_dict(dict_data, orient='index')
        else:
            df_steamspy = df_steamspy.append(pd.DataFrame.from_dict(dict_data, orient='index'))
    save_csv(df_steamspy, 'steamspy.csv')

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



#get_steamspy_data(page_num=35)


df_app_list = pd.read_csv('app_list_details_error.csv')
steam_appid = df_app_list['appid']
game_name = df_app_list['name']


for appid in steam_appid[21445:]:
    df = get_steamspy_details(appid)

    if appid == 1244460:
        df_steamspy = df
    else:
        df_steamspy = pd.concat([df_steamspy,df], ignore_index=True, axis=0, join='outer')

    save_csv(df_steamspy, 'steamspy_details_8.csv')

    print(f"Done Data - appid : {appid} ")
    print(df_steamspy.tail(1))
    print("**" * 20)




# #steam_columns = ['typ/e', 'name', 'steam_appid', 'required_age', 'is_free', 'controller_support',
#     'dlc',  'fullgame', 'supported_languages', 'pc_requirements', 'mac_requirements',
#     'linux_requirements', 'legal_notice', 'drm_notice', 'ext_user_account_notice',
#     'developers', 'publishers', 'demos', 'price_overview', 'packages', 'package_groups',
#     'platforms', 'metacritic', 'reviews', 'categories', 'genres', 
#     'recommendations', 'achievements', 'release_date', 'content_descriptors']

##
# for i in range (len(df_app_list)):
#     try:
#         time.sleep(0.3)
#         data = steam_request(steam_appid[i], game_name[i])

#         if i == 0:
#             df_steamdata = data
#         else:
#             df_steamdata = pd.concat([df_steamdata,data], ignore_index=True, axis=0, join='outer')

#         print(f"Data - steam ID : {steam_appid[i]}, Game Name : {game_name[i]}") 
#         print(df_steamdata.tail(1))
#         print("-"*30)

#     except:
#         data = None
#         pass


# save_csv(df_steamdata, 'steam.csv')

#df_steam = pd.read_csv('steam.csv')
#print(df_steam.T.head())

