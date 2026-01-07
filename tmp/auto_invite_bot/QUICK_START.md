# 快速使用指南

## 📁 项目文件说明

```
tmp/auto_invite_bot/
├── main.py                 # 主程序（邀约机器人核心）
├── auto_clicker.py         # 自动点击模块（模拟人类点击）
├── record_manager.py       # 记录管理模块（邀约记录存储）
├── selector_helper.py      # 选择器辅助工具（帮助找到正确的选择器）
├── config.json             # 配置文件
├── requirements.txt        # 依赖包列表
├── run.sh                  # 快速启动脚本
├── README.md               # 详细使用说明
└── QUICK_START.md          # 本文件（快速使用指南）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd tmp/auto_invite_bot
pip install -r requirements.txt
```

### 2. 配置程序

编辑 `main.py`，修改以下内容：

```python
# 第232行左右，修改达人广场URL
START_URL = "https://你的达人广场URL"  # ⚠️ 必须修改

# 第235行左右，设置最大处理页数（可选）
MAX_PAGES = None  # None表示不限制，例如设置为 5 只处理前5页
```

### 3. 调整选择器（重要！）

由于每个页面的结构可能不同，你需要根据实际情况调整选择器。

**方法1：使用选择器辅助工具（推荐）**

```bash
cd tmp/auto_invite_bot
python3 selector_helper.py
```

按照工具提示，在浏览器中打开达人广场页面，然后检查各个元素的class名称。

**方法2：手动检查**

1. 在Chrome浏览器中打开达人广场页面
2. 右键点击达人卡片 → 检查
3. 查看HTML结构，找到达人的class名称
4. 右键点击达人名称 → 检查
5. 找到达人名称的class名称
6. 编辑 `main.py` 的 `process_current_page()` 方法，替换选择器

示例修改（第157行左右）：

```python
# 修改前（示例）
talent_elements = self.driver.find_elements(By.CLASS_NAME, "talent-item")
name_element = element.find_element(By.CLASS_NAME, "talent-name")

# 修改后（根据实际情况）
talent_elements = self.driver.find_elements(By.CLASS_NAME, "your-talent-class")
name_element = element.find_element(By.CLASS_NAME, "your-name-class")
```

### 4. 运行程序

**方法1：使用启动脚本（推荐）**

```bash
cd tmp/auto_invite_bot
bash run.sh
```

然后选择选项1运行邀约机器人。

**方法2：直接运行**

```bash
cd tmp/auto_invite_bot
python3 main.py
```

## 📊 查看结果

### 查看邀约记录

```bash
# 方法1：查看JSON文件
cat tmp/auto_invite_bot/invite_records.json

# 方法2：使用启动脚本
bash run.sh
# 选择选项3

# 方法3：使用Python
python3 -c "from record_manager import RecordManager; manager = RecordManager('tmp/auto_invite_bot/invite_records.json'); manager.print_statistics()"
```

### 查看日志

```bash
# 方法1：查看日志文件
cat tmp/auto_invite_bot/bot.log

# 方法2：查看最近50行
tail -n 50 tmp/auto_invite_bot/bot.log

# 方法3：使用启动脚本
bash run.sh
# 选择选项4
```

## ⚙️ 配置参数

编辑 `config.json` 调整运行参数：

```json
{
  "headless": false,           // 是否无头模式（true=后台运行，false=显示浏览器）
  "implicit_wait": 10,         // 元素查找等待时间（秒）
  "page_load_timeout": 30,    // 页面加载超时时间（秒）
  "min_delay": 1.0,            // 最小随机延迟（秒）- 建议设置在1-3秒之间
  "max_delay": 3.0,            // 最大随机延迟（秒）- 建议设置在2-5秒之间
  "max_retries": 3,            // 点击失败最大重试次数
  "click_retry_delay": 1.0,    // 点击重试延迟（秒）
  "record_file": "tmp/auto_invite_bot/invite_records.json",  // 邀约记录文件路径
  "log_file": "tmp/auto_invite_bot/bot.log"                 // 日志文件路径
}
```

## 🎯 邀约流程

程序会自动执行以下步骤：

1. ✅ 在达人广场页面找到所有达人
2. ✅ 点击每个达人的详情
3. ✅ 点击"邀请带货"按钮
4. ✅ 点击"添加上次邀约商品"
5. ✅ 点击"确认"按钮
6. ✅ 点击"发送邀约"
7. ✅ 返回达人广场
8. ✅ 继续下一个达人
9. ✅ 当前页处理完后自动翻页
10. ✅ 跳过已邀约的达人

## 🔧 常见问题

### 问题1：找不到元素

**错误**：`✗ 点击失败: 元素未找到`

**解决**：
1. 使用 `python3 selector_helper.py` 检查元素选择器
2. 增加等待时间：修改 `config.json` 中的 `implicit_wait` 或 `page_load_timeout`
3. 确认页面是否完全加载

### 问题2：点击被拦截

**错误**：`元素点击被拦截`

**解决**：
1. 增加点击延迟：修改 `config.json` 中的 `click_retry_delay`
2. 检查是否有弹窗需要关闭
3. 手动检查页面是否有覆盖层

### 问题3：页面结构不同

**解决**：
1. 使用浏览器开发者工具检查页面元素
2. 根据实际情况修改 `main.py` 中的选择器
3. 参考下面的选择器调整部分

## 🔍 选择器调整说明

### 达人卡片容器

在 `main.py` 第157行左右：

```python
# 查找达人卡片 - 修改 class 名称
talent_elements = self.driver.find_elements(By.CLASS_NAME, "你的达人卡片class")
```

### 达人名称

在 `main.py` 第163行左右：

```python
# 查找达人名称 - 修改 class 名称
name_element = element.find_element(By.CLASS_NAME, "你的达人名称class")
```

### 邀约按钮

在 `invite_single_talent()` 方法中（第76行左右）：

```python
# 详情按钮
self.clicker.click_by_xpath("//button[contains(text(), '详情')]", "详情按钮")

# 邀请带货按钮
self.clicker.click_by_xpath("//button[contains(text(), '邀请带货')]", "邀请带货按钮")

# 添加上次邀约商品
self.clicker.click_by_xpath("//button[contains(text(), '添加上次邀约商品')]", "添加上次邀约商品")

# 确认按钮
self.clicker.click_by_xpath("//button[contains(text(), '确认')]", "确认按钮")

# 发送邀约按钮
self.clicker.click_by_xpath("//button[contains(text(), '发送邀约')]", "发送邀约按钮")

# 下一页按钮
self.clicker.click_by_xpath("//button[contains(text(), '下一页')]", "下一页按钮")
```

**提示**：
- 如果按钮文本不完全匹配，可以使用 `contains` 或调整XPath
- 也可以使用CSS选择器：`self.clicker.click_by_css(".btn-submit", "提交按钮")`

## ⚠️ 注意事项

1. **合法使用**：请确保符合平台规则，不要滥用自动邀约
2. **频率控制**：合理配置延迟时间，避免被检测
3. **测试优先**：先测试少量邀约，确认流程正常
4. **数据备份**：定期备份 `invite_records.json`
5. **登录状态**：运行前确保已在浏览器中登录微信小店
6. **网络稳定**：确保网络连接稳定，避免加载失败

## 📝 使用示例

### 示例1：测试单个邀约

修改 `main.py`，只处理第一个达人：

```python
def process_current_page(self) -> int:
    # ... 省略前面的代码 ...

    # 只邀约第一个达人
    if talents:
        talent = talents[0]
        # ... 邀约逻辑 ...
        return 1

    return 0
```

### 示例2：限制处理页数

```python
# 在main.py的main()函数中
MAX_PAGES = 5  # 只处理前5页
```

### 示例3：无头模式运行

修改 `config.json`：

```json
{
  "headless": true  // 后台运行，不显示浏览器窗口
}
```

## 📞 需要帮助？

1. 查看 `README.md` 获取详细说明
2. 查看 `bot.log` 了解错误信息
3. 使用 `selector_helper.py` 找到正确的选择器
4. 检查浏览器开发者工具了解页面结构

---

**祝使用愉快！如有问题请查看日志文件。**
