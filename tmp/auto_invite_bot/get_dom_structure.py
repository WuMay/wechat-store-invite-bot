#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取微信小店达人广场页面的DOM结构
使用此脚本可以获取动态加载后的HTML结构，帮助找到正确的选择器
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_dom_structure():
    """获取页面的DOM结构"""
    # 配置Chrome选项
    chrome_options = Options()

    # 使用系统Chrome用户数据目录
    import platform
    import getpass

    system = platform.system()
    username = getpass.getuser()

    if system == 'Windows':
        user_data_dir = f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data"
    elif system == 'Darwin':  # Mac
        user_data_dir = f"/Users/{username}/Library/Application Support/Google/Chrome"
    else:  # Linux
        user_data_dir = f"/home/{username}/.config/google-chrome"

    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    chrome_options.add_argument('--profile-directory=Default')

    # 禁用自动化控制特征
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # 初始化浏览器
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 打开达人广场页面
        url = "https://store.weixin.qq.com/shop/findersquare/find"
        print(f"正在打开页面: {url}")
        driver.get(url)

        # 等待页面加载
        print("等待页面加载完成...")
        time.sleep(5)

        # 等待达人列表加载
        print("等待达人列表加载...")
        time.sleep(5)

        # 查找包含"长江声乐课堂"的元素（如果存在）
        try:
            from selenium.webdriver.common.by import By
            talent_name_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '长江声乐课堂')]")
            if talent_name_elements:
                print("\n✓ 找到达人名称元素!")
                for i, elem in enumerate(talent_name_elements):
                    print(f"\n--- 达人名称元素 {i+1} ---")
                    print(f"文本: {elem.text}")
                    print(f"HTML: {elem.get_attribute('outerHTML')[:500]}")

                    # 向上查找父元素
                    parent = elem.find_element(By.XPATH, "..")
                    print(f"父元素HTML: {parent.get_attribute('outerHTML')[:500]}")

        except Exception as e:
            print(f"查找达人名称时出错: {e}")

        # 获取整个页面的HTML
        print("\n" + "="*80)
        print("页面HTML结构:")
        print("="*80)

        page_html = driver.page_source

        # 保存到文件
        with open('/tmp/findersquare_dom.html', 'w', encoding='utf-8') as f:
            f.write(page_html)

        print(f"\n✓ 完整HTML已保存到: /tmp/findersquare_dom.html")

        # 搜索包含"flex flex-row items-center"的元素（达人名称的class）
        print("\n" + "="*80)
        print("搜索达人名称相关元素:")
        print("="*80)

        from selenium.webdriver.common.by import By
        try:
            # 查找所有包含flex类的元素
            flex_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'flex flex-row items-center')]")

            print(f"\n找到 {len(flex_elements)} 个包含 'flex flex-row items-center' 的元素")

            for i, elem in enumerate(flex_elements[:5]):  # 只显示前5个
                print(f"\n--- 元素 {i+1} ---")
                print(f"文本: {elem.text}")
                print(f"HTML: {elem.get_attribute('outerHTML')[:300]}")

                # 查找父元素（达人卡片）
                try:
                    parent = elem.find_element(By.XPATH, "..")
                    parent_classes = parent.get_attribute('class')
                    print(f"父元素class: {parent_classes}")

                    # 继续向上查找父元素
                    grandparent = parent.find_element(By.XPATH, "..")
                    grandparent_classes = grandparent.get_attribute('class')
                    print(f"父元素父元素class: {grandparent_classes}")

                except:
                    pass

        except Exception as e:
            print(f"搜索元素时出错: {e}")

        print("\n" + "="*80)
        print("脚本运行完成！")
        print("="*80)
        print("\n提示:")
        print("1. 查看 /tmp/findersquare_dom.html 获取完整HTML")
        print("2. 根据上面的输出，找到达人卡片的class")
        print("3. 将class信息更新到 main.py 中")

        # 保持浏览器打开，方便用户查看
        input("\n按回车键关闭浏览器...")

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == "__main__":
    print("="*80)
    print("微信小店达人广场 - DOM结构获取工具")
    print("="*80)
    print("\n此工具将:")
    print("1. 打开达人广场页面")
    print("2. 获取动态加载后的DOM结构")
    print("3. 帮助你找到达人卡片的class")
    print("\n" + "="*80 + "\n")

    get_dom_structure()
