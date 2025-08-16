#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub自动上传脚本
自动将YouTube下载器项目上传到GitHub
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if check and result.returncode != 0:
            print(f"❌ 命令执行失败: {cmd}")
            print(f"错误信息: {result.stderr}")
            return False
        return result
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False

def check_git_installed():
    """检查Git是否已安装"""
    print("🔍 检查Git是否已安装...")
    result = run_command("git --version", check=False)
    if result and result.returncode == 0:
        print("✅ Git已安装")
        return True
    else:
        print("❌ Git未安装")
        print("💡 请先安装Git: https://git-scm.com/downloads")
        return False

def setup_git_config():
    """设置Git用户配置"""
    print("\n📝 设置Git用户信息...")
    
    username = input("请输入您的GitHub用户名: ").strip()
    email = input("请输入您的邮箱: ").strip()
    
    if not username or not email:
        print("❌ 用户名和邮箱不能为空")
        return False
    
    # 设置Git配置
    run_command(f'git config --global user.name "{username}"')
    run_command(f'git config --global user.email "{email}"')
    
    print("✅ Git用户信息已设置")
    return True

def init_git_repo():
    """初始化Git仓库"""
    print("\n🔄 初始化Git仓库...")
    
    if Path(".git").exists():
        print("⚠️ Git仓库已存在，跳过初始化")
        return True
    
    result = run_command("git init")
    if result:
        print("✅ Git仓库初始化完成")
        return True
    return False

def add_files():
    """添加文件到Git"""
    print("\n📁 添加文件到Git...")
    
    result = run_command("git add .")
    if result:
        print("✅ 文件添加完成")
        return True
    return False

def commit_changes():
    """提交更改"""
    print("\n💾 提交更改...")
    
    commit_message = "Initial commit: YouTube Ultra HD Downloader - Free Version"
    result = run_command(f'git commit -m "{commit_message}"')
    
    if result:
        print("✅ 更改已提交")
        return True
    return False

def create_github_repo():
    """指导用户创建GitHub仓库"""
    print("\n🌐 请创建GitHub仓库:")
    print("1. 访问 https://github.com/new")
    print("2. 输入仓库名称 (建议: yt_zipper)")
    print("3. 选择 Public 或 Private")
    print("4. 不要勾选 'Add a README file'")
    print("5. 不要勾选 'Add .gitignore'")
    print("6. 不要勾选 'Choose a license'")
    print("7. 点击 'Create repository'")
    
    # 自动打开浏览器
    try:
        webbrowser.open("https://github.com/new")
        print("🌐 已自动打开GitHub创建仓库页面")
    except:
        print("🌐 请手动打开: https://github.com/new")
    
    return input("\n请输入GitHub仓库URL (例如: https://github.com/username/yt_zipper.git): ").strip()

def add_remote_repo(repo_url):
    """添加远程仓库"""
    print("\n🔗 添加远程仓库...")
    
    result = run_command(f'git remote add origin "{repo_url}"')
    if result:
        print("✅ 远程仓库已添加")
        return True
    return False

def push_to_github():
    """推送到GitHub"""
    print("\n📤 推送到GitHub...")
    
    # 设置主分支名称
    run_command("git branch -M main")
    
    # 推送到GitHub
    result = run_command("git push -u origin main")
    
    if result:
        print("🎉 上传成功！")
        return True
    else:
        print("❌ 上传失败，请检查:")
        print("   1. 网络连接")
        print("   2. GitHub仓库URL是否正确")
        print("   3. 是否有推送权限")
        return False

def show_future_commands():
    """显示后续更新命令"""
    print("\n💡 后续更新命令:")
    print("   git add .")
    print("   git commit -m '更新说明'")
    print("   git push")

def main():
    """主函数"""
    print("🚀 YouTube下载器 - GitHub自动上传脚本")
    print("=" * 50)
    
    # 检查Git是否安装
    if not check_git_installed():
        input("\n按回车键退出...")
        return
    
    # 设置Git配置
    if not setup_git_config():
        input("\n按回车键退出...")
        return
    
    # 初始化Git仓库
    if not init_git_repo():
        input("\n按回车键退出...")
        return
    
    # 添加文件
    if not add_files():
        input("\n按回车键退出...")
        return
    
    # 提交更改
    if not commit_changes():
        input("\n按回车键退出...")
        return
    
    # 创建GitHub仓库
    repo_url = create_github_repo()
    if not repo_url:
        print("❌ 仓库URL不能为空")
        input("\n按回车键退出...")
        return
    
    # 添加远程仓库
    if not add_remote_repo(repo_url):
        input("\n按回车键退出...")
        return
    
    # 推送到GitHub
    if push_to_github():
        print(f"📍 仓库地址: {repo_url}")
        show_future_commands()
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
