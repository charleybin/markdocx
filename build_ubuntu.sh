#!/bin/bash

# Ubuntu 系统构建脚本
# 使用指定的Python环境构建可执行文件

PYTHON_PATH="/opt/miniconda3/envs/office-service/bin/python"
PIP_PATH="/opt/miniconda3/envs/office-service/bin/pip"

echo "=== MarkDocx Ubuntu 构建脚本 ==="
echo "使用Python环境: $PYTHON_PATH"

# 检查Python环境是否存在
if [ ! -f "$PYTHON_PATH" ]; then
    echo "错误：指定的Python路径不存在: $PYTHON_PATH"
    echo "请先运行 ./setup_ubuntu.sh 进行安装"
    exit 1
fi

# 检查是否安装了pyinstaller
echo "检查pyinstaller..."
if ! $PYTHON_PATH -c "import PyInstaller" 2>/dev/null; then
    echo "pyinstaller未找到，正在安装..."
    $PIP_PATH install pyinstaller
fi

# 构建可执行文件
echo "正在构建可执行文件..."
$PYTHON_PATH -m PyInstaller --noconfirm --onefile --console --add-data "./src/config:config/" "src/markdocx.py"

if [ $? -eq 0 ]; then
    echo ""
    echo "构建成功！"
    echo "可执行文件位于: dist/markdocx"
    echo ""
    echo "使用方法:"
    echo "  ./dist/markdocx example/example.md"
    echo "  ./dist/markdocx example/example.md -o output.docx"
    echo "  ./dist/markdocx example/example.md -a  # 转换后自动打开文件"
else
    echo "构建失败！请检查错误信息。"
    exit 1
fi 