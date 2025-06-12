#!/bin/bash

# Ubuntu 系统安装脚本
# 使用指定的Python环境

PYTHON_PATH="/opt/miniconda3/envs/office-service/bin/python"
PIP_PATH="/opt/miniconda3/envs/office-service/bin/pip"

echo "=== MarkDocx Ubuntu 安装脚本 ==="
echo "使用Python环境: $PYTHON_PATH"

# 检查Python环境是否存在
if [ ! -f "$PYTHON_PATH" ]; then
    echo "错误：指定的Python路径不存在: $PYTHON_PATH"
    echo "请确保已经创建了office-service环境"
    exit 1
fi

# 检查pip是否存在
if [ ! -f "$PIP_PATH" ]; then
    echo "错误：pip未找到: $PIP_PATH"
    exit 1
fi

# 安装依赖
echo "正在安装Python依赖..."
$PIP_PATH install -r requirements.txt

echo "安装完成！"
echo ""
echo "使用方法："
echo "1. 直接运行Python脚本："
echo "   $PYTHON_PATH src/markdocx.py example/example.md"
echo ""
echo "2. 构建可执行文件（可选）："
echo "   ./build_ubuntu.sh"
echo ""
echo "3. 测试转换："
echo "   $PYTHON_PATH src/markdocx.py example/example.md -o test_output.docx" 