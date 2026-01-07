import time
import random
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class AutoClicker:
    """自动点击器，模拟人类点击行为"""

    def __init__(self, driver, config: dict):
        self.driver = driver
        self.min_delay = config.get('min_delay', 1.0)
        self.max_delay = config.get('max_delay', 3.0)
        self.max_retries = config.get('max_retries', 3)
        self.click_retry_delay = config.get('click_retry_delay', 1.0)
        self.implicit_wait = config.get('implicit_wait', 10)

        # 设置隐式等待时间
        self.driver.implicitly_wait(self.implicit_wait)

    def human_like_delay(self):
        """模拟人类随机延迟"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)

    def move_to_element(self, element):
        """模拟鼠标移动到元素"""
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element)
            actions.perform()
            time.sleep(random.uniform(0.3, 0.8))
        except Exception as e:
            print(f"鼠标移动失败: {e}")

    def click_with_retry(self, by: By, value: str, description: str = "") -> bool:
        """带重试机制的点击，模拟人类行为"""
        for attempt in range(self.max_retries):
            try:
                # 等待元素可见
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, value))
                )

                # 模拟鼠标移动
                self.move_to_element(element)

                # 随机延迟
                time.sleep(random.uniform(0.2, 0.5))

                # 点击
                element.click()
                print(f"✓ 点击成功: {description}")

                # 点击后的随机延迟
                self.human_like_delay()
                return True

            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                print(f"✗ 点击失败 (尝试 {attempt + 1}/{self.max_retries}): {description} - {str(e)}")

                if attempt < self.max_retries - 1:
                    # 尝试滚动到元素位置
                    try:
                        element = self.driver.find_element(by, value)
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                        time.sleep(self.click_retry_delay)
                    except:
                        time.sleep(self.click_retry_delay)

        return False

    def click_by_text(self, text: str, partial: bool = False, description: str = "") -> bool:
        """根据文本内容点击元素"""
        by = By.PARTIAL_LINK_TEXT if partial else By.LINK_TEXT
        return self.click_with_retry(by, text, description or text)

    def click_by_xpath(self, xpath: str, description: str = "") -> bool:
        """根据XPath点击元素"""
        return self.click_with_retry(By.XPATH, xpath, description or xpath)

    def click_by_css(self, css_selector: str, description: str = "") -> bool:
        """根据CSS选择器点击元素"""
        return self.click_with_retry(By.CSS_SELECTOR, css_selector, description or css_selector)

    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """等待元素出现"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            return None

    def wait_for_clickable(self, by: By, value: str, timeout: int = 10):
        """等待元素可点击"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        except TimeoutException:
            return None

    def scroll_down(self, amount: int = None):
        """滚动页面"""
        if amount:
            self.driver.execute_script(f"window.scrollBy(0, {amount});")
        else:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(0.5, 1.0))

    def go_back(self):
        """返回上一页"""
        self.driver.back()
        self.human_like_delay()
