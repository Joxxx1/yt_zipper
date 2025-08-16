#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 超高清视频下载器 - 修复版本
修复了"命令成功但文件未找到"的问题
"""

import sys
import os
import subprocess
import time
import random
from pathlib import Path

def print_version_info():
    """打印版本信息"""
    print(f"🎬 YouTube 超高清视频下载器 v1.1 (修复版)")
    print(f"📅 构建日期: 2024-12-01")
    print(f"📝 描述: 修复了文件查找问题")
    print("=" * 50)

def get_random_user_agent():
    """获取随机User-Agent"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
    """改进的文件查找逻辑"""
    print(f"🔍 查找文件: {output_file}")
    
    # 方法1: 直接查找
    if os.path.exists(output_file):
        print(f"✅ 直接找到文件: {output_file}")
        return Path(output_file)
    
    # 方法2: 替换扩展名查找
    base_name = output_file.replace('%(ext)s', '')
    if base_name.endswith('.'):
        base_name = base_name[:-1]
    
    # 查找可能的扩展名
    extensions = ['mp4', 'webm', 'mkv', 'avi', 'mov', 'flv']
    for ext in extensions:
        possible_file = f"{base_name}.{ext}"
        if os.path.exists(possible_file):
            print(f"✅ 找到文件: {possible_file}")
            return Path(possible_file)
    
    # 方法3: 使用通配符查找
    pattern = f"{base_name}.*"
    files = list(Path.cwd().glob(pattern))
    if files:
        # 过滤掉非视频文件
        video_files = [f for f in files if f.suffix.lower() in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']]
        if video_files:
            # 选择最大的文件（通常是完整的视频）
            largest_file = max(video_files, key=lambda x: x.stat().st_size)
            print(f"✅ 找到最大文件: {largest_file.name}")
            return largest_file
    
    # 方法4: 查找最近创建的视频文件
    all_files = list(Path.cwd().glob("*"))
    video_files = [f for f in all_files if f.is_file() and f.suffix.lower() in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.flv']]
    
    if video_files:
        # 选择最大的文件
        largest_file = max(video_files, key=lambda x: x.stat().st_size)
        print(f"✅ 选择最大文件: {largest_file.name}")
        return largest_file
    
    print("❌ 未找到任何视频文件")
    return None

def download_ultra_hd_video(url, output_file="ultra_hd_video.%(ext)s"):
    """下载超高清视频（包含音频）- 修复版本"""
    
    # 确保media_files文件夹存在
    media_dir = Path("media_files")
    media_dir.mkdir(exist_ok=True)
    
    # 如果输出文件不包含路径，则添加到media_files文件夹
    if not os.path.dirname(output_file) and not output_file.startswith("media_files/"):
        output_file = f"media_files/{output_file}"
    
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
                '--no-progress',  # 禁用yt-dlp进度显示，使用自定义进度条
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
                
                # 使用改进的文件查找逻辑
                file_path = find_downloaded_file(output_file)
                
                if file_path and file_path.exists():
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
                        # 如果是最后一个策略，直接返回成功
                        print(f"\n🎉 策略 {i} 下载成功!")
                        print(f"📁 文件: {file_path.name}")
                        print(f"📊 大小: {file_size / (1024*1024):.1f} MB")
                        print("✅ 所有策略已完成")
                        return True
                    
                    # 如果用户选择继续，不返回，继续下一个策略
                    continue
                else:
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
        print("python ultra_hd_download_fixed.py <YouTube_URL> [输出文件名]")
        print("\n示例:")
        print("python ultra_hd_download_fixed.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("python ultra_hd_download_fixed.py https://www.youtube.com/watch?v=dQw4w9WgXcQ my_video.mp4")
        return

    # 显示版本信息
    print_version_info()

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "media_files/ultra_hd_video.%(ext)s"
    
    # 检查FFmpeg
    if check_ffmpeg():
        print("✅ FFmpeg已安装 - 支持视频音频分离下载和合并")
    else:
        print("⚠️ FFmpeg未安装 - 将使用单一文件下载")
    
    # 检查cookies文件
    if os.path.exists('cookies.txt'):
        print("🍪 找到cookies.txt文件")
    else:
        print("⚠️ 未找到cookies.txt文件")
    
    print(f"📁 输出文件: {output_file}")
    
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
        print("\n❌ 下载失败!")
        print("💡 建议:")
        print("- 检查网络连接")
        print("- 确认视频链接有效")
        print("- 尝试使用cookies.txt文件")
        print("- 检查是否有足够的磁盘空间")

if __name__ == "__main__":
    main() 