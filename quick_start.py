#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 超高清视频下载器 - Python启动器
避免批处理文件编码问题
"""

import sys
import os

def print_header():
    """打印标题"""
    print("🎬 YouTube 超高清视频下载器 v1.1")
    print("📅 修复版本 (解决文件查找问题)")
    print("=" * 50)
    print()
    print("💡 修复内容:")
    print("- 修复了'命令成功但文件未找到'的问题")
    print("- 改进了文件查找逻辑")
    print("- 使用自定义进度条显示")
    print()

def get_user_input():
    """获取用户输入"""
    # 获取URL
    while True:
        url = input("请输入YouTube视频链接: ").strip()
        if url:
            break
        print("❌ 请输入有效的链接")
    
    # 获取自定义文件名
    custom_name = input("请输入自定义文件名 (直接回车使用默认名称): ").strip()
    
    return url, custom_name

def main():
    """主函数"""
    print_header()
    
    try:
        # 获取用户输入
        url, custom_name = get_user_input()
        
        print()
        print("正在下载视频 (修复版本)...")
        print()
        
        # 导入下载器模块
        try:
            from ultra_hd_download_fixed import download_ultra_hd_video
            
            # 执行下载
            if custom_name:
                success = download_ultra_hd_video(url, custom_name)
            else:
                success = download_ultra_hd_video(url)
            
            if success:
                print()
                print("🎉 下载成功完成!")
            else:
                print()
                print("❌ 下载失败!")
                
        except ImportError:
            print("❌ 错误: 无法导入下载器模块")
            print("请确保 ultra_hd_download_fixed.py 在同一目录")
        except Exception as e:
            print(f"❌ 下载错误: {e}")
    
    except KeyboardInterrupt:
        print()
        print("⏹️ 用户取消下载")
    except Exception as e:
        print(f"❌ 程序错误: {e}")
    
    print()
    input("按回车键退出...")

if __name__ == "__main__":
    main() 