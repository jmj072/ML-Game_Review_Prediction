import os
import time
import requests
import  pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://steamspy.com/app"

def get_page(page_url):
    """
    get_page 함수는 페이지 URL 을 받아 해당 페이지를 가져오고 파싱한 두
    결과들을 리턴합니다.

    예를 들어 `page_url` 이 `https://github.com` 으로 주어진다면
        1. 해당 페이지를 requests 라이브러리를 통해서 가져오고 해당 response 객체를 page 변수로 저장
        2. 1번의 response 의 html 을 BeautifulSoup 으로 파싱한 soup 객체를 soup 변수로 저장
        3. 저장한 soup, page 들을 리턴하고 함수 종료

    파라미터:
        - page_url: 받아올 페이지 url 정보입니다.

    리턴:
        - soup: BeautifulSoup 으로 파싱한 객체
        - page: requests 을 통해 받은 페이지 (requests 에서 사용하는 response
        객체입니다).
    """
    page = requests.get(page_url)
    if page:
        soup = BeautifulSoup(page.content, 'html.parser')

        return soup, page

    else:
        # response is none usually means too many requests. Wait and try again 
        print('No response, Retry After 10 seconds...')
        time.sleep(10)
        print('Retrying...')
        
        return get_page(page_url)



    




def get_other_details(appid):
    search_url = f'{BASE_URL}/{appid}'

    try:
        soup, page = get_page(search_url)
    except:
        print('No response, Retry After 10 seconds...')
        time.sleep(10)
        print('Retrying...')
        return get_other_details(appid)


    date = soup.find(class_='p-r-30')
    text = date.p.text


    
    try: 
        release_date = text.split('Release date')[-1].split(':')[1].replace('Price', '').strip()
        release_year = release_date.split(' ')[-1]
        release_year = int(release_year)
    except:
        release_year = None


    
    try:
        Priece = text.split('Price')[-1].split(':')[1].split(' ')[1]
        if Priece[0] == '$':
            Priece = Priece
        else:
            Priece = None
    except:
        Priece = None


    
    
    try:
        user_score = text.split('Old userscore')[-1].split(':')[1].split(' ')[1].strip()
        if user_score[-1] == '%':
            user_score = user_score
        else:
            user_score = None
    except:
        user_score = None

    
    try:
        meta_score = text.split('Metascore')[-1].split(':')[1].split(' ')[1].strip()
        if meta_score[-1] == '%':
            meta_score = meta_score
        else:
            meta_score = None
    except:
        meta_score = None

    data = [[appid, release_year, Priece, user_score, meta_score]]
    #data ={'appid':appid, 'release_year': release_year, 'Priece': Priece, 'user_score' : user_score, 'meta_score' : meta_score}
    return data

def save_csv(dataframe,file_name):
    directort_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(directort_path, file_name)
    csv = dataframe.to_csv(csv_path, index=False)
    return csv


df_app_list = pd.read_csv('app_list_other_details_error.csv')
steam_appid = df_app_list['appid']
game_name = df_app_list['name']


for appid in steam_appid[1772:]:

    temp_data = get_other_details(appid)


    if appid == 252570:
        df = pd.DataFrame(temp_data, columns=['appid', 'release_year', 'Priece', 'user_score', 'meta_score'])
    else:
        temp_df = pd.DataFrame(temp_data, columns=['appid', 'release_year', 'Priece', 'user_score', 'meta_score'])
        df = df.append(temp_df)

    print(df.tail(1))
    save_csv(df, 'steamspy_other_details_6.csv')
