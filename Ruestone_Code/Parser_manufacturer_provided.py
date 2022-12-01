import json
import sqlite3
from tqdm import tqdm

def parse():
    logs_samsung_account = []
    logs_services_apps = []
    logs_app_usage = []
    logs_url = []
    logs_notification = []
    logs_app_usage_fold = []
    logs_search_keyword = []
    #type = [] # Type: ['samsung_account', 'services_apps', 'app_usage', 'url', 'notification', 'app_usage_fold', 'search_keyword']

    with open("../Image/Manufacturer_Provided/JW/Customization_Service_collected_data_jw_220622.txt", "r", encoding="UTF-8") as file:
        raw = file.readlines()

        try:
            for i in range(len(raw)):
                log = json.loads(raw[i])
                #print(log)

                if log["type"] == "samsung_account":
                    logs_samsung_account.append(log)

                if log["type"] == "services_apps":
                    logs_services_apps.append(log)

                if log["type"] == "app_usage":
                    logs_app_usage.append(log)

                if log["type"] == "url":
                    logs_url.append(log)

                if log["type"] == "notification":
                    logs_notification.append(log)

                if log["type"] == "app_usage_fold":
                    logs_app_usage_fold.append(log)

                if log["type"] == "search_keyword":
                    logs_search_keyword.append(log)

                # if log["type"] not in type:
                #     type.append(log["type"])

        except Exception as e:
            print("ERROR:", e)

        return logs_samsung_account, logs_services_apps, logs_app_usage, logs_url, logs_notification, logs_app_usage_fold, logs_search_keyword

def account_info(logs_samsung_account):
    print("[System] >>> Analyzing on [Samsung account]...")

    conn = sqlite3.connect("../result.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE account_info (type TEXT, collect_time TEXT, gender TEXT, birthday TEXT, country_code TEXT, source TEXT)")
    cur.execute("INSERT INTO account_info VALUES(?,?,?,?,?,?);", (logs_samsung_account[0]["type"], logs_samsung_account[0]["row_data"]["collect_time"], logs_samsung_account[0]["row_data"]["gender"], logs_samsung_account[0]["row_data"]["birthday"], logs_samsung_account[0]["row_data"]["country_code"], "SmartSwitch"))
    conn.commit()
    conn.close()

    print("[System] >>> Done")

def wifi_bt_connection(logs_services_apps): #services_apps: {"type":"services_apps","row_data":{"collect_time":"2021-04-12 11:04:16 +0000","sync_time":"2021-04-15 01:02:01 +0000","device_model":"SM-F916N","mcc":"450","mnc":"06","service_type":"framework","data_type":"wifi_bt_connection","details":"{\"data\":[{\"connection_type\":\"4\",\"duration\":\"132140959\",\"registered_type\":\"ANALYZED_PLACE\",\"place_category\":\"HOME\",\"mac_address\":\"42:23:aa:ce:d4:cf\",\"device_name\":\"\\\"SK_WiFiGIGAD4CC_5G\\\"\"}]}"}
    print("[System] >>> Analyzing on [Wifi & Bluetooth Connections]...")

    conn = sqlite3.connect("../result.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE wifi_bt_history (type TEXT, collect_time TEXT, sync_time TEXT, device_mode TEXT, mcc TEXT, mnc TEXT, service_type TEXT, data_type TEXT, connection_type TEXT, duration TEXT, registered_type TEXT, place_category TEXT, mac_address TEXT, device_name TEXT)")

    logs = []
    for i in range(len(logs_services_apps)):
        if "data_type" in logs_services_apps[i]["row_data"]:
            if logs_services_apps[i]["row_data"]["data_type"] == "wifi_bt_connection":
                logs.append(logs_services_apps[i])

    i = 0

    for i in tqdm(range(len(logs))):
        details = json.loads(logs[i]["row_data"]["details"])
        connection_type = details["data"][0]["connection_type"]
        duration = details["data"][0]["duration"]
        registered_type = details["data"][0]["registered_type"]
        place_category = details["data"][0]["place_category"]
        mac_address = details["data"][0]["mac_address"]
        device_name = details["data"][0]["device_name"]

        cur.execute("INSERT INTO wifi_bt_history VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (logs[i]["type"], logs[i]["row_data"]["collect_time"], logs[i]["row_data"]["sync_time"], logs[i]["row_data"]["device_model"], logs[i]["row_data"]["mcc"],
                                                                                       logs[i]["row_data"]["mnc"], logs[i]["row_data"]["service_type"], logs[i]["row_data"]["data_type"], connection_type, duration, registered_type, place_category, mac_address, device_name))

    conn.commit()
    conn.close()

    print("[System] >>> Done")

def app_usage(logs_app_usage): #{'type': 'app_usage', 'row_data': {'collect_time': '2022-05-01 05:08:00 +0000', 'device_model': 'SM-T720', 'mcc': '450', 'mnc': '', 'android_version': '01:11', 'baseband_version': 'T720XXU2DUJ1', 'app_usage_id': 'com.synology.dsvideo', 'app_usage_duration': '5809', 'current_app': None, 'geohash': None}}
    print("[System] >>> Analyzing on [App Usage]...")

    conn = sqlite3.connect("../result.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE app_usage (type TEXT, collect_time TEXT, device_model TEXT, mcc TEXT, mnc TEXT, android_version TEXT, baseband_version TEXT, app_name TEXT, app_usage_duration TEXT, current_app TEXT, geohash TEXT)")

    for i in tqdm(range(len(logs_app_usage))):
        cur.execute("INSERT INTO app_usage VALUES(?,?,?,?,?,?,?,?,?,?,?);", (logs_app_usage[i]["type"], logs_app_usage[i]["row_data"]["collect_time"], logs_app_usage[i]["row_data"]["device_model"], logs_app_usage[i]["row_data"]["mcc"], logs_app_usage[i]["row_data"]["mnc"], logs_app_usage[i]["row_data"]["android_version"],
                    logs_app_usage[i]["row_data"]["baseband_version"], logs_app_usage[i]["row_data"]["app_usage_id"], logs_app_usage[i]["row_data"]["app_usage_duration"], logs_app_usage[i]["row_data"]["current_app"], logs_app_usage[i]["row_data"]["geohash"]))

    conn.commit()
    conn.close()

    print("[System] >>> Done")

#{'type': 'url', 'row_data': {'collect_time': '2021-10-09 01:14:13 +0000', 'device_model': 'SM-F916N', 'mcc': '450', 'mnc': '06', 'url_title': '손흥민·지수, 또다시 온라인발 열애설…3가지 증거는?', 'url_url': 'http://m.newspic.kr/view.html?nid=2021100809454296035&pn=179&cp=C0QgE99g&utm_medium=affiliate&utm_campaign=2021100809454296035&utm_source=np210729C0QgE99g#_enliple', 'url_host': 'm.newspic.kr', 'url_path': '/view.html', 'url_query': 'nid=2021100809454296035&pn=179&cp=C0QgE99g&utm_medium=affiliate&utm_campaign=2021100809454296035&utm_source=np210729C0QgE99g', 'duration': '46636', 'current_app': None, 'geohash': None}}
def web_history(logs_url):
    print("[System] >>> Analyzing on [Web History]...")

    conn = sqlite3.connect("../result.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE web_history (type TEXT, collect_time TEXT, device_model TEXT, mcc TEXT, mnc TEXT, url_title TEXT, url TEXT, url_host TEXT, url_path TEXT, url_query TEXT, duration TEXT, current_app TEXT, geohash TEXT)")

    for i in tqdm(range(len(logs_url))):
        cur.execute("INSERT INTO web_history VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);", (logs_url[i]["type"], logs_url[i]["row_data"]["collect_time"], logs_url[i]["row_data"]["device_model"], logs_url[i]["row_data"]["mcc"], logs_url[i]["row_data"]["mnc"], logs_url[i]["row_data"]["url_title"],
                    logs_url[i]["row_data"]["url_url"], logs_url[i]["row_data"]["url_host"], logs_url[i]["row_data"]["url_path"], logs_url[i]["row_data"]["url_query"], logs_url[i]["row_data"]["duration"], logs_url[i]["row_data"]["current_app"], logs_url[i]["row_data"]["geohash"]))

    conn.commit()
    conn.close()

def keyword(logs_search_keyword):
    print("[System] >>> Analyzing on [Keyword Search History]...")

    conn = sqlite3.connect("../result.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE search_history (type TEXT, collect_time TEXT, device_model TEXT, mcc TEXT, mnc TEXT, keyword TEXT, category TEXT, url TEXT, geohash TEXT)")

    for i in tqdm(range(len(logs_search_keyword))):
        cur.execute("INSERT INTO search_history VALUES(?,?,?,?,?,?,?,?,?);", (logs_search_keyword[i]["type"], logs_search_keyword[i]["row_data"]["collect_time"], logs_search_keyword[i]["row_data"]["device_model"], logs_search_keyword[i]["row_data"]["mcc"], logs_search_keyword[i]["row_data"]["mnc"],
                                                                             logs_search_keyword[i]["row_data"]["keyword"], logs_search_keyword[i]["row_data"]["category"], logs_search_keyword[i]["row_data"]["uri"], logs_search_keyword[i]["row_data"]["geohash"]))

    conn.commit()
    conn.close()

def main():
    logs_samsung_account, logs_services_apps, logs_app_usage, logs_url, logs_notification, logs_app_usage_fold, logs_search_keyword = parse()
    account_info(logs_samsung_account)
    wifi_bt_connection(logs_services_apps)
    app_usage(logs_app_usage)
    web_history(logs_url)
    keyword(logs_search_keyword)

if __name__ == '__main__':
    main()


