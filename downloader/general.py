import os
import requests
import time
from downloader_cli.download import Download

import re
import urllib.parse

def shorten_filename(url):
    # Extract the filename from the URL
    filename = url.split('/')[-1]
    
    # Remove URL parameters if any
    filename = filename.split('?')[0]
    
    # Decode URL-encoded characters
    filename = urllib.parse.unquote(filename)
    
    # Define the allowed characters in filenames
    allowed_characters = r'[^a-zA-Z0-9\s._-]'
    
    # Keep only allowed characters
    filename = re.sub(allowed_characters, '', filename)
    
    # Optionally truncate the filename if it's too long (e.g., to 255 characters)
    max_length = 255
    if len(filename) > max_length:
        filename, ext = filename[:max_length - len(filename.split('.')[-1]) - 1], filename.split('.')[-1]
        filename = f"{filename}.{ext}"
    
    return filename


class FileDownloader:
    def __init__(self, download_path=os.path.join(os.getcwd(), 'downloads', 'general')):
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)
        self.max_file_size = 2 * 1024 * 1024 * 1024  # 2 GB in bytes
        self.max_download_time = 5 * 60  # 5 minutes in seconds

    def download_file(self, link):
        try:
            # Extract filename from the link
            filename = shorten_filename(link)
            filepath = os.path.join(self.download_path, filename)
            
            start_time = time.time()
            chunk_size = 8192  # 8 KB
            downloaded_size = 0

            with requests.get(link, stream=True, allow_redirects=True) as response:
                response.raise_for_status()
                with open(filepath, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:  # Filter out keep-alive new chunks
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            
                            # Check download time
                            if time.time() - start_time > self.max_download_time:
                                print("Download exceeded the maximum allowed time of 5 minutes.")
                                file.close()
                                os.remove(filepath)
                                return False, None, []
                            
                            # Check file size
                            if downloaded_size > self.max_file_size:
                                print("Downloaded file exceeds the maximum allowed size of 2 GB.")
                                file.close()
                                os.remove(filepath)
                                return False, None, []

            # Verify the downloaded file size
            downloaded_file_size = os.path.getsize(filepath)
            if downloaded_file_size > self.max_file_size:
                print("Downloaded file exceeds the maximum allowed size of 2 GB.")
                os.remove(filepath)  # Remove the file if it exceeds the limit
                return False, None, []

            # Get the list of downloaded files
            file_list = [os.path.join(self.download_path, f) for f in os.listdir(self.download_path) if os.path.isfile(os.path.join(self.download_path, f))]

            # Check if download is successful
            download_successful = True

            # Prepare the file metadata information
            file_metadata = ""
            if len(file_list) == 1:
                file_name = file_list[0]
                file_size = os.path.getsize(file_name) / (1024 * 1024)  # Convert to MB
                file_extension = os.path.splitext(file_name)[1]

                # Append metadata information in Markdown format
                file_metadata += f"***File Name:*** `{os.path.basename(file_name)}`\n" \
                                 f"***Size:*** {file_size:.2f} MB\n" \
                                 f"***File Type:*** {file_extension}\n\n"
            else:
                return False, None, []

            # Return a summary including check (download_successful), caption, and file metadata
            return download_successful, file_metadata, file_list[0]

        except Exception as e:
            # Handle any exceptions that may occur during download
            print(f"Failed to download {link}: {str(e)}")
            return False, None, []

# # Example usage
# if __name__ == "__main__":
#     downloader = FileDownloader()
#     success, metadata, file_path = downloader.download_file("https://ash-speed.hetzner.com/100MB.bin")
#     if success:
#         print(metadata)
