from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time

import config
import user_manage, node_manage, software_manage, entity_manage


class AdminTest:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.service = FirefoxService(executable_path=config.geckodriver_path)
        self.driver = webdriver.Firefox(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 600)

    def user_login(self, user):
        print(">>>>>开始 用户登录 测试<<<<<")
        user_manage.test_login(self.driver, self.wait, user)
        print("=====结束 用户登录 测试=====")

    def user_info(self):
        print(">>>>>开始 用户信息查询 测试<<<<<")
        user_manage.test_info(self.driver, self.wait)
        print("=====结束 用户信息查询 测试=====")

    def user_approve(self, isApproved):
        print(">>>>>开始 用户审批 测试<<<<<")
        user_manage.test_approve(self.driver, self.wait, isApproved)
        print("=====结束 用户审批 测试=====")

    def user_update(self, user):
        print(">>>>>开始 用户信息更新 测试<<<<<")
        user_manage.test_update(self.driver, self.wait, user)
        print("=====结束 用户信息更新 测试=====")

    def user_delete(self):
        print(">>>>>开始 用户删除 测试<<<<<")
        user_manage.test_delete(self.driver, self.wait)
        print("=====结束 用户删除 测试=====")

    def node_info(self):
        print(">>>>>开始 节点信息查询 测试<<<<<")
        node_manage.test_info(self.driver, self.wait)
        print("=====结束 节点信息查询 测试=====")

    def node_update(self, user):
        print(">>>>>开始 节点信息更新 测试<<<<<")
        node_manage.test_update(self.driver, self.wait, node)
        print("=====结束 节点信息更新 测试=====")

    def software_approve(self, isApproved):
        print(">>>>>开始 软件审批 测试<<<<<")
        software_manage.test_approve(self.driver, self.wait, isApproved)
        print("=====结束 软件审批 测试=====")

    def software_info(self):
        print(">>>>>开始 软件信息查询 测试<<<<<")
        software_manage.test_info(self.driver, self.wait)
        print("=====结束 软件信息查询 测试=====")

    def software_update(self, software):
        print(">>>>>开始 软件信息更新 测试<<<<<")
        software_manage.test_update(self.driver, self.wait, software)
        print("=====结束 软件信息更新 测试=====")

    def entity_info(self):
        print(">>>>>开始 实体信息查询 测试<<<<<")
        entity_manage.test_info(self.driver, self.wait)
        print("=====结束 实体信息查询 测试=====")

    def entity_distribute(self, software_name, ppk_count):
        print(">>>>>开始 实体部分密钥下发 测试<<<<<")
        entity_manage.test_distribute(self.driver, self.wait, software_name, ppk_count)
        print("=====结束 实体部分密钥下发 测试=====")

    def entity_withdraw(self):
        print(">>>>>开始 实体撤销 测试<<<<<")
        entity_manage.test_withdraw(self.driver, self.wait)
        print("=====结束 实体撤销 测试=====")

    def entity_update(self):
        print(">>>>>开始 存活实体更新 测试<<<<<")
        entity_manage.test_alive(self.driver, self.wait)
        print("=====结束 存活实体更新 测试=====")

    def close_browser(self):
        self.driver.quit()


if __name__ == "__main__":
    test = AdminTest()

    # 用户管理
    user = ["Plant_Manager", "user_pwd"]
    test.user_login(user)
    test.user_info()
    user_is_approved = True
    test.user_approve(user_is_approved)

    editor = {
        "user_name": "Nav_Operator02",
        "user_role": "editor",
        "user_phone": "15099783222",
        "user_email": "NavOperator02@nav.com",
    }
    test.user_update(editor)
    # test.user_delete()

    # 节点管理
    test.node_info()
    node = {
        "node_id": "node_id",
        "node_ip": "192.168.3.17",
        "node_desc": "这是一段测试使用AP的描述",
    }
    test.node_update(node)

    # 等待用户提交软件注册申请
    time.sleep(30)

    # 软件管理
    software_is_approved = True
    test.software_approve(software_is_approved)
    test.software_info()

    software = {
        "software_name": "测试软件1",
        "software_version": "v0.9.1",
        "software_desc": "这是一段测试软件1的新描述",
    }
    test.software_update(software)

    # 实体管理
    test.entity_info()
    software_name = "Process1"
    ppk_count = 10
    test.entity_distribute(software_name, ppk_count)

    # 此时可将对应软件放到file_upload，测试互认证
    time.sleep(60)

    test.entity_withdraw()

    test.entity_update()

    test.close_browser()
