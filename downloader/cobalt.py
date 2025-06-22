import requests, json, os,re
from utils.loader import Loader
from urllib.parse import quote
from typing import Union, Dict, Tuple, Any

import mimetypes
import random
import subprocess

import hashlib
import time
import random

random_filename_hash = lambda: hashlib.sha256(f"{time.time()}_{random.random()}".encode()).hexdigest()[:16]

def remove_file_safely(filepath: str):
    try:
        os.remove(os.path.realpath(filepath))
    except FileNotFoundError:
        pass

class cobalt(object):
    """An Tiktok Downloader Module You Can't Ignore

    usage:
    tt_dlp(link) : returns bool, caption, filepath_list
    Type = Post-Video, Post-Image, Carousel, Public-Story, None"""

    def __init__(self, link, audio=False) -> None:
        # self.link = link
        self.method = "cobalt"
        self.link = link
        self.audio = audio
        self.headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            }
        self.body = (
        {
            "url": link,
            "videoQuality": "max",
            "filenameStyle": "pretty",
            "youtubeVideoCodec":"h264",
            "tiktokH265":True
        }
        if self.audio == False
        else {
            "url": link,
            "downloadMode": 'audio',
            "audioFormat": "mp3",
            "tiktokFullAudio": True,
            "filenameStyle": "pretty",
        }
    )
        # self.api = "https://kityune.imput.net/api/json"
        # self.api= "https://olly.imput.net/api/json"
        # self.api= "http://146.190.137.147:9000/"
        # self.api ="https://c.blahaj.ca/"
        # https://api.cobalt.tools/api/serverInfo
        # api_list = ["https://cobalt-7.kwiatekmiki.com/api/serverInfo","https://cobalt-api.kwiatekmiki.com/", "https://cobalt.api.timelessnesses.me/", "https://cobalt-us.kwiatekmiki.com/", "https://dl.khyernet.xyz/", "https://cobalt-backend.canine.tools/", "https://downloadapi.stuff.solutions/api/serverInfo", "https://api.co.rooot.gay/"]
        self.api = "https://cobalt-api.kwiatekmiki.com/"

    def get_page_title(self, url):
        if re.match(r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$",url):
            import requests
            get_youtube_title = lambda url: (lambda yt_api_key=os.getenv('YT_APIV2'), video_id=re.search(r"(?:v=|shorts/|.be/)([^&?/]+)", url).group(1): requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={yt_api_key}").json()['items'][0]['snippet']['title'] if video_id else None)() if re.search(r"(?:v=|shorts/|.be/)([^&?/]+)", url) else None
            title = get_youtube_title(url)
        elif re.match(r"((https:\/\/)?(((www.)?tiktok\.com\/@[-a-z\.A-Z0-9_]+\/(video|photo)\/\d+)|(vt\.tiktok\.com\/[-a-zA-Z0-9]+)))",url):
            title = Tiktok_Title_Extractor.title_extractor(url)
        else:
            import requests
            title = (
                lambda r: (
                    r.text.split("<title>")[1].split("</title>")[0]
                    if "<title>" in r.text
                    else None
                )
            )(requests.get(url))
        return title

    def get_valid_filename(self, url: str) -> Union[None, str]:
        """
        Fetches the filename provided by the server in the Content-Disposition header.
        
        :param str url: The URL to fetch the filename from.
        :return str: The filename provided by the server or None if not found.
        """
        try:
            # Send a HEAD request to the URL to get the headers
            response = requests.head(url, allow_redirects=True)
            
            # Check if 'Content-Disposition' header is present
            if 'Content-Disposition' in response.headers:
                # Extract the filename from the 'Content-Disposition' header
                filename_match = re.search(r'filename="?(?P<filename>[^"]+)"?', response.headers['Content-Disposition'])
                if filename_match:
                    return filename_match.group("filename")
            else:
                return random_filename_hash()
                
                return mini_hash()
            # If no filename found in headers, return None
            print(f"Cannot find specific filename from URL headers: {url}, skipped!")
            return None
        
        except requests.RequestException as e:
            print(f"Error fetching headers for {url}: {e}")
            return None
    
        
    def download_media(self, url, directory=os.path.join(os.getcwd(), "downloads")):
        try:
            # # Extract a base filename from the URL
            # raw_filename = re.split(r"[\|\+\/]+", urlparse(url).path)[-2]
            # base_filename, _ = os.path.splitext(
            #     raw_filename
            # )  # Ignore the extension in URL
            base_filename = self.get_valid_filename(url)
            # Ensure the directory exists
            os.makedirs(directory, exist_ok=True)

            # Temporary file path to save the downloaded content
            temp_file_path = os.path.join(directory, base_filename)

            # Use lynx to download the content
            result = subprocess.run(["lynx", "-source", url], capture_output=True)
            result.check_returncode()

            # Save the content to a temporary file
            with open(temp_file_path, "wb") as file:
                file.write(result.stdout)

            # Detect the file type using the `file` command
            mime_type = subprocess.run(
                ["file", "--mime-type", "-b", temp_file_path],
                capture_output=True,
                text=True,
            ).stdout.strip()
            extension = mimetypes.guess_extension(mime_type)

            # If an extension is detected, rename the file with the correct extension
            if extension:
                final_file_path = f"{temp_file_path}{extension}"
                os.rename(temp_file_path, final_file_path)
            else:
                # Default to .bin if unknown
                if not temp_file_path.endswith(("mp4","jpeg","jpg","mp3","mkv", "avc")):
                    final_file_path = f"{temp_file_path}.mp4"
                    os.rename(temp_file_path, final_file_path)
                else:
                    final_file_path=temp_file_path
            
            if os.path.realpath(final_file_path):
                return final_file_path
            else:
                print(
                    f"Video wasn't downloaded for some reasons : \n\t{url}\n\tFilepath:{final_file_path} "
                )
                remove_file_safely(final_file_path)
                return False
            
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
        except FileNotFoundError as e:
            print(f"Executable not found: {e}")
        except OSError as e:
            print(f"OS error: {e}")

    def here_we_download(self, all_links):
        filepath = []
        for media_link in all_links:
            file = self.download_media(media_link)
            if file:
                filepath.append(file)
            else:
                remove_file_safely(file)
        return filepath

    def download(self):
        try:
            # with Loader("Requesting API....", "API Response Received✅"):
            response = requests.post(
                self.api, headers=self.headers, data=json.dumps(self.body)
            )
            # print(response)
            # print(response.text)

            if response.status_code == 200:
                mydict = response.json()
                typeofcontent = mydict["status"]


                if typeofcontent == "redirect" or typeofcontent == "stream":
                    download_list = [mydict["url"]]
                elif typeofcontent == "picker":
                    download_list = [obj["url"] for obj in mydict["picker"]]
                else:
                    download_list = [mydict["url"]]
                with Loader("Getting Caption", "Caption Extracted ✅"):
                    CAPTION = self.get_page_title(self.link)

                with Loader(
                    f"Downloading {len(download_list)} Files",
                    f"Downloaded {len(download_list)} Files ✅",
                ):
                    files = self.here_we_download(download_list)
                    if len(files)>0:
                        return typeofcontent, CAPTION, files
            else:
                print("\nAPI responded failure: " + str(response.status_code))
                # print(response.text)
                # print(mydict)
                return False, None, []
        except Exception as e:
            print(e)
            print("main exception occurred")
            return False, None, []


class Tiktok_Title_Extractor:
    """A Tiktok Title extraction Module"""

    @staticmethod
    def fetch_video_data(url):
        """Fetch video data using the provided API."""
        response = requests.get(
            f"https://douyin.wtf/api/hybrid/video_data?url={quote(url)}&minimal=false",
            headers={'accept': 'application/json'}
        )
        return response.json()

    @staticmethod
    def title_extractor(link):
        """Extract the title in the specified format."""
        data = Tiktok_Title_Extractor.fetch_video_data(link)
        
        # Extract nickname, uniqueId, and title from the JSON response
        nickname = data.get("data", {}).get("author", {}).get("nickname", "")
        uniqueId = data.get("data", {}).get("author", {}).get("uniqueId", "")
        title = data.get("data", {}).get("imagePost", {}).get("title","")
        description = data.get("data", {}).get("desc", "")

        # Format the title
        if title and description:
            cap = f"{title} \n\n {description}"
        elif title:
            cap = title
        elif description:
            cap = description
        else:
            cap = "✨"
        
        if nickname and uniqueId:
            formatted_title = f"{nickname} ({uniqueId}) \n\n {cap}"
        elif nickname:
            formatted_title = f"{nickname} \n\n {cap}"
        elif uniqueId:
            formatted_title = f"{uniqueId} \n\n {cap}"
        else:
            formatted_title = f"{cap}"
            
        return formatted_title

## Test Links
# link = "https://www.tiktok.com/@ruang.rakyat/video/7311900622423362848?is_from_webapp=1&sender_device=pc"  #
# link = "https://vt.tiktok.com/ZSNs3eATL/"  # story
# link = "https://vt.tiktok.com/ZSasdsadNs3eGAp/"  # - pictures
# link = "https://www.tiktok.com/@cinnamon_girlll0/video/7305513849812208898"
# link = "https://www.tiktok.com/@comal_bissta/video/73019192323483034127623"


# Working Links
# link = "https://vt.tiktok.com/ZSNGNPF8s/"
# link = "https://vt.tiktok.com/ZSNGN8hvB/"
# link = "https://vt.tiktok.com/ZSNGNyJqr/"
# link = "https://vt.tiktok.com/ZSNGNBaCu/"
# # link = "https://vt.tiktok.com/ZSNGNLKAB/"
# # test = Tiktok_Title_Extractor(link)
# # testreturn = test.title_extractor()
# # print(testreturn)
# # link = "https://www.tiktok.com/@_sicparvismagna_/video/7315130414534888736"
# insatnces = tt_dlp(link)
# check, caption, filelist = insatnces.download()
# print(check)
# print(caption)
# print(filelist)
