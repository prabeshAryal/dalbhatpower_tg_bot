import os,requests
from utils.loader import Loader

class rapid_ig(object):
    '''An Instagram Downloader Module You Can't Ignore 

    usage:
    ig_dlp(link) : returns bool, caption, filepath_list
    Type = Post-Video, Post-Image, Carousel, Public-Story, None '''

    def __init__(self, link) -> None:
        self.headers = {
            "X-RapidAPI-Key": os.getenv('X_RapidAPI_Key'),
            "X-RapidAPI-Host": 'instagram-downloader-download-instagram-videos-stories.p.rapidapi.com',
        }
        self.querystring = {"url": link}
        self.link = link
        self.api = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"

    
    def get_page_title(self,url):
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

    
    
    def analyzeresponse(self,resposnsejson, urlll):
        try:
            if resposnsejson['Type'] == "Post-Video" or resposnsejson['Type']=='Post-Image' or resposnsejson['Type']=='Carousel':
                # print(resposnsejson)
                # thumbnail = resposnsejson["thumbnail"]
                try:
                    caption = resposnsejson["title"]
                except KeyError:
                    caption=self.get_page_title(urlll)
                return resposnsejson['Type'], caption, resposnsejson['media'] if isinstance(resposnsejson['media'], list) else [resposnsejson['media']]
        except KeyError as e:
            # print('No Key named' + e)
            try:
                username = resposnsejson['username']
                caption=f'Stories by {username}'
                storylist = resposnsejson["stories"]
                medialist=[]
                for stories in storylist:
                    medialist.append(stories['media'])
                return 'Public-Story',caption,medialist
            except KeyError as d:
                # print('No Key named' + d)
                return 'Unsupported-Type',None,[]
    
    def download_media(self,url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            filename = url.split('/')[-1].split('?')[0]
            download_path = os.path.join('downloads', filename)

            # Create the 'downloads' directory if it doesn't exist
            os.makedirs('downloads', exist_ok=True)

            with open(download_path, 'wb') as file:
                file.write(response.content)
            return os.path.join(os.getcwd(),download_path)

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            raise FileNotFoundError
        
    
    def here_we_download(self,all_links):
        filepath = []
        for media_link in all_links:
            file = self.download_media(media_link)
            filepath.append(file)
        return filepath
        
    def download(self):
        with Loader("Requesting API....","API Response Received"):
            response = requests.get(self.api, headers=self.headers, params=self.querystring)
        with Loader("Extracting Required Headers"," "):
            if response.status_code == 200:
                makejson = response.json()
                downloadType,CAPTION,download_list=self.analyzeresponse(makejson,self.link)
                # print(downloadType)
                # print(CAPTION)
                # print(download_list)
            else:                
                print("\nAPI responded failure: " + str(response.status_code))
                return False, None,[]
            if downloadType=='Unsupported-Type':
                print('The format is not supported yet.')
                return False, None,[]
            else:
                with Loader("Download Started","Downloading Completed Successfully"):
                    files=self.here_we_download(download_list)
                    return downloadType, CAPTION, files
            



# link = 'https://www.instagram.com/p/CuXWxYkPx19/'
# link ='https://www.instagram.com/reel/CvKawUbPRgn/?utm_source=ig_web_copy_link'
# link='https://www.instagram.com/p/Cvt1onCOXSk/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=='
# link = 'https://www.instagram.com/stories/evaaa.g__/3164772748186767392/'
# ig_downloader = ig_dlp(link)
# # caption, files = ig_downloader.download()
# # print("Caption:", caption)
# # print("Files:", files)
# status,Cap,files=ig_downloader.download()
# print(status)
# print(Cap)
# print(files)