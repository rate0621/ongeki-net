import sys, os
import csv
import sqlite3

conn = sqlite3.connect('my_ongeki.db')

cur = conn.cursor()                

cur.execute("""
CREATE TABLE IF NOT EXISTS playlog_detail (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    music_name         TEXT    NOT NULL,
    difficult          TEXT    NOT NULL,
    play_date          TEXT    NOT NULL,
    battle_score       INTEGER NOT NULL,
    over_damage        REAL    NOT NULL,
    technical_score    INTEGER NOT NULL,
    max_combo          INTEGER NOT NULL,
    critical_break     INTEGER NOT NULL,
    _break             INTEGER NOT NULL,
    hit                INTEGER NOT NULL,
    miss               INTEGER NOT NULL,
    bell               INTEGER NOT NULL,
    damage             INTEGER NOT NULL,
    tap                INTEGER NOT NULL,
    hold               INTEGER NOT NULL,
    side_tap           INTEGER NOT NULL,
    side_hold          INTEGER NOT NULL,
    set_chara_1        TEXT    NOT NULL,
    set_chara_1_level  INTEGER NOT NULL,
    set_chara_1_attack INTEGER NOT NULL,
    set_chara_2        TEXT    NOT NULL,
    set_chara_2_level  INTEGER NOT NULL,
    set_chara_2_attack INTEGER NOT NULL,
    set_chara_3        TEXT    NOT NULL,
    set_chara_3_level  INTEGER NOT NULL,
    set_chara_3_attack INTEGER NOT NULL,
    jacket_id          TEXT    NOT NULL
);
""")

conn.commit()
conn.close()


