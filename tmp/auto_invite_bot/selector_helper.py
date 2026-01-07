#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选择器辅助工具 - 帮助用户找到正确的页面选择器
使用方法：
1. 先启动浏览器并手动到达人广场页面
2. 运行此脚本
3. 根据提示检查元素
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class SelectorHelper:
    """选择器辅助工具"""

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def inspect_element(self):
        """检查元素"""
        print("\n" + "="*60)
        print("选择器辅助工具")
        print("="*60)
        print("\n请先手动在浏览器中打开达人广场页面")
        print("然后按回车键继续...")
        input()

        print("\n现在，在浏览器中右键点击你想检查的元素，选择'检查'")
        print("找到元素的 HTML 标签，告诉我元素的：")
        print("1. class 属性（如：class=\"talent-item\"）")
        print("2. id 属性（如果有）")
        print("3. 文本内容（如果有）")
        print("\n输入 'quit' 退出工具\n")

        while True:
            choice = input("\n你想检查哪个元素？\n1. 达人卡片容器\n2. 达人名称\n3. 详情按钮\n4. 邀请带货按钮\n5. 添加上次邀约商品按钮\n6. 确认按钮\n7. 发送邀约按钮\n8. 下一页按钮\n请选择 (1-8) 或输入 'quit': ").strip()

            if choice.lower() == 'quit':
                break

            selector = input("\n请输入元素的 class 名称: ").strip()

            if selector:
                try:
                    elements = self.driver.find_elements(By.CLASS_NAME, selector)

                    if elements:
                        print(f"\n✓ 找到 {len(elements)} 个匹配的元素")

                        for i, elem in enumerate(elements[:3]):  # 只显示前3个
                            print(f"\n元素 {i+1}:")
                            print(f"  - 文本: {elem.text[:50]}")
                            print(f"  - HTML: {elem.get_attribute('outerHTML')[:200]}")

                        input("\n按回车键继续...")
                    else:
                        print(f"\n✗ 未找到 class='{selector}' 的元素")
                        print("请检查：")
                        print("  1. class 名称是否正确")
                        print("  2. 页面是否已加载完成")
                        print("  3. 元素是否在 iframe 中")

                except Exception as e:
                    print(f"\n✗ 查找元素时出错: {str(e)}")

    def __del__(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()


def main():
    """主函数"""
    helper = SelectorHelper()
    try:
        helper.inspect_element()
    except KeyboardInterrupt:
        print("\n\n用户中断")
    finally:
        print("\n工具已关闭")


if __name__ == "__main__":
    main()
