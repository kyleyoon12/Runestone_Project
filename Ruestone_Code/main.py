import module.path as p
import parser_extractor as e
import parser_db_insert as d
import module.mode as m
import visualization as v
import module.decryption as c

class Core():
    def run(self):
        while True:
            self.n, self.task = m.Mode.mode_select(self) #SmartSwitch Decryption
            if self.n == 1 and self.task == "decrypt":
                c.Decryption.setting(self)

            if self.n == 1 and self.task == "parse": #Manufacturer - Parse
                p.Path.create_result_db_path(self)
                ma_logs = self.__ma_extractor()
                self.__db_insert(ma_logs)

            if self.n == 2 and self.task == "parse": #SmartSwitch - Parse after decryption
                p.Path.create_result_db_path(self)
                sm_logs = self.__sm_extractor() # l = logs
                self.__db_insert(sm_logs)

            if self.n == 3 and self.task == 1: #Functions - Location Tracker
                p.Path.create_result_vis_path(self)
                self.__visualization()

            if self.n == 4:
                break

    def __sm_extractor(self):
        path_to_file = p.Path.sm_source_file_path(self)
        logs = e.Extractor.sm_extractor(self, path_to_file)

        return logs

    def __ma_extractor(self):
        path_to_file = p.Path.ma_source_file_path(self)
        logs = e.Extractor.ma_extractor(self, path_to_file)

        return logs

    def __db_insert(self, l):
        path_to_db = p.Path.result_db_path(self)
        d.DB_insert(self.n, l, path_to_db) #mode, logs, path_to_db

    def __visualization(self):
        path_to_db = p.Path.result_db_path(self)
        path_to_result = p.Path.path_to_visualization(self)
        v.Visualization.make_html(self, path_to_db, path_to_result)

if __name__ == '__main__':
    a = Core()
    a.run()

    ### Expected Log Files Via SmartSwitch
    # logging_all_bluetooth_dictionary: 블루투스(1)
    # logging_all_bluetooth_log: 블루투스(2)
    # logging_app_usage: 앱 사용 이력
    # logging_bluetooth_device_dictionary: 블루투스(3)
    # logging_bluetooth_log: 블루투스(4)
    # logging_charging_log: 충전 이력
    # logging_country_app_count: 앱의 Country Code가 "KR"인 앱에 대한 정보
    # logging_cpp_path_history_log:
    # logging_headset_log:
    # logging_location_log:
    # logging_motion_log:
    # logging_music_playback_log:
    # logging_screen_log:
    # logging_screen_state_log:
    # logging_search_keyword_log:
    # logging_setting_change:
    # logging_web_info:
    # logging_web_log:
    # logging_wifi_connection_log:
    # monitoring_country_info:
    # monitoring_current_place_log:
    # monitoring_tpo_context_event:

    ### Expeceted types of logs provided by the Manufacturer
    # Account Info:
    # Wifi & Bluetooth Connection Logs:
    # App Usage History:
    # Web(Default Samsung Browser App) History:
    # Web Search Keyword Logs:




