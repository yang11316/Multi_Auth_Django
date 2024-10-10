from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

import config


# 节点信息查询
def test_info(driver, wait):
    # 打开节点信息页面
    node_info_url = f"http://{config.test_ip}:{config.test_port}/#/node/manage"
    if driver.current_url != node_info_url:
        start_time = time.time()
        driver.get(node_info_url)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"节点信息查询API - 响应时间: {response_time:.2f} 秒")
    driver.refresh()

    try:
        # 获取第1页的表格内容
        header_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "el-table__header"))
        )

        header_columns = header_element.find_elements(By.XPATH, ".//th//div")
        header_data = [col.text for col in header_columns]
        print("表头:", header_data)

        body_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "el-table__body"))
        )
        rows = body_element.find_elements(By.XPATH, ".//tbody/tr")
        for i, row in enumerate(rows):
            cells = row.find_elements(By.XPATH, ".//td//div")
            cell_data = [cell.text for cell in cells]
            print(f"第{i + 1}行: {cell_data}")

        # 获取当前条目总数
        count_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "el-pagination__total"))
        )
        print(f"当前条目总数: {count_element.text}")

    except Exception as e:
        print("节点信息查询失败或页面未正确加载:", e)


# 节点信息更新
def test_update(driver, wait, node):
    # 打开节点信息页面
    node_info_url = f"http://{config.test_ip}:{config.test_port}/#/node/manage"
    if driver.current_url != node_info_url:
        driver.get(node_info_url)
    driver.refresh()

    try:
        # 获取第1页的表格内容
        header_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "el-table__header"))
        )

        header_columns = header_element.find_elements(By.XPATH, ".//th//div")
        header_data = [col.text for col in header_columns]
        print("表头:", header_data)

        body_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "el-table__body"))
        )
        rows = body_element.find_elements(By.XPATH, ".//tbody/tr")
        if len(rows) > 0:
            # 处理最后一行条目，点击编辑按钮
            last_cell = rows[-1].find_elements(By.XPATH, ".//td")[-1]
            # print(last_cell.get_attribute("innerHTML"))
            # 由于操作按钮所在列为固定列，先强制滚动到包含该按钮的父容器
            table_container = driver.find_element(By.CSS_SELECTOR, ".el-table")
            driver.execute_script(
                "arguments[0].scrollLeft = arguments[0].scrollWidth", table_container
            )

            button = last_cell.find_element(By.CSS_SELECTOR, ".el-button--primary")
            driver.execute_script("arguments[0].click();", button)

            # 输入新的节点信息
            desc_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".info-drawer__content .el-form-item:nth-of-type(3) textarea",
                    )
                )
            )
            # 将input框预填的原内容清除
            desc_field.clear()
            for c in node["node_desc"]:
                desc_field.send_keys(c)
                time.sleep(0.01)
            # 预先获取更新按钮
            update_button = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div[2]/section/div/div/div[2]/div/div/section/div/div/button[2]",
                    )
                )
            )

            # 点击更新
            update_button.click()
            confirm_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")
                )
            )

            start_time = time.time()
            # 提交节点信息更新
            confirm_button.click()
            end_time = time.time()
            response_time = end_time - start_time
            print(f"节点信息更新API - 响应时间: {response_time:.2f} 秒")

            try:
                config.getMsg(wait)
            except Exception as e:
                print("消息加载失败:", e)

        else:
            print("数据为空！")

    except Exception as e:
        print("节点信息更新失败或页面未正确加载:", e)
