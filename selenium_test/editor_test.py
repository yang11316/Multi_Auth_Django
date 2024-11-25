from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time

import config
import user_manage, software_manage


class EditorTest:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.service = FirefoxService(executable_path=config.geckodriver_path)
        self.driver = webdriver.Firefox(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 600)

    def user_register(self, user):
        print(">>>>>开始 用户资质申请 测试<<<<<")
        user_manage.test_register(self.driver, self.wait, user)
        print("=====结束 用户资质申请 测试=====")

    def user_login(self, user):
        print(">>>>>开始 用户登录 测试<<<<<")
        user_manage.test_login(self.driver, self.wait, user)
        print("=====结束 用户登录 测试=====")

    def software_register(self, rsoftware):
        print(">>>>>开始 软件注册 测试<<<<<")
        software_manage.test_register(self.driver, self.wait, rsoftware)
        print("=====结束 软件注册 测试=====")

    def close_browser(self):
        self.driver.quit()


if __name__ == "__main__":
    test = EditorTest()

    user = ["Nav_Operator02", "user_pwd"]
    test.user_register(user)

    # 软件开发人员提交注册申请后，启动admin_test，通过该审批
    time.sleep(30)

    test.user_login(user)
    rsoftware = {
        "rsoftware_name": "测试软件1",
        "rsoftware_version": "v0.9.0",
        "rsoftware_desc": "这是一段测试软件1的描述",
        "entity_ip": "192.168.3.17",
    }
    test.software_register(rsoftware)
    
    test.close_browser()
