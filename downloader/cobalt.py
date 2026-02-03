import requests
import json
import os
import re
import hashlib
import time
import random
import mimetypes
from typing import Union, List, Tuple, Optional, Dict, Any
from urllib.parse import quote

# --- Helper Functions ---

def random_filename_hash() -> str:
    """Generates a short, random filename hash."""
    return hashlib.sha256(f"{time.time()}_{random.random()}".encode()).hexdigest()[:16]

def remove_file_safely(filepath: Optional[str]):
    """Removes a file if it exists, ignoring FileNotFoundError."""
    if not filepath:
        return
    try:
        os.remove(os.path.realpath(filepath))
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error removing file {filepath}: {e}")

# --- Title Extraction (Refined) ---

class TiktokTitleExtractor:
    """A refined TikTok Title extraction module."""

    @staticmethod
    def fetch_video_data(url: str) -> Dict[str, Any]:
        """Fetches video data using the douyin.wtf API with error handling."""
        api_url = f"https://douyin.wtf/api/hybrid/video_data?url={quote(url)}&minimal=false"
        try:
            response = requests.get(api_url, headers={'accept': 'application/json'}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Could not fetch TikTok data: {e}")
            return {}

    @staticmethod
    def extract_title(link: str) -> str:
        """Extracts and formats the title from the TikTok API response."""
        data = TiktokTitleExtractor.fetch_video_data(link)
        
        author_data = data.get("data", {}).get("author", {})
        nickname = author_data.get("nickname", "")
        unique_id = author_data.get("uniqueId", "")
        
        post_data = data.get("data", {})
        title = post_data.get("imagePost", {}).get("title", "")
        description = post_data.get("desc", "")

        # Determine the main caption content
        cap = description
        if title and description:
            cap = f"{title}\n\n{description}"
        elif title:
            cap = title
        elif not description:
            cap = "✨"
        
        # Format the author line
        author_line = ""
        if nickname and unique_id:
            author_line = f"{nickname} ({unique_id})"
        elif nickname or unique_id:
            author_line = nickname or unique_id
            
        return f"{author_line}\n\n{cap}".strip() if author_line else cap.strip()

# --- Main Downloader Class ---

class cobalt:
    """
    A robust media downloader using the Cobalt API.
    It cycles through multiple API instances for increased reliability.
    """

    # List of available Cobalt API endpoints
    API_ENDPOINTS = [
        "https://api.cobalt.blackcat.sweeux.org/",
        "https://cobalt-api.kwiatekmiki.com/",
        "https://cobalt-api.meowing.de/"
    ]

    def __init__(self, link: str, audio: bool = False) -> None:
        """
        Initializes the downloader with the target link and options.

        :param str link: The URL of the media to download.
        :param bool audio: If True, downloads only the audio (sets downloadMode to 'audio').
        """
        self.link = link
        self.audio = audio
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
        # Construct the request body based on whether audio only is requested
        if self.audio:
            self.body = {
                "url": self.link,
                "downloadMode": "audio",
                "audioFormat": "mp3",
                "audioBitrate": "128",
                "filenameStyle": "pretty",
                "tiktokFullAudio": True,
            }
        else:
            self.body = {
                "url": self.link,
                "videoQuality": "max",
                "filenameStyle": "pretty",
                "youtubeVideoCodec": "h264",
                "allowH265": True
            }

    def _get_page_title(self) -> str:
        """
        Extracts the page title from the URL. Supports TikTok, YouTube, and generic pages.
        Returns the original link as a fallback.
        """
        # TikTok
        if re.match(r"((https?:\/\/)?(((www.)?tiktok\.com\/@[-a-z\.A-Z0-9_]+\/(video|photo)\/\d+)|(vt\.tiktok\.com\/[-a-zA-Z0-9]+)))", self.link):
            return TiktokTitleExtractor.extract_title(self.link)
        
        # YouTube (Note: API key method removed for simplicity and to avoid external dependencies)
        if re.match(r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$", self.link):
            try:
                # A simpler method to get title without API key
                response = requests.get(f"https://noembed.com/embed?url={self.link}")
                response.raise_for_status()
                data = response.json()
                if data and "title" in data:
                    return data["title"]
            except (requests.RequestException, json.JSONDecodeError) as e:
                print(f"Could not fetch YouTube title via oEmbed: {e}")

        # Generic Fallback
        try:
            response = requests.get(self.link, timeout=10)
            response.raise_for_status()
            if title_match := re.search(r"<title>(.*?)<\/title>", response.text, re.IGNORECASE):
                return title_match.group(1).strip()
        except requests.RequestException as e:
            print(f"Could not fetch generic page title: {e}")
            
        return self.link # Fallback to the link itself

    def _download_file(self, url: str, directory: str) -> Optional[str]:
        """
        Downloads a single file from a URL using requests.
        This replaces the original platform-dependent `lynx` and `file` implementation.

        :param str url: The URL of the file to download.
        :param str directory: The directory to save the file in.
        :return: The full path to the downloaded file, or None if download failed.
        """
        os.makedirs(directory, exist_ok=True)
        
        try:
            with requests.get(url, stream=True, timeout=20) as r:
                r.raise_for_status()
                
                # Determine filename
                filename = random_filename_hash()
                if cd := r.headers.get('content-disposition'):
                    if filename_match := re.search(r'filename="?([^"]+)"?', cd):
                        filename = os.path.basename(filename_match.group(1))

                # Determine extension
                base_filename, ext = os.path.splitext(filename)
                if not ext:
                    content_type = r.headers.get('content-type')
                    extension = mimetypes.guess_extension(content_type) if content_type else '.mp4'
                    final_filepath = os.path.join(directory, f"{base_filename}{extension or '.bin'}")
                else:
                    final_filepath = os.path.join(directory, filename)

                # Download the file
                with open(final_filepath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"Successfully downloaded: {final_filepath}")
                return final_filepath

        except requests.RequestException as e:
            print(f"Failed to download media from {url}. Error: {e}")
            return None


    def download(self) -> Tuple[Union[bool, str], Optional[str], List[str]]:
        """
        Attempts to download media by posting to a randomly selected cobalt API endpoint, retrying up to 3 times.

        :return: A tuple containing (status, caption, list_of_filepaths).
                 - status: 'redirect', 'picker', 'stream' on success, False on failure.
                 - caption: The extracted media caption/title.
                 - list_of_filepaths: A list of paths to the downloaded files.
        """
        import logging
        import random
        attempts = 0
        max_attempts = 3
        api_response = None
        last_error = None
        while attempts < max_attempts:
            api_endpoint = random.choice(self.API_ENDPOINTS)
            try:
                logging.info(f"Attempting to use API: {api_endpoint}")
                response = requests.post(
                    url=api_endpoint,
                    headers=self.headers,
                    data=json.dumps(self.body),
                    timeout=15
                )
                if response.status_code == 200:
                    api_response = response.json()
                    logging.info(f"API success from {api_endpoint}")
                    break
                else:
                    last_error = f"API {api_endpoint} returned status {response.status_code}: {response.text[:100]}"
                    logging.error(last_error)
            except requests.RequestException as e:
                last_error = f"API {api_endpoint} failed: {e}"
                logging.error(last_error)
            attempts += 1

        if not api_response:
            logging.error(f"Cobalt API endpoint failed after {max_attempts} attempts. Last error: {last_error}")
            return False, None, []

        status = api_response.get("status")
        if not status or status == "error":
            logging.error(f"API responded with an error: {api_response.get('error', 'Unknown error')}")
            return False, None, []

        download_list = []
        if status in ["redirect", "tunnel"]:
            download_list.append(api_response["url"])
        elif status == "picker":
            download_list = [item["url"] for item in api_response.get("picker", [])]
            if audio_url := api_response.get("audio"):
                logging.info("Found separate audio track for slideshow.")
                download_list.append(audio_url)
        elif status == "local-processing":
            download_list = api_response.get("tunnel", [])

        if not download_list:
            logging.error("API response did not contain any downloadable links.")
            return False, None, []

        # Get caption
        logging.info("Extracting caption...")
        caption = self._get_page_title()

        # Download all media files
        logging.info(f"Downloading {len(download_list)} file(s)...")
        filepaths = [self._download_file(url, "downloads") for url in download_list]
        successful_downloads = [fp for fp in filepaths if fp]

        if not successful_downloads:
            logging.error("All file downloads failed.")
            return False, caption, []

        return status, caption, successful_downloads


if __name__ == '__main__':
    # --- Example Usage ---
    # This block will only run when the script is executed directly.
    
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )

    test_links = [
"https://www.instagram.com/p/DOImrGikw1g/?igsh=YnRldnV5Ym94eWFx"
    ]

    selected_link = random.choice(test_links)
    logging.info(f"Testing with link: {selected_link}")

    downloader = CobaltDownloader(selected_link)
    download_status, media_caption, file_list = downloader.download()

    logging.info("DOWNLOAD PROCESS COMPLETE")
    logging.info(f"Status: {download_status}")
    logging.info(f"Caption: {media_caption}")
    logging.info(f"Files Downloaded ({len(file_list)}):")
    for f in file_list:
        logging.info(f"- {f}")

