from Cryptodome.Cipher import AES
import codecs
import hashlib

class Decryption:
    def setting(self):
        path_to_raw = input("[System] >>> Input the path to raw file to decrypt:")
        dummy_value = input("[System] >>> Input the dummy value:")
        path_to_decrypted = input("[System] >>> Input the path to save the decrypted file:")

        logs = {
            "all_bluetooth_dictionary": "/logging_all_bluetooth_dictionary",
            "all_bluetooth_log": "/logging_all_bluetooth_log",
            "app_usage": "/logging_app_usage",
            "bluetooth_device_dictionary": "/logging_bluetooth_device_dictionary",
            "bluetooth_log": "/logging_bluetooth_log",
            "charging_log": "/logging_charging_log",
            "country_app_count": "/logging_country_app_count",
            "cpp_path_history_log": "/logging_cpp_path_history_log",
            "headset_log": "/logging_headset_log",
            "location_log": "/logging_location_log",
            "motion_log": "/logging_motion_log",
            "music_playback_log": "/logging_music_playback_log",
            "screen_log": "/logging_screen_log",
            "screen_state_log": "/logging_screen_state_log",
            "search_keyword_log": "/logging_search_keyword_log",
            "setting_change": "/logging_setting_change",
            "web_info": "/logging_web_info",
            "web_log": "/logging_web_log",
            "wifi_connection_log": "/logging_wifi_connection_log",
            "monitoring_country_info": "/monitoring_country_info",
            "monitoring_current_place_log": "/monitoring_current_place_log",
            "monitoring_tpo_context_event": "/monitoring_tpo_context_event"
        }

        def decryption(logfile_name, path_to_raw, path_to_decrypted, dummy_value):
            key = '0b1e96db05d64ea4'  # Fixed String Key
            # AES Decrypt - dummy value
            #dummy_value = input("[System] >>> Input dummy value: ")
            bytesStr = codecs.decode(dummy_value, 'hex_codec')

            decipher = AES.new(key.encode(), AES.MODE_ECB)
            V = decipher.decrypt(bytesStr)
            # print("V:", V)
            V = V.rstrip(b'\x00')
            # print("V: ", V)

            DK = hashlib.sha256(V).hexdigest()
            # print("DK: ",DK)

            # Alg.6 Key generation (16 bytes)
            Key = DK[0:32]
            # print("Key: ",bytearray.fromhex(Key))

            # IV
            with open(path_to_raw + logfile_name, "rb") as file:
                IV = file.read()[:16]

            with open(path_to_raw + logfile_name, "rb") as file:
                C = file.read()[16:]

                # AES-CBC-PKCS Decrypt
                decipher2 = AES.new(bytearray.fromhex(Key), AES.MODE_CBC, IV)
                output_value = decipher2.decrypt(C)


                output = open(path_to_decrypted + logfile_name, "wb")
                # outputdb = open('test2.db', 'wb')
                output.write(output_value)

        for i in range(len(logs)):
            decryption(logs["all_bluetooth_dictionary"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["all_bluetooth_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["app_usage"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["bluetooth_device_dictionary"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["bluetooth_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["charging_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["country_app_count"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["cpp_path_history_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["headset_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["location_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["motion_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["music_playback_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["screen_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["screen_state_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["search_keyword_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["setting_change"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["web_info"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["web_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["wifi_connection_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["monitoring_country_info"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["monitoring_current_place_log"], path_to_raw, path_to_decrypted, dummy_value)
            decryption(logs["monitoring_tpo_context_event"], path_to_raw, path_to_decrypted, dummy_value)

        print("[System] >>> Decryption Finished")

    def decryption(self, logfile_name, path_to_raw, path_to_decrypted):
        key = '0b1e96db05d64ea4' #Fixed String Key
        #AES Decrypt - dummy value
        dummy_value = input("[System] >>> Input dummy value: ")
        bytesStr = codecs.decode(dummy_value, 'hex_codec')
        #print(type(bytesStr))
        #print("Byte String: ",bytesStr)
        # print(msg.hex())  #암호 텍스트를 16진수 표현으로 변환

        decipher = AES.new(key.encode(), AES.MODE_ECB)
        V = decipher.decrypt(bytesStr)
        #print("V:", V)
        V = V.rstrip(b'\x00')
        #print("V: ", V)

        DK = hashlib.sha256(V).hexdigest()
        #print("DK: ",DK)

        #Alg.6 Key generation (16 bytes)
        Key = DK[0:32]
        #print("Key: ",bytearray.fromhex(Key))

        #IV
        with open(path_to_raw + logfile_name, "rb") as file:
            IV = file.read()[:16]

        with open(path_to_raw + logfile_name, "rb") as file:
            C = file.read()[16:]

        # f = open('logging_location_log', 'rb')
        # #f = open('backup.db', 'rb') # Open encrypted file
        # IV = f.read()[:16]
        # #print("IV: ",IV)

        #C
        # f = open('logging_location_log', 'rb') # Open encrypted file
        # C = f.read()[16:]


        #AES-CBC-PKCS Decrypt

            decipher2 = AES.new(bytearray.fromhex(Key), AES.MODE_CBC, IV)
            output_value = decipher2.decrypt(C)

        # print(C.hex())
        # print(output_value.hex())

            output = open(path_to_decrypted + logfile_name, "wb")
            #outputdb = open('test2.db', 'wb')
            output.write(output_value)