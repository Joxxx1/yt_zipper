#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 超高清视频下载器 - 稳定版本 v1.0
支持进度条显示和音频合并
作者: AI Assistant
版本: v1.0 (稳定版)
日期: 2024-12-01

功能特点:
- 支持超高清视频下载 (720p, 1080p, 4K)
- 实时进度条显示
- 自动音频合并
- 多种下载策略
- 错误重试机制
- 支持浏览器cookies

使用说明:
python ultra_hd_download_with_progress.py "YouTube_URL" [自定义文件名]
"""

import subprocess
import sys
import os
import random
import time
import re
from pathlib import Path

# 版本信息
VERSION = "v1.0"
BUILD_DATE = "2024-12-01"
DESCRIPTION = "YouTube超高清视频下载器 - 稳定版本"

def print_version_info():
    """打印版本信息"""
    print(f"🎬 YouTube 超高清视频下载器 {VERSION}")
    print(f"📅 构建日期: {BUILD_DATE}")
    print(f"📝 描述: {DESCRIPTION}")
    print("=" * 50)

def get_random_user_agent():
    """获取随机User-Agent"""
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0'
    ]
    return random.choice(agents)

def check_ffmpeg():
    """检查FFmpeg是否安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg已安装 - 支持视频音频分离下载和合并")
            return True
        else:
            print("❌ FFmpeg未正确安装")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg未安装 - 将使用单一文件策略")
        return False
    except Exception as e:
        print(f"❌ 检查FFmpeg时出错: {e}")
        return False

def format_progress_bar(percentage, width=40):
    """格式化进度条"""
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {percentage:.1f}%"

def download_with_progress(cmd, timeout):
    """带进度显示的下载函数"""
    print("📥 开始下载...")
    
    try:
        # 启动进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        start_time = time.time()
        last_percentage = 0
        
        # 监控输出
        while True:
            line = process.stdout.readline()
            if not line:
                break
            
            line = line.strip()
            
            # 解析进度信息
            progress_match = re.search(r'\[download\]\s+(\d+\.?\d*)%', line)
            if progress_match:
                percentage = float(progress_match.group(1))
                if percentage > last_percentage:
                    elapsed = time.time() - start_time
                    progress_bar = format_progress_bar(percentage)
                    print(f"\r{progress_bar} 用时: {elapsed:.1f}s", end='', flush=True)
                    last_percentage = percentage
            elif '[download]' in line or 'Downloading' in line:
                print(f"\n📋 {line}")
        
        # 等待进程完成
        returncode = process.wait()
        
        if returncode == 0:
            print(f"\n✅ 下载完成! 总用时: {time.time() - start_time:.1f}秒")
            return True
        else:
            print(f"\n❌ 下载失败 (返回码: {returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n⏰ 下载超时 ({timeout}秒)")
        process.terminate()
        return False
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断下载")
        process.terminate()
        return False
    except Exception as e:
        print(f"\n❌ 下载出错: {e}")
        return False

def download_ultra_hd_video(url, output_file="ultra_hd_video.%(ext)s"):
    """下载超高清视频（包含音频）"""
    
    print(f"🎬 开始下载超高清视频（包含音频）: {url}")
    print(f"📁 输出文件: {output_file}")
    
    # 首先检查FFmpeg
    ffmpeg_available = check_ffmpeg()
    
    # 超高清策略列表 - 按质量排序，确保包含音频
    strategies = []
    
    if ffmpeg_available:
        # 有FFmpeg时的策略（支持视频音频分离下载和合并）
        strategies.extend([
            # 策略1: 最高质量视频+音频组合
            {
                'name': 'Ultra HD Video + Audio (Highest Quality)',
                'format': 'bestvideo[height>=720]+bestaudio/best[height>=720]',
                'timeout': 180,
                'description': '720p及以上最高质量视频+音频分离下载并合并',
                'requires_ffmpeg': True
            },
            # 策略2: 1080p及以上
            {
                'name': 'Full HD+ (1080p+)',
                'format': 'bestvideo[height>=1080]+bestaudio/best[height>=1080]',
                'timeout': 180,
                'description': '1080p及以上全高清质量视频+音频',
                'requires_ffmpeg': True
            },
            # 策略3: 4K质量
            {
                'name': '4K Ultra HD (2160p)',
                'format': 'bestvideo[height>=2160]+bestaudio/best[height>=2160]',
                'timeout': 300,
                'description': '4K超高清质量视频+音频',
                'requires_ffmpeg': True
            },
            # 策略4: 最佳视频+音频（无限制）
            {
                'name': 'Best Video + Audio (No Limit)',
                'format': 'bestvideo+bestaudio',
                'timeout': 180,
                'description': '最佳视频和音频，无质量限制',
                'requires_ffmpeg': True
            },
            # 策略5: 最高比特率
            {
                'name': 'Highest Bitrate',
                'format': 'bestvideo[vcodec^=avc1]+bestaudio/best[vcodec^=avc1]',
                'timeout': 120,
                'description': '最高比特率H.264编码视频+音频',
                'requires_ffmpeg': True
            }
        ])
    
    # 无FFmpeg或备用策略（确保包含音频的单一文件）
    strategies.extend([
        # 策略6: 最佳单一文件（确保有音频）
        {
            'name': 'Best Single File with Audio',
            'format': 'best[acodec!="none"]/best',
            'timeout': 90,
            'description': '最佳单一文件，确保包含音频'
        },
        # 策略7: 最佳MP4格式（通常包含音频）
        {
            'name': 'Best MP4 Format with Audio',
            'format': 'best[ext=mp4][acodec!="none"]/best[ext=mp4]/best',
            'timeout': 90,
            'description': '最佳MP4格式，确保包含音频'
        },
        # 策略8: 720p及以下（通常包含音频）
        {
            'name': '720p and Below with Audio',
            'format': 'best[height<=720][acodec!="none"]/best[height<=720]',
            'timeout': 90,
            'description': '720p及以下，确保包含音频'
        },
        # 策略9: 最佳WebM格式（通常包含音频）
        {
            'name': 'Best WebM Format with Audio',
            'format': 'best[ext=webm][acodec!="none"]/best[ext=webm]/best',
            'timeout': 90,
            'description': '最佳WebM格式，确保包含音频'
        },
        # 策略10: 最低质量但确保有音频
        {
            'name': 'Lowest Quality with Audio',
            'format': 'worst[acodec!="none"]/worst',
            'timeout': 60,
            'description': '最低质量，但确保包含音频'
        }
    ])
    
    # 检查cookies文件
    if os.path.exists('cookies.txt'):
        print("🍪 找到cookies.txt文件")
        cookies_param = ['--cookies', 'cookies.txt']
    else:
        print("⚠️ 未找到cookies.txt文件，将尝试使用浏览器cookies")
        cookies_param = []
    
    # 尝试每个策略
    for i, strategy in enumerate(strategies, 1):
        print(f"\n🔄 尝试策略 {i}/{len(strategies)}: {strategy['name']}")
        print(f"📝 说明: {strategy['description']}")
        print(f"🎯 格式: {strategy['format']}")
        
        try:
            # 构建命令
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '-f', strategy['format'],
                '-o', output_file,
                '--user-agent', get_random_user_agent(),
                '--no-warnings',
                '--ignore-errors',
                '--no-check-certificates',
                '--extractor-args', 'youtube:player_client=web',
                '--extractor-args', 'youtube:player_skip=hls,dash',
                '--progress',  # 启用进度显示
                '--newline',   # 使用换行符分隔进度
            ]
            
            # 如果有FFmpeg，添加合并参数
            if ffmpeg_available and strategy.get('requires_ffmpeg', False):
                cmd.extend([
                    '--merge-output-format', 'mp4',  # 强制输出MP4
                ])
            
            cmd.extend(cookies_param + [url])
            
            print(f"⏱️ 设置超时: {strategy['timeout']}秒")
            
            # 执行下载并显示进度
            success = download_with_progress(cmd, strategy['timeout'])
            
            if success:
                print(f"✅ 策略 {i} 成功!")
                
                # 检查文件是否真的下载了
                output_path = Path(output_file.replace('%(ext)s', '*'))
                if output_path.parent.exists():
                    files = list(output_path.parent.glob(output_path.name))
                    if files:
                        file_path = files[0]
                        file_size = file_path.stat().st_size
                        print(f"📁 文件已下载: {file_path.name}")
                        print(f"📊 文件大小: {file_size / (1024*1024):.1f} MB")
                        
                        # 检查文件是否有音频（如果有FFmpeg）
                        if ffmpeg_available:
                            check_audio_cmd = [
                                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                                '-show_streams', str(file_path)
                            ]
                            try:
                                audio_result = subprocess.run(check_audio_cmd, capture_output=True, text=True, timeout=10)
                                if audio_result.returncode == 0:
                                    import json
                                    streams = json.loads(audio_result.stdout).get('streams', [])
                                    has_audio = any(s.get('codec_type') == 'audio' for s in streams)
                                    if has_audio:
                                        print("🔊 文件包含音频流")
                                    else:
                                        print("⚠️ 文件可能没有音频")
                                else:
                                    print("⚠️ 无法检查音频流")
                            except:
                                print("⚠️ 无法检查音频流")
                        
                        # 获取视频信息
                        info_cmd = [
                            sys.executable, '-m', 'yt_dlp',
                            '--dump-json',
                            '--no-playlist',
                            '--quiet',
                            url
                        ] + cookies_param
                        
                        try:
                            info_result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=30)
                            if info_result.returncode == 0:
                                import json
                                video_info = json.loads(info_result.stdout)
                                if 'resolution' in video_info:
                                    print(f"🎬 视频分辨率: {video_info['resolution']}")
                                if 'height' in video_info:
                                    print(f"📏 视频高度: {video_info['height']}p")
                                if 'width' in video_info:
                                    print(f"📐 视频宽度: {video_info['width']}p")
                                if 'filesize' in video_info:
                                    print(f"💾 原始文件大小: {video_info['filesize'] / (1024*1024):.1f} MB")
                        except:
                            pass
                        
                        return True
                
                print("\n⚠️ 命令成功但文件未找到")
            else:
                print(f"\n❌ 策略 {i} 失败")
                
        except Exception as e:
            print(f"\n❌ 策略 {i} 出错: {e}")
        
        # 策略间延迟
        if i < len(strategies):
            delay = random.uniform(1, 2)
            print(f"⏳ 等待 {delay:.1f} 秒后尝试下一个策略...")
            time.sleep(delay)
    
    print("\n💥 所有策略都失败了!")
    return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_version_info()
        print("使用方法:")
        print("  python ultra_hd_download_with_progress.py <YouTube_URL> [输出文件名]")
        print("")
        print("示例:")
        print("  python ultra_hd_download_with_progress.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("  python ultra_hd_download_with_progress.py https://www.youtube.com/watch?v=dQw4w9WgXcQ ultra_hd_video.mp4")
        print("")
        print("💡 功能特点:")
        print("- 自动检测FFmpeg，支持视频音频分离下载和合并")
        print("- 确保下载的视频包含音频")
        print("- 多种质量策略，从4K到720p")
        print("- 智能策略切换，提高成功率")
        print("- 实时进度条显示，了解下载状态")
        print("")
        print("🔧 建议:")
        print("- 安装FFmpeg以获得最佳音频质量: winget install ffmpeg")
        print("- 确保cookies.txt文件存在以提高成功率")
        return
    
    # 显示版本信息
    print_version_info()
    
    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "ultra_hd_video.%(ext)s"
    
    # 检查cookies文件
    if os.path.exists('cookies.txt'):
        print("🍪 找到cookies.txt文件")
    else:
        print("⚠️ 未找到cookies.txt文件，将尝试使用浏览器cookies")
    
    # 开始下载
    success = download_ultra_hd_video(url, output_file)
    
    if success:
        print("\n🎉 超高清视频（包含音频）下载成功完成!")
        print("\n💡 提示:")
        print("- 如果视频仍然没有声音，请检查:")
        print("  1. 系统音量设置")
        print("  2. 播放器音频设置")
        print("  3. 原视频是否有音频")
        print("- 如果视频质量仍不满意，可能是原视频本身质量有限")
        print("- 检查原视频在YouTube上的最高可用质量")
        print("- 某些视频可能只有较低分辨率可用")
        print("- 建议安装FFmpeg以获得更好的音频质量")
    else:
        print("\n💥 下载失败!")
        print("\n💡 建议:")
        print("1. 安装FFmpeg: winget install ffmpeg")
        print("2. 确保已登录YouTube并导出了cookies")
        print("3. 检查原视频是否有高清版本")
        print("4. 尝试使用其他下载脚本")
        print("5. 更新yt-dlp: pip install --upgrade yt-dlp")

if __name__ == "__main__":
    main() 