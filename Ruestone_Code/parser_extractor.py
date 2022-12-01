import json

#logging_all_bluetooth_dictionary: 블루투스(1)
#logging_all_bluetooth_log: 블루투스(2)
#logging_app_usage: 앱 사용 이력
#logging_bluetooth_device_dictionary: 블루투스(3)
#logging_bluetooth_log: 블루투스(4)
#logging_charging_log: 충전 이력
#logging_country_app_count: 앱의 Country Code가 "KR"인 앱에 대한 정보
#logging_cpp_path_history_log
#logging_headset_log
#logging_location_log
#logging_motion_log
#logging_music_playback_log
#logging_screen_log
#logging_screen_state_log
#logging_search_keyword_log
#logging_setting_change
#logging_web_info
#logging_web_log
#logging_wifi_connection_log
#monitoring_country_info
#monitoring_current_place_log
#monitoring_tpo_context_event

class Extractor:
    def __init__(self):
        pass

    def sm_extractor(self, path_to_file): #logging_location_log, logging_cpp_path_history_log
        self.sm_result = {}

        # logging_all_bluetooth_dictionary: 블루투스 주소, 이름, 가장 마지막 연결시간(?-확실치않음), 최초 연결된 시간(?-확실치않음)
        all_bluetooth_dictionary = "logging_all_bluetooth_dictionary"
        with open(path_to_file + all_bluetooth_dictionary, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_all_bluetooth_dictionary = json.loads(raw[0])
            self.sm_result["records_all_bluetooth_dictionary"] = logs_all_bluetooth_dictionary["records"]
            #records_all_bluetooth_dictionary = logs_all_bluetooth_dictionary["records"]

        # logging_all_bluetooth_log: 블루투스 주소, 연결 및 해제 시간
        all_bluetooth_log = "logging_all_bluetooth_log"
        with open(path_to_file + all_bluetooth_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_all_bluetooth_log = json.loads(raw[0])
            self.sm_result["records_all_bluetooth_log"] = logs_all_bluetooth_log["records"]
            #records_all_bluetooth_log = logs_all_bluetooth_log["records"]

        # logging_app_usage: 앱 사용 이력
        app_usage = "logging_app_usage"
        with open(path_to_file + app_usage, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_app_usge = json.loads(raw[0])
            self.sm_result["records_app_usage"] = logs_app_usge["records"]
            #records_app_usage = logs_app_usge["records"]

        # logging_bluetooth_device_dictionary: 블루투스 주소, 이름, 가장 마지막 연결시간(?-확실치않음), 최초 연결된 시간(?-확실치않음)
        bluetooth_device_dictionary = "logging_bluetooth_device_dictionary"
        with open(path_to_file + bluetooth_device_dictionary, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_bluetooth_device_dictionary = json.loads(raw[0])
            self.sm_result["records_bluetooth_device_dictionary"] = logs_bluetooth_device_dictionary["records"]
            #records_bluetooth_device_dictionary = logs_bluetooth_device_dictionary["records"]

        # logging_bluetooth_log: 블루투스
        bluetooth_log = "logging_bluetooth_log"
        with open(path_to_file + bluetooth_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_bluetooth_log = json.loads(raw[0])
            self.sm_result["records_bluetooth_log"] = logs_bluetooth_log["records"]
            #records_bluetooth_log = logs_bluetooth_log["records"]

        # logging_charging_log: 충전 이력
        charging_log = "logging_charging_log"
        with open(path_to_file + charging_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_charing_log = json.loads(raw[0])
            self.sm_result["records_charging_log"] = logs_charing_log["records"]
            #records_charging_log = logs_charing_log["records"]

        # logging_country_app_count: 앱의 Country Code가 "KR"인 앱에 대한 정보, count 값은 뭔지 모르겠음
        country_app_count = "logging_country_app_count"
        with open(path_to_file + country_app_count, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_country_app_count = json.loads(raw[0])
            self.sm_result["records_country_app_count"] = logs_country_app_count["records"]
            #records_country_app_count = logs_country_app_count["records"]

        # logging_cpp_path_history_log: 기초 위치정보
        cpp_path_history_log = "logging_cpp_path_history_log"
        with open(path_to_file + cpp_path_history_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_cpp_path_history_log= json.loads(raw[0])
            self.sm_result["records_cpp_path_history"] = logs_cpp_path_history_log["records"]
            #records_cpp_path_history = logs_cpp_path_history_log["records"]

        # logging_headset_log: 현재 데이터 없음
        headset_log = "logging_headset_log"
        with open(path_to_file + headset_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_headset_log= json.loads(raw[0])
            self.sm_result["records_headset_log"] = logs_headset_log["records"]
            #records_headset_log = logs_headset_log["records"]

        # logging_location_log: 위치정보(위도,경도,고도) 및 시간
        location_log = "logging_location_log"
        with open(path_to_file + location_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_location_log = json.loads(raw[0])
            self.sm_result["records_location_log"] = logs_location_log["records"]
            #records_location_log = logs_location_log["records"]

        # logging_motion_log: 특정 시간대 Motion(WALK, STATIONARY, VEHICLE)
        motion_log = "logging_motion_log"
        with open(path_to_file + motion_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_motion_log= json.loads(raw[0])
            self.sm_result["records_motion_log"] = logs_motion_log["records"]
            records_motion_log = logs_motion_log["records"]

        # logging_music_playback_log: 시간대 재생한 음악 및 음악 실행시킨 패키지명(ex.멜론-com.iloen.melon, com.sec.android.app.music)
        music_playback_log = "logging_music_playback_log"
        with open(path_to_file + music_playback_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_music_playback_log= json.loads(raw[0])
            self.sm_result["records_music_playback_log"] = logs_music_playback_log["records"]
            #records_music_playback_log = logs_music_playback_log["records"]

        # logging_screen_log
        screen_log = "logging_screen_log"
        with open(path_to_file + screen_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_screen_log= json.loads(raw[0])
            self.sm_result["records_screen_log"] = logs_screen_log["records"]
            #records_screen_log = logs_screen_log["records"]

        # logging_screen_state_log
        screen_state_log = "logging_screen_state_log"
        with open(path_to_file + screen_state_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_screen_state_log= json.loads(raw[0])
            self.sm_result["records_screen_state_log"] = logs_screen_state_log["records"]
            #records_screen_state_log = logs_screen_state_log["records"]

        # logging_search_keyword_log
        search_keyword_log = "logging_search_keyword_log"
        with open(path_to_file + search_keyword_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_search_keyword_log= json.loads(raw[0])
            self.sm_result["records_search_keyword_log"] = logs_search_keyword_log["records"]
            #records_search_keyword_log = logs_search_keyword_log["records"]

        # logging_setting_change
        setting_change = "logging_setting_change"
        with open(path_to_file + setting_change, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_setting_change= json.loads(raw[0])
            self.sm_result["records_setting_change"] = logs_setting_change["records"]
            #records_setting_change = logs_setting_change["records"]

        # logging_web_info
        web_info = "logging_web_info"
        with open(path_to_file + web_info, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_web_info= json.loads(raw[0])
            self.sm_result["records_web_info"] = logs_web_info["records"]
            #records_web_info = logs_web_info["records"]

        # logging_web_log
        web_log = "logging_web_log"
        with open(path_to_file + web_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_web_log= json.loads(raw[0])
            self.sm_result["records_web_log"] = logs_web_log["records"]
            #records_web_log = logs_web_log["records"]

        # logging_wifi_connection_log
        wifi_connection_log = "logging_wifi_connection_log"
        with open(path_to_file + wifi_connection_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_wifi_connection_log= json.loads(raw[0])
            self.sm_result["records_wifi_connection_log"] = logs_wifi_connection_log["records"]
            #records_wifi_connection_log = logs_wifi_connection_log["records"]

        # monitoring_country_info
        monitoring_country_info = "monitoring_country_info"
        with open(path_to_file + monitoring_country_info, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_monitoring_country_info= json.loads(raw[0])
            self.sm_result["records_monitoring_country_info"] = logs_monitoring_country_info["records"]
            #records_monitoring_country_info = logs_monitoring_country_info["records"]

        # monitoring_current_place_log
        monitoring_current_place_log = "monitoring_current_place_log"
        with open(path_to_file + monitoring_current_place_log, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_monitoring_current_place_log= json.loads(raw[0])
            self.sm_result["records_monitoring_current_place_log"] = logs_monitoring_current_place_log["records"]
            #records_monitoring_current_place_log = logs_monitoring_current_place_log["records"]

        # monitoring_tpo_context_event
        monitoring_tpo_context_event = "monitoring_tpo_context_event"
        with open(path_to_file + monitoring_tpo_context_event, "r", encoding="UTF-8") as file:
            raw = file.readlines()
            logs_monitoring_tpo_context_event= json.loads(raw[0])
            self.sm_result["records_monitoring_tpo_context_event"] = logs_monitoring_tpo_context_event["records"]
            #records_monitoring_tpo_context_event = logs_monitoring_tpo_context_event["records"]

        return self.sm_result

    def ma_extractor(self, path_to_file):
        self.ma_result = {}

        logs_samsung_account = []
        logs_wifi_bt_connection = []
        logs_app_usage = []
        logs_web_history = []
        logs_notification = []
        logs_app_usage_fold = []
        logs_search_keyword = []

        with open(path_to_file, "r", encoding="UTF-8") as file:
            raw = file.readlines()

            try:
                for i in range(len(raw)):
                    log = json.loads(raw[i])
                    # print(log)

                    if log["type"] == "samsung_account":
                        logs_samsung_account.append(log)

                    if log["type"] == "services_apps":
                        logs_wifi_bt_connection.append(log)

                    if log["type"] == "app_usage":
                        logs_app_usage.append(log)

                    if log["type"] == "url":
                        logs_web_history.append(log)

                    if log["type"] == "notification":
                        logs_notification.append(log)

                    if log["type"] == "app_usage_fold":
                        logs_app_usage_fold.append(log)

                    if log["type"] == "search_keyword":
                        logs_search_keyword.append(log)

                    # if log["type"] not in type:
                    #     type.append(log["type"])

                self.ma_result["samsung_account"] = logs_samsung_account
                self.ma_result["wifi_bt_connection"] = logs_wifi_bt_connection
                self.ma_result["app_usage"] = logs_app_usage
                self.ma_result["web_history"] = logs_web_history
                self.ma_result["app_usage_fold"] = logs_app_usage_fold
                self.ma_result["search_keyword"] = logs_search_keyword

            except Exception as e:
                print("ERROR:", e)

            return self.ma_result


