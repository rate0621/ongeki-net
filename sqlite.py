import sys, os
import sqlite3
import pandas as pd


#pandasでcsvファイルを読み込む
df = pd.read_csv("base_rate.csv")


#db作成
dbname = "code.db"

#dbコネクト
conn = sqlite3.connect(dbname)
c = conn.cursor()

#dbのnameをcode_1332とし、読み込んだcsvファイルをsqlに書き込む
#if_existsでもしすでにcode_1332が存在していても、置き換えるように指示
df.to_sql("base_rate", conn, if_exists="replace")

#作成したdbを見てみる
select_sql = 'select * from base_rate'
for row in c.execute(select_sql):
    print(row)

conn.close()

