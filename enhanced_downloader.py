#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 超高清视频下载器 - 增强版
专门处理YouTube反爬虫问题
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
    print(f"🎬 YouTube 超高清视频下载器 v2.1 (增强版)")
    print(f"📅 构建日期: 2024-12-01")
    print(f"🛡️ 专门处理YouTube反爬虫问题")
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
                        # 提取百分比
                        percent_start = line.find('[') + 1
                        percent_end = line.find('%')
                        if percent_start > 0 and percent_end > percent_start:
                            percent_str = line[percent_start:percent_end]
                            if percent_str.replace('.', '').isdigit():
                                progress = float(percent_str)
                                if progress > last_progress:
                                    last_progress = progress
                                    bar = format_progress_bar(progress)
                                    print(f"📊 {bar}")
                    except:
                        pass
        
        process.wait()
        elapsed_time = time.time() - start_time
        
        if process.returncode == 0:
            print(f"✅ 下载完成! 总用时: {elapsed_time:.1f}秒")
            return True
        else:
            print(f"❌ 下载失败! 用时: {elapsed_time:.1f}秒")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ 下载超时 ({timeout}秒)")
        process.kill()
        return False
    except Exception as e:
        print(f"❌ 下载出错: {e}")
        return False

def find_downloaded_file(output_file):
    """查找下载的文件 - 改进版本"""
    output_path = Path(output_file)
    
    # 方法1: 直接检查文件是否存在
    if output_path.exists():
        return output_path
    
    # 方法2: 检查media_files文件夹
    media_dir = Path("media_files")
    if media_dir.exists():
        # 查找同名文件
        for file_path in media_dir.glob("*"):
            if file_path.name == output_path.name:
                return file_path
        
        # 查找最近修改的文件
        files = list(media_dir.glob("*"))
        if files:
            latest_file = max(files, key=lambda x: x.stat().st_mtime)
            return latest_file
    
    # 方法3: 在当前目录查找
    current_dir = Path(".")
    for file_path in current_dir.glob("*"):
        if file_path.is_file() and file_path.suffix in ['.mp4', '.webm', '.m4a', '.mkv']:
            return file_path
    
    return None

def download_enhanced_video(url, output_file="enhanced_video.%(ext)s"):
    """增强版视频下载 - 专门处理反爬虫问题"""
    
    # 确保media_files文件夹存在
    media_dir = Path("media_files")
    media_dir.mkdir(exist_ok=True)
    
    # 如果输出文件不包含路径，则添加到media_files文件夹
    if not os.path.dirname(output_file) and not output_file.startswith("media_files/"):
        output_file = f"media_files/{output_file}"
    
    print(f"🎬 开始下载视频: {url}")
    print(f"📁 输出文件: {output_file}")
    
    # 检查cookies
    cookies_available = check_cookies()
    if not cookies_available:
        print("❌ 需要有效的cookies文件才能下载")
        print("💡 请按照以下步骤获取cookies:")
        print("1. 在浏览器中登录YouTube")
        print("2. 使用浏览器扩展导出cookies.txt文件")
        print("3. 将cookies.txt放在程序目录中")
        return False
    
    # 检查FFmpeg
    ffmpeg_available = check_ffmpeg()
    
    # 增强版策略列表 - 专门处理反爬虫
    strategies = [
        # 策略1: 使用cookies + 最佳质量
        {
            'name': 'Cookies + Best Quality',
            'format': 'best[acodec!="none"]/best',
            'timeout': 120,
            'description': '使用cookies验证，最佳质量',
            'requires_cookies': True
        },
        # 策略2: 使用cookies + 720p及以上
        {
            'name': 'Cookies + 720p+',
            'format': 'best[height>=720][acodec!="none"]/best[height>=720]',
            'timeout': 120,
            'description': '使用cookies验证，720p及以上',
            'requires_cookies': True
        },
        # 策略3: 使用cookies + MP4格式
        {
            'name': 'Cookies + MP4 Format',
            'format': 'best[ext=mp4][acodec!="none"]/best[ext=mp4]/best',
            'timeout': 120,
            'description': '使用cookies验证，MP4格式',
            'requires_cookies': True
        },
        # 策略4: 使用cookies + 低质量备用
        {
            'name': 'Cookies + Low Quality Backup',
            'format': 'worst[acodec!="none"]/worst',
            'timeout': 90,
            'description': '使用cookies验证，低质量备用',
            'requires_cookies': True
        },
        # 策略5: 无cookies尝试 (备用)
        {
            'name': 'No Cookies Fallback',
            'format': 'best[acodec!="none"]/best',
            'timeout': 60,
            'description': '无cookies备用方案',
            'requires_cookies': False
        }
    ]
    
    # 构建cookies参数
    cookies_arg = ['--cookies', 'cookies.txt'] if cookies_available else []
    
    # 尝试每个策略
    for i, strategy in enumerate(strategies, 1):
        print(f"\n🔄 尝试策略 {i}/{len(strategies)}: {strategy['name']}")
        print(f"📝 说明: {strategy['description']}")
        
        # 如果策略需要cookies但cookies不可用，跳过
        if strategy['requires_cookies'] and not cookies_available:
            print("⏭️ 跳过此策略 (需要cookies)")
            continue
        
        try:
            # 构建yt-dlp命令
            cmd = [
                'python', '-m', 'yt_dlp',
                '--format', strategy['format'],
                '--output', output_file,
                '--user-agent', get_random_user_agent(),
                '--no-progress',
                '--newline',
                '--no-warnings',
                '--ignore-errors',
                '--no-check-certificates',
                '--extractor-args', 'youtube:player_client=web',
                '--extractor-args', 'youtube:player_skip=hls,dash'
            ]
            
            # 添加cookies参数
            if strategy['requires_cookies'] and cookies_available:
                cmd.extend(cookies_arg)
            
            cmd.append(url)
            
            print(f"⏱️ 设置超时: {strategy['timeout']}秒")
            
            # 执行下载
            success = download_with_progress(cmd, strategy['timeout'])
            
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
        print("python enhanced_downloader.py <YouTube_URL> [输出文件名]")
        print("\n示例:")
        print("python enhanced_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("python enhanced_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ my_video.mp4")
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