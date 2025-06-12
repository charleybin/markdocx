#!/bin/bash

# Linux/macOS 构建脚本
# 检查是否安装了pyinstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "pyinstaller not found. Installing..."
    pip install pyinstaller
fi

# 构建可执行文件
pyinstaller --noconfirm --onefile --console --add-data "./src/config:config/"  "src/markdocx.py"

echo "构建完成！可执行文件位于 dist/markdocx"
echo "Build completed! Executable is located at dist/markdocx" 