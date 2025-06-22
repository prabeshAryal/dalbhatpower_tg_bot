import requests
import json
import os
import re
from urllib.parse import quote
# Assuming you have this loader utility. If not, remove or replace Loader calls.
try:
    from utils.loader import Loader 
except ImportError:
    # Simple placeholder if Loader is not available
    class Loader:
        def __init__(self, start_msg="", end_msg="", delay=0.1):
            self.start_msg = start_msg
            self.end_msg = end_msg
            self.is_running = False
            print(start_msg) # Print start message immediately

        def __enter__(self):
            self.start()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.stop()
            if exc_type is None:
                print(self.end_msg) # Print end message only on success

        def start(self):
            self.is_running = True
            # print(self.start_msg) # Already printed in init

        def stop(self):
            self.is_running = False
            # print(self.end_msg) # Printed in __exit__

        @property
        def message(self):
            return self._message
        
        @message.setter
        def message(self, value):
            self._message = value
            # You could add print logic here if needed for updates
            # print(f"\r{value}", end="")


class tt_dlp(object):
    """A Tiktok Downloader Module using douyin.wtf API
       Handles both videos and image posts (carousels).

    usage:
    instance = tt_dlp(link)
    status, caption, filelist = instance.download()

    status: bool - True if download successful, False otherwise.
    caption: str - Formatted caption of the video/post.
    filelist: list - List of absolute file paths to downloaded media.
    """

    def __init__(self, link) -> None:
        self.link = link
        # API endpoint using the provided structure
        self.api_base = "https://douyin.wtf/api/hybrid/video_data"
        self.headers = {'accept': 'application/json'}

    def _fetch_video_data(self):
        """Fetch video/post data using the douyin.wtf API."""
        try:
            api_url = f"{self.api_base}?url={quote(self.link)}&minimal=false"
            # Use Loader context manager for cleaner start/end messages
            with Loader(f"Requesting API for {self.link}", "API Response Received✅"):
                response = requests.get(api_url, headers=self.headers, timeout=30)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            data = response.json()
            # Check API-level success code
            if data.get("code") != 200:
                print(f"\nAPI Error: Code {data.get('code')}, Message: {data.get('message', 'Unknown error')}")
                return None

            return data.get("data") # Return the actual data payload

        except requests.exceptions.Timeout:
            print(f"\nError: API request timed out for {self.link}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"\nError fetching data from API: {e}")
            return None
        except json.JSONDecodeError:
            print(f"\nError: Could not decode JSON response from API.")
            return None

    def _extract_caption(self, data):
        """Extract and format the caption from the fetched data."""
        if not data:
            return "✨" # Default caption if no data

        author_info = data.get("author", {})
        nickname = author_info.get("nickname", "")
        unique_id = author_info.get("unique_id", "") 

        description = data.get("desc", "")
        # image_title = data.get("imagePost", {}).get("title", "") # This seems unreliable
        
        content_caption = description if description else "✨" # Default if no desc

        # Format the final caption
        author_part = ""
        if nickname and unique_id:
            author_part = f"{nickname} (@{unique_id})"
        elif nickname:
            author_part = nickname
        elif unique_id:
            author_part = f"@{unique_id}"

        if author_part:
            formatted_caption = f"{author_part}\n\n{content_caption}"
        else:
            formatted_caption = content_caption

        # Add hashtags from text_extra if present
        hashtags = []
        text_extra = data.get("text_extra", [])
        if text_extra:
            for item in text_extra:
                if item.get("type") == 1 and item.get("hashtag_name"): # Type 1 is hashtag
                    hashtags.append(f"#{item['hashtag_name']}")
    
        if hashtags:
            # Append hashtags neatly, checking if caption needs newline
            if formatted_caption and formatted_caption != "✨":
                # Check if description was already added and might contain hashtags
                if not any(tag in content_caption for tag in hashtags):
                    formatted_caption += "\n\n" + " ".join(hashtags)
            else: # If caption was just author or default, add hashtags
                formatted_caption += "\n\n" + " ".join(hashtags)
        
        return formatted_caption.strip() # Remove leading/trailing whitespace


    def _extract_download_info(self, data):
        """Extract download URLs and determine content type (image or video)."""
        if not data:
            return None, None, None

        aweme_id = data.get("aweme_id")

        # --- Image Post Check ---
        image_post_data = data.get("image_post_info")
        if image_post_data and isinstance(image_post_data.get("images"), list):
            image_urls = []
            for image_item in image_post_data["images"]:
                display_image_info = image_item.get("display_image")
                if display_image_info and display_image_info.get("url_list"):
                    # Prefer display_image (seems non-watermarked)
                    url = display_image_info["url_list"][0] # Take the first one
                    if url.startswith(('http://', 'https://')):
                        image_urls.append(url)
                    else:
                        print(f"\nWarning: Skipping invalid image URL: {url}")
                # Add fallback here if needed (e.g., check 'thumbnail' or others if 'display_image' fails)
                # else:
                #     thumbnail_info = image_item.get("thumbnail") 
                #     # ... etc

            if image_urls:
                print(f"\nFound {len(image_urls)} images in post.")
                return image_urls, 'image', aweme_id

        # --- Video Check (Fallback) ---
        video_info = data.get("video")
        if video_info:
            # Prioritize non-watermarked play_addr
            play_addr = video_info.get("play_addr")
            if play_addr and play_addr.get("url_list"):
                valid_urls = [url for url in play_addr.get("url_list") if url.startswith(('http://', 'https://'))]
                if valid_urls:
                    print("\nFound video stream.")
                    return [valid_urls[0]], 'video', aweme_id # Return first valid play URL

            # Fallback to watermarked download_addr if play_addr fails
            download_addr = video_info.get("download_addr")
            if download_addr and download_addr.get("url_list"):
                valid_urls = [url for url in download_addr.get("url_list") if url.startswith(('http://', 'https://'))]
                if valid_urls:
                    print("\nWarning: Using video download_addr, might be watermarked.")
                    return [valid_urls[0]], 'video', aweme_id

        # --- No media found ---
        print("\nError: No suitable video or image download links found in API response.")
        return None, None, aweme_id # Return aweme_id even if no links found

    def _download_media_file(self, url, content_type, base_filename):
        """Downloads a single media file."""
        try:
            with Loader(f"Downloading {base_filename}...", "", 0.05) as dl_loader:
                response = requests.get(url, allow_redirects=True, stream=True, timeout=60)
                response.raise_for_status()

                # Determine extension
                extension = ".mp4" # Default for video
                if content_type == 'image':
                    # Try to get from URL, default to jpg
                    url_path = url.split('?')[0].lower()
                    if '.jpeg' in url_path or '.jpg' in url_path:
                        extension = ".jpg"
                    elif '.png' in url_path:
                        extension = ".png"
                    elif '.webp' in url_path:
                        extension = ".webp"
                    else:
                        # Check Content-Type header as a fallback
                        content_type_header = response.headers.get('Content-Type', '').lower()
                        if 'image/jpeg' in content_type_header:
                            extension = ".jpg"
                        elif 'image/png' in content_type_header:
                            extension = ".png"
                        elif 'image/webp' in content_type_header:
                            extension = ".webp"
                        else:
                            extension = ".jpg" # Final fallback for images

                # Sanitize base_filename
                safe_filename = re.sub(r'[\\/*?:"<>|]', "", str(base_filename))
                filename = f"{safe_filename}{extension}"
                download_path = os.path.join("downloads", filename)

                os.makedirs("downloads", exist_ok=True)

                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                bytes_downloaded = 0

                with open(download_path, "wb") as file:
                    for data_chunk in response.iter_content(block_size):
                        file.write(data_chunk)
                        bytes_downloaded += len(data_chunk)
                        # Update loader progress (optional visual feedback)
                        if total_size > 0:
                            progress = (bytes_downloaded / total_size) * 100
                            # Update the message in the loader if it supports it
                            # dl_loader.message = f"Downloading {filename} ({progress:.1f}%)" 

            print(f"Downloaded {filename} ✅") # Print success per file
            return os.path.abspath(download_path)

        except requests.exceptions.Timeout:
            print(f"\nError: Timeout while downloading {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"\nError downloading {url}: {e}")
            return None
        except IOError as e:
            print(f"\nError writing file {download_path}: {e}")
            return None


    def download(self):
        """Fetches data, extracts info, and downloads media."""
        fetched_data = self._fetch_video_data()

        if not fetched_data:
            return False, "Could not fetch video data.", []

        caption = self._extract_caption(fetched_data)
        download_urls, content_type, aweme_id = self._extract_download_info(fetched_data)

        if not aweme_id:
            aweme_id = "tiktok_media_" + str(hash(self.link))[:8]

        if not download_urls or not content_type:
            print(f"\nCould not find downloadable media for {aweme_id}.")
            # Return True for caption success, but False for overall download status
            return False, caption, []

        # --- Download Files ---
        downloaded_files = []
        total_files = len(download_urls)
        print(f"Attempting to download {total_files} {content_type}(s)...")

        for i, url in enumerate(download_urls):
            # Add index only if multiple files
            filename_base = f"{aweme_id}_{i+1}" if total_files > 1 else aweme_id
            filepath = self._download_media_file(url, content_type, filename_base)
            if filepath:
                downloaded_files.append(filepath)
            else:
                print(f"Failed to download item {i+1} ({url})")


        if not downloaded_files:
            print(f"\nAll downloads failed for {aweme_id}.")
            return False, caption, []

        if len(downloaded_files) < total_files:
            print(f"\nWarning: Only downloaded {len(downloaded_files)} out of {total_files} items.")
            # Decide if partial success is True or False. Let's return True if at least one file downloaded.
            return True, caption, downloaded_files 

        # Full Success
        print(f"\nSuccessfully downloaded {len(downloaded_files)} {content_type}(s).")
        return True, caption, downloaded_files


# # --- Example Usage ---
# if __name__ == "__main__":
#     test_links = [
#         # Video Example (from previous tests)
#         "https://www.tiktok.com/@purnimaneupane01/video/7490912020192120082", 
#         # Image Post Example (using aweme_id from your image JSON)
#         "https://www.tiktok.com/@deepty.chettri/photo/7485351923801967890", 
#         # Another Image Post Example Link
#         "https://www.tiktok.com/@tiktok/photo/7340652633445879042",
#         # Failing URL
#         "https://invalid.url/test" 
#     ]

#     for link in test_links:
#         print("=" * 50)
#         print(f"Processing Link: {link}")
#         print("-" * 50)
#         instance = tt_dlp(link)
#         status, caption, filelist = instance.download()

#         print("\n--- Download Results ---")
#         print(f"Overall Status: {status}")
#         print(f"Extracted Caption:\n{caption}")
#         print(f"Downloaded File List: {filelist}")
#         print("=" * 50 + "\n")