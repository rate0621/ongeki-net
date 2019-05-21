import sys, os
import csv
import sqlite3

class Db:
    def __init__(self):
        here = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.my_ongeki_datas_db = here + '/../../ongeki.db'

    def getLastPlayDate(self):
        conn = sqlite3.connect(self.my_ongeki_datas_db)
        cur  = conn.cursor()
        cur.execute('SELECT play_date FROM playlog_detail ORDER BY play_date DESC')

        rec = cur.fetchone()

        if rec is None:
            last_play_date = 0
        else:
            last_play_date = rec[0]

        return last_play_date


    def insertPlayDetail(self, detail):
        conn = sqlite3.connect(self.my_ongeki_datas_db)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO playlog_detail VALUES (
                null,
                :music_name,
                :difficult,
                :play_date,
                :battle_score,
                :over_damage,
                :technical_score,
                :max_combo,
                :critical_break,
                :_break,
                :hit,
                :miss,
                :bell,
                :damage,
                :tap,
                :hold,
                :side_tap,
                :side_hold,
                :set_chara_1,
                :set_chara_1_level,
                :set_chara_1_attack,
                :set_chara_2,
                :set_chara_2_level,
                :set_chara_2_attack,
                :set_chara_3,
                :set_chara_3_level,
                :set_chara_3_attack,
                :jacket_id
            )
        """,
        detail)

        print ('Insert ' + detail['music_name'] + ' ' + detail['play_date'])
        conn.commit()
        conn.close()


if __name__ == '__main__':
    db = Db()
    last_play_date = db.getLastPlayDate()
    print (last_play_date)

