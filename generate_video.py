#!/usr/bin/env python3
"""
Advanced YouTube Downloader with multiple methods
"""

import yt_dlp
import pytube
import os
from pathlib import Path

class AdvancedYouTubeDownloader:
    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def method_ytdlp_best(self, url):
        """Method 1: yt-dlp best quality"""
        ydl_opts = {
            'outtmpl': str(self.output_dir / 'ytdlp_best_%(title)s.%(ext)s'),
            'format': 'best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def method_ytdlp_720p(self, url):
        """Method 2: yt-dlp 720p"""
        ydl_opts = {
            'outtmpl': str(self.output_dir / 'ytdlp_720p_%(title)s.%(ext)s'),
            'format': 'best[height<=720]',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def method_ytdlp_audio(self, url):
        """Method 3: yt-dlp audio only"""
        ydl_opts = {
            'outtmpl': str(self.output_dir / 'ytdlp_audio_%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    
    def method_pytube_hd(self, url):
        """Method 4: Pytube HD"""
        yt = pytube.YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=str(self.output_dir), filename='pytube_hd_video')
    
    def method_pytube_audio(self, url):
        """Method 5: Pytube audio"""
        yt = pytube.YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=str(self.output_dir), filename='pytube_audio')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python advanced_downloader.py <YouTube_URL>")
        sys.exit(1)
    
    downloader = AdvancedYouTubeDownloader()
    url = sys.argv[1]
    
    # Execute all methods
    methods = [
        downloader.method_ytdlp_best,
        downloader.method_ytdlp_720p,
        downloader.method_ytdlp_audio,
        downloader.method_pytube_hd,
        downloader.method_pytube_audio,
    ]
    
    for method in methods:
        try:
            print(f"Executing {method.__name__}...")
            method(url)
            print(f"✓ {method.__name__} completed")
        except Exception as e:
            print(f"✗ {method.__name__} failed: {e}")
