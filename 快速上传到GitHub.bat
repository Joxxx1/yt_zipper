@echo off
chcp 65001 >nul
title 🚀 快速上传到GitHub
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 YouTube下载器上传工具                    ║
echo ║                       快速上传到GitHub                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 请选择上传方式：
echo.
echo [1] 🎯 自动上传（推荐）
echo [2] 📖 查看详细指南
echo [3] 🔧 手动上传步骤
echo [4] ❌ 退出
echo.

set /p choice="请选择 (1-4): "

if "%choice%"=="1" goto auto_upload
if "%choice%"=="2" goto show_guide
if "%choice%"=="3" goto manual_steps
if "%choice%"=="4" goto exit
goto invalid_choice

:auto_upload
echo.
echo 🎯 启动自动上传...
call upload_to_github.bat
goto end

:show_guide
echo.
echo 📖 打开详细指南...
start GITHUB_UPLOAD_GUIDE.md
echo ✅ 详细指南已打开
goto end

:manual_steps
echo.
echo 🔧 手动上传步骤：
echo.
echo 1️⃣ 安装Git: https://git-scm.com/downloads
echo 2️⃣ 创建GitHub仓库: https://github.com/new
echo 3️⃣ 运行以下命令：
echo.
echo    git init
echo    git add .
echo    git commit -m "Initial commit"
echo    git remote add origin https://github.com/用户名/仓库名.git
echo    git push -u origin main
echo.
echo 💡 详细说明请查看 GITHUB_UPLOAD_GUIDE.md
goto end

:invalid_choice
echo.
echo ❌ 无效选择，请重新选择
goto end

:end
echo.
echo 按任意键退出...
pause >nul

:exit
exit
