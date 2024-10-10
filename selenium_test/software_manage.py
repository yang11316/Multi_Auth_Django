from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

import config


# 软件注册
def test_register(driver, wait, rsoftware):
    # 打开软件注册页面
    register_url = f"http://{config.test_ip}:{config.test_port}/#/sw/register"
    if driver.current_url != register_url:
        driver.get(register_url)
    driver.refresh()

    # 等待并输入软件名称、软件版本号、软件描述、部署实体IP
    rsoftware_name_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div/div/div[1]/div/input",
            )
        )
    )
    for c in rsoftware["rsoftware_name"]:
        rsoftware_name_field.send_keys(c)
        time.sleep(0.01)

    rsoftware_version_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/section/div/form/div[1]/div/div/div[2]/div/input",
            )
        )
    )
    for c in rsoftware["rsoftware_version"]:
        rsoftware_version_field.send_keys(c)
        time.sleep(0.01)

    rsoftware_desc_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/section/div/form/div[2]/div/div/div/div/input",
            )
        )
    )
    for c in rsoftware["rsoftware_desc"]:
        rsoftware_desc_field.send_keys(c)
        time.sleep(0.01)

    entity_ip_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/section/div/form/div[3]/div/div[1]/div[3]/table/tbody/tr/td/div/div/input",
            )
        )
    )
    for c in rsoftware["entity_ip"]:
        entity_ip_field.send_keys(c)
        time.sleep(0.01)

    # 预先获取注册按钮
    register_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/section/div/form/div[3]/div/div[2]/div/button[1]",
            )
        )
    )

    try:
        start_time = time.time()
        # 提交软件注册申请
        register_button.click()
        end_time = time.time()
        response_time = end_time - start_time
        print(f"软件注册API - 响应时间: {response_time:.2f} 秒")

        try:
            config.getMsg(wait)
        except Exception as e:
            print("消息加载失败:", e)

    except Exception as e:
        print("注册失败或页面未正确加载:", e)


# 软件审批
def test_approve(driver, wait, isApproved):
    # 打开软件审批页面
    software_info_url = f"http://{config.test_ip}:{config.test_port}/#/software/review"
    if driver.current_url != software_info_url:
        driver.get(software_info_url)
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
            # 处理最后一行条目，点击审批通过按钮
            last_cell = rows[-1].find_elements(By.XPATH, ".//td")[-1]
            # print(last_cell.get_attribute("innerHTML"))
            # 由于操作按钮所在列为固定列，先强制滚动到包含该按钮的父容器
            table_container = driver.find_element(By.CSS_SELECTOR, ".el-table")
            driver.execute_script(
                "arguments[0].scrollLeft = arguments[0].scrollWidth", table_container
            )
            if isApproved:
                button = last_cell.find_element(By.CSS_SELECTOR, ".el-button--success")

                start_time = time.time()
                driver.execute_script("arguments[0].click();", button)
                end_time = time.time()
                response_time = end_time - start_time
                print(f"软件审批API - 响应时间: {response_time:.2f} 秒")
            else:
                button = last_cell.find_element(By.CSS_SELECTOR, ".el-button--danger")

                start_time = time.time()
                driver.execute_script("arguments[0].click();", button)
                end_time = time.time()
                response_time = end_time - start_time
                print(f"软件审批API - 响应时间: {response_time:.2f} 秒")

            try:
                config.getMsg(wait)
            except Exception as e:
                print("消息加载失败:", e)
        else:
            print("数据为空！")

    except Exception as e:
        print("软件审批失败或页面未正确加载:", e)


# 软件信息查询
def test_info(driver, wait):
    # 打开软件信息页面
    software_info_url = f"http://{config.test_ip}:{config.test_port}/#/software/manage"
    if driver.current_url != software_info_url:
        start_time = time.time()
        driver.get(software_info_url)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"软件信息查询API - 响应时间: {response_time:.2f} 秒")
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
        print("软件信息查询失败或页面未正确加载:", e)


# 软件信息更新
def test_update(driver, wait, software):
    # 打开软件信息页面
    software_info_url = f"http://{config.test_ip}:{config.test_port}/#/software/manage"
    if driver.current_url != software_info_url:
        driver.get(software_info_url)
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
            # 处理第一行条目，点击编辑按钮
            last_cell = rows[0].find_elements(By.XPATH, ".//td")[-1]
            # print(last_cell.get_attribute("innerHTML"))
            # 由于操作按钮所在列为固定列，先强制滚动到包含该按钮的父容器
            table_container = driver.find_element(By.CSS_SELECTOR, ".el-table")
            driver.execute_script(
                "arguments[0].scrollLeft = arguments[0].scrollWidth", table_container
            )

            button = last_cell.find_element(By.CSS_SELECTOR, ".el-button--primary")
            driver.execute_script("arguments[0].click();", button)

            # 输入新的
            software_version_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".info-drawer__content .el-form-item:nth-of-type(2) input",
                    )
                )
            )
            software_version_field.clear()
            for c in software["software_version"]:
                software_version_field.send_keys(c)
                time.sleep(0.01)
            # 输入新的
            software_name_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".info-drawer__content .el-form-item:nth-of-type(4) input",
                    )
                )
            )
            software_name_field.clear()
            for c in software["software_name"]:
                software_name_field.send_keys(c)
                time.sleep(0.01)
            # 输入新的软件信息
            software_desc_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".info-drawer__content .el-form-item:nth-of-type(6) textarea",
                    )
                )
            )
            software_desc_field.clear()
            for c in software["software_desc"]:
                software_desc_field.send_keys(c)
                time.sleep(0.01)
            # 预先获取更新按钮
            update_button = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div[2]/section/div/div/div[3]/div/div/section/div/div/button[2]",
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
            # 提交软件信息更新
            confirm_button.click()
            end_time = time.time()
            response_time = end_time - start_time
            print(f"软件信息更新API - 响应时间: {response_time:.2f} 秒")

            try:
                config.getMsg(wait)
            except Exception as e:
                print("消息加载失败:", e)

        else:
            print("数据为空！")

    except Exception as e:
        print("软件信息更新失败或页面未正确加载:", e)
