"""
YouTube 超高清视频下载器
版本: v1.0
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "YouTube超高清视频下载器 - 支持进度条显示和音频合并"

from .ultra_hd_downloader import main, download_ultra_hd_video

__all__ = ['main', 'download_ultra_hd_video']
