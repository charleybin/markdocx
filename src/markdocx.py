import argparse
import os
import sys
import platform
import subprocess

import yaml
from yaml import FullLoader

# 添加当前文件所在目录的父目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.parser.md_parser import md2html
import time

from src.provider.docx_processor import DocxProcessor

config: dict = {
    "version": "0.1.0"
}


# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        # 获取当前脚本所在目录作为基础路径
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# 跨平台打开文件
def open_file_cross_platform(filepath):
    """
    跨平台打开文件的函数
    在Windows使用os.startfile，在Linux使用xdg-open，在macOS使用open
    """
    try:
        if platform.system() == 'Windows':
            os.startfile(filepath)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(['open', filepath])
        else:  # Linux and other Unix systems
            subprocess.call(['xdg-open', filepath])
    except Exception as e:
        print(f"[WARNING] Could not open file automatically: {e}")
        print(f"[INFO] Please manually open: {filepath}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append("-h")

    parser = argparse.ArgumentParser(description="markdocx - %s" % config["version"])
    parser.add_argument('input', help="Markdown file path")
    parser.add_argument('-o', '--output', help="Optional. Path to save docx file")
    parser.add_argument('-s', '--style',
                        help="Optional. YAML file with style configuration")
    parser.add_argument('-a', action="store_true",
                        help="Optional. Automatically open docx file when finished converting")
    args = parser.parse_args()
    
    # 处理输入和输出路径
    input_path = os.path.abspath(args.input)
    if args.output is not None:
        docx_path = os.path.abspath(args.output)
    else:
        # 默认输出到与输入文件相同的目录
        docx_path = os.path.splitext(input_path)[0] + ".docx"
    
    # 确保输出目录存在
    output_dir = os.path.dirname(docx_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    html_path = os.path.splitext(input_path)[0] + ".html"

    start_time = time.time()  # 记录转换耗时
    md2html(input_path, html_path)
    # 在打包成单文件exe后，直接以文件打开default_style.yaml会因为路径问题无法载入
    # Pyinstaller 可以将资源文件一起bundle到exe中，
    # 当exe在运行时，会生成一个临时文件夹，程序可通过sys._MEIPASS访问临时文件夹中的资源
    # https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
    if not args.style:
        args.style = resource_path(os.path.join("config", "default_style.yaml"))

    with open(args.style, "r", encoding="utf-8") as file:
        conf = yaml.load(file, FullLoader)

    DocxProcessor(style_conf=conf) \
        .html2docx(html_path, docx_path)
    done_time = time.time()

    print("[SUCCESS] Convert finished in:", "%.4f" % (done_time - start_time), "sec(s).")
    print("[SUCCESS] Docx saved to:", docx_path)

    if args.a:
        open_file_cross_platform(docx_path)
