import pandas as pd
import json
from os import path, remove

PROCESSED_FILE_NAME = './clustered_data.csv'
POST_PROCESSED_FILE_NAME = './post_processed_data.csv'
JSON_FILE_NAME = './dictionaries.json'

TYPE_MAP = {
    'view': 0,
    'cart': 1,
    'purchase': 2,
    'remove_from_cart': 3
}

processed_data = pd.read_csv(PROCESSED_FILE_NAME).head(n=10)
data_columns = [
    # 'event_time',
    'event_type',
    'product_id',
    'category_id',
    'brand',
    'price', 
    'user_id', 
    'user_session',
    'cluster'
]

def get_key(val, my_dict): 
    for key, value in my_dict.items(): 
         if val == value: 
             return key 
  
    return "key doesn't exist"

if path.exists(POST_PROCESSED_FILE_NAME):
    remove(POST_PROCESSED_FILE_NAME)

with open(JSON_FILE_NAME, 'r') as fp:
    dictionaries = json.load(fp)

df_columns = pd.DataFrame(columns=data_columns)
df_columns.to_csv(POST_PROCESSED_FILE_NAME, mode='a', header=True, index=False)

BATCH_SIZE = 5
counter = 0
cnt_2 = 1
record_count = processed_data.shape[0]
new_data = []

def get_event_time(day, hour):
    return f'2019-11-{int(day)} {int(hour)}:0:0 UTC'

for index, row in processed_data.iterrows():
    counter = counter + 1
    obj = {
        'event_time': get_event_time(row["day"], row["hour"]),
        'event_type': get_key(row["event_type"], TYPE_MAP),
        'product_id': get_key(row["product_id"], dictionaries["product_map"]),
        'category_id': get_key(row["category_id"], dictionaries["category_map"]),
        'category_code': get_key(row["category_id"], dictionaries["category_map"]),
        'brand': get_key(row["brand"], dictionaries["brand_map"]),
        'price': row["price"],
        'user_id': get_key(row["user_id"], dictionaries["user_map"]),
        'user_session': get_key(row["user_session"],dictionaries["session_map"]),
        "cluster": int(row["cluster"])
    }

    new_data.append(obj)
    if counter == BATCH_SIZE:
        print('Status ', (round((cnt_2 * BATCH_SIZE)/record_count * 100,2)), ' %')
        cnt_2 = cnt_2 + 1
        counter = 0
        df2 = pd.DataFrame(new_data)
        new_data = []
        df2.to_csv(POST_PROCESSED_FILE_NAME, mode='a', header=False, index=False)
