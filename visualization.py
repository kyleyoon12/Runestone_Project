import sqlite3

conn = sqlite3.connect("../Case/1/result.db")
cur = conn.cursor()
cur.execute("SELECT latitude, longitude, time_string FROM location_log") #ALL
#cur.execute("SELECT latitude, longitude, time_string FROM location_log where time_string like '2022/05/07%'") #Particular Day
rows = cur.fetchall()

log = []

for row in rows:
    if float(row[0]) != 0:
        log.append([float(row[0]), float(row[1]), '<div style="padding:5px;">%s</div>' % row[2]])

if len(log) < 4000:
    print(log)
    print("log")

else:
    result = []
    for i in range(0, len(log), 2):
        result.append(log[i])

    print(result)
    print("result")

