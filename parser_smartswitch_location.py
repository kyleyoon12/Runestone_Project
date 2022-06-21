import json
import sqlite3
from tqdm import tqdm

def parse():
    path_to_file = "D:/Digital Forensics/16. 논문/6. Samsung_Apps/Visualization/Case/2/"

    location_first_file = "logging_location_log"
    with open(path_to_file + location_first_file, "r", encoding="UTF-8") as file:
        raw = file.readlines()
        log = json.loads(raw[0])
        records_location = log["records"] #type = list {"_id":57137,"latitude":37.58491134643555,"longitude":127.0269775390625,"altitude":59.5,"provider":"passive_network","accuracy":11.597999572753906,"bearing":0,"speed":0,"time":1649726511927,"time_string":"2022\/04\/12 10:21:51","timezone_id":"Asia\/Seoul","created_at":1649726511000}

    location_second_file = "logging_cpp_path_history_log"

    return records_location

def location_log(records_location):
    conn = sqlite3.connect("../Visualization/Case/2/result.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE location_log (id TEXT, latitude TEXT, longitude TEXT, altitude TEXT, provider TEXT, accuracy TEXT, bearing TEXT, speed TEXT, time TEXT, time_string TEXT, timezone_id TEXT, created_at TEXT)")


    for i in tqdm(range(len(records_location))):
        record = json.loads(records_location[i])
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

        cur.execute("INSERT INTO location_log VALUES(?,?,?,?,?,?,?,?,?,?,?,?);", (
        _id, latitude, longitude, altitude, provider, accuracy, bearing, speed, time, time_string, timezone_id,
        created_at))

    conn.commit()
    conn.close()


def main():
    records_location = parse()
    location_log(records_location)

if __name__ == '__main__':
    main()
