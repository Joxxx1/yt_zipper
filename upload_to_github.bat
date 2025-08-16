@echo off
chcp 65001 >nul
echo 🚀 YouTube下载器 - GitHub自动上传脚本
echo ============================================
echo.

:: 检查Git是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git未安装，请先安装Git
    echo 💡 下载地址: https://git-scm.com/downloads
    echo.
    pause
    exit /b 1
)

echo ✅ Git已安装
echo.

:: 设置Git用户信息
echo 📝 设置Git用户信息...
set /p git_username="请输入您的GitHub用户名: "
set /p git_email="请输入您的邮箱: "

git config --global user.name "%git_username%"
git config --global user.email "%git_email%"

echo ✅ Git用户信息已设置
echo.

:: 初始化Git仓库
echo 🔄 初始化Git仓库...
if exist .git (
    echo ⚠️ Git仓库已存在，跳过初始化
) else (
    git init
    echo ✅ Git仓库初始化完成
)
echo.

:: 添加所有文件
echo 📁 添加文件到Git...
git add .
echo ✅ 文件添加完成
echo.

:: 提交更改
echo 💾 提交更改...
git commit -m "Initial commit: YouTube Ultra HD Downloader - Free Version

🎬 YouTube超高清视频下载器 v2.1
✨ 功能特点:
- 支持4K/8K超高清视频下载
- 内置反爬虫保护机制
- 支持cookies验证
- 实时下载进度显示
- 多种下载策略
- 完全免费开源

🛠️ 技术栈:
- Python 3.7+
- yt-dlp
- FFmpeg
- 跨平台支持

📁 包含文件:
- 增强版下载器 (enhanced_downloader.py)
- 超高清下载器 (ultra_hd_download_fixed.py)
- 专业版下载器 (enhanced_downloader_pro.py)
- Python启动器 (quick_start.py)
- 批处理启动器 (start_downloader.bat)
- 独立模块 (youtube_ultra_hd_downloader/)

🔐 许可证: MIT"
echo ✅ 更改已提交
echo.

:: 获取GitHub仓库URL
echo.
echo 🌐 请创建GitHub仓库:
echo 1. 访问 https://github.com/new
echo 2. 输入仓库名称 (建议: yt_zipper)
echo 3. 选择 Public 或 Private
echo 4. 不要勾选 "Add a README file"
echo 5. 不要勾选 "Add .gitignore"
echo 6. 不要勾选 "Choose a license"
echo 7. 点击 "Create repository"
echo.
set /p repo_url="请输入GitHub仓库URL (例如: https://github.com/username/yt_zipper.git): "

:: 添加远程仓库
echo 🔗 添加远程仓库...
git remote add origin "%repo_url%"
echo ✅ 远程仓库已添加
echo.

:: 推送到GitHub
echo 📤 推送到GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo 🎉 上传成功！
    echo 📍 仓库地址: %repo_url%
    echo.
    echo 💡 后续更新命令:
    echo    git add .
    echo    git commit -m "更新说明"
    echo    git push
) else (
    echo.
    echo ❌ 上传失败，请检查:
    echo    1. 网络连接
    echo    2. GitHub仓库URL是否正确
    echo    3. 是否有推送权限
)

echo.
pause
