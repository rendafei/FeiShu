import os
from utils import request
import json
import requests


# APP_ID=cli_a253ba19ad78900b
# APP_SECRET=UlibhsrSZVUXx8xs2tNL7cDGvFOvGqpv

class Client(object):
    """初始化服务类，初始化时设立属性_host = .env 文件中的LARK_HOST"""

    def __init__(self, lark_host):
        self._host = lark_host

    """获取app_access_token"""

    def get_app_access_token(self, app_id, app_secret):
        url = self._host + 'auth/v3/app_access_token/internal'
        header = {
            "Content-type": "application/json;charset=utf-8",
        }
        data = {
            "app_id": app_id,
            "app_secret": app_secret,
        }
        res = requests.request('POST', url=url, params=data, headers=header)
        # resp = request('POST', url=url, headers=header, payload=data)
        resp = res.json()
        return resp['app_access_token']

    """获取 tenant_access_token"""

    def get_tenant_access_token(self, app_id, app_secret):
        url = self._host + 'auth/v3/tenant_access_token/internal'
        header = {
            "Context-type": "application/json;charset=utf-8",
        }
        data = {
            'app_id': app_id,
            'app_secret': app_secret,
        }
        res = requests.request('POST', url=url, params=data, headers=header)
        resp = res.json()
        return resp['tenant_access_token']

    """获取多维表格数据"""

    def get_data_list(self, app_token, tenant_access_token, table_id):
        url = self._host + f"bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size=20"
        header = {
            "Authorization": "Bearer " + tenant_access_token,
        }
        res = requests.request('GET', url=url, headers=header)
        resp = res.json()
        return resp["data"]["items"]

    """获取应用机器人所在群组信息"""

    def get_detail_group(self, tenant_access_token):
        url = self._host + "im/v1/chats"
        header = {
            "Authorization": "Bearer " + tenant_access_token,
        }
        req = requests.request("GET", url=url, headers=header)
        resp = req.json()
        return resp['data']['items']

    """获取群成员ID，用于@"""

    def get_user_id(self, tenant_access_token, chat_id):
        url = self._host + f"im/v1/chats/{chat_id}/members"
        header = {
            "Authorization": "Bearer " + tenant_access_token,
        }
        param = {
            "member_id_type": "user_id",
            "page_size": 100
        }
        req = requests.request("GET", url=url, params=param, headers=header)
        resp = req.json()
        return resp["data"]["items"]

    """发送生日祝福"""

    def send_bir_message(self, tenant_access_token, chat_id, user_id, user_name):
        url = self._host + "im/v1/messages"
        params = {"receive_id_type": "chat_id"}
        data = {
            'receive_id': chat_id,
            "content": "{\"text\":\"<at user_id=\\\" " + str(user_id) + " \\\">" + user_name + "</at> 生日快乐\"}",
            "msg_type": "text",
        }
        headers = {
            'Authorization': "Bearer " + tenant_access_token,
            "Context-type": "application/json;charset=utf-8",
        }
        req = requests.request("POST", url=url, params=params, headers=headers, data=data)
        resq = req.json()
        return resq["code"]
