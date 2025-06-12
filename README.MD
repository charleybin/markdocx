# markdocx

将你的 markdown 文件转换为 MS Word（.docx）/ Convert your Markdown files to MS Word (.docx).

🚧 正在开发中 / Under development

## 效果图

![example](assets/example.png)

## 使用方法

### Windows 系统
1. 在 [Release](https://github.com/greyovo/markdocx/releases) 下载可执行文件（暂未提供 macOS 版）
2. 在可执行文件所在目录，终端执行命令：`.\markdocx path/to/your/file.md`，会在 md 文件的同目录下生成同名 docx 文件。

### Ubuntu/Linux 系统

#### 方式1：使用便捷脚本（推荐）
1. 运行安装脚本：
   ```bash
   ./setup_ubuntu.sh
   ```

2. 使用转换工具：
   ```bash
   # 显示帮助信息
   ./markdocx_ubuntu.sh
   
   # 转换markdown文件
   ./markdocx_ubuntu.sh example/example.md
   
   # 指定输出文件
   ./markdocx_ubuntu.sh input.md -o output.docx
   
   # 转换后自动打开文件
   ./markdocx_ubuntu.sh input.md -a
   ```

#### 方式2：直接使用Python脚本
```bash
# 安装依赖
/opt/miniconda3/envs/office-service/bin/pip install -r requirements.txt

# 运行转换
/opt/miniconda3/envs/office-service/bin/python src/markdocx.py example/example.md
```

#### 方式3：构建可执行文件
```bash
# 构建
./build_ubuntu.sh

# 使用构建的可执行文件
./dist/markdocx example/example.md
```

完整命令示例：

```shell script
markdocx input.md -o ouput.docx -s style.yaml -a
```
其中：
 - `-o` 可选参数，其后附上输出路径，默认保存到与 `input.md` 同目录位置、同名的 Word 文件。
 - `-s` 可选参数，其后附上定义样式的 YAML 文件的路径。默认使用内置样式 `src/config/default_style.yaml`。
 - `-a` 可选参数，在完成导出后自动打开 Word 文件

注意，如果是路径中**包含空格**，需要用英文(半角)双引号包起来，如

```shell script
markdocx "D:/my folder/the input.md" -o "D:/my folder/the output.md"
```

## 已知问题 ⁉️ 

1. 行内的样式超过一个的句子会在解析时会被忽略，**不会**出现在最终word文件中。例如此类：
    ```markdown
    **又加粗又*斜体***
    <u>**又加粗又*斜体*又下划线**</u>
    ```
    请避免使用复合标记。
    
2. 无序列表和有序列表目前最大解析层级为两级，超过两层的内容会被丢弃

## 🖼️ 增强图片下载功能

MarkDocx 支持增强的图片下载功能，可以解决网络图片访问中的各种问题：

### 🚀 功能特性

- ✅ **SSL证书验证失败** - 支持自签名证书，解决企业内网图片访问问题
- ✅ **需要登录的图片** - 自动读取浏览器Cookie，访问私有图片资源
- ✅ **反爬虫防护** - 模拟真实浏览器请求，绕过反爬虫机制
- ✅ **网络超时问题** - 智能重试机制，提高下载成功率
- ✅ **权限验证** - 支持自定义请求头，处理API接口图片

### 🔧 解决的常见错误

#### SSL证书问题
**错误信息**：
```
[RESOURCE ERROR]: certificate verify failed: self-signed certificate
```
**解决方案**：程序默认跳过SSL验证，支持自签名证书

#### Cookie验证问题
**错误信息**：
```
[RESOURCE ERROR]: HTTP Error 403: Forbidden
```
**解决方案**：自动读取浏览器Cookie，支持需要登录的图片

### 📋 使用方法

#### 基本使用（自动功能）
```bash
# 普通使用，自动应用所有增强功能
./markdocx_ubuntu.sh example/test.md

# 程序会自动：
# - 读取浏览器Cookie
# - 跳过SSL验证
# - 模拟真实浏览器请求
```

#### 针对特定网站

**方法1：使用浏览器登录后转换**
1. 在浏览器中正常登录需要验证的网站
2. 确保图片可以在浏览器中正常显示
3. 运行转换命令，程序会自动读取浏览器Cookie

**方法2：手动配置请求头**
编辑 `src/config/image_config.yaml` 文件：

```yaml
# 图片下载配置
use_browser_cookies: true    # 使用浏览器Cookie
verify_ssl: false           # 跳过SSL验证
timeout: 15                 # 超时时间

# 自定义请求头
custom_headers:
  User-Agent: "Mozilla/5.0 ..."
  Referer: "https://your-site.com"
  Authorization: "Bearer your-token"
```

### 📊 效果对比

| 功能 | 之前 | 现在 |
|------|------|------|
| SSL证书验证 | ❌ 失败报错 | ✅ 自动跳过验证 |
| 需要登录的图片 | ❌ 403/401错误 | ✅ 自动使用浏览器Cookie |
| 反爬虫网站 | ❌ 被拒绝访问 | ✅ 模拟真实浏览器 |
| 网络超时 | ❌ 直接失败 | ✅ 智能重试 |
| 下载进度 | ❌ 无反馈 | ✅ 显示字节数 |

### 🔍 调试信息

程序会显示详细的下载信息：

```bash
[COOKIES] Loaded cookies from Chrome          # Cookie加载状态
[IMAGE] fetching: https://example.com/img.jpg # 开始下载
[SUCCESS] Downloaded 144868 bytes             # 下载成功
```

如果遇到问题，会显示具体错误：
```bash
[SSL ERROR] certificate verify failed         # SSL问题
[NETWORK ERROR] Connection timeout            # 网络问题
[FALLBACK] Using urllib with SSL disabled     # 使用备用方法
```

### 🎯 支持的场景

- ✅ **企业内网图片**（自签名SSL证书）
- ✅ **私有相册图片**（需要登录验证）
- ✅ **图床服务**（反爬虫保护）
- ✅ **API接口图片**（需要Authorization）
- ✅ **CDN加速图片**（需要Referer验证）

### 🆘 常见问题

**Q: 图片还是下载失败怎么办？**
A: 检查以下几点：
1. 确保浏览器中能正常访问图片
2. 检查网络连接
3. 尝试增加超时时间
4. 查看错误信息，可能需要特殊的请求头

**Q: 某些私有图片无法下载？**
A: 
1. 先在浏览器中登录相关网站
2. 确保浏览器Cookie可访问（关闭隐私模式）
3. 可能需要手动配置特殊的请求头

## 自定义样式参数

### 段落类型名称

| YAML 中的值 | 含义     |
| ----------- | -------- |
| h1          | 一级标题 |
| h2          | 二级标题 |
| h3          | 三级标题 |
| h4          | 四级标题 |
| normal      | 正文     |

### 示例模板

完整 YAML 见 [src/config/default_style.yaml](src/config/default_style.yaml)

```yaml
h1: # 段落类型名称，可取的值见上表
  font:
    default: Times New Roman # 西文字体，默认 [Times New Roman]
    east-asia: 宋体 # 中文字体，默认 [宋体]
    size: 12 # 字体大小，默认 [12]，单位：pt
    color: "000000" # RGB颜色 16 进制值，必须是字符串，默认 ["000000"] 纯黑色
    extra: # 默认不添加这些样式。支持下列样式，有则生效，无则忽略
    - bold # 加粗
    - italic # 斜体
    - underline # 下划线
    - strike # 删除线
  first-line-indent: 0 # 首行缩进，默认 [0]，单位：倍
  line-spacing: 1.2 # 行距，默认 [1.2] 单位：倍，表示行距设置为 1.2 倍行高，
  space:
    before: 0 # 段前空格，默认 [0] pt
    after: 0 # 段后空格，默认 [0] pt
```

## 从源码构建

1. 需要 Python 3.0+ 环境
2. 安装依赖 `pip install -r requirements.txt`
3. 入口文件 `markdocx.py`
4. 构建可执行文件
   1. Windows 下运行 `build.bat`
   2. Ubuntu/Linux 下运行 `./build_ubuntu.sh`
   3. macOS 复制 `build.bat` 中的命令到终端执行（待验证）

## 未来计划

- [x] 使用 YAML 导入样式参数
- [x] 增强图片下载功能（支持SSL、Cookie、反爬虫）
- [x] Ubuntu/Linux 系统支持
- [ ] 支持更多段落类型设置
- [ ] 提供 GUI
- [ ] 提供 macOS 版本。目前我只有 Windows 设备，欢迎参与贡献:)

## 可解析的语法

- [x] 普通段落
- [x] 一到四级标题，保留大纲导航
- [x] 本地图片、网络图片、图片标题
- [x] 有序列表、无序列表、TODO List
- [x] 引用块
- [x] 表格
- [x] 超链接
- [x] 分割线，在 Word 中表现为分页符
- [x] 加粗、斜体、下划线
- [x] 行内代码
- [x] 上标、下标
- [x] 高亮文本
- [ ] 代码块样式优化（或转换为图片）

## 暂时无法实现
- LaTeX
- 脚注

## 感谢开源项目

- [python-docx](https://python-docx.readthedocs.io)
- [python-markdown](https://python-markdown.github.io)
- [beautifulsoup4](https://beautifulsoup.readthedocs.io)
- [pyyaml](https://pyyaml.org)
- [requests](https://docs.python-requests.org)
- [browser-cookie3](https://github.com/borisbabic/browser_cookie3)