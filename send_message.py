import os
import time

from api import *
from os import getenv
from dotenv import find_dotenv, load_dotenv
import datetime

print("start")

load_dotenv(find_dotenv(), verbose=True)
# print(os.getenv("LARK_HOST"))
test = Client(os.getenv("LARK_HOST"))
Token = test.get_app_access_token(os.getenv("APP_ID"), os.getenv("APP_SECRET"))
List = test.get_data_list(app_token="bascno69957RY8XosYuC5llpRFc", table_id='tblzPs7ery9n6uwl',
                          tenant_access_token=Token)
bir_user = []
now_time = datetime.datetime.now()
for each_time in List:
    print("start")
    month = int(time.strftime('%m', time.localtime(each_time["fields"]["生日"] / 1000)))
    day = int(time.strftime('%d', time.localtime(each_time["fields"]["生日"] / 1000)))
    if now_time.month == month and now_time.day == day:
        bir_user.append(each_time["fields"]["姓名"])
item = test.get_detail_group(tenant_access_token=Token)
chat_id = " "
for each_group in item:
    if each_group["name"] == "生日":
        chat_id = each_group["chat_id"]
        break
members = test.get_user_id(tenant_access_token=Token, chat_id=chat_id)
user_id = []
for each_member in members:
    if each_member['name'] in bir_user:
        user_id.append(each_member['member_id'])
for name, each_id in zip(bir_user, user_id):
    print(name, each_id, '\n')

for (name, each_id) in zip(bir_user, user_id):
    print("start")
    test.send_bir_message(tenant_access_token=Token, chat_id=chat_id, user_id=each_id, user_name=name)


# flag = test.send_bir_message(tenant_access_token=Token, chat_id=item[0]["chat_id"], user_id=user_id)
