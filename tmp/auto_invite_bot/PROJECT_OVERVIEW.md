# 项目概览

## 📋 项目说明

本项目是一个自动化工具，用于在微信小店达人广场页面自动发送带货邀请给达人。通过模拟人类点击行为，实现自动化邀约流程，并记录所有邀约历史到本地。

## ✨ 核心功能

### 1. 自动化邀约流程
- 自动遍历达人广场的所有达人
- 点击达人详情进入详情页
- 发送带货邀约（添加商品 → 确认 → 发送）
- 自动返回达人广场继续邀约
- 支持多页自动翻页

### 2. 模拟人类行为
- 随机延迟时间（可配置1-5秒）
- 鼠标移动模拟
- 平滑滚动效果
- 避免被平台检测为机器人

### 3. 智能去重
- 记录所有已邀约达人
- 自动跳过重复邀约
- 支持断点续传
- 记录保存在JSON文件中

### 4. 完善的日志系统
- 详细的操作日志
- 实时统计信息
- 错误追踪和记录
- 支持查看邀约历史

### 5. 灵活的配置
- 可调整延迟时间
- 可设置重试次数
- 支持有头/无头模式
- 可配置最大处理页数

## 📂 项目结构

```
tmp/auto_invite_bot/
├── main.py                 # 主程序（12KB）
│   ├── WechatStoreInviteBot  # 主类
│   │   ├── init_browser()     # 初始化浏览器
│   │   ├── navigate_to_talent_square()  # 导航到达人广场
│   │   ├── invite_single_talent()       # 邀约单个达人
│   │   ├── process_current_page()       # 处理当前页面
│   │   ├── has_next_page()              # 检查是否有下一页
│   │   ├── go_to_next_page()            # 翻到下一页
│   │   └── run()                        # 运行机器人
│   └── main()                  # 入口函数
│
├── auto_clicker.py         # 自动点击模块（4.6KB）
│   └── AutoClicker
│       ├── human_like_delay()     # 模拟人类延迟
│       ├── move_to_element()      # 鼠标移动
│       ├── click_with_retry()     # 带重试的点击
│       ├── click_by_text()        # 按文本点击
│       ├── click_by_xpath()       # 按XPath点击
│       ├── click_by_css()         # 按CSS点击
│       ├── wait_for_element()     # 等待元素
│       ├── scroll_down()          # 滚动页面
│       └── go_back()              # 返回上一页
│
├── record_manager.py       # 记录管理模块（2.5KB）
│   └── RecordManager
│       ├── _load_records()        # 加载记录
│       ├── _save_records()        # 保存记录
│       ├── is_invited()           # 检查是否已邀约
│       ├── add_record()           # 添加记录
│       ├── get_statistics()       # 获取统计
│       ├── get_all_records()      # 获取所有记录
│       └── print_statistics()     # 打印统计
│
├── selector_helper.py      # 选择器辅助工具（3.4KB）
│   └── SelectorHelper
│       ├── inspect_element()      # 检查元素
│       └── 帮助用户找到正确的选择器
│
├── test_config.py          # 配置测试脚本（5.6KB）
│   ├── test_config()            # 测试配置文件
│   ├── test_main_config()       # 测试主程序配置
│   ├── test_dependencies()      # 测试依赖包
│   └── main()                   # 主函数
│
├── config.json             # 配置文件
├── requirements.txt        # 依赖包列表
├── run.sh                  # 快速启动脚本
├── README.md               # 详细使用说明（6.8KB）
├── QUICK_START.md          # 快速使用指南（7.5KB）
└── PROJECT_OVERVIEW.md      # 本文件（项目概览）
```

## 🛠️ 技术栈

- **语言**: Python 3.8+
- **浏览器自动化**: Selenium 4.15+
- **浏览器**: Chrome（通过 ChromeDriver）
- **依赖管理**: pip
- **数据存储**: JSON（邀约记录）
- **日志**: Python logging 模块

## 📦 依赖包

```txt
selenium>=4.15.0      # 浏览器自动化
webdriver-manager>=4.0.1  # 自动管理ChromeDriver
pillow>=10.1.0         # 图像处理（备用）
```

## 🔧 关键特性

### 1. 随机延迟机制
```python
delay = random.uniform(min_delay, max_delay)  # 1-3秒
time.sleep(delay)
```

### 2. 鼠标移动模拟
```python
actions = ActionChains(self.driver)
actions.move_to_element(element)
actions.perform()
```

### 3. 点击重试机制
```python
for attempt in range(max_retries):  # 最多重试3次
    try:
        element.click()
        return True
    except Exception:
        time.sleep(click_retry_delay)
```

### 4. 元素等待机制
```python
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, xpath))
)
```

### 5. 去重检查
```python
if not record_manager.is_invited(talent_id):
    # 邀约达人
    record_manager.add_record(talent_id, talent_name, "success")
```

## 📊 数据流程

```
开始
  ↓
初始化浏览器
  ↓
导航到达人广场
  ↓
获取当前页面的达人列表
  ↓
遍历每个达人
  ↓
检查是否已邀过
  ├─ 是 → 跳过
  └─ 否 → 继续邀约流程
      ↓
    点击详情
      ↓
    点击邀请带货
      ↓
    添加上次邀约商品
      ↓
    点击确认
      ↓
    点击发送邀约
      ↓
    记录邀约结果
      ↓
    返回达人广场
      ↓
  下一个达人
  ↓
当前页面处理完？
  ├─ 是 → 检查是否有下一页
  │       ├─ 有 → 翻页
  │       └─ 无 → 结束
  └─ 否 → 继续
  ↓
结束
  显示统计信息
```

## 🔐 安全特性

### 1. 防检测措施
- 禁用自动化控制特征
- 随机用户代理
- 随机延迟时间
- 模拟真实鼠标移动
- 平滑滚动

### 2. 错误处理
- 捕获所有异常
- 自动重试机制
- 优雅的错误恢复
- 详细日志记录

### 3. 数据安全
- 邀约记录本地存储
- 不上传任何数据
- 支持数据备份

## 📈 性能优化

### 1. 并发控制
- 单线程串行处理
- 避免并发请求
- 符合人类操作习惯

### 2. 资源管理
- 自动关闭浏览器
- 及时释放资源
- 内存占用优化

### 3. 网络优化
- 合理的等待时间
- 避免频繁请求
- 重试机制保证成功率

## 🚀 使用建议

### 初次使用
1. 先运行 `test_config.py` 检查配置
2. 使用 `selector_helper.py` 找到正确的选择器
3. 先测试少量邀约（1-3个）
4. 确认流程正常后大规模使用

### 参数建议
- min_delay: 1.0-2.0秒
- max_delay: 2.0-5.0秒
- max_retries: 3-5次
- implicit_wait: 10秒

### 注意事项
- 确保网络稳定
- 保持登录状态
- 定期备份记录
- 监控日志输出

## 📝 未来扩展

可能的改进方向：
1. 支持多账号并发
2. 添加邀约模板功能
3. 支持定时任务
4. 添加Web界面
5. 支持邀约成功率统计
6. 添加邮件/微信通知

## 📄 许可证

本项目仅供学习和个人使用，请勿用于商业用途或违反平台规则的行为。

## 👨‍💻 作者

Vibe Coding 前端专家

---

**项目完成时间**: 2024-01-07
**版本**: 1.0.0
**状态**: ✅ 已完成
