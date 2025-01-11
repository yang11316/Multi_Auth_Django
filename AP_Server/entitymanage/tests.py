import time
import json
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class ApiTest(TestCase):
    """
    Test the API:
    cd AP_Server
    python3 manage.py test --keepdb
    """

    def setUp(self):
        # mock从AS接收的认证参数
        self.add_data = {
            "software_id": "90bf038d8e7bfb860ee4f8ae3704c8cb",
            "user_id": "ded740c908a0879769d8b63ba7b3e0cb",
            "entity_ip": "192.168.3.17",
            "software_hash": "58149a63232a1385df16c3557236ff0c",
            "acc_cur": "97c86d58d268e005cd20271e8ddf52b47cecc1f9030d75c9525c37d409f4de8c384bf274e88a7f9ec020be5b978eabfd7cc601d9b7c2284ceb03b75e9899bc60",
            "entity_pair": [
                {
                    "entity_pid": "fc85c32a5e8a5ccded2b2385987a5623",
                    "entity_parcialkey": "8ed2e9229f418c5f09694bba58a820d46e648b4a35539704782ff6b7f4051e620ef8528fbb18074e13d3b0b20fc6bfe677a2b0049bd14524fb2b1c8a1c4718d6",
                }
            ],
            "aux": "fc85c32a5e8a5ccded2b2385987a5623",
        }
        self.delete_data = {
            "aux_data": {
                "aux": "5f367f7766f1952d2ca0ef5db307dff266f3de71ea3b42e58f069b053b58f5c34b3aa5a3e0b134479e41fd78aa10bf19427501c38942bb5df335b1d28d499b57",
                "acc_cur": "8ed2e9229f418c5f09694bba58a820d46e648b4a35539704782ff6b7f4051e620ef8528fbb18074e13d3b0b20fc6bfe677a2b0049bd14524fb2b1c8a1c4718d6",
                "withdraw_pid": "853e9ff326b0cf2c275acab32776dfe7",
            }
        }
        # csrf_client = Client(enforce_csrf_checks=True)
        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0")
        # 发json，走HTTP短连接
        self.header = {"Connection": "close"}

    def test_get_entity(self):
        url = reverse("get-entity")

        start_time = time.time()
        response = self.client.post(url, data=json.dumps(self.add_data), content_type="application/json", headers=self.header)
        end_time = time.time()
        time_use = end_time - start_time

        print(f"AP接收更新凭证后的计算耗时: {time_use} 秒")
        print(response.json())
        self.assertEqual(response.json().get("status"), "success")

    def test_get_aux_data(self):
        # 对应urls.py
        url = reverse("get-aux-data")

        start_time = time.time()
        response = self.client.post(url, data=json.dumps(self.delete_data), content_type="application/json", headers=self.header)
        end_time = time.time()
        time_use = end_time - start_time

        print(f"AP接收更新凭证后的计算耗时: {time_use} 秒")
        print(response.json())
        self.assertEqual(response.json().get("status"), "success")
