# YouTube 视频下载器 (yt_zipper)

一个功能强大的YouTube视频下载工具，支持图形界面和命令行两种模式，可以批量下载视频并自动打包成ZIP文件。

## ✨ 主要功能

- 🎬 **批量下载**: 支持单个或批量下载YouTube视频
- 🖥️ **图形界面**: 现代化的GUI界面，操作简单直观
- 💻 **命令行**: 强大的命令行工具，支持脚本自动化
- 📦 **自动打包**: 下载完成后自动创建ZIP压缩包
- 📊 **进度显示**: 实时显示下载进度和状态
- 🎯 **格式选择**: 支持多种视频格式和质量选择
- 🔧 **配置管理**: 支持配置文件保存用户偏好
- 📝 **日志记录**: 详细的下载日志和错误信息

## 🚀 快速开始

### 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt
```

### 运行程序

#### 方式1: 720p高清下载（推荐）
```bash
python direct_720p_download.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "my_video.mp4"
```

#### 方式2: 最高质量下载
```bash
python best_quality_download.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "my_video.mp4"
```

#### 方式3: 启动脚本（图形界面）
```bash
python run.py
```

#### 方式4: 图形界面
```bash
python gui.py
# 或者
python main.py --gui
```

#### 方式5: 命令行
```bash
# 下载单个视频
python main.py -u https://www.youtube.com/watch?v=dQw4w9WgXcQ -o video.zip

# 批量下载
python main.py -l urls.txt -o playlist.zip

# 指定格式
python main.py -u https://www.youtube.com/watch?v=dQw4w9WgXcQ -o video.zip -f 720p
```

## 📖 详细使用说明

### 图形界面模式

1. **启动GUI**: 运行 `python gui.py` 或 `python run.py` 选择图形界面
2. **添加视频**: 
   - 单个链接: 在"单个链接"框中输入URL，点击"添加"
   - 批量链接: 在"批量链接"框中输入多个URL（每行一个），点击"添加批量"
3. **设置选项**:
   - 输出目录: 选择下载文件保存位置
   - 视频格式: 选择视频质量（best, 720p, 1080p等）
   - 保留下载文件: 是否在打包后保留原始文件
4. **开始下载**: 点击"开始下载"按钮
5. **查看进度**: 在进度条和日志区域查看下载状态

### 命令行模式

#### 基本用法

```bash
# 下载单个视频
python main.py -u <URL> -o <output.zip>

# 从文件读取URL列表
python main.py -l <urls.txt> -o <output.zip>

# 启动图形界面
python main.py --gui
```

#### 高级选项

```bash
# 指定视频格式
python main.py -u <URL> -o <output.zip> -f 720p

# 保留下载文件
python main.py -u <URL> -o <output.zip> -k

# 只下载到目录，不打包
python main.py -u <URL> -d <output_dir>

# 详细输出
python main.py -u <URL> -o <output.zip> -v

# 静默模式
python main.py -u <URL> -o <output.zip> -q
```

#### 命令行参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `-u, --url` | 一个或多个YouTube视频URL | `-u https://youtube.com/watch?v=xxx` |
| `-l, --list` | 包含URL的文本文件 | `-l urls.txt` |
| `-o, --output` | 输出ZIP文件路径 | `-o videos.zip` |
| `-d, --output-dir` | 输出目录（不打包） | `-d ./videos` |
| `-f, --format` | 视频格式 | `-f 720p` |
| `-k, --keep` | 保留下载文件 | `-k` |
| `--no-zip` | 不创建ZIP文件 | `--no-zip` |
| `--retries` | 下载重试次数 | `--retries 5` |
| `--timeout` | 下载超时时间(秒) | `--timeout 300` |
| `--verbose` | 详细输出 | `-v` |
| `--quiet` | 静默模式 | `-q` |
| `--gui` | 启动图形界面 | `--gui` |

### 视频质量选择

#### 推荐下载脚本

1. **720p高清下载器** (`direct_720p_download.py`)
   - 专门针对720p优化
   - 使用格式ID确保质量
   - 成功率高，推荐使用

2. **最高质量下载器** (`best_quality_download.py`)
   - 尝试多种策略
   - 自动选择最佳质量
   - 兼容性好

3. **超高清下载器** (`ultra_hd_download.py`)
   - 显示所有可用格式
   - 帮助诊断质量问题
   - 适合高级用户

#### 支持的视频格式

- `bestvideo+bestaudio/best` - 最佳质量（默认）
- `best` - 最佳单一文件
- `worst` - 最低质量
- `720p` - 720p分辨率
- `1080p` - 1080p分辨率
- `mp4` - MP4格式
- `webm` - WebM格式

#### 质量等级说明

| 分辨率 | 质量等级 | 文件大小 | 适用场景 |
|--------|----------|----------|----------|
| 360p | 标清 | 1-3 MB | 快速预览 |
| 480p | 标清+ | 3-5 MB | 一般观看 |
| 720p | 高清 | 5-15 MB | 推荐质量 |
| 1080p | 全高清 | 15-50 MB | 高质量观看 |
| 4K | 超高清 | 50+ MB | 专业用途 |

> 💡 **提示**: 如果下载的视频不清晰，请使用 `direct_720p_download.py` 脚本，它会专门下载720p高清版本。

## 📁 文件结构

```
yt_zipper/
├── main.py          # 主程序（命令行界面）
├── gui.py           # 图形界面
├── downloader.py    # 下载核心模块
├── run.py           # 启动脚本
├── requirements.txt # 依赖包列表
└── README.md        # 说明文档
```

## ⚙️ 配置管理

程序会自动创建配置文件 `~/.yt_zipper_config.json`，包含以下设置：

```json
{
  "output_dir": "~/Downloads/youtube_videos",
  "format": "bestvideo+bestaudio/best",
  "keep_files": false,
  "max_retries": 3,
  "timeout": 600,
  "concurrent_downloads": 1
}
```

## 🔧 故障排除

### 常见问题

1. **无法启动GUI**
   - 确保已安装所有依赖: `pip install -r requirements.txt`
   - 检查Python版本（需要3.8+）

2. **下载失败**
   - 检查网络连接
   - 确认URL格式正确
   - 尝试不同的视频格式
   - 确保已登录YouTube并导出cookies

3. **视频质量不清晰**
   - 使用 `direct_720p_download.py` 下载720p高清版本
   - 检查原视频在YouTube上的最高可用质量
   - 确保cookies文件有效

4. **权限错误**
   - 确保有写入输出目录的权限
   - 在Windows上尝试以管理员身份运行

5. **yt-dlp错误**
   - 更新yt-dlp: `pip install --upgrade yt-dlp`
   - 检查ffmpeg是否安装

6. **需要验证错误**
   - 确保已登录YouTube
   - 导出cookies文件到项目目录
   - 参考 `Chrome_Cookies_Guide.md` 文档

### 日志查看

- GUI模式: 在界面底部的日志区域查看
- 命令行模式: 使用 `-v` 参数查看详细输出

## 📋 系统要求

- Python 3.8+
- yt-dlp
- tkinter (GUI模式)
- ffmpeg (自动下载)

## ⚠️ 法律声明

本工具仅供**教育和个人备份**使用。下载或重新分发受版权保护的内容可能违反YouTube的服务条款和/或当地法律。请确保您有权下载目标内容。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 支持

如果遇到问题，请：
1. 查看本文档的故障排除部分
2. 检查程序日志输出
3. 提交Issue描述问题

## 🚨 解决下载卡住问题

如果遇到"尝试策略 X/X: Cookies File + Best Quality 不动了"的情况：

### 推荐解决方案

**使用改进版下载脚本**（最可靠）:
```bash
python improved_download.py "https://www.youtube.com/watch?v=VIDEO_ID" "output.mp4"
```

**使用快速下载脚本**:
```bash
python quick_download.py "https://www.youtube.com/watch?v=VIDEO_ID" "output.mp4"
```

### 手动解决卡住问题

**Windows**:
```bash
# 查看Python进程
tasklist | findstr python

# 终止卡住的进程
taskkill /F /PID <PID>
```

**Linux/Mac**:
```bash
# 查看Python进程
ps aux | grep python

# 终止卡住的进程
kill -9 <PID>
```

### 详细解决方案

- 查看 `TIMEOUT_SOLUTION.md` 获取详细说明
- 查看 `ANTI_DETECTION_README.md` 了解反检测功能
- 查看 `FINAL_SOLUTION.md` 获取完整解决方案

### 成功率对比

| 脚本 | 超时控制 | 卡住处理 | 成功率 |
|------|----------|----------|--------|
| `improved_download.py` | ✅ 30-60秒 | ✅ 自动跳过 | ~95% |
| `quick_download.py` | ❌ 无限制 | ❌ 可能卡住 | ~90% |
| `main.py` | ❌ 无限制 | ❌ 可能卡住 | ~70% |
