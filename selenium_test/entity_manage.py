from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

import config


# 实体信息查询
def test_info(driver, wait):
    # 打开实体信息页面
    entity_info_url = f"http://{config.test_ip}:{config.test_port}/#/entity/manage"
    if driver.current_url != entity_info_url:
        start_time = time.time()
        driver.get(entity_info_url)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"实体信息查询API - 响应时间: {response_time:.2f} 秒")
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
        print("实体信息查询失败或页面未正确加载:", e)

# 实体部分密钥下发
def test_distribute(driver, wait, software_name, ppk_count):
    # 打开实体管理页面
    entity_info_url = f"http://{config.test_ip}:{config.test_port}/#/entity/manage"
    if driver.current_url != entity_info_url:
        driver.get(entity_info_url)
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
        
        # 找到包含指定 software_name 的行
        target_row = None
        for row in rows:
            columns = row.find_elements(By.XPATH, ".//td")
            # 假设软件名在第3列
            if columns[2].text == software_name:
                target_row = row
                break

        if target_row:
            # 处理匹配的条目，点击下发按钮
            last_cell = target_row.find_elements(By.XPATH, ".//td")[-1]
            # 强制滚动到包含该按钮的父容器
            table_container = driver.find_element(By.CSS_SELECTOR, ".el-table")
            driver.execute_script(
                "arguments[0].scrollLeft = arguments[0].scrollWidth", table_container
            )
            button = last_cell.find_element(By.CSS_SELECTOR, ".el-button--success")
            driver.execute_script("arguments[0].click();", button)
            
            ppk_count_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div[2]/div[2]/div[1]/input",
                    )
                )
            )
            ppk_count_field.send_keys(ppk_count)

            confirm_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")
                )
            )

            start_time = time.time()
            # 提交
            confirm_button.click()
            try:
                config.getMsg(wait)
            except Exception as e:
                print("消息加载失败:", e)
                
            end_time = time.time()
            response_time = end_time - start_time
            print(f"实体部分密钥下发API - 响应时间: {response_time:.2f} 秒")
        else:
            print(f"未找到匹配的软件名：{software_name}")

    except Exception as e:
        print("实体部分密钥下发失败或页面未正确加载:", e)

# 实体部分密钥下发
# def test_distribute(driver, wait, software_name):
#     # 打开实体管理页面
#     entity_info_url = f"http://{config.test_ip}:{config.test_port}/#/entity/manage"
#     if driver.current_url != entity_info_url:
#         driver.get(entity_info_url)
#     driver.refresh()

#     try:
#         # 获取第1页的表格内容
#         header_element = wait.until(
#             EC.presence_of_element_located((By.CLASS_NAME, "el-table__header"))
#         )

#         header_columns = header_element.find_elements(By.XPATH, ".//th//div")
#         header_data = [col.text for col in header_columns]
#         print("表头:", header_data)

#         body_element = wait.until(
#             EC.presence_of_element_located((By.CLASS_NAME, "el-table__body"))
#         )
#         rows = body_element.find_elements(By.XPATH, ".//tbody/tr")
#         if len(rows) > 0:
#             # 处理最后一行条目，点击下发按钮
#             last_cell = rows[-1].find_elements(By.XPATH, ".//td")[-1]
#             # print(last_cell.get_attribute("innerHTML"))
#             # 由于操作按钮所在列为固定列，先强制滚动到包含该按钮的父容器
#             table_container = driver.find_element(By.CSS_SELECTOR, ".el-table")
#             driver.execute_script(
#                 "arguments[0].scrollLeft = arguments[0].scrollWidth", table_container
#             )
#             button = last_cell.find_element(By.CSS_SELECTOR, ".el-button--success")
#             driver.execute_script("arguments[0].click();", button)

#             confirm_button = wait.until(
#                 EC.presence_of_element_located(
#                     (By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")
#                 )
#             )

#             start_time = time.time()
#             # 提交
#             confirm_button.click()
#             end_time = time.time()
#             response_time = end_time - start_time
#             print(f"实体部分密钥下发API - 响应时间: {response_time:.2f} 秒")

#             try:
#                 config.getMsg(wait)
#             except Exception as e:
#                 print("消息加载失败:", e)
#         else:
#             print("数据为空！")

#     except Exception as e:
#         print("实体部分密钥下发失败或页面未正确加载:", e)


# 实体撤销
def test_withdraw(driver, wait):
    # 打开实体信息页面
    entity_info_url = f"http://{config.test_ip}:{config.test_port}/#/entity/manage"
    if driver.current_url != entity_info_url:
        driver.get(entity_info_url)
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
            # 处理最后一行条目，点击撤销按钮
            last_cell = rows[-1].find_elements(By.XPATH, ".//td")[-1]
            # print(last_cell.get_attribute("innerHTML"))
            # 由于操作按钮所在列为固定列，先强制滚动到包含该按钮的父容器
            table_container = driver.find_element(By.CSS_SELECTOR, ".el-table")
            driver.execute_script(
                "arguments[0].scrollLeft = arguments[0].scrollWidth", table_container
            )

            delete_button = last_cell.find_element(
                By.CSS_SELECTOR, ".el-button--danger"
            )
            # 点击撤销
            driver.execute_script("arguments[0].click();", delete_button)

            confirm_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")
                )
            )
            start_time = time.time()
            # 点击提交
            confirm_button.click()
            end_time = time.time()
            response_time = end_time - start_time
            print(f"实体撤销API - 响应时间: {response_time:.2f} 秒")

            try:
                config.getMsg(wait)
            except Exception as e:
                print("消息加载失败:", e)

    except Exception as e:
        print("实体撤销失败或页面未正确加载:", e)


# 存活实体更新
def test_alive(driver, wait):
    print("=====首次进入实体管理页面=====")
    test_info(driver, wait)

    # 启动或关闭一个部署实体
    time.sleep(30)

    print("=====更新后的实体管理页面=====")
    test_info(driver, wait)