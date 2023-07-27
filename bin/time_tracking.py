import time

time_intervals_list = []

rate_of_change = 0

def calculate_changes():
    global rate_of_change, time_intervals_list

    if len(time_intervals_list) == 12:
        time_intervals_list.pop(0)

    time_intervals_list.append(rate_of_change)

    if rate_of_change > 0:
        rate_of_change = 0

    result = sum(time_intervals_list)

    print(f'List: {time_intervals_list}')

    return result

def increase_checkin_by_one():
    global rate_of_change

    rate_of_change += 1

def execute():
    while True:
        time.sleep(5)
        calculate_changes()

