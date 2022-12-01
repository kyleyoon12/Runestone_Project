import os

class Mode:
    def mode_select(self):
        print("""
        <Select Mode>
        1. Log files deecryption
        2. Parse log files
        3. Location Tracker (Make Sure the "Result.db" is ready)  
        4. Terminate         
        """)

        mode_one = int(input("[System] >>> Input number: "))

        if mode_one == 1:
            task = "decrypt"

            return mode_one, task

        if mode_one == 2:

            print("""
            <Select the source file to parse>
            1. Manufacturer
            2. SmartSwitch
            """)

            mode_two = int(input("[System] >>> Input number: "))
            task = "parse"

            return mode_two, task

        if mode_one == 3:
            print("""
            <Select Functions>
            1. Location Tracker
            2. (T.B.A)
            """)

            mode_functions = int(input("[System] >>> Input number:"))

            if mode_functions == 1:
                return mode_one, mode_functions

            # if mode_functions == 2:
            #     return mode_one, mode_functions

        if mode_one == 4:
            print("[System] >>> Terminated")
            dummy = "1"

            return mode_one, dummy