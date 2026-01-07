#!/bin/bash
# 快速启动脚本

echo "=========================================="
echo "微信小店达人广场自动邀约机器人"
echo "=========================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到 Python3，请先安装 Python3"
    exit 1
fi

# 进入脚本所在目录
cd "$(dirname "$0")"

# 检查依赖
echo "检查依赖..."
if ! python3 -c "import selenium" 2>/dev/null; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误：依赖安装失败"
        exit 1
    fi
fi

echo "依赖检查完成"
echo ""

# 显示菜单
echo "请选择操作："
echo "1. 运行邀约机器人"
echo "2. 运行选择器辅助工具（帮助找到正确的选择器）"
echo "3. 查看邀约记录"
echo "4. 查看日志"
echo "5. 清空邀约记录（谨慎操作）"
echo "0. 退出"
echo ""

read -p "请输入选项 (0-5): " choice

case $choice in
    1)
        echo ""
        echo "启动邀约机器人..."
        python3 main.py
        ;;
    2)
        echo ""
        echo "启动选择器辅助工具..."
        python3 selector_helper.py
        ;;
    3)
        echo ""
        echo "邀约记录："
        if [ -f "invite_records.json" ]; then
            cat invite_records.json
        else
            echo "暂无邀约记录"
        fi
        ;;
    4)
        echo ""
        echo "最近日志："
        if [ -f "bot.log" ]; then
            tail -n 50 bot.log
        else
            echo "暂无日志"
        fi
        ;;
    5)
        echo ""
        read -p "确认要清空所有邀约记录吗？(yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            echo "{}" > invite_records.json
            echo "邀约记录已清空"
        else
            echo "操作已取消"
        fi
        ;;
    0)
        echo "退出"
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "操作完成"
