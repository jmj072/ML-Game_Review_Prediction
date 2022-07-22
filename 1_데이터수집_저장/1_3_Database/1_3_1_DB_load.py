import pandas as pd
import psycopg2

# Database Connect (PostgreSQL)
conn = psycopg2.connect(
    host = 'john.db.elephantsql.com',
    password = 'XmjhDueuKG8ReGkOm7nGXunlDwevVI3L',
    user = 'mptqsere',
    database = 'mptqsere'
    )
print(conn)
cur = conn.cursor()

# Table Create
## 1. app_list Table
def Create_table_app_list ():
    cur.execute("DROP TABLE IF EXISTS app_list CASCADE;")
    cur.execute("""
                CREATE TABLE app_list (
                    Id INTEGER PRIMARY KEY,
                    Game_name TEXT
                    );
                """)
    return "Done Create app_list Table."

## 2. steamspy_details Table
def Create_table_steamspy_details ():
    cur.execute("DROP TABLE IF EXISTS steamspy_details;")
    cur.execute("""
            CREATE TABLE steamspy_details (
            "appid" INTEGER PRIMARY KEY,
            "name" TEXT,
            "developer" TEXT,
            "publisher" TEXT,
            "positive_review" INTEGER,
            "negative_review" INTEGER,
            "owners" TEXT,
            "average_playtime_from_2009" INTEGER,
            "average_playtime_2weeks" INTEGER,
            "median_playtime_from_2009" INTEGER,
            "median_playtime_2weeks" INTEGER,            
            "initial_price" FLOAT,
            "current_price" FLOAT,
            "discount_precent" FLOAT,
            "ccu" INTEGER,
            "language" TEXT,
            "genre" TEXT,
            "tags" Text,
            FOREIGN KEY(appid) REFERENCES app_list(Id)
            );
            """)
    return "Done Create steamspy_details Table."

## 3. steamspy_other_details Table
# relese_year 가 NaN인 경우가 있어서, Text로 입력함
def Create_table_steamspy_otherdetails ():
    cur.execute("DROP TABLE IF EXISTS steamspy_otherdetails;")
    cur.execute("""
            CREATE TABLE steamspy_otherdetails (
            "appid" INTEGER PRIMARY KEY,
            "release_year" TEXT, 
            "steam_userscore" TEXT,
            "metascore" TEXT,
            FOREIGN KEY(appid) REFERENCES app_list(Id)
            );
        """)
    return "Done Create steamspy_otherdetails Table."


# Create_table_app_list()
# Create_table_steamspy_details()
Create_table_steamspy_otherdetails()

# Dataset Load
df1 = pd.read_csv('G:/내 드라이브/CodeStates/Section3/Section3_project/ML-Game_Positive_Prediction/1_데이터수집_저장/1_1_steamspyAPI/1_1_2_steamspy_details.csv')
df2 = pd.read_csv('G:/내 드라이브/CodeStates/Section3/Section3_project/ML-Game_Positive_Prediction/1_데이터수집_저장/1_2_webscraping/1_2_2_steamspy_other_details.csv')
app_list = pd.read_csv('G:/내 드라이브/CodeStates/Section3/Section3_project/ML-Game_Positive_Prediction/1_데이터수집_저장/1_1_steamspyAPI/1_1_3_app_list.csv')

# 중복된 값 제거 (appid를 기준으로)
df1 = df1.drop_duplicates(['appid'], keep = 'first',  ignore_index = True) #appid를 기준으로, 첫번째 중복값만 남기고 제거 (제거 후, index값 재지정)
df2 = df2.drop_duplicates(['appid'], keep = 'first',  ignore_index = True)
app_list = app_list.drop_duplicates(['appid'], keep = 'first',  ignore_index = True)


# Insert Data into app_list Table
for idx, row in app_list.iterrows() :
   cur.execute(
       "INSERT INTO app_list VALUES (%s, %s)",
       (row['appid'], str(row['name']))
   )
   conn.commit()
   print('Insert Data: ', idx + 1)

# Insert Data into steamspy_details Table
for idx, row in df1.iterrows() :
   cur.execute(
       "INSERT INTO steamspy_details VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
       (row['appid'], str(row['name']), str(row['developer']), str(row['publisher']), row['positive'], row['negative'], str(row['owners']), 
        row['average_forever'], row['average_2weeks'], row['median_forever'], row['median_2weeks'],
        row['initialprice'], row['price'], row['discount'], row['ccu'],
        str(row['languages']), str(row['genre']), str(row['tags'])
        )
   )
   conn.commit()   
   print('Insert Data: ', idx + 1)

# Insert Data into steamspy_otherdetails Table
for idx, row in df2.iterrows() :
   cur.execute(
       "INSERT INTO steamspy_otherdetails VALUES (%s, %s, %s, %s)",
       (row['appid'], row['release_year'], str(row['user_score']), str(row['meta_score']))
   )
   conn.commit()
   print('Insert Data: ', idx + 1)
   print('appid :', row['appid'])   
   print('release_year :', row['release_year'])
