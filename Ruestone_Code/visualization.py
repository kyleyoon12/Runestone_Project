import sqlite3
import folium
from tqdm import tqdm
import json

class Visualization:
    def make_html(self, db_path, html_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("SELECT local, details from timeline where event is 'Location'") #ALL
        rows = cur.fetchall()

        m = folium.Map(location=[37.566697, 126.978426], zoom_start=12)
        for i in tqdm(range(len(rows))):
            json_replaced = rows[i][1].replace("'", "\"")
            j = json.loads(json_replaced)
            folium.Marker(location=[float(j["latitude"]), float(j["longitude"])], popup=rows[i][0]).add_to(m)

        m.save(html_path)
        print("[System] >>> Working on...")
        print("[System] >>> Visualization Completed")

    def make_html2(self, db_path, html_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='sm_location_log'")
        rows = cur.fetchall()

        if len(rows) == 1: #0이면 테이블 없음 / 1이면 테이블 있음
            cur.execute("SELECT latitude, longitude, time_string FROM sm_location_log") #ALL
            rows = cur.fetchall()

            m = folium.Map(location=[37.566697, 126.978426], zoom_start=12)

            for i in tqdm(range(len(rows))):
                folium.Marker(location=[float(rows[i][0]), float(rows[i][1])], popup=rows[i][2]).add_to(m)

            m.save(html_path)
            print("[System] >>> Visualization Completed")
