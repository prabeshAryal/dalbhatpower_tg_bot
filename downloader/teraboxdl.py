import os
import requests
import random

from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
from rich.console import Console


def download_file(url: str, filename: str) -> bool:
    """Function to download a file from a URL."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_length = int(response.headers.get('content-length', 0))
            downloaded_length = 0
            console = Console()
            with console.status("[bold green]Downloading") as status:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[green]Downloading..", justify="right"),
                    BarColumn(),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                    console=Console(),
                ) as progress:
                    task = progress.add_task("[green]Downloading..", total=total_length)
                    os.makedirs(os.path.dirname(filename)) if not os.path.exists(os.path.dirname(filename)) else None
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                downloaded_length += len(chunk)
                                progress.update(task, advance=len(chunk))
                    progress.stop()
            console.print("[reset]", end="")
            return True
        else:
            print(f"Failed to download file from {url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred while downloading file: {str(e)}")
        return False


def terabox_dlp(link: str) -> tuple:
    """Function to download media from teraboxvideodownloader API."""
    url = f"https://teraboxvideodownloader.nepcoderdevs.workers.dev/?url={link}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Extract necessary data
            resolutions = data["response"][0]["resolutions"]
            fast_download_link = resolutions.get("Fast Download")
            hd_video_link = resolutions.get("HD Video")
            # thumbnail_url = data["response"][0].get("thumbnail")
            video_title = data["response"][0].get("title")
            
            # Download files
            file_list = []
            if fast_download_link:
                filename = f"{video_title}_fast_download.mp4"
                filename = os.path.join(os.getcwd(),'downloads',filename)
                if download_file(fast_download_link, filename):
                    file_list.append(filename) 
            elif hd_video_link:
                filename = f"{video_title}_hd_video.mp4"
                if download_file(hd_video_link, filename):
                    file_list.append(filename)
            
            # Generate caption
            caption = f"Video Title: {video_title}\n"
            
            if file_list:
                return True, caption, file_list
            else:
                return False, None, []
        
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return False, None, []
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False, None, []


# # Example usage:
# link = "https://www.example.com/video_link"
# status, caption, file_list = terabox_dl(link)
# if status:
#     print(f"Download successful. Caption: {caption}")
#     print(f"Files downloaded: {file_list}")
# else:
#     print("Download failed.")
