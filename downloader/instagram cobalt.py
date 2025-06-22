import os,requests,json
from utils.loader import Loader

class ig_dlp(object):
    '''An Instagram Downloader Module You Can't Ignore 

    usage:
    ig_dlp(link) : returns bool, caption, filepath_list
    Type = Post-Video, Post-Image, Carousel, Public-Story, None '''

    def __init__(self, link) -> None:
        # self.link = link
        self.method = 'cobalt'
        self.link = link
        if self.method == 'cobalt':
            self.headers = {
                "content-type": "application/json",
                "accept": "application/json",
            }
            self.body = {
                        "url": link,
                        "vCodec": "h264",
                        "vQuality": "max"
                    }
            self.api = "https://api.cobalt.tools/api/json"

    def get_page_title(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx and 5xx)

            # Find the position of the opening and closing <title> tags
            start_index = response.text.find('<title>')
            end_index = response.text.find('</title>')

            if start_index != -1 and end_index != -1:
                start_index += len('<title>')
                return response.text[start_index:end_index]
            else:
                return None  # No title tag found

        except requests.exceptions.RequestException as e:
            print("Couldn't Get Caption so replacing with ✨")
            return "✨"

    def download_media(self,downloadType, url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            filename = url.split('/')[-1].split('?')[0] if downloadType != 'stream' else url.split('?')[-1].split('=')[1].replace('&','')+".mp4"
            download_path = os.path.join('downloads', filename)

            # Create the 'downloads' directory if it doesn't exist
            os.makedirs('downloads', exist_ok=True)

            with open(download_path, 'wb') as file:
                file.write(response.content)
            return os.path.join(os.getcwd(), download_path)

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            raise FileNotFoundError

    def here_we_download(self, downloadType, all_links):
        filepath = []
        for media_link in all_links:
            file = self.download_media(downloadType, media_link)
            filepath.append(file)
        return filepath

    def download(self):
        try:
            with Loader("Requesting API....", "API Response Received✅"):
                response = requests.post(
                    self.api, headers=self.headers, data=json.dumps(self.body))
                mydict = response.json()
            # print(mydict)
            if response.status_code == 200:
                if mydict['status'] == 'redirect' or mydict['status'] == 'stream':
                    download_list = [mydict['url']]
                    # print(download_list)
                    downloadType = mydict['status']
                elif mydict['status'] == 'picker':
                    download_list = [item['url'] for item in mydict['picker'] if 'url' in item]
                    # print(download_list)
                    downloadType = mydict['status']
                with Loader("Getting Caption", "Caption Extracted ✅"):
                    CAPTION = self.get_page_title(self.link)
                with Loader(f"Downloading {len(download_list)} Files", f"Downloaded {len(download_list)} Files ✅"):
                    files = self.here_we_download(downloadType, download_list)
                return downloadType, CAPTION, files
            else:
                print("\nAPI responded failure: " +
                        str(response.status_code))
                return False, None, []
        except Exception as e:
            print(e)
            return False, None, []


# url = "https://www.instagram.com/reels/CufCAL1p7Ub/"  # reels
# url = "https://www.instagram.com/reel/Cs1afZSr_Ci/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=="  # reel
# url = "https://www.instagram.com/p/CwRX29MI0Hq/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=="  # post, sigle
# url = "https://www.instagram.com/p/CrveD1XPau5/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=="  # carousel
# url = "https://www.instagram.com/p/Cg9BeutMPm3URpBNFVyH1c_et4C3Mm_IDXv1V40/?img_index=1"
# url = 'https://www.instagram.com/stories/evaaa.g__/3174965177308244912/'

# url = "https://www.instagram.com/p/C58Tedtt5Iv/?igsh=MTB1Ym40MzZhaWh5OQ=="
# url = "https://www.facebook.com/share/r/VQJMifZXWWcBFgvR/?mibextid=xfxF2i"
# url = "https://www.facebook.com/reel/199061536629079"

# url = "https://www.facebook.com/photo/?fbid=399782902846407&set=a.112771498214217"
# instance = ig_dlp(url)
# check, caption, filelist = instance.download()
# print(check)
# print(caption)
# print(filelist)
