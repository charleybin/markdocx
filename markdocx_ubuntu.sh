#!/bin/bash

# MarkDocx Ubuntu 运行脚本
# 使用指定的Python环境运行markdocx

PYTHON_PATH="/opt/miniconda3/envs/office-service/bin/python"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKDOCX_SCRIPT="$SCRIPT_DIR/src/markdocx.py"

# 检查Python环境是否存在
if [ ! -f "$PYTHON_PATH" ]; then
    echo "错误：指定的Python路径不存在: $PYTHON_PATH"
    echo "请先运行 ./setup_ubuntu.sh 进行安装"
    exit 1
fi

# 检查markdocx脚本是否存在
if [ ! -f "$MARKDOCX_SCRIPT" ]; then
    echo "错误：markdocx脚本不存在: $MARKDOCX_SCRIPT"
    exit 1
fi

# 如果没有参数，显示帮助信息
if [ $# -eq 0 ]; then
    echo "MarkDocx - Markdown 转 DOCX 工具 (Ubuntu版)"
    echo ""
    echo "使用方法:"
    echo "  $0 <input.md> [options]"
    echo ""
    echo "示例:"
    echo "  $0 example/example.md"
    echo "  $0 input.md -o output.docx"
    echo "  $0 input.md -s custom_style.yaml -a"
    echo ""
    echo "选项:"
    echo "  -o, --output    指定输出文件路径"
    echo "  -s, --style     指定样式YAML文件"
    echo "  -a              转换完成后自动打开文件"
    echo ""
    exit 0
fi

# 运行markdocx
echo "正在转换文件..."
$PYTHON_PATH "$MARKDOCX_SCRIPT" "$@" 