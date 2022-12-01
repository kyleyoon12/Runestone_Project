import os

class Path:
    def create_result_db_path(self):
        self.case_name = input("[System] >>> Input Case Name:")
        if not os.path.exists("../Result/DB/%s" % self.case_name):
            os.mkdir("../Result/DB/%s" % self.case_name)

        else:
            print("[System] >>> Folder with the same name already exist!")
            #print("[System] >>> Failed to create a folder. Please check the name!")

    def create_result_vis_path(self):
        self.case_name = input("[System] >>> Input Case Name:")
        if not os.path.exists("../Result/Location_Tracker/%s" % self.case_name):
            os.mkdir("../Result/Location_Tracker/%s" % self.case_name)

        else:
            print("[System] >>> Folder with the same name already exist!")
            #print("[System] >>> Failed to create a folder. Please check the name!")

    def ma_source_file_path(self):
        path_to_file = input("[System] >>> Input the path:")
        #path_to_file = "../Image/Manufacturer_Provided/JW/Customization_Service_collected_data_jw_220622.txt" - 최초
        #path_to_file = "../Image/Manufacturer_Provided/KY_fold2/Customization_Service_collected_data2_fold2_220618.txt"

        return path_to_file

    def sm_source_file_path(self):
        path_to_file = input("[System] >>> Input the path:")
        #path_to_file = "../Image/SmartSwitch/JW/20220512/"
        #path_to_file = "../Image/SmartSwitch/KY/20220522/"

        return path_to_file



    def result_db_path(self):
        path_to_result_db = "../Result/DB/%s/result.db" % self.case_name

        return path_to_result_db

    def path_to_visualization(self):
        path_to_vis = "../Result/Location_Tracker/%s/location_tracker.html" % self.case_name
        #path_to_vis = "../Result/DB/%s/result.db" % self.case_name

        return path_to_vis