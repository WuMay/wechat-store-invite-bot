#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信小店达人广场自动邀约机器人
"""

import json
import logging
import time
import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from auto_clicker import AutoClicker
from record_manager import RecordManager


class WechatStoreInviteBot:
    """微信小店达人广场邀约机器人"""

    def __init__(self, config_file: str = "config.json"):
        # 加载配置
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # 初始化记录管理器
        self.record_manager = RecordManager(self.config['record_file'])

        # 设置日志
        self._setup_logging()

        # 初始化浏览器
        self.driver = None
        self.clicker = None

    def _setup_logging(self):
        """设置日志"""
        log_file = self.config.get('log_file', 'bot.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def init_browser(self):
        """初始化浏览器"""
        chrome_options = Options()

        # 是否无头模式
        if self.config.get('headless', False):
            chrome_options.add_argument('--headless')

        # 优化浏览器设置
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # 设置用户代理，模拟真实浏览器
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # 初始化驱动
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # 设置页面加载超时
        self.driver.set_page_load_timeout(self.config.get('page_load_timeout', 30))

        # 初始化点击器
        self.clicker = AutoClicker(self.driver, self.config)

        self.logger.info("浏览器初始化成功")

    def navigate_to_talent_square(self, url: str):
        """导航到达人广场页面"""
        self.logger.info(f"正在导航到达人广场: {url}")
        self.driver.get(url)
        time.sleep(2)

    def invite_single_talent(self, talent_name: str, talent_id: str) -> bool:
        """邀约单个达人"""
        self.logger.info(f"开始邀约达人: {talent_name}")

        try:
            # 1. 点击详情按钮，跳转到达人详情页
            if not self.clicker.click_by_xpath(
                "//button[contains(text(), '详情')]",
                "详情按钮"
            ):
                self.logger.error(f"点击详情按钮失败: {talent_name}")
                return False

            # 2. 点击"邀请带货"按钮
            if not self.clicker.click_by_xpath(
                "//button[contains(text(), '邀请带货')]",
                "邀请带货按钮"
            ):
                self.logger.error(f"点击邀请带货按钮失败: {talent_name}")
                self.driver.back()
                return False

            # 3. 点击"添加上次邀约商品"
            if not self.clicker.click_by_xpath(
                "//button[contains(text(), '添加上次邀约商品')]",
                "添加上次邀约商品"
            ):
                self.logger.error(f"点击添加上次邀约商品失败: {talent_name}")
                # 尝试返回达人详情页
                self.driver.back()
                return False

            # 4. 点击确认按钮
            if not self.clicker.click_by_xpath(
                "//button[contains(text(), '确认')]",
                "确认按钮"
            ):
                self.logger.error(f"点击确认按钮失败: {talent_name}")
                self.driver.back()
                return False

            # 5. 点击发送邀约
            if not self.clicker.click_by_xpath(
                "//button[contains(text(), '发送邀约')]",
                "发送邀约按钮"
            ):
                self.logger.error(f"点击发送邀约失败: {talent_name}")
                self.driver.back()
                return False

            # 6. 关闭当前页面，返回达人广场
            self.driver.back()
            self.clicker.human_like_delay()

            # 7. 记录邀约成功
            self.record_manager.add_record(talent_id, talent_name, "success")
            self.logger.info(f"✓ 邀约成功: {talent_name}")

            return True

        except Exception as e:
            self.logger.error(f"邀约过程中发生异常: {talent_name} - {str(e)}")
            # 尝试返回达人广场
            self.driver.back()
            self.clicker.human_like_delay()
            self.record_manager.add_record(talent_id, talent_name, "failed")
            return False

    def process_current_page(self) -> int:
        """处理当前页面的所有达人"""
        self.logger.info("开始处理当前页面的达人")

        # 获取当前页面所有达人列表
        # 注意：这里需要根据实际的页面结构调整XPath或CSS选择器
        # 以下是示例代码，实际使用时需要调整

        talents = []
        try:
            # 假设每个达人项都有 class="talent-item"
            talent_elements = self.driver.find_elements(By.CLASS_NAME, "talent-item")

            for element in talent_elements:
                try:
                    # 获取达人名称（需要根据实际情况调整）
                    name_element = element.find_element(By.CLASS_NAME, "talent-name")
                    talent_name = name_element.text.strip()

                    # 获取达人ID（可以从URL或data属性中获取）
                    # 这里假设有一个data-id属性
                    talent_id = element.get_attribute("data-id") or talent_name

                    if not self.record_manager.is_invited(talent_id):
                        talents.append({
                            'name': talent_name,
                            'id': talent_id,
                            'element': element
                        })
                    else:
                        self.logger.info(f"跳过已邀约达人: {talent_name}")

                except NoSuchElementException:
                    continue

        except Exception as e:
            self.logger.error(f"获取达人列表失败: {str(e)}")
            return 0

        # 邀约每个达人
        success_count = 0
        for talent in talents:
            # 点击达人卡片，确保元素可见
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", talent['element'])
                time.sleep(1)

                if self.invite_single_talent(talent['name'], talent['id']):
                    success_count += 1

                # 每邀约完一个，休息一下
                time.sleep(2)

            except Exception as e:
                self.logger.error(f"邀约达人失败: {talent['name']} - {str(e)}")
                continue

        return success_count

    def has_next_page(self) -> bool:
        """检查是否有下一页"""
        try:
            # 检查下一页按钮是否存在且可点击
            next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '下一页')]")
            return next_button.is_enabled()
        except NoSuchElementException:
            return False

    def go_to_next_page(self) -> bool:
        """翻到下一页"""
        self.logger.info("正在翻到下一页...")

        try:
            if not self.clicker.click_by_xpath(
                "//button[contains(text(), '下一页')]",
                "下一页按钮"
            ):
                return False

            # 等待页面加载
            time.sleep(2)
            self.logger.info("翻页成功")
            return True

        except Exception as e:
            self.logger.error(f"翻页失败: {str(e)}")
            return False

    def run(self, start_url: str, max_pages: int = None):
        """运行机器人"""
        self.logger.info("="*50)
        self.logger.info("微信小店达人广场邀约机器人启动")
        self.logger.info("="*50)

        try:
            # 初始化浏览器
            self.init_browser()

            # 导航到达人广场
            self.navigate_to_talent_square(start_url)

            # 显示初始统计
            self.record_manager.print_statistics()

            # 当前页码
            current_page = 1

            # 处理每一页
            while True:
                self.logger.info(f"\n{'='*50}")
                self.logger.info(f"正在处理第 {current_page} 页")
                self.logger.info(f"{'='*50}\n")

                # 处理当前页面的所有达人
                self.process_current_page()

                # 更新统计
                self.record_manager.print_statistics()

                # 检查是否还有下一页
                if not self.has_next_page():
                    self.logger.info("已到达最后一页，结束邀约")
                    break

                # 检查是否达到最大页数限制
                if max_pages and current_page >= max_pages:
                    self.logger.info(f"已达到最大页数限制 {max_pages}，结束邀约")
                    break

                # 翻到下一页
                if not self.go_to_next_page():
                    self.logger.error("翻页失败，结束邀约")
                    break

                current_page += 1

            # 最终统计
            self.logger.info("\n" + "="*50)
            self.logger.info("邀约完成！最终统计：")
            self.logger.info("="*50)
            self.record_manager.print_statistics()

        except KeyboardInterrupt:
            self.logger.info("\n用户中断，正在停止...")
            self.record_manager.print_statistics()

        except Exception as e:
            self.logger.error(f"运行过程中发生错误: {str(e)}", exc_info=True)

        finally:
            # 关闭浏览器
            if self.driver:
                self.driver.quit()
                self.logger.info("浏览器已关闭")


def main():
    """主函数"""
    # 配置达人广场的起始URL
    START_URL = "https://你的达人广场URL"  # 需要替换为实际的URL

    # 最大处理页数（None表示不限制）
    MAX_PAGES = None

    # 创建并运行机器人
    bot = WechatStoreInviteBot()
    bot.run(START_URL, MAX_PAGES)


if __name__ == "__main__":
    main()
