from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

"""
    版本及对应关系
    firefox: 130.0.1
    geckodriver: 0.35.0
    selenium: 4.24.0

    全局配置，根据测试环境修改
    test_ip: 指定测试IP
    test_port: 指定前端端口
    geckodriver_path: 指定驱动位置
"""

test_ip = "localhost"
test_port = 9528
geckodriver_path = "/snap/bin/geckodriver"

# 用于从vue的el-message中读取回显的对应消息
def getMsg(wait):
    msg_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".el-message"))
    )
    message_text = msg_element.text
    message_class = msg_element.get_attribute("class")

    if "el-message--success" in message_class:
        message_type = "Success"
    elif "el-message--error" in message_class:
        message_type = "Error"
    elif "el-message--warning" in message_class:
        message_type = "Warning"
    elif "el-message--info" in message_class:
        message_type = "Info"
    else:
        message_type = "Unknown"

    print(f"{message_type}: {message_text}")
