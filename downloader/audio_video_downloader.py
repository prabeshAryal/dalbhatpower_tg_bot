import yt_dlp
import requests,re
import os, shutil

class theOPDownloader():
    

    def __init__(self) -> None:
        self.caption= "✨"
        self.final_filename = None
        # pass
    
    def convert_html(self, string):
        string= string.replace('<', '&lt')
        string= string.replace('>', '&gt')
        return string
    
   
    def caption_cleaner(self,title):
        text = re.sub(r'\d{4}\/\d{2}\/\d{2}|(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)|UTC|@[A-Za-z0-9_.]+|\#[A-Za-z0-9_]+|▫️$|•| :\n|\n\.\n|\.\n\.|follow|via|credit|Follow|Via| - |',"",title)
        text = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)',"", text)
        text = re.sub(r'[\s]{3}','',text)
        return text
    
    def download_audio(self,link,*args):
        # twitter_regex = r"https?://(?:\w+\.)?twitter\.com/\w+/status/(\d+)"
        try:
            ydl_opts = {
                'max_filesize':2000000000,
                'format': 'm4a/bestaudio/best',
                'no_playlist': True,
                # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    }],
                'trim_file_name' : 100,
                'restrictfilenames': False,
                'ignoreerrors': True,
                'no_warnings':True, 
                'quiet': True,
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link,download=True)   
                filepath=ydl.prepare_filename(info)
                video_title = info['title']           
            video_title = self.caption if video_title == '' else video_title

            video_title = self.convert_html(video_title)
            filepath = filepath.replace('.m4a', '.mp3')
            filepath = os.path.join(os.getcwd(), filepath)
            CAPTION = '<a href="{}">{}</a>'.format(link,video_title)
            if os.path.isfile(filepath):
                return CAPTION, filepath , True
            else:
                shutil.rmtree(os.path.join(os.getcwd(), 'downloads'))
                raise Exception
        except Exception as e:
            print(e)
            return "Couldn't download Audio", None, False
   
    def download_video(self,link,*args):
        # twitter_regex = r"https?://(?:\w+\.)?twitter\.com/\w+/status/(\d+)"
        try:
            ydl_opts = {
                'max_filesize':2000000000,
                'format_sort': ['res:1080','ext:mp4:m4a'],
                # 'format_sort': ['ext:mp4:m4a'],
                'no_playlist': True,
                'trim_file_name' : 25,
                'restrictfilenames': True,
                'ignoreerrors': True,
                'no_warnings':True, 
                'quiet': True,
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link,download=True)   
                filepath=ydl.prepare_filename(info)
                video_title = info['title']           
            video_title = self.caption if video_title == '' else video_title
            video_title = self.convert_html(video_title)
            filepath = os.path.join(os.getcwd(), filepath)
            CAPTION = '<a href="{}">{}</a>'.format(link,video_title)
            if os.path.isfile(filepath):
                return CAPTION, filepath , True
            else:
                shutil.rmtree(os.path.join(os.getcwd(), 'downloads'))
                raise Exception
        except Exception as e:
            print(e)
            return "Couldn't download Video", None, False
    
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
    
    def short_vids(self,link,*args):
        try:
            instagram_reels_pattern = r"(?:https?://)?(?:(?:www|m)\.)?instagram\.com/reel(s)?/[-a-zA-Z0-9_]+"
            youtube_shorts_pattern = r"(?:https?://)?(?:(?:www|m)\.)?(?:youtu(?:be\.com/shorts/|\.be/))[-a-zA-Z0-9]+"
            tiktok_pattern = r"(?:https?://)?(?:(?:www|m)\.)?(?:tiktok\.com/@[-a-zA-Z0-9_]+/video/\d+|vt\.tiktok\.com/[-a-zA-Z0-9]+)"
            #tiktok_pattern
            # if re.match(tiktok_pattern,link):
            if re.match(r"(?:https:\/\/)?([vt]+)\.([tiktok]+)\.([com]+)\/([\/\w@?=&\.-]+)", link):
                r = requests.head(link, allow_redirects=False)
                link = r.headers['Location']
            ydl_opts = {'ignoreerrors': True,
                        'no_playlist': True,
                        'no_warnings':True, 
                        'trim_file_name' : 25,
                        'restrictfilenames': True,
                        'outtmpl': 'downloads/%(title)s.%(ext)s',
                        'format' : 'mp4',
                        }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                filepath=ydl.prepare_filename(info)
                video_title = info['title']
            filepath = os.path.join(os.getcwd(), filepath)
            if re.match(instagram_reels_pattern,link):
                video_title = self.get_page_title(link)
            video_title = self.caption if video_title == '' else video_title
            video_title = self.convert_html(video_title)
            CAPTION = '<a href="{}">{}</a>'.format(link,video_title)
            return CAPTION, filepath, True    
        except Exception as e:
            print(e)
            shutil.rmtree(os.path.join(os.getcwd(), 'downloads'))
            return None, None, False
        #InstaPattern Not Supported
        
    
    

# print(theOPDownloader().short_vids('https://vt.tiktok.com/fsd/'))
# print(theOPDownloader().short_vids('https://www.tiktok.com/@sdf/video/3453453'))

# # print(theOPDownloader().short_vids('https://www.youtube.com/shorts/zczxc'))
# print(theOPDownloader().short_vids('https://www.youtube.com/shorts/bod1NEE9VaA?feature=share'))

# print(theOPDownloader().download_video('https://twitter.com/TheKhabriTweets/status/1688108979619262464?s=20'))

# print(theOPDownloader().download_video('https://www.instagram.com/reels/CubnJShJEYL/'))
# print(theOPDownloader().download_video('https://www.reddit.com/r/dankindianmemes/comments/15jdnrb/when_a_kolkatian_says_their_chicken_biryani_is/'))

# print(theOPDownloader().download_video('https://youtu.be/F3PyHc8Q080'))

# print(theOPDownloader().download_audio('https://youtu.be/4e-I6IDBgK0'))
# print(theOPDownloader().download_audio('https://youtube.com/playlist?list=PLRadDPkbiRs_aaRP652TwXpT0oj65Q0tr'))
