import asyncio
import os
import re
import json
import yt_dlp
from typing import Union, Optional, Tuple
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch
import logging
import random
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DOWNLOAD_FOLDER = "downloads"
MAX_RETRIES = 3
RETRY_DELAY = 2
MAX_FILE_SIZE_MB = 250  # Maximum allowed file size in MB

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def cookie_txt_file() -> Optional[str]:
    """Get a random cookie file from cookies directory"""
    cookie_dir = os.path.join(os.getcwd(), "cookies")
    if not os.path.exists(cookie_dir):
        return None
    
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        return None
    
    return os.path.join(cookie_dir, random.choice(cookies_files))

def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from URL"""
    patterns = [
        r"youtube\.com/watch\?v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"youtube\.com/embed/([^/]+)",
        r"youtube\.com/v/([^/]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

async def download_with_yt_dlp(
    link: str, 
    media_type: str, 
    format_id: Optional[str] = None,
    title: Optional[str] = None
) -> Optional[str]:
    """Download media using yt-dlp with cookies"""
    cookie_file = cookie_txt_file()
    if not cookie_file:
        logger.warning("No cookies found. Some videos may not download.")
    
    video_id = extract_video_id(link) or link.split('v=')[-1].split('&')[0]
    
    # Check cache first
    ext = "mp3" if media_type == "audio" else "mp4"
    file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.{ext}")
    if os.path.exists(file_path):
        logger.info(f"Using cached file: {file_path}")
        return file_path
    
    ydl_opts = {
        "format": "bestaudio/best" if media_type == "audio" else "bestvideo[height<=720]+bestaudio",
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, f"{video_id}.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }
    
    if cookie_file:
        ydl_opts["cookiefile"] = cookie_file
    
    if media_type == "audio":
        ydl_opts["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    if format_id and title:
        ydl_opts["format"] = format_id
        ydl_opts["outtmpl"] = os.path.join(DOWNLOAD_FOLDER, title)
        if media_type == "audio":
            ydl_opts["outtmpl"] += ".%(ext)s"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, link, download=True)
            ext = "mp3" if media_type == "audio" else info['ext']
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.{ext}")
            
            if os.path.exists(file_path):
                return file_path
    except Exception as e:
        logger.error(f"Failed to download {media_type}: {str(e)}")
    
    return None

async def get_stream_url(link: str, media_type: str) -> Optional[str]:
    """Get streaming URL using yt-dlp"""
    cookie_file = cookie_txt_file()
    if not cookie_file:
        logger.warning("No cookies found. Some videos may not stream.")
    
    ydl_opts = {
        "format": "bestaudio/best" if media_type == "audio" else "bestvideo[height<=720]+bestaudio",
        "quiet": True,
        "no_warnings": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }
    
    if cookie_file:
        ydl_opts["cookiefile"] = cookie_file
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, link, download=False)
            return info.get('url')
    except Exception as e:
        logger.error(f"Failed to get stream URL: {str(e)}")
        return None

async def download_song(link: str) -> Optional[str]:
    """Download audio from YouTube"""
    return await download_with_yt_dlp(link, "audio")

async def download_video(link: str) -> Optional[str]:
    """Download video from YouTube"""
    return await download_with_yt_dlp(link, "video")

async def check_file_size(link: str) -> Optional[int]:
    """Check total file size of all formats"""
    cookie_file = cookie_txt_file()
    if not cookie_file:
        logger.warning("No cookies found. Cannot check file size.")
        return None
    
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "cookiefile": cookie_file,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, link, download=False)
            formats = info.get('formats', [])
            total_size = sum(f.get('filesize', 0) for f in formats)
            return total_size
    except Exception as e:
        logger.error(f"Failed to check file size: {str(e)}")
        return None

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None) -> bool:
        if videoid:
            link = self.base + link
        return re.search(self.regex, link) is not None

    async def url(self, message_1: Message) -> Optional[str]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset:entity.offset + entity.length]
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None) -> Tuple[str, str, int, str, str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        results = VideosSearch(link, limit=1)
        result = (await results.next())["result"][0]
        
        title = result["title"]
        duration_min = result["duration"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        vidid = result["id"]
        duration_sec = 0 if str(duration_min) == "None" else int(time_to_seconds(duration_min))
        
        return title, duration_min, duration_sec, thumbnail, vidid

    async def video(self, link: str, videoid: Union[bool, str] = None) -> Tuple[int, str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        # Try to get streaming URL first
        stream_url = await get_stream_url(link, "video")
        if stream_url:
            return 1, stream_url
        
        # Fall back to download if streaming not available
        file_path = await download_video(link)
        return (1, file_path) if file_path else (0, "Failed to download video")

    async def playlist(self, link: str, limit: int, user_id: int, videoid: Union[bool, str] = None) -> List[str]:
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        
        cookie_file = cookie_txt_file()
        if not cookie_file:
            return []
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "cookiefile": cookie_file,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, link, download=False)
                entries = info.get('entries', [])
                return [entry['id'] for entry in entries[:limit] if 'id' in entry]
        except Exception as e:
            logger.error(f"Failed to get playlist: {str(e)}")
            return []

    async def track(self, link: str, videoid: Union[bool, str] = None) -> Tuple[dict, str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        results = VideosSearch(link, limit=1)
        result = (await results.next())["result"][0]
        
        track_details = {
            "title": result["title"],
            "link": result["link"],
            "vidid": result["id"],
            "duration_min": result["duration"],
            "thumb": result["thumbnails"][0]["url"].split("?")[0],
        }
        return track_details, result["id"]

    async def formats(self, link: str, videoid: Union[bool, str] = None) -> Tuple[List[dict], str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        cookie_file = cookie_txt_file()
        if not cookie_file:
            return [], link
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "cookiefile": cookie_file,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, link, download=False)
                formats = []
                for f in info.get('formats', []):
                    try:
                        if not "dash" in str(f.get("format", "")).lower():
                            formats.append({
                                "format": f.get("format"),
                                "filesize": f.get("filesize"),
                                "format_id": f.get("format_id"),
                                "ext": f.get("ext"),
                                "format_note": f.get("format_note"),
                                "yturl": link,
                            })
                    except:
                        continue
                return formats, link
        except Exception as e:
            logger.error(f"Failed to get formats: {str(e)}")
            return [], link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ) -> Tuple[str, str, str, str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        
        results = VideosSearch(link, limit=10)
        result = (await results.next()).get("result")
        selected = result[query_type]
        
        return (
            selected["title"],
            selected["duration"],
            selected["thumbnails"][0]["url"].split("?")[0],
            selected["id"]
        )

    async def download(
        self,
        link: str,
        mystic,
        video: bool = False,
        videoid: Union[bool, str] = None,
        songaudio: bool = False,
        songvideo: bool = False,
        format_id: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Tuple[Optional[str], bool]:
        """
        Download media and return (file_path_or_url, is_local_file)
        """
        if videoid:
            link = self.base + link
        
        if songvideo or songaudio:
            # Handle song downloads
            file_path = await download_with_yt_dlp(link, "audio", format_id, title)
            return (file_path, True) if file_path else (None, False)
        elif video:
            # Try to get streaming URL first
            stream_url = await get_stream_url(link, "video")
            if stream_url:
                return stream_url, False
            
            # Fall back to download if streaming not available
            file_path = await download_with_yt_dlp(link, "video", format_id, title)
            return (file_path, True) if file_path else (None, False)
        else:
            # Default to audio download
            file_path = await download_with_yt_dlp(link, "audio", format_id, title)
            return (file_path, True) if file_path else (None, False)

