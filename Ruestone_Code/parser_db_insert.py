import json
import sqlite3
from tqdm import tqdm
from module import convert_time

class DB_insert:
    def __init__(self, mode, logs, db_path):
        self.place_dictionary = {}

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * from sqlite_master WHERE type='table' AND name='timeline'")
        row = cur.fetchall()

        if row:
            pass

        else:
            cur.execute("CREATE TABLE timeline (local time TEXT, event TEXT, details TEXT)")

        conn.commit()
        conn.close()

        if mode == 1:
            self.l = logs
            self.db_path = db_path
            self.ma_run()

        if mode == 2:
            self.l = logs
            self.db_path = db_path
            self.sm_run()

    def ma_run(self):
        self.__ma_account_info(self.l["samsung_account"], self.db_path)
        self.__ma_wifi_bt_connection(self.l["wifi_bt_connection"], self.db_path)
        self.__ma_app_usage(self.l["app_usage"], self.db_path)
        self.__ma_web_history(self.l["web_history"], self.db_path)
        self.__ma_web_search_keyword(self.l["search_keyword"], self.db_path)

    @staticmethod
    def __ma_account_info(logs_samsung_account, db_path):
        if len(logs_samsung_account) == 0:
            print("[SYSTEM] >>> No logs - samsung_account")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE ma_account_info (type TEXT, collect_time_local TEXT, collect_time TEXT, gender TEXT, birthday TEXT, country_code TEXT, source TEXT)")
            collect_time_local = convert_time.make_local(logs_samsung_account[0]["row_data"]["collect_time"])
            cur.execute("INSERT INTO ma_account_info VALUES(?,?,?,?,?,?,?);", (
            logs_samsung_account[0]["type"], collect_time_local, logs_samsung_account[0]["row_data"]["collect_time"],
            logs_samsung_account[0]["row_data"]["gender"], logs_samsung_account[0]["row_data"]["birthday"],
            logs_samsung_account[0]["row_data"]["country_code"], "Manufacturer"))
            conn.commit()
            conn.close()

    @staticmethod
    def __ma_wifi_bt_connection(logs_wifi_bt_connection, db_path):
        if len(logs_wifi_bt_connection) == 0:
            print("[SYSTEM] >>> No logs - wifi_bt_connection")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE ma_wifi_bt_connection (type TEXT, collect_time_local TEXT, collect_time TEXT, sync_time TEXT, device_mode TEXT, mcc TEXT, mnc TEXT, service_type TEXT, data_type TEXT, connection_type TEXT, duration_ms INTEGER, registered_type TEXT, place_category TEXT, mac_address TEXT, device_name TEXT, source TEXT)")

            logs = []
            for i in range(len(logs_wifi_bt_connection)):
                if "data_type" in logs_wifi_bt_connection[i]["row_data"]:
                    if logs_wifi_bt_connection[i]["row_data"]["data_type"] == "wifi_bt_connection":
                        logs.append(logs_wifi_bt_connection[i])

            for x in tqdm(range(len(logs))):
                details = json.loads(logs[x]["row_data"]["details"])
                connection_type = details["data"][0]["connection_type"]
                duration = details["data"][0]["duration"]
                registered_type = details["data"][0]["registered_type"]
                place_category = details["data"][0]["place_category"]
                mac_address = details["data"][0]["mac_address"]
                device_name = details["data"][0]["device_name"]

                collect_time_local = convert_time.make_local(logs[x]["row_data"]["collect_time"])

                cur.execute("INSERT INTO ma_wifi_bt_connection VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                logs[x]["type"], collect_time_local, logs[x]["row_data"]["collect_time"], logs[x]["row_data"]["sync_time"],
                logs[x]["row_data"]["device_model"], logs[x]["row_data"]["mcc"],
                logs[x]["row_data"]["mnc"], logs[x]["row_data"]["service_type"], logs[x]["row_data"]["data_type"],
                connection_type, int(duration), registered_type, place_category, mac_address, device_name, "Manufacturer"))

                if connection_type == "1":
                    ct = "Bluetooth"

                if connection_type == "4":
                    ct = "WiFi"

                #Timeline
                #connection_type: 4=wifi 1=bluetooth
                db_dict = {"connection_type": ct, "device_name": device_name, "mac_address": mac_address, "duration": int(duration), "place_category": place_category}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",(collect_time_local, "Connected Wifi_or_BT", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __ma_app_usage(logs_app_usage, db_path):
        if len(logs_app_usage) == 0:
            print("[SYSTEM] >>> No logs - app_usage")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()

            cur.execute("CREATE TABLE ma_app_usage (type TEXT, collect_time_local TEXT, collect_time TEXT, device_model TEXT, mcc TEXT, mnc TEXT, android_version TEXT, baseband_version TEXT, app_name TEXT, app_usage_duration_ms INTEGER, current_app TEXT, geohash TEXT, source TEXT)")

            for i in tqdm(range(len(logs_app_usage))):
                collect_time_local = convert_time.make_local(logs_app_usage[i]["row_data"]["collect_time"])
                cur.execute("INSERT INTO ma_app_usage VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);", (logs_app_usage[i]["type"], collect_time_local, logs_app_usage[i]["row_data"]["collect_time"], logs_app_usage[i]["row_data"]["device_model"], logs_app_usage[i]["row_data"]["mcc"], logs_app_usage[i]["row_data"]["mnc"], logs_app_usage[i]["row_data"]["android_version"],
                            logs_app_usage[i]["row_data"]["baseband_version"], logs_app_usage[i]["row_data"]["app_usage_id"], int(logs_app_usage[i]["row_data"]["app_usage_duration"]), logs_app_usage[i]["row_data"]["current_app"], logs_app_usage[i]["row_data"]["geohash"], "Manufacturer"))

                db_dict = {"app_name": logs_app_usage[i]["row_data"]["app_usage_id"], "device_model": logs_app_usage[i]["row_data"]["device_model"], "app_usage_duration": logs_app_usage[i]["row_data"]["app_usage_duration"]}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (collect_time_local, "Used App", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __ma_web_history(logs_web_history, db_path):
        if len(logs_web_history) == 0:
            print("[SYSTEM] >>> No logs - web_history")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE ma_web_history (type TEXT, collect_time_local TEXT, collect_time TEXT, device_model TEXT, mcc TEXT, mnc TEXT, url_title TEXT, url TEXT, url_host TEXT, url_path TEXT, url_query TEXT, duration_ms INTEGER, current_app TEXT, geohash TEXT, source TEXT)")

            for i in tqdm(range(len(logs_web_history))):
                collect_time_local = convert_time.make_local(logs_web_history[i]["row_data"]["collect_time"])
                cur.execute("INSERT INTO ma_web_history VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                logs_web_history[i]["type"], collect_time_local, logs_web_history[i]["row_data"]["collect_time"], logs_web_history[i]["row_data"]["device_model"],
                logs_web_history[i]["row_data"]["mcc"], logs_web_history[i]["row_data"]["mnc"], logs_web_history[i]["row_data"]["url_title"],
                logs_web_history[i]["row_data"]["url_url"], logs_web_history[i]["row_data"]["url_host"],
                logs_web_history[i]["row_data"]["url_path"], logs_web_history[i]["row_data"]["url_query"],
                int(logs_web_history[i]["row_data"]["duration"]), logs_web_history[i]["row_data"]["current_app"],
                logs_web_history[i]["row_data"]["geohash"], "Manufacturer"))

                db_dict = {"url_title": logs_web_history[i]["row_data"]["url_title"], "url": logs_web_history[i]["row_data"]["url_url"], "duration_ms": logs_web_history[i]["row_data"]["duration"]}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (collect_time_local, "Browsed Web", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __ma_web_search_keyword(logs_search_keyword, db_path):
        if len(logs_search_keyword) == 0:
            print("[SYSTEM] >>> No logs - search_keyword")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE ma_web_search_keyword (type TEXT, collect_time_local TEXT, collect_time TEXT, device_model TEXT, mcc TEXT, mnc TEXT, keyword TEXT, category TEXT, url TEXT, geohash TEXT, source TEXT)")

            for i in tqdm(range(len(logs_search_keyword))):
                collect_time_local = convert_time.make_local(logs_search_keyword[i]["row_data"]["collect_time"])
                cur.execute("INSERT INTO ma_web_search_keyword VALUES(?,?,?,?,?,?,?,?,?,?,?);", (
                logs_search_keyword[i]["type"], collect_time_local, logs_search_keyword[i]["row_data"]["collect_time"],
                logs_search_keyword[i]["row_data"]["device_model"], logs_search_keyword[i]["row_data"]["mcc"],
                logs_search_keyword[i]["row_data"]["mnc"],
                logs_search_keyword[i]["row_data"]["keyword"], logs_search_keyword[i]["row_data"]["category"],
                logs_search_keyword[i]["row_data"]["uri"], logs_search_keyword[i]["row_data"]["geohash"], "Manufacturer"))

                db_dict = {"keyword": logs_search_keyword[i]["row_data"]["keyword"], "url": logs_search_keyword[i]["row_data"]["uri"]}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (collect_time_local, "Search Keyword", db_dict_str))

            conn.commit()
            conn.close()

    def sm_run(self):
        try:
            bluetooth_dictionary = self.__sm_all_bluetooth_dictionary(self.l["records_all_bluetooth_dictionary"], self.db_path)
            self.__sm_all_bluetooth_log(self.l["records_all_bluetooth_log"], self.db_path, bluetooth_dictionary) #timeline done
            self.__sm_app_usage(self.l["records_app_usage"], self.db_path) #timeline done
            self.__sm_bluetooth_device_dictionary(self.l["records_bluetooth_device_dictionary"], self.db_path)
            self.__sm_bluetooth_log(self.l["records_bluetooth_log"], self.db_path)
            self.__sm_monitoring_current_place_log(self.l["records_monitoring_current_place_log"], self.db_path) #timeline done
            self.__sm_charging_log(self.l["records_charging_log"], self.db_path) #timeline done
            self.__sm_country_app_count(self.l["records_country_app_count"], self.db_path)
            self.__sm_cpp_path_history(self.l["records_cpp_path_history"], self.db_path) #timeline done
            self.__sm_location_log(self.l["records_location_log"], self.db_path) #timeline done
            self.__sm_motion_log(self.l["records_motion_log"], self.db_path) #timeline done
            self.__sm_music_playback_log(self.l["records_music_playback_log"], self.db_path) #timeline done
            self.__sm_screen_log(self.l["records_screen_log"], self.db_path) #timeline 해야할까말까 고민
            self.__sm_screen_state_log(self.l["records_screen_state_log"], self.db_path) #timeline 해야할까말까 고민
            self.__sm_search_keyword_log(self.l["records_search_keyword_log"], self.db_path) #timeline done
            self.__sm_setting_change(self.l["records_setting_change"], self.db_path) #timeline done
            self.__sm_web_info(self.l["records_web_info"], self.db_path) #timeline done
            self.__sm_web_log(self.l["records_web_log"], self.db_path) #timeline 안해도될듯, web_info에서 각 url마다 id부여해서 딕셔너리화한 정도
            self.__sm_wifi_connection_log(self.l["records_wifi_connection_log"], self.db_path) #timeline done
            self.__sm_monitoring_country_info(self.l["records_monitoring_country_info"], self.db_path) #timeline 안해도될듯
            self.__sm_monitoring_tpo_context_event(self.l["records_monitoring_tpo_context_event"], self.db_path)


        except Exception as e:
            print("[SYSTEM] >>> Error: ", e)

    @staticmethod
    def __sm_all_bluetooth_dictionary(records_all_bluetooth_dictionary, db_path):
        # '{"_id":2536,"address":"C8:B2:9B:A4:BD:10","name":"CENTERJ","alias":"CENTERJ","major_cod":256,"cod":260,"last_seen_time":1650422858435,"last_seen_time_string":"2022\\/04\\/20 11:47:38","created_at":1650422854255}'
        # logging_all_bluetooth_dictionary: 블루투스 주소, 이름, 가장 마지막 연결시간(?-확실치않음), 최초 연결된 시간(?-확실치않음)

        bluetooth_dictionary = {}

        if len(records_all_bluetooth_dictionary) == 0:
            print("[SYSTEM] >>> logging_all_bluetooth_dictionary file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_all_bluetooth_dictionary (id TEXT, address TEXT, name TEXT, alias TEXT, major_cod TEXT, cod TEXT, last_seen_time TEXT, last_seen_time_string TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_all_bluetooth_dictionary))):
                record = json.loads(records_all_bluetooth_dictionary[i])
                _id = record["_id"]
                address = record["address"]
                if len(record) == 9:
                    name = record["name"]
                    alias = record["alias"]

                else:
                    name = ""
                    alias = ""
                major_cod = record["major_cod"]
                cod = record["cod"]
                last_seen_time = record["last_seen_time"]
                last_seen_time_string = record["last_seen_time_string"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_all_bluetooth_dictionary VALUES(?,?,?,?,?,?,?,?,?,?);", (
                _id, address, name, alias, major_cod, cod, last_seen_time, last_seen_time_string,
                created_at, "SmartSwitch"))

                bluetooth_dictionary[address] = name

            conn.commit()
            conn.close()

            return bluetooth_dictionary

    @staticmethod
    def __sm_all_bluetooth_log(records_all_bluetooth_log, db_path, bluetooth_dictionary):
        # '{"_id":2412,"address":"C0:DC:DA:93:B1:0A","connection_type":"CONNECTED","time":1649759697264,"time_string":"2022\\/04\\/12 19:34:57","timezone_id":"Asia\\/Seoul","created_at":1649759697000}'
        # logging_all_bluetooth_log: 블루투스 주소, 연결 및 해제 시간

        if len(records_all_bluetooth_log) == 0:
            print("[SYSTEM] >>> logging_all_bluetooth_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_all_bluetooth_log (id TEXT, address TEXT, name TEXT, connection_type TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_all_bluetooth_log))):
                record = json.loads(records_all_bluetooth_log[i])
                _id = record["_id"]
                address = record["address"]
                connection_type = record["connection_type"]
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]
                name = bluetooth_dictionary[address]

                cur.execute("INSERT INTO sm_all_bluetooth_log VALUES(?,?,?,?,?,?,?,?,?);", (
                _id, address, name, connection_type, time, time_string, timezone_id,
                created_at, "SmartSwitch"))

                db_dict = {"connection_type": connection_type, "name": name, "address": address}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Connected Bluetooth", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_app_usage(records_app_usage, db_path):
        # {"_id":21095,"package_name":"com.facebook.katana","class_name":"com.facebook.katana.activity.FbMainTabActivity","start_time":1649744815446,"start_time_string":"2022\/04\/12 15:26:55","end_time":1649744895131,"end_time_string":"2022\/04\/12 15:28:15","timezone_id":"Asia\/Seoul","created_at":1649762317000}
        # logging_app_usage: 앱 사용 이력

        if len(records_app_usage) == 0:
            print("[SYSTEM] >>> logging_app_usage file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_app_usage (id TEXT, package_name TEXT, class_name TEXT, start_time TEXT, start_time_string TEXT, end_time TEXT, end_time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_app_usage))):
                record = json.loads(records_app_usage[i])
                _id = record["_id"]
                package_name = record["package_name"]
                class_name = record["class_name"]
                start_time = record["start_time"]
                start_time_string = record["start_time_string"]
                end_time = record["end_time"]
                end_time_string = record["end_time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_app_usage VALUES(?,?,?,?,?,?,?,?,?,?);", (
                    _id, package_name, class_name, start_time, start_time_string, end_time, end_time_string, timezone_id, created_at, "SmartSwitch"))

                db_dict = {"app_name": package_name, "class_name": class_name, "end_time_string": end_time_string}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (start_time_string, "Used App", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_bluetooth_device_dictionary(records_bluetooth_device_dictionary, db_path):
        # '{"_id":2,"address":"10:55:48:00:71:DA","name":"Chevy MyLink","alias":"Chevy MyLink","cod":1032,"last_seen_time":1651902867885,"last_seen_time_string":"2022\\/05\\/07 14:54:27","created_at":1651902867000}'
        # logging_all_bluetooth_log: 블루투스 주소, 연결 및 해제 시간

        if len(records_bluetooth_device_dictionary) == 0:
            print("[SYSTEM] >>> logging_all_bluetooth_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_bluetooth_device_dictionary (id TEXT, address TEXT, name TEXT, alias TEXT, cod TEXT, last_seen_time TEXT, last_seen_time_string TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_bluetooth_device_dictionary))):
                record = json.loads(records_bluetooth_device_dictionary[i])
                _id = record["_id"]
                address = record["address"]
                name = record["name"]
                alias = record["alias"]
                cod = record["cod"]
                last_seen_time = record["last_seen_time"]
                last_seen_time_string = record["last_seen_time_string"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_bluetooth_device_dictionary VALUES(?,?,?,?,?,?,?,?,?);", (
                _id, address, name, alias, cod, last_seen_time, last_seen_time_string,
                created_at, "SmartSwitch"))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_bluetooth_log(records_bluetooth_log, db_path):
        # '{"_id":1,"address":"10:55:48:00:71:DA","connection_type":"DISCONNECTED","time":1651902744933,"time_string":"2022\\/05\\/07 14:52:24","timezone_id":"Asia\\/Seoul","created_at":1651902744000}'
        # logging_bluetooth_log: 블루투스(4)

        if len(records_bluetooth_log) == 0:
            print("[SYSTEM] >>> logging_bluetooth_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_bluetooth_log (id TEXT, address TEXT, connection_type TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_bluetooth_log))):
                record = json.loads(records_bluetooth_log[i])
                _id = record["_id"]
                address = record["address"]
                connection_type = record["connection_type"]
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_bluetooth_log VALUES(?,?,?,?,?,?,?,?);", (
                _id, address, connection_type, time, time_string, timezone_id,
                created_at, "SmartSwitch"))

            conn.commit()
            conn.close()

    def __sm_charging_log(self, records_charging_log, db_path):
        # '{"_id":1673,"connected":"1","plugged":0,"level":68,"place_id":5,"time":1649778631768,"time_string":"2022\\/04\\/13 00:50:31","timezone_id":"Asia\\/Seoul","created_at":1649778631000}'
        # charing_log: 핸드폰 충전 이력, 충전 장소(place_id -> crosscheck 필요)
        # place_id만 있고 place_Category는 monitoring부분에 dictionary가 있음

        if len(records_charging_log) == 0:
            print("[SYSTEM] >>> logging_charging_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_charging_log (id TEXT, connected TEXT, plugged TEXT, level TEXT, place_id TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_charging_log))):
                record = json.loads(records_charging_log[i])
                _id = record["_id"]
                connected = record["connected"]
                plugged = record["plugged"]
                level = record["level"]
                place_id = record["place_id"]
                p_category = self.place_dictionary[place_id] #ex)place_id = 5 => place category = HOME
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]
                if connected == "1":
                    connection_type = "CONNECTED"

                if connected == "0":
                    connection_type = "DISCONNECTED"

                cur.execute("INSERT INTO sm_charging_log VALUES(?,?,?,?,?,?,?,?,?,?);", (
                _id, connected, plugged, level, place_id, time, time_string, timezone_id,
                created_at, "SmartSwitch"))

                db_dict = {"place_category": p_category, "connection_type": connection_type, "plugged": plugged, "level": level}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Charged Phone", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_country_app_count(records_country_app_count, db_path):
        # '{"_id":14708,"package_name":"com.sec.android.app.myfiles","country_code":"KR","count":15,"created_at":1652312153000}'
        # logging_country_app_count: 앱의 Country Code가 "KR"인 앱에 대한 정보, count 값은 뭔지 모르겠음

        if len(records_country_app_count) == 0:
            print("[SYSTEM] >>> logging_country_app_count file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_country_app_count (id TEXT, package_name TEXT, country_code TEXT, count TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_country_app_count))):
                record = json.loads(records_country_app_count[i])
                _id = record["_id"]
                package_name = record["package_name"]
                country_code = record["country_code"]
                count = record["count"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_country_app_count VALUES(?,?,?,?,?,?);", (
                _id, package_name, country_code, count, created_at, "SmartSwitch"))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_cpp_path_history(records_cpp_path_history, db_path):
        # '{"id":4105,"latitude":37.58549880981445,"longitude":127.02165222167969,"accuracy":190,"timestamp":1649773504000,"time_string":"2022\\/04\\/12 23:25:04","timezone_id":"Asia\\/Seoul","created_at":1649773899000}'
        # logging_cpp_path_history_log: 기초 위치정보, 추후 location_log랑 통합

        if len(records_cpp_path_history) == 0:
            print("[SYSTEM] >>> logging_cpp_path_history file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_cpp_path_history (id TEXT, latitude TEXT, longitude TEXT, accuracy TEXT, timestamp TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_cpp_path_history))):
                record = json.loads(records_cpp_path_history[i])
                _id = record["id"]
                latitude = record["latitude"]
                longitude = record["longitude"]
                accuracy = record["accuracy"]
                timestamp = record["timestamp"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_cpp_path_history VALUES(?,?,?,?,?,?,?,?,?);", (
                _id, latitude, longitude, accuracy, timestamp, time_string, timezone_id, created_at, "SmartSwitch"))

                db_dict = {"latitude": str(latitude), "longitude": str(longitude)}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Location", db_dict_str))

            conn.commit()
            conn.close()

    #@staticmethod
    #def headset_log(records_headset_log, db_path): #이미지 둘다 데이터 없음
        #if len(records_headset_log) == 0:
        #    print("[SYSTEM] >>> logging_headset_log file has no records")

        # else:
        #     conn = sqlite3.connect(db_path)
        #     cur = conn.cursor()
        #     cur.execute(
        #         "CREATE TABLE headset_log (id TEXT, latitude TEXT, longitude TEXT, accuracy TEXT, timestamp TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")
        #
        #     for i in tqdm(range(len(records_cpp_path_history))):
        #         record = json.loads(records_cpp_path_history[i])
        #         _id = record["id"]
        #         latitude = record["latitude"]
        #         longitude = record["longitude"]
        #         accuracy = record["accuracy"]
        #         timestamp = record["timestamp"]
        #         time_string = record["time_string"]
        #         timezone_id = record["timezone_id"]
        #         created_at = record["created_at"]
        #
        #         cur.execute("INSERT INTO cpp_path_history VALUES(?,?,?,?,?,?,?,?,?);", (
        #         _id, latitude, longitude, accuracy, timestamp, time_string, timezone_id, created_at, "SmartSwitch"))
        #
        #     conn.commit()
        #     conn.close()

    @staticmethod
    def __sm_location_log(records_location_log, db_path):
        # {"_id":34034,"latitude":37.584598541259766,"longitude":127.02656555175781,"altitude":69,"provider":"passive_network","accuracy":92.9000015258789,"bearing":0,"speed":0,"time":1649762341666,"time_string":"2022\/04\/12 20:19:01","timezone_id":"Asia\/Seoul","created_at":1649762341000}
        # logging_location_log: 위치정보(위도,경도,고도) 및 시간

        if len(records_location_log) == 0:
            print("[SYSTEM] >>> logging_location_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_location_log (id TEXT, latitude TEXT, longitude TEXT, altitude TEXT, provider TEXT, accuracy TEXT, bearing TEXT, speed TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_location_log))):
                record = json.loads(records_location_log[i])
                _id = record["_id"]
                latitude = record["latitude"]
                longitude = record["longitude"]
                altitude = record["altitude"]
                provider = record["provider"]
                accuracy = record["accuracy"]
                bearing = record["bearing"]
                speed = record["speed"]
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_location_log VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                _id, latitude, longitude, altitude, provider, accuracy, bearing, speed, time, time_string, timezone_id,
                created_at, "SmartSwitch"))

                db_dict = {"latitude": str(latitude), "longitude": str(longitude), "altitude": str(altitude)}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Location", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_motion_log(records_motion_log, db_path):
        '{"_id":34085,"motion_type":"STATIONARY","time":1649762315010,"time_string":"2022\\/04\\/12 20:18:35","timezone_id":"Asia\\/Seoul","created_at":1649762323000}'
        # logging_motion_log: 특정 시간대 Motion(WALK, STATIONARY, VEHICLE, LOGGING_START)

        if len(records_motion_log) == 0:
            print("[SYSTEM] >>> logging_motion_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_motion_log (id TEXT, motion_type TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_motion_log))):
                record = json.loads(records_motion_log[i])
                _id = record["_id"]
                motion_type = record["motion_type"]
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_motion_log VALUES(?,?,?,?,?,?,?);", (
                _id, motion_type, time, time_string, timezone_id, created_at, "SmartSwitch"))

                #db_dict = {"motion_type": motion_type}
                #db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Motion", motion_type))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_music_playback_log(records_music_playback_log, db_path):
        # {"_id":394,"time":1649807719941,"time_string":"2022\/04\/13 08:55:19","timezone_id":"Asia\/Seoul","session_name":"com.iloen.melon","track":"회전목마 (Feat. Zion.T, 원슈타인) (Prod. Slom)","album":"쇼미더머니 10 Episode 2","artist":"sokodomo","genre":"","created_at":1649807719000}
        # logging_music_playback_log: 시간대 재생한 음악 및 음악 실행시킨 패키지명(ex.멜론-com.iloen.melon, com.sec.android.app.music)

        if len(records_music_playback_log) == 0:
            print("[SYSTEM] >>> logging_music_playback_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_music_playback_log (id TEXT, time TEXT, time_string TEXT, timezone_id TEXT, session_name TEXT, track TEXT, album TEXT, artist TEXT, genre TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_music_playback_log))):
                record = json.loads(records_music_playback_log[i])
                _id = record["_id"]
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                session_id = record["session_name"]
                track = record["track"]
                album = record["album"]
                artist = record["artist"]
                genre = record["genre"]
                created_at = record["created_at"]


                cur.execute("INSERT INTO sm_music_playback_log VALUES(?,?,?,?,?,?,?,?,?,?,?);", (
                _id, time, time_string, timezone_id, session_id, track, album, artist, genre, created_at, "SmartSwitch"))

                db_dict = {"artist": artist, "track": track, "app": session_id}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Played Music", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_screen_log(records_screen_log, db_path):
        # '{"_id":454,"package_names":"com.netmarble.enn","screen_type":2,"event_time":1624158429208,"event_time_string":"2021\\/06\\/20 12:07:09","state":1,"timezone_id":"Asia\\/Seoul","created_at":1624158430000}'
        # logging_screen_log: 시간대 "screen(추정)"에 보여지는 화면이 뭔지 패키지명(ex.유튜브를 보고 있었다면 해당 시간과 유튜브앱 패키지명 명기)
        # screen_type = 1or2인데 분할화면 여부인지 확인불가, state=1or2인데 여부 확인 불가

        if len(records_screen_log) == 0:
            print("[SYSTEM] >>> logging_screen_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_screen_log (id TEXT, package_names TEXT, screen_type TEXT, event_time TEXT, event_time_string TEXT, state TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_screen_log))):
                record = json.loads(records_screen_log[i])
                _id = record["_id"]
                package_names = record["package_names"]
                screen_type = record["screen_type"]
                event_time = record["event_time"]
                event_time_string = record["event_time_string"]
                state = record["state"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_screen_log VALUES(?,?,?,?,?,?,?,?,?);", (
                _id, package_names, screen_type, event_time, event_time_string, state, timezone_id, created_at, "SmartSwitch"))

            #timeline 넣기에 해석 필요

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_screen_state_log(records_screen_state_log, db_path):
        # '{"_id":64438,"screen_state":1,"user_present":0,"use_keyguard":1,"time":1649748859628,"time_string":"2022\\/04\\/12 16:34:19","timezone_id":"Asia\\/Seoul","created_at":1649748859000}'
        # logging_screen_state_log: 시간대 "screen_state"(스크린 상태=1or0)
        # screen_state, user_present, use_keyguard 다 0or1인데 의미하는 바 파악 필요

        if len(records_screen_state_log) == 0:
            print("[SYSTEM] >>> logging_screen_state_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_screen_state_log (id TEXT, screen_state TEXT, user_present TEXT, use_keyguard TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_screen_state_log))):
                record = json.loads(records_screen_state_log[i])
                _id = record["_id"]
                screen_state = record["screen_state"]
                user_present = record["user_present"]
                use_keyguard = record["use_keyguard"]
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_screen_state_log VALUES(?,?,?,?,?,?,?,?,?);", (
                _id, screen_state, user_present, use_keyguard, time, time_string, timezone_id, created_at, "SmartSwitch"))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_search_keyword_log(records_search_keyword_log, db_path):
        # '{"_id":22,"category":"browser","keyword":"그린폰","reference_uri":"search.kt.com","source":"SBROWSER","time":1652104641333,"time_string":"2022\\/05\\/09 22:57:21","created_at":1652104641000}'
        # logging_search_keyword_log: 시간대 삼성브라우저앱(추정-SBROWSER)에서 검색한 키워드

        if len(records_search_keyword_log) == 0:
            print("[SYSTEM] >>> logging_search_keyword_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_search_keyword_log (id TEXT, category TEXT, keyword TEXT, reference_uri TEXT, source_from TEXT, time TEXT, time_string TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_search_keyword_log))):
                record = json.loads(records_search_keyword_log[i])
                _id = record["_id"]
                category = record["category"]
                keyword = record["keyword"]
                reference_uri = record["reference_uri"]
                source = record["source"]
                time = record["time"]
                time_string = record["time_string"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_search_keyword_log VALUES(?,?,?,?,?,?,?,?,?);", (
                _id, category, keyword, reference_uri, source, time, time_string, created_at, "SmartSwitch"))

                db_dict = {"keyword": keyword, "reference_uri": reference_uri, "source_from": source}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Search Keyword", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_setting_change(records_setting_change, db_path):
        # '{"_id":7982,"setting_id":"mode_ringer","event_time":1649770080106,"event_time_string":"2022\\/04\\/12 22:28:00","timezone_id":"Asia\\/Seoul","value":2,"created_at":1649770080000}'
        # logging_setting_change_log: 시간대 핸드폰 설정 변경내역(gps on/off, 소리모드 변경 등)

        if len(records_setting_change) == 0:
            print("[SYSTEM] >>> logging_setting_change file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_setting_change_log (id TEXT, setting_id TEXT, event_time TEXT, event_time_string TEXT, timezond_id TEXT, value TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_setting_change))):
                record = json.loads(records_setting_change[i])
                _id = record["_id"]
                setting_id = record["setting_id"]
                event_time = record["event_time"]
                event_time_string = record["event_time_string"]
                timezone_id = record["timezone_id"]
                value = record["value"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_setting_change_log VALUES(?,?,?,?,?,?,?,?);", (
                _id, setting_id, event_time, event_time_string, timezone_id, value, created_at, "SmartSwitch"))

                #db_dict = {"Setting Type": setting_id, "reference_uri": reference_uri, "source_from": source}
                #db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (event_time_string, "Changed Setting", setting_id))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_web_info(records_web_info, db_path):
        # '{"_id":218,"title":"내지역 상세날씨-오늘","url":"http:\\/\\/www.kr-weathernews.com\\/mv3\\/html\\/today.html?region=1100000000#_hourly","update_time":1652052366761}'
        # logging_web_info_log: 시간대 핸드폰 설정 변경내역(gps on/off, 소리모드 변경 등)

        if len(records_web_info) == 0:
            print("[SYSTEM] >>> logging_web_info file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_web_info_log (id TEXT, title TEXT, url TEXT, update_time TEXT, source TEXT)")

            for i in tqdm(range(len(records_web_info))):
                record = json.loads(records_web_info[i])
                _id = record["_id"]
                title = record["title"]
                url = record["url"]
                update_time = record["update_time"]
                converted_time = convert_time.to_local_time(update_time)

                cur.execute("INSERT INTO sm_web_info_log VALUES(?,?,?,?,?);", (
                _id, title, url, update_time, "SmartSwitch"))

                db_dict = {"title": title, "url": url}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (converted_time, "Browsed Web", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_web_log(records_web_log, db_path):
        # '{"web_info_id":132,"time":1649656686423,"time_string":"2022\\/04\\/11 14:58:06","created_at":1649656686000}'
        # logging_web_info_log: 시간대 핸드폰 설정 변경내역(gps on/off, 소리모드 변경 등)

        if len(records_web_log) == 0:
            print("[SYSTEM] >>> logging_web_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_web_log (web_info_id TEXT, time TEXT, time_string TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_web_log))):
                record = json.loads(records_web_log[i])
                web_info_id = record["web_info_id"]
                time = record["time"]
                time_string = record["time_string"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_web_log VALUES(?,?,?,?,?);", (
                    web_info_id, time, time_string, created_at, "SmartSwitch"))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_wifi_connection_log(records_wifi_connection_log, db_path):
        # '{"_id":189,"ssid":"\\"U+zone\\"","bssid":"40:27:0b:02:dc:6a","connection_type":"CONNECTED","time":1649897012574,"time_string":"2022\\/04\\/14 09:43:32","timezone_id":"Asia\\/Seoul","created_at":1649897012000}'
        # logging_wifi_connection_log:

        if len(records_wifi_connection_log) == 0:
            print("[SYSTEM] >>> logging_wifi_connection_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_wifi_connection_log (_id TEXT, ssid TEXT, connection_type TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_wifi_connection_log))):
                record = json.loads(records_wifi_connection_log[i])
                _id = record["_id"]
                ssid = record["ssid"]
                connection_type = record["connection_type"]
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_wifi_connection_log VALUES(?,?,?,?,?,?,?,?);", (
                    _id, ssid, connection_type, time, time_string, timezone_id, created_at, "SmartSwitch"))

                db_dict = {"ssid": ssid, "connection_type": connection_type}
                db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Connected WiFi", db_dict_str))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_monitoring_country_info(records_monitoring_country_info, db_path):
        # '{"_id":8,"country_type":"HOME","current_country":"KR","home_country":"KR","check_type":"MOBILE","time":1651579417214,"time_string":"2022\\/05\\/03 21:03:37","created_at":1648991298000}'
        # monitoring_country_info:

        if len(records_monitoring_country_info) == 0:
            print("[SYSTEM] >>> monitoring_country_info file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_monitoring_country_info (_id TEXT, ssid TEXT, connection_type TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_monitoring_country_info))):
                record = json.loads(records_monitoring_country_info[i])
                _id = record["_id"]
                country_type = record["country_type"]
                home_country = record["home_country"]
                check_type = record["check_type"]
                time = record["time"]
                time_string = record["time_string"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_monitoring_country_info VALUES(?,?,?,?,?,?,?,?);", (
                    _id, country_type, home_country, check_type, time, time_string, created_at, "SmartSwitch"))

            conn.commit()
            conn.close()

    def __sm_monitoring_current_place_log(self, records_monitoring_current_place_log, db_path):
        # '{"_id":1497,"place_category":"FREQUENTLY_VISITED","registered_type":"ANALYZED_PLACE","place_id":69,"time":1649772958280,"time_string":"2022\\/04\\/12 23:15:58","timezone_id":"Asia\\/Seoul","confidence":0.4300000071525574,"created_at":1649772958000}'
        # monitoring_current_place_log:

        if len(records_monitoring_current_place_log) == 0:
            print("[SYSTEM] >>> monitoring_current_place_log file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_monitoring_current_place_log (_id TEXT, place_category TEXT, registered_type TEXT, place_id TEXT, time TEXT, time_string TEXT, timezone_id TEXT, confidence TEXT, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_monitoring_current_place_log))):
                record = json.loads(records_monitoring_current_place_log[i])
                _id = record["_id"]
                place_category = record["place_category"]
                registered_type = record["registered_type"]
                place_id = record["place_id"]
                time = record["time"]
                time_string = record["time_string"]
                timezone_id = record["timezone_id"]
                confidence = record["confidence"]
                created_at = record["created_at"]

                cur.execute("INSERT INTO sm_monitoring_current_place_log VALUES(?,?,?,?,?,?,?,?,?,?);", (
                    _id, place_category, registered_type, place_id, time, time_string, timezone_id, confidence, created_at, "SmartSwitch"))

                if place_category == "WORK" or "NEAR_WORK":
                    self.place_dictionary[place_id] = "WORK"

                if place_category == "HOME"  or "NEAR_HOME":
                    self.place_dictionary[place_id] = "HOME"

                if place_category == "FREQUENTLY_VISITED":
                    self.place_dictionary[place_id] = "FREQUENTLY_VISITED"

                #db_dict = {"place_category": place_category}
                #db_dict_str = str(db_dict)
                cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                            (time_string, "Current Place", place_category))

            conn.commit()
            conn.close()

    @staticmethod
    def __sm_monitoring_tpo_context_event(records_monitoring_tpo_context_event, db_path):
        # {'_id': 29712, 'category': 'TIME', 'subcategory': 'SLEEP_TIME', 'tpo_context': 'BEFORE_BEDTIME', 'is_trigger_context': 1, 'time': 1649778108391, 'time_text': '2022/04/13 00:41:48', 'expired_time': 1649785307798, 'expired_time_text': '2022/04/13 02:41:47', 'timezone_id': 'Asia/Seoul', 'confidence': 0.9049999713897705, 'is_enough_sampling': 1, 'base_time': 6107798, 'base_time_text': '01:41:47', 'event_time': 1649778108295, 'event_time_text': '2022/04/13 00:41:48', 'reference_uri': 'content://com.samsung.android.rubin.persona.sleeppattern/sleep_pattern_info', 'id': 1695, 'created_at': 1649778108000}
        # monitoring_tpo_context_event:

        if len(records_monitoring_tpo_context_event) == 0:
            print("[SYSTEM] >>> monitoring_tpo_context_event file has no records")

        else:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE sm_monitoring_tpo_context_event_log (_id TEXT, category TEXT, subcategory TEXT, tpo_context TEXT, is_trigger_context TEXT, time TEXT, time_string TEXT, expired_time TEXT, expired_text_string TEXT, timezone_id TEXT, confidence TEXT, is_enough_sampling TEXT, base_time TEXT, base_time_string TEXT, event_time TEXT, event_time_string TEXT, reference_uri TEXT, id text, created_at TEXT, source TEXT)")

            for i in tqdm(range(len(records_monitoring_tpo_context_event))):
                record = json.loads(records_monitoring_tpo_context_event[i])
                if len(record) == 15:
                    _id = record["_id"]
                    category = record["category"]
                    subcategory = record["subcategory"]
                    tpo_context = record["tpo_context"]
                    is_trigger_context = record["is_trigger_context"]
                    time = record["time"]
                    time_string = record["time_text"]
                    expired_time = record["expired_time"]
                    expired_time_string = record["expired_time_text"]
                    timezone_id = record["timezone_id"]
                    confidence = record["confidence"]
                    is_enough_sampling = record["is_enough_sampling"]
                    base_time = ""
                    base_time_string = ""
                    event_time = record["event_time"]
                    event_time_string = record["event_time_text"]
                    reference_uri = ""
                    id = ""
                    created_at = record["created_at"]

                    cur.execute(
                        "INSERT INTO sm_monitoring_tpo_context_event_log VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                        (
                            _id, category, subcategory, tpo_context, is_trigger_context, time, time_string,
                            expired_time, expired_time_string, timezone_id, confidence, is_enough_sampling, base_time,
                            base_time_string, event_time, event_time_string, reference_uri, id, created_at,
                            "SmartSwitch"))

                if len(record) == 16:
                    _id = record["_id"]
                    category = record["category"]
                    subcategory = record["subcategory"]
                    tpo_context = record["tpo_context"]
                    is_trigger_context = record["is_trigger_context"]
                    time = record["time"]
                    time_string = record["time_text"]
                    expired_time = record["expired_time"]
                    expired_time_string = record["expired_time_text"]
                    timezone_id = record["timezone_id"]
                    confidence = record["confidence"]
                    is_enough_sampling = record["is_enough_sampling"]
                    base_time = ""
                    base_time_string = ""
                    event_time = record["event_time"]
                    event_time_string = record["event_time_text"]
                    reference_uri = record["reference_uri"]
                    id = ""
                    created_at = record["created_at"]

                    cur.execute(
                        "INSERT INTO sm_monitoring_tpo_context_event_log VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                        (
                            _id, category, subcategory, tpo_context, is_trigger_context, time, time_string,
                            expired_time, expired_time_string, timezone_id, confidence, is_enough_sampling, base_time,
                            base_time_string, event_time, event_time_string, reference_uri, id, created_at,
                            "SmartSwitch"))

                if len(record) == 17:
                    _id = record["_id"]
                    category = record["category"]
                    subcategory = record["subcategory"]
                    tpo_context = record["tpo_context"]
                    is_trigger_context = record["is_trigger_context"]
                    time = record["time"]
                    time_string = record["time_text"]
                    expired_time = record["expired_time"]
                    expired_time_string = record["expired_time_text"]
                    timezone_id = record["timezone_id"]
                    confidence = record["confidence"]
                    is_enough_sampling = record["is_enough_sampling"]
                    base_time = ""
                    base_time_string = ""
                    event_time = record["event_time"]
                    event_time_string = record["event_time_text"]
                    reference_uri = record["reference_uri"]
                    id = record["id"]
                    created_at = record["created_at"]

                    cur.execute(
                        "INSERT INTO sm_monitoring_tpo_context_event_log VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                        (
                            _id, category, subcategory, tpo_context, is_trigger_context, time, time_string,
                            expired_time, expired_time_string, timezone_id, confidence, is_enough_sampling, base_time,
                            base_time_string, event_time, event_time_string, reference_uri, id, created_at,
                            "SmartSwitch"))

                if len(record) == 18:
                    _id = record["_id"]
                    category = record["category"]
                    subcategory = record["subcategory"]
                    tpo_context = record["tpo_context"]
                    is_trigger_context = record["is_trigger_context"]
                    time = record["time"]
                    time_string = record["time_text"]
                    expired_time = record["expired_time"]
                    expired_time_string = record["expired_time_text"]
                    timezone_id = record["timezone_id"]
                    confidence = record["confidence"]
                    is_enough_sampling = record["is_enough_sampling"]
                    base_time = record["base_time"]
                    base_time_string = record["base_time_text"]
                    event_time = record["event_time"]
                    event_time_string = record["event_time_text"]
                    reference_uri = record["reference_uri"]
                    id = ""
                    created_at = record["created_at"]

                    cur.execute(
                        "INSERT INTO sm_monitoring_tpo_context_event_log VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                        (
                            _id, category, subcategory, tpo_context, is_trigger_context, time, time_string,
                            expired_time, expired_time_string, timezone_id, confidence, is_enough_sampling, base_time,
                            base_time_string, event_time, event_time_string, reference_uri, id, created_at,
                            "SmartSwitch"))

                if len(record) == 19:
                    _id = record["_id"]
                    category = record["category"]
                    subcategory = record["subcategory"]
                    tpo_context = record["tpo_context"]
                    is_trigger_context = record["is_trigger_context"]
                    time = record["time"]
                    time_string = record["time_text"]
                    expired_time = record["expired_time"]
                    expired_time_string = record["expired_time_text"]
                    timezone_id = record["timezone_id"]
                    confidence = record["confidence"]
                    is_enough_sampling = record["is_enough_sampling"]
                    base_time = record["base_time"]
                    base_time_string = record["base_time_text"]
                    event_time = record["event_time"]
                    event_time_string = record["event_time_text"]
                    reference_uri = record["reference_uri"]
                    id = record["id"]
                    created_at = record["created_at"]

                    cur.execute(
                        "INSERT INTO sm_monitoring_tpo_context_event_log VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                        (
                            _id, category, subcategory, tpo_context, is_trigger_context, time, time_string,
                            expired_time, expired_time_string, timezone_id, confidence, is_enough_sampling, base_time,
                            base_time_string, event_time, event_time_string, reference_uri, id, created_at,
                            "SmartSwitch"))

                    db_dict = {"tpo_context": tpo_context, "category": category, "subcategory": subcategory}
                    db_dict_str = str(db_dict)
                    cur.execute("INSERT INTO timeline VALUES(?,?,?);",
                                (event_time_string, "Monitoring Log", db_dict_str))

            conn.commit()
            conn.close()