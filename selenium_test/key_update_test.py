from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import threading
import time

import admin_test, editor_test


def run_admin(admin_user, rsoftware_name, rsoftware_total, ppk_count):
    # 给mysql写入数据留出时间，可适当缩短，后同
    time.sleep(5)
    print("********** Admin线程开始执行 **********")
    admin.user_login(admin_user)

    admin.user_approve(True)
    user_approval.set()

    print("Admin等待Editor注册软件...")
    software_approval.wait()
    time.sleep(5)

    print("Admin继续执行后续操作: ")
    # 注意：这里需要预先将打包的process放到/home/default/file_upload目录下
    for i in range(1, rsoftware_total + 1):
        admin.software_approve(True)

    for i in range(1, rsoftware_total + 1):
        time.sleep(10)
        admin.entity_distribute(f"{rsoftware_name}{i}", ppk_count)

    admin.close_browser()
    print("********** Admin线程执行完成 **********")


def run_editor(editor_user, rsoftware_name, rsoftware_total, entity_ip):
    print("********** Editor线程开始执行 **********")
    editor.user_register(editor_user)

    print("Editor等待Admin审核...")
    user_approval.wait()

    print("Editor继续执行后续操作: ")
    editor.user_login(editor_user)
    for i in range(1, rsoftware_total + 1):
        rsoftware = {
            "rsoftware_name": f"{rsoftware_name}{i}",
            "rsoftware_version": "1.0.0",
            "rsoftware_desc": f"这是一段测试软件{i}的描述",
            "entity_ip": entity_ip,
        }
        editor.software_register(rsoftware)
    software_approval.set()

    editor.close_browser()
    print("********** Editor线程执行完成 **********")


if __name__ == "__main__":
    admin = admin_test.AdminTest()
    editor = editor_test.EditorTest()

    user_approval = threading.Event()
    software_approval = threading.Event()

    # 指定mysql预置的管理员账密，以及要注册的新软件开发人员账密
    admin_user = ["Plant_Manager", "user_pwd"]
    editor_user = ["Test_Operator", "user_pwd"]
    # 指定需要注册的软件总数
    rsoftware_name = "密钥更新测试软件"
    rsoftware_total = 5
    # 指定部署AP的IP
    entity_ip = "192.168.3.17"
    # 指定需下发的部分密钥数目
    ppk_count = 2

    admin_thread = threading.Thread(
        target=run_admin, args=(admin_user, rsoftware_name, rsoftware_total, ppk_count)
    )
    editor_thread = threading.Thread(
        target=run_editor,
        args=(editor_user, rsoftware_name, rsoftware_total, entity_ip),
    )

    editor_thread.start()
    admin_thread.start()

    editor_thread.join()
    admin_thread.join()
