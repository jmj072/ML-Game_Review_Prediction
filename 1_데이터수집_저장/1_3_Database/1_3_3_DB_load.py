import psycopg2
import csv

conn = psycopg2.connect(
    host = 'john.db.elephantsql.com',
    password = '10BJ8vKMCewphIv0BeAf0-i8ZazkHzik',
    user = 'qnqtbswf',
    database = 'qnqtbswf'
    )

print(conn)
cur = conn.cursor()

# Create all_list Table
def Create_table_app_list ():
    cur.execute("DROP TABLE IF EXISTS app_list;")
    cur.execute("""
                CREATE TABLE app_list (
                    Id INTEGER PRIMARY KEY,
                    Game_name TEXT
                    );
                """)
    return "Done Create app_list Table."

# Create steamspy data table
def Create_table_steamspy ():
    cur.execute("DROP TABLE IF EXISTS steamspy;")
    cur.execute("""
            CREATE TABLE steamspy (
            "appid" INTEGER PRIMARY KEY,
            "Game_name" TEXT,
            "developer" TEXT,
            "publisher" TEXT,
            "positive_review" INTEGER,
            "negative_review" INTEGER,
            "average_playtime_from_2009" FLOAT,
            "initial_price_KRW" INTEGER,
            "language" TEXT,
            "genre" VARCHAR(255),
            "release_year" INTEGER,
            "Korean_language_support" INTEGER,
            "indie_game" INTEGER,
            "price_discount" INTEGER,
            "positive_ratio" FLOAT,
            "price_group" VARCHAR(255),
            FOREIGN KEY(appid) REFERENCES app_list(Id)
            );
        """)

# with open('app_list_test_2.csv', 'r',  encoding='UTF-8') as f:
#     reader = csv.reader(f)
#     next(reader)
#     for row in reader:
#         cur.execute(
#         "INSERT INTO app_list VALUES (%s, %s)",
#         (row[0], str(row[1]))
#         )
#         conn.commit()
Create_table_steamspy ()

with open('steamspy_dataset_db_upload.csv', 'r',  encoding='UTF-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cur.execute(
        "INSERT INTO steamspy VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
        row[1], str(row[2]), str(row[3]), str(row[4]), row[5], row[6], row[7], row[8], 
        str(row[9]), str(row[10]), row[11], row[12], row[13], row[14],row[15], str(row[16])
        )
        )
        conn.commit()
