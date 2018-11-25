import csv
import sqlite3

# DBを表すConnectionオブジェクトをRAM上に作成して、DBに接続する。
conn = sqlite3.connect('my_ongeki.db')
# DB上の処理対象の行を指し示すためのCursorオブジェクトを作成する。 
cur = conn.cursor()                

# 受注表という名前のtableを作成する。
cur.execute("""CREATE TABLE play_result (
id INTEGER PRIMARY KEY AUTOINCREMENT,
music_name NOT NULL,
play_date NOT NULL,
play_date NOT NULL,
play_date NOT NULL,
play_date NOT NULL,
play_date NOT NULL,
play_date NOT NULL,
);""")

# 受注表(csv)を開く。
with open('./sqlite/jyuchuhyo.csv', 'rb') as f: 
    b = csv.reader(f)
    header = next(b)
    for t in b:
        # tableに各行のデータを挿入する。
        cur.execute('INSERT INTO 受注表 VALUES (?,?,?,?,?);', t)　

# 以降、sqlite3のDBからデータの読み出し例
# 受注個数が20より小さいものを3項目（列）表示
cur.execute('SELECT 受注番号, 商品コード, 納品日 FROM 受注表 WHERE 受注個数 < 20;')
for row in cur: # 書き方① for文を使う。
    print row

# 受注表の内容を全部表示
cur.execute('SELECT * FROM 受注表;')
print cur.fetchall()    # 書き方② fetchall()を使う。リストを返す。

# 受注表のうち納品日を重複を排除して表示
cur.execute('SELECT DISTINCT 納品日 FROM 受注表;')
print cur.fetchall()

# DBの変更を保存する。
conn.commit()
# データベースとの接続を閉じる。
conn.close()


<img src="https://ongeki-net.com/ongeki-mobile/img/music/ab4ebdf01a8085a4.png" class="m_5 f_l">
