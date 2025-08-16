# 🎬 YouTube 超高清视频下载器

一个功能强大的YouTube视频下载工具，支持超高清视频下载和反爬虫保护。

## ✨ 功能特点

- 🎥 支持超高清视频下载（4K、8K）
- 🛡️ 内置反爬虫保护机制
- 🍪 支持cookies验证
- 📊 实时下载进度显示
- 🔄 自动重试机制
- 💻 跨平台支持（Windows、macOS、Linux）
- 🆓 完全免费，无需付费

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用方法

#### 方法1：使用Python启动器（推荐）
```bash
python quick_start.py
```

#### 方法2：使用批处理文件（Windows）
```bash
start_downloader.bat
```

#### 方法3：直接使用下载器
```bash
python enhanced_downloader.py "视频链接"
```

## 📁 文件说明

### 核心文件
- `enhanced_downloader.py` - 增强版下载器（免费版）
- `ultra_hd_download_fixed.py` - 超高清下载器（免费版）
- `enhanced_downloader_pro.py` - 专业版下载器（免费版）
- `quick_start.py` - Python启动器
- `start_downloader.bat` - 批处理启动器

### 配置文件
- `requirements.txt` - Python依赖包
- `cookies.txt` - YouTube cookies文件（需要用户提供）
- `cookies_example.txt` - cookies文件示例
- `get_cookies.py` - 自动获取cookies脚本
- `COOKIES_SETUP_GUIDE.md` - cookies设置指南
- `LICENSE` - 开源许可证

### 独立模块
- `youtube_ultra_hd_downloader/` - 独立的下载器模块

## 🔧 使用说明

1. **准备cookies文件**：
   - 运行 `python get_cookies.py` 自动获取cookies
   - 或参考 `COOKIES_SETUP_GUIDE.md` 手动获取
   - 确保cookies.txt文件在项目根目录

2. **安装依赖**：运行`pip install -r requirements.txt`

3. **启动程序**：运行`python quick_start.py`

4. **输入链接**：粘贴YouTube视频链接

5. **开始下载**：程序会自动下载最高质量的视频

## 🎯 支持的格式

- 视频格式：MP4、WebM、M4V
- 音频格式：M4A、MP3、AAC
- 分辨率：最高支持8K
- 帧率：最高支持60fps

## 🛠️ 系统要求

- Python 3.7+
- FFmpeg（用于视频处理）
- 稳定的网络连接

## 📝 注意事项

- 请确保遵守YouTube的服务条款
- 仅用于个人学习和研究用途
- 下载的视频仅供个人使用
- 所有功能完全免费，无需付费

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。

---

**💡 提示**：首次使用建议先运行`python quick_start.py`体验完整功能！
