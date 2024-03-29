import time
import datetime

def check_user_in_chat(username, group_to_users):
    chat_num = 0
    for key in group_to_users:
        if username in group_to_users[key]:
            chat_num = int(key)
    return chat_num

def get_timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    return st