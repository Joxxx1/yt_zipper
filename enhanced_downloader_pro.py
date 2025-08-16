#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 超高清视频下载器 - 增强版专业版（免费版）
专门处理YouTube反爬虫问题，无需付费即可使用
"""

import sys
import os
import subprocess
import time
import random
import json
import datetime
from pathlib import Path

def print_version_info():
    """打印版本信息"""
    print(f"🎬 YouTube 超高清视频下载器 v2.1 (增强版专业版)")
    print(f"📅 构建日期: 2024-12-01")
    print(f"🛡️ 专门处理YouTube反爬虫问题")
    print(f"🆓 免费版 - 无需付费即可使用")
    print("=" * 50)

def check_cookies():
    """检查cookies文件"""
    cookies_file = "cookies.txt"
    if os.path.exists(cookies_file):
        file_size = os.path.getsize(cookies_file)
        print(f"🍪 找到cookies文件: {cookies_file}")
        print(f"📊 文件大小: {file_size / 1024:.1f} KB")
        
        # 检查cookies文件内容
        try:
            with open(cookies_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'youtube.com' in content and 'cookies' in content.lower():
                    print("✅ cookies文件格式正确")
                    return True
                else:
                    print("⚠️ cookies文件可能不是YouTube格式")
                    return False
        except Exception as e:
            print(f"❌ 读取cookies文件失败: {e}")
            return False
    else:
        print("❌ 未找到cookies.txt文件")
        return False

def get_random_user_agent():
    """获取随机User-Agent"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    return random.choice(user_agents)

def check_ffmpeg():
    """检查FFmpeg是否可用"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def format_progress_bar(percentage, width=40):
    """格式化进度条"""
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {percentage:.1f}%"

def download_with_progress(cmd, timeout):
    """带进度显示的下载"""
    print("📥 开始下载...")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        start_time = time.time()
        last_progress = 0
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                line = output.strip()
                print(f"📋 {line}")
                
                # 解析进度信息
                if '[download]' in line and '%' in line:
                    try:
                        # 提取进度百分比
                        percent_str = line.split('%')[0].split()[-1]
                        if percent_str.replace('.', '').isdigit():
                            progress = float(percent_str)
                            if progress > last_progress:
                                elapsed = time.time() - start_time
                                if progress > 0:
                                    eta = (elapsed / progress) * (100 - progress)
                                    print(f"⏱️ 进度: {format_progress_bar(progress)} | 预计剩余: {eta:.1f}秒")
                                last_progress = progress
                    except:
                        pass
        
        return process.returncode == 0
    except Exception as e:
        print(f"❌ 下载过程出错: {e}")
        return False

def find_downloaded_file(output_file):
    """查找下载的文件"""
    # 如果输出文件包含扩展名占位符，需要查找实际文件
    if '%(ext)s' in output_file:
        base_name = output_file.replace('%(ext)s', '')
        # 查找可能的扩展名
        for ext in ['mp4', 'webm', 'm4a', 'mp3']:
            file_path = Path(f"{base_name}{ext}")
            if file_path.exists():
                return file_path
        return None
    else:
        file_path = Path(output_file)
        return file_path if file_path.exists() else None

def download_enhanced_video(url, output_file):
    """增强版视频下载函数"""
    print(f"🎬 开始下载: {url}")
    print(f"📁 输出文件: {output_file}")
    
    # 定义多种下载策略
    strategies = [
        {
            "name": "超高清策略 (最佳质量)",
            "cmd": [
                "yt-dlp",
                "--cookies", "cookies.txt",
                "--user-agent", get_random_user_agent(),
                "--format", "bestvideo[ext=mp4][height>=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--merge-output-format", "mp4",
                "--output", output_file,
                "--no-check-certificates",
                "--prefer-ffmpeg",
                "--add-metadata",
                "--write-thumbnail",
                "--embed-subs",
                "--sub-lang", "zh-Hans,en",
                "--write-description",
                "--write-info-json",
                "--no-playlist",
                "--extract-audio",
                "--audio-format", "m4a",
                "--audio-quality", "0",
                url
            ]
        },
        {
            "name": "高清策略 (1080p)",
            "cmd": [
                "yt-dlp",
                "--cookies", "cookies.txt",
                "--user-agent", get_random_user_agent(),
                "--format", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
                "--merge-output-format", "mp4",
                "--output", output_file,
                "--no-check-certificates",
                "--prefer-ffmpeg",
                "--add-metadata",
                "--no-playlist",
                url
            ]
        },
        {
            "name": "标准策略 (720p)",
            "cmd": [
                "yt-dlp",
                "--cookies", "cookies.txt",
                "--user-agent", get_random_user_agent(),
                "--format", "best[height<=720][ext=mp4]/best[ext=mp4]/best",
                "--output", output_file,
                "--no-check-certificates",
                "--prefer-ffmpeg",
                "--add-metadata",
                "--no-playlist",
                url
            ]
        },
        {
            "name": "兼容策略 (通用格式)",
            "cmd": [
                "yt-dlp",
                "--cookies", "cookies.txt",
                "--user-agent", get_random_user_agent(),
                "--format", "best",
                "--output", output_file,
                "--no-check-certificates",
                "--no-playlist",
                url
            ]
        }
    ]
    
    print(f"🎯 将尝试 {len(strategies)} 种下载策略")
    
    for i, strategy in enumerate(strategies, 1):
        print(f"\n🔄 尝试策略 {i}/{len(strategies)}: {strategy['name']}")
        print(f"📋 命令: {' '.join(strategy['cmd'])}")
        
        try:
            # 执行下载命令
            success = download_with_progress(strategy['cmd'], timeout=300)
            
            if success:
                print(f"✅ 策略 {i} 成功!")
                file_path = find_downloaded_file(output_file)
                if file_path and file_path.exists():
                    file_size = file_path.stat().st_size
                    print(f"📁 文件: {file_path.name}")
                    print(f"📊 大小: {file_size / (1024*1024):.1f} MB")
                    
                    # 询问用户是否继续尝试下一个策略
                    if i < len(strategies):
                        print(f"\n🎉 策略 {i} 下载成功!")
                        print(f"📁 文件: {file_path.name}")
                        print(f"📊 大小: {file_size / (1024*1024):.1f} MB")
                        
                        while True:
                            choice = input(f"\n是否继续尝试下一个策略以获得更高质量? (y/n): ").strip().lower()
                            if choice in ['y', 'yes', '是', '继续']:
                                print(f"🔄 继续尝试策略 {i+1}/{len(strategies)}...")
                                break
                            elif choice in ['n', 'no', '否', '停止']:
                                print("✅ 下载完成，停止尝试其他策略")
                                return True
                            else:
                                print("❓ 请输入 y (是) 或 n (否)")
                    else:
                        print(f"\n🎉 策略 {i} 下载成功!")
                        print(f"📁 文件: {file_path.name}")
                        print(f"📊 大小: {file_size / (1024*1024):.1f} MB")
                        print("✅ 所有策略已完成")
                        return True
                    
                    continue
                else:
                    print("\n⚠️ 命令成功但文件未找到")
            else:
                print(f"\n❌ 策略 {i} 失败")
                
        except Exception as e:
            print(f"\n❌ 策略 {i} 出错: {e}")
        
        # 策略间延迟
        if i < len(strategies):
            delay = random.uniform(2, 3)
            print(f"⏳ 等待 {delay:.1f} 秒后尝试下一个策略...")
            time.sleep(delay)
    
    print("\n💥 所有策略都失败了!")
    print("\n💡 建议:")
    print("1. 检查网络连接")
    print("2. 确认视频链接有效")
    print("3. 更新cookies.txt文件")
    print("4. 尝试使用VPN或代理")
    print("5. 等待一段时间后重试")
    return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_version_info()
        print("使用方法:")
        print("python enhanced_downloader_pro.py <YouTube_URL> [输出文件名]")
        print("\n示例:")
        print("python enhanced_downloader_pro.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("python enhanced_downloader_pro.py https://www.youtube.com/watch?v=dQw4w9WgXcQ my_video.mp4")
        return

    # 显示版本信息
    print_version_info()

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "enhanced_video.%(ext)s"
    
    # 检查cookies
    if check_cookies():
        print("✅ cookies文件可用")
    else:
        print("⚠️ cookies文件不可用，部分功能可能受限")
    
    # 检查FFmpeg
    if check_ffmpeg():
        print("✅ FFmpeg已安装")
    else:
        print("⚠️ FFmpeg未安装")
    
    print(f"📁 输出文件: {output_file}")
    
    # 开始下载
    success = download_enhanced_video(url, output_file)
    
    if success:
        print("\n🎉 视频下载成功完成!")
    else:
        print("\n❌ 下载失败!")

if __name__ == "__main__":
    main() 