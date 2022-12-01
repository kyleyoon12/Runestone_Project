import datetime, time

def make_local(raw):
    replaced = raw.replace(" +0000", "")
    original_format = "%Y-%m-%d %H:%M:%S"
    struct = datetime.datetime.strptime(replaced, original_format)
    add_hours = datetime.timedelta(hours=9)
    local_struct = struct + add_hours
    final_format = "%Y/%m/%d %H:%M:%S"
    converted = datetime.datetime.strftime(local_struct, final_format)

    return converted

def to_local_time(raw):
    time = raw/1000
    time_formatted = datetime.datetime.fromtimestamp(time).strftime("%Y/%m/%d %H:%M:%S")

    return time_formatted