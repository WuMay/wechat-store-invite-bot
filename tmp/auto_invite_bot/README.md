# 微信小店达人广场自动邀约机器人

一个自动化工具，用于在微信小店达人广场页面自动发送带货邀请给达人，模拟人类点击行为，避免被检测。

## 功能特性

✅ **自动邀约流程**
- 自动点击达人详情
- 点击"邀请带货"按钮
- 添加邀约商品并确认
- 发送邀约
- 返回达人广场

✅ **模拟人类行为**
- 随机延迟（可配置）
- 鼠标移动模拟
- 随机点击间隔
- 平滑滚动

✅ **智能去重**
- 记录已邀约达人
- 自动跳过重复邀约
- 支持断点续传

✅ **分页处理**
- 自动翻页
- 可设置最大页数限制
- 支持处理多页达人

✅ **完善的日志和记录**
- 邀约记录本地存储（JSON格式）
- 详细的日志输出
- 实时统计信息

✅ **错误处理**
- 自动重试机制
- 异常捕获和恢复
- 优雅的错误提示

## 安装步骤

### 1. 环境要求

- Python 3.8+
- Chrome 浏览器（最新版）

### 2. 安装依赖

```bash
cd /tmp/auto_invite_bot
pip install -r requirements.txt
```

### 3. 配置参数

编辑 `config.json` 文件，根据需要调整参数：

```json
{
  "headless": false,           // 是否无头模式（true=后台运行，false=显示浏览器）
  "implicit_wait": 10,         // 元素查找等待时间（秒）
  "page_load_timeout": 30,    // 页面加载超时时间（秒）
  "min_delay": 1.0,            // 最小随机延迟（秒）
  "max_delay": 3.0,            // 最大随机延迟（秒）
  "max_retries": 3,            // 点击失败最大重试次数
  "click_retry_delay": 1.0,    // 点击重试延迟（秒）
  "record_file": "/tmp/auto_invite_bot/invite_records.json",  // 邀约记录文件路径
  "log_file": "/tmp/auto_invite_bot/bot.log"                 // 日志文件路径
}
```

## 使用方法

### ⚠️ 重要提示

**关于浏览器登录状态**：
- 程序会使用你系统Chrome的登录状态（共享Cookie、token、缓存等）
- **运行程序时请关闭系统Chrome浏览器**，避免数据冲突
- 首次运行如果未登录，需要在自动打开的浏览器中手动登录微信小店账号
- 登录后会自动保存，之后运行无需重复登录

**反检测特性**：
- 使用系统Chrome用户数据目录，真实浏览器指纹
- 移除webdriver标识，难以被识别为自动化工具
- 模拟真实用户操作：随机延迟、鼠标移动、平滑滚动
- 使用真实User-Agent和浏览器启动参数

### 0. 测试配置（推荐）

在运行程序前，先测试配置是否正确：

```bash
cd tmp/auto_invite_bot
python3 test_config.py
```

测试脚本会检查：
- 配置文件是否存在且格式正确
- 依赖包是否已安装
- 主程序配置是否完整

### 1. 修改主程序配置

编辑 `main.py` 文件，设置达人广场的起始URL：

```python
# 配置达人广场的起始URL
START_URL = "https://你的达人广场URL"  # 需要替换为实际的URL

# 最大处理页数（None表示不限制）
MAX_PAGES = None
```

### 2. 根据实际页面调整选择器

⚠️ **重要**：由于不同的页面结构可能不同，你需要根据实际的微信小店达人广场页面调整选择器。

在 `main.py` 的 `process_current_page()` 方法中，修改以下部分：

```python
# 获取达人列表 - 需要根据实际情况调整
talent_elements = self.driver.find_elements(By.CLASS_NAME, "talent-item")

# 获取达人名称 - 需要根据实际情况调整
name_element = element.find_element(By.CLASS_NAME, "talent-name")
talent_name = name_element.text.strip()

# 获取达人ID - 需要根据实际情况调整
talent_id = element.get_attribute("data-id") or talent_name
```

**如何找到正确的选择器：**

1. 在Chrome浏览器中打开达人广场页面
2. 右键点击达人卡片，选择"检查"
3. 查看HTML结构，找到达人卡片的class或ID
4. 右键点击达人名称，选择"检查"
5. 查看达人名称的class或ID
6. 将找到的选择器替换到代码中

### 3. 调整邀约流程中的按钮选择器

在 `invite_single_talent()` 方法中，也需要根据实际情况调整XPath：

```python
# 1. 点击详情按钮
self.clicker.click_by_xpath("//button[contains(text(), '详情')]", "详情按钮")

# 2. 点击邀请带货按钮
self.clicker.click_by_xpath("//button[contains(text(), '邀请带货')]", "邀请带货按钮")

# 3. 点击添加上次邀约商品
self.clicker.click_by_xpath("//button[contains(text(), '添加上次邀约商品')]", "添加上次邀约商品")

# 4. 点击确认按钮
self.clicker.click_by_xpath("//button[contains(text(), '确认')]", "确认按钮")

# 5. 点击发送邀约
self.clicker.click_by_xpath("//button[contains(text(), '发送邀约')]", "发送邀约按钮")
```

如果按钮的文本不完全匹配，可以使用模糊匹配或根据其他属性查找。

### 4. 运行程序

```bash
cd /tmp/auto_invite_bot
python main.py
```

### 5. 监控运行

程序运行时会输出详细的日志信息，包括：
- 当前处理的达人
- 点击操作结果
- 邀约成功/失败统计

你可以随时按 `Ctrl+C` 停止程序，邀约记录会自动保存。

## 邀约记录

邀约记录保存在 `invite_records.json` 文件中，格式如下：

```json
{
  "达人ID1": [
    {
      "name": "达人名称",
      "status": "success",
      "time": "2024-01-07 14:30:25"
    }
  ],
  "达人ID2": [
    {
      "name": "达人名称",
      "status": "failed",
      "time": "2024-01-07 14:31:10"
    }
  ]
}
```

## 日志文件

所有操作日志保存在 `bot.log` 文件中，包括：
- 每个操作的时间戳
- 操作结果
- 错误信息

## 常见问题

### 1. 找不到元素

**问题**：提示 "点击失败: 元素未找到"

**解决方法**：
- 检查页面是否完全加载
- 使用浏览器开发者工具检查元素的选择器是否正确
- 增加等待时间（修改 `implicit_wait` 或 `page_load_timeout`）

### 2. 点击被拦截

**问题**：提示 "元素点击被拦截"

**解决方法**：
- 检查是否有弹窗或覆盖层
- 尝试滚动到元素位置
- 增加点击前的延迟时间

### 3. 页面加载超时

**问题**：提示 "页面加载超时"

**解决方法**：
- 增加 `page_load_timeout` 配置值
- 检查网络连接
- 确认URL是否正确

### 4. 如何查看邀请记录

**方法1**：查看 `invite_records.json` 文件
```bash
cat /tmp/auto_invite_bot/invite_records.json
```

**方法2**：使用 Python 查看
```python
from record_manager import RecordManager
manager = RecordManager('/tmp/auto_invite_bot/invite_records.json')
manager.print_statistics()
```

## 注意事项

⚠️ **重要提醒**：

1. **合法使用**：请确保你的邀约行为符合平台规则，不要滥用自动邀约功能。

2. **频率控制**：合理配置延迟时间，避免因操作过快被平台检测。

3. **测试优先**：在正式使用前，建议先测试少量邀约，确认流程正常后再大规模使用。

4. **数据备份**：定期备份 `invite_records.json` 文件，避免数据丢失。

5. **选择器更新**：如果页面结构发生变化，需要及时更新代码中的选择器。

6. **浏览器版本**：确保Chrome浏览器是最新版本，避免兼容性问题。

## 技术支持

如果遇到问题，可以：
1. 查看 `bot.log` 日志文件，了解详细错误信息
2. 使用浏览器开发者工具检查页面元素
3. 调整配置参数，优化运行效果

## 许可证

本项目仅供学习和个人使用，请勿用于商业用途或违反平台规则的行为。
