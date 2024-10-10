from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

import config


# 用户资质申请
def test_register(driver, wait, user):
    username = user[0]
    password = user[1]

    # 打开登录页面
    login_url = f"http://{config.test_ip}:{config.test_port}/#/login"
    if driver.current_url != login_url:
        driver.get(login_url)
    driver.refresh()

    # 点击注册
    register_abbr = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[1]/form/div[4]/a/span")
        )
    )
    register_abbr.click()

    # 等待并输入用户名和密码
    username_field = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".info-drawer__content .el-form-item:nth-of-type(1) input",
            )
        )
    )
    username_field.send_keys(username)
    password_field = driver.find_element(
        By.CSS_SELECTOR,
        ".info-drawer__content .el-form-item:nth-of-type(2) input",
    )
    password_field.send_keys(password)
    repeat_password_field = driver.find_element(
        By.CSS_SELECTOR,
        ".info-drawer__content .el-form-item:nth-of-type(3) input",
    )
    repeat_password_field.send_keys(password)

    # 预先获取注册按钮
    register_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[1]/div/div[2]/div/div/div/section/div/div/button[2]",
            )
        )
    )

    try:
        # 点击提交
        register_button.click()
        confirm_button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")
            )
        )

        start_time = time.time()
        # 提交用户申请
        confirm_button.click()
        end_time = time.time()
        response_time = end_time - start_time
        print(f"用户资质申请API - 响应时间: {response_time:.2f} 秒")

        try:
            config.getMsg(wait)
        except Exception as e:
            print("消息加载失败:", e)

    except Exception as e:
        print("注册失败或页面未正确加载:", e)


# 用户登录
def test_login(driver, wait, user):
    username = user[0]
    password = user[1]

    # 打开登录页面
    login_url = f"http://{config.test_ip}:{config.test_port}/#/login"
    if driver.current_url != login_url:
        driver.get(login_url)
    driver.refresh()

    # 等待并输入用户名和密码
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.send_keys(username)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)

    # 预先获取登录按钮
    login_button = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div[1]/form/div[4]/button")
        )
    )

    try:
        start_time = time.time()
        login_button.click()
        end_time = time.time()
        response_time = end_time - start_time
        print(f"用户登录API - 响应时间: {response_time:.2f} 秒")

        main_url = f"http://{config.test_ip}:{config.test_port}/#/main"
        if driver.current_url != main_url:
            raise Exception("登录失败")

        # 输出首页标题
        print(driver.title)
        main_text_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[2]/section/div/div")
            )
        )
        # 输出首页的用户角色
        print(main_text_element.text)

    except Exception as e:
        print("页面未正确加载:", e)


# 用户信息查询
def test_info(driver, wait):
    # 打开用户信息页面
    user_info_url = f"http://{config.test_ip}:{config.test_port}/#/user/manage"
    if driver.current_url != user_info_url:
        start_time = time.time()
        driver.get(user_info_url)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"用户信息查询API - 响应时间: {response_time:.2f} 秒")
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
        print("用户信息查询失败或页面未正确加载:", e)


# 用户审批
def test_approve(driver, wait, isApproved):
    # 打开用户审批页面
    user_info_url = f"http://{config.test_ip}:{config.test_port}/#/user/review"
    if driver.current_url != user_info_url:
        driver.get(user_info_url)
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
                print(f"用户审批API - 响应时间: {response_time:.2f} 秒")
            else:
                button = last_cell.find_element(By.CSS_SELECTOR, ".el-button--danger")
                
                start_time = time.time()
                driver.execute_script("arguments[0].click();", button)
                end_time = time.time()
                response_time = end_time - start_time
                print(f"用户审批API - 响应时间: {response_time:.2f} 秒")

            try:
                config.getMsg(wait)
            except Exception as e:
                print("消息加载失败:", e)
        else:
            print("数据为空！")

    except Exception as e:
        print("用户审批失败或页面未正确加载:", e)


# 用户信息更新
def test_update(driver, wait, user):
    # 打开用户信息页面
    user_info_url = f"http://{config.test_ip}:{config.test_port}/#/user/manage"
    if driver.current_url != user_info_url:
        driver.get(user_info_url)
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

            # 输入新的用户信息
            username_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".info-drawer__content .el-form-item:nth-of-type(2) input",
                    )
                )
            )
            # 将input框预填的原内容清除
            username_field.clear()
            for c in user["user_name"]:
                username_field.send_keys(c)
                time.sleep(0.01)
            role_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".info-drawer__content .el-form-item:nth-of-type(3) input",
                    )
                )
            )
            role_field.clear()
            for c in user["user_role"]:
                role_field.send_keys(c)
                time.sleep(0.01)
            email_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".info-drawer__content .el-form-item:nth-of-type(4) input",
                    )
                )
            )
            email_field.clear()
            for c in user["user_email"]:
                email_field.send_keys(c)
                time.sleep(0.01)
            phone_field = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".info-drawer__content .el-form-item:nth-of-type(5) input",
                    )
                )
            )
            phone_field.clear()
            for c in user["user_phone"]:
                phone_field.send_keys(c)
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
            # 提交用户信息更新
            confirm_button.click()
            end_time = time.time()
            response_time = end_time - start_time
            print(f"用户信息更新API - 响应时间: {response_time:.2f} 秒")

            try:
                config.getMsg(wait)
            except Exception as e:
                print("消息加载失败:", e)

        else:
            print("数据为空！")

    except Exception as e:
        print("用户信息更新失败或页面未正确加载:", e)


# 用户删除
def test_delete(driver, wait):
    # 打开用户信息页面
    user_info_url = f"http://{config.test_ip}:{config.test_port}/#/user/manage"
    if driver.current_url != user_info_url:
        driver.get(user_info_url)
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
            # 处理最后一行条目，点击删除按钮
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
            # 点击删除
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
            print(f"用户删除API - 响应时间: {response_time:.2f} 秒")

            try:
                config.getMsg(wait)
            except Exception as e:
                print("消息加载失败:", e)

    except Exception as e:
        print("用户删除失败或页面未正确加载:", e)
