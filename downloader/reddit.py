import os
import re
import requests
import subprocess
from datetime import datetime, timezone
from rich.console import Console
from rich.progress import Progress
import html
import json
# Initialize rich console
console = Console()


def update_cookies():
    cookie_string = """
    # Netscape HTTP Cookie File
    # http://curl.haxx.se/rfc/cookie_spec.html
    # This is a generated file!  Do not edit.

    .www.reddit.com	TRUE	/	TRUE	1751201161	__stripe_mid	1a4e9126-2bd4-43f8-8fe0-a611af4cf815106f8b
    .reddit.com	TRUE	/	TRUE	1751201119	pc	g7
    .reddit.com	TRUE	/	TRUE	1721784741	datadome	1f4OdDtExKxTyUhGNMqD2oiwDh5l2Ns9ixlicNceLaP1pR3CbR9GrH-knrrd49BCORL4b5kC2EVT8GeqrITc~Sv4Yp5pxt~XTVFy5aiSXq_4I32nFTCJE4-JQr9VV8Dt
    .reddit.com	TRUE	/	TRUE	1743958214	csv	2
    .reddit.com	TRUE	/	TRUE	1743958214	edgebucket	i34GiSqMAunKHhm8OD
    .reddit.com	TRUE	/	TRUE	1743958221	reddit_session	78466240805932%2C2024-03-02T16%3A50%3A17%2Ca85c61085dd30d24278547c913b139080d963f3a
    .reddit.com	TRUE	/	TRUE	1743958224	loid	000000000rtaw5u5gs.2.1704929947565.Z0FBQUFBQmw0MWpNX1EzaHhqQjRrcC1EcmFqWmNLQXBrVVc4OEExQ0R6Q0ZfUVNRLU9qVFh5Q3p2R0ptdUhDal9kZkplQ2tmbHRNR09DUGU5dTVicUlCMkFja2F2SXY4cmNnTXlYamtudXlqb0NHU2ZJLTQ4YVBvcno2VWFmVlcyMWJJc0t3U19ibl8
    .reddit.com	TRUE	/	FALSE	1754225118	theme	2
    www.reddit.com	FALSE	/	FALSE	1753356300	eu_cookie	{%22opted%22:true%2C%22nonessential%22:false}
    .reddit.com	TRUE	/	TRUE	1719768159	token_v2	eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzE5NzY4MTU2LjU5Mjk3OSwiaWF0IjoxNzE5NjgxNzU2LjU5Mjk3OCwianRpIjoiblJYRllHWm9JRjRHWTg0cUVyRGxjVGJfdG1sdmRRIiwiY2lkIjoiMFItV0FNaHVvby1NeVEiLCJsaWQiOiJ0Ml9ydGF3NXU1Z3MiLCJhaWQiOiJ0Ml9ydGF3NXU1Z3MiLCJsY2EiOjE3MDQ5Mjk5NDc1NjUsInNjcCI6ImVKeGtrZEdPdERBSWhkLWwxejdCX3lwX05odHNjWWFzTFFhb2szbjdEVm9jazcwN2NMNGlIUDhuS0lxRkxFMnVCS0drS1dFRld0T1VOaUx2NTh5OU9aRUZTeUZUUjg0M3l3b2thVXBQVW1ONXB5bFJ3V1prTGxmYXNVS0RCNllwVlM2WjIwS1BTNXZRM0kxRnowNk1xbHhXSHRUWW8zSnBiR01LMnhQanpjWnFReXF1eTZsTVlGa29uOFdMZnZ5Ry10WS1mN2JmaEhZd3JLZ0tEX1RPdUZ4d1lfSERGSGJfbnByMGJGMndxTDNYZzlRLTEtTjI3Yk5tb2RtNV9WelB2emFTY1RtRzVpZll2N3QtQ1IxNDVIbVpVUWN3WWcwX3lyQWo2X0N2T29ES0JRV01KWWhQSTVBcmwyX19KZGl1VGY4YXR5ZC0tR2JFVFdfNHJSbW81eExFb1VfajZ6Y0FBUF9fWERfZTR3IiwicmNpZCI6Ik1WLWJKajExeXFmdmo5ZmktWW1LSWROdTN6RjBMdVRKbTVDd0p2Y2tVN2MiLCJmbG8iOjJ9.IHGGJxR9XvfdiTv4wR53OBA3SzmVSfL-4lR_dm12zFHZFXmVtRX3-q_UwBFXVVRf4LlfTdyjlHKha6uDzioJ-MlBrOCbEFff4yrJOORROXVIEQmD5OIt5ogGaXSiIklkNdvw_I4h_WWHhBxz-6Uvt58vxecdJwkZtMsp80fKSHZoxSj2YZx08MOWVg-tDMz_0Q3RUQs82wV2OLF58EroXis1Z8tj11JvnNdxQSi-B0SoeawnS63veDgRgyF2QQEsQXO8RSaSu7EN9ZVsnVOYCFv3mjtML3tHMYoDJ3ZxrGKeTMzfBY2zwJmUhKNBw4x9SggLznslZCoXWs3sViur8Q
    .reddit.com	TRUE	/	FALSE	1751253302	t2_rtaw5u5gs_recentclicks3	t3_1drr86d%2Ct3_1drfrlv%2Ct3_1drgg7d%2Ct3_1drfna8%2Ct3_9rdhm4%2Ct3_1dqc8bp%2Ct3_1dqqc3m%2Ct3_1dp74u9%2Ct3_1dra0di%2Ct3_1drakqm
    .reddit.com	TRUE	/	TRUE	0	csrf_token	ee429ae25c74ff0e1ac024b010644672
    .reddit.com	TRUE	/	TRUE	1719724509	session_tracker	qbifnphdkhlaimphrr.0.1719717309413.Z0FBQUFBQm1nTTI5NDF5QTl3Zk94TzdMZW5MMW5HNkp3QVczR2kwUlhnOFNPdWpxZll0bTNTS3pxdkFqN2FjbUxTVnZKZ0pxNU0tUVFWQ2sySGxWSHpWb1o1VUJBQVRZRlpSMDZaNWI0YnQ1Mk1Zb0xJR0t0bUsxNE00SmVidG5pRElEUm9KdkVteks
    """

    # Function to parse cookie string into a dictionary
    def parse_cookie_string(cookie_string):
        cookies = {}
        for line in cookie_string.strip().split('\n'):
            if not line.startswith('#'):
                parts = line.strip().split('\t')
                if len(parts) >= 7:  # Adjusted to handle potential variations in the cookie string
                    cookies[parts[5]] = parts[6]
        return cookies


    # Parse the cookie string
    cookies = parse_cookie_string(cookie_string)
    # session.cookies.update(cookies)
    return cookies

def get_frame_count(url):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-count_frames",
        "-show_entries",
        "stream=nb_read_frames",
        "-of",
        "json",
        url,
    ]

    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode == 0:
        info = json.loads(result.stdout)
        frame_count = int(info["streams"][0]["nb_read_frames"])
        return frame_count
    else:
        console.print(f"[red]An error occurred with ffprobe: {result.stderr}")
        return None


def time_ago(timestamp):
    timestamp_datetime = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    time_diff = now - timestamp_datetime

    days = time_diff.days
    years = days // 365
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60

    if years >= 1:
        return timestamp_datetime.strftime("%B %d, %Y")
    elif days > 0:
        return f"{days} days ago"
    elif hours > 0:
        return f"{hours} hours ago"
    elif minutes > 0:
        return f"{minutes} minutes ago"
    else:
        return "Just now"


class Reddit:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.data = self.fetch_data()
        self.links = []
        self.caption = ""
        

    # def fetch_data(self):
    #     # r = requests.head(self.url, allow_redirects=False)
    #     # self.url = r.headers["Location"]
    #     self.session.cookies.update(update_cookies())
    #     url = self.url.split("?")[0]
    #     json_url = url + ("/" if url[-1] != "/" else "") + ".json"
    #     # print(json_url)
    #     try:
    #         response = self.session.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
    #         response.raise_for_status()
    #         print(response.json())
    #         return response.json()[0]["data"]["children"][0]["data"]
    #     except Exception as e:
    #         console.print(f"[red]An error occurred while fetching data: {e}")
    #         return None
    def fetch_data(self):

        self.session.cookies.update(update_cookies())
        
         # Attempt to resolve URL redirection using the session
        try:
            head_response = self.session.head(self.url, allow_redirects=True)
            # Update the URL to the final redirected URL
            final_url = head_response.url
            # console.print(f"[green]Final URL resolved to: {final_url}")
        except Exception as e:
            # console.print(f"[yellow]Warning: Could not resolve URL redirection. Error: {e}")
            final_url = self.url
        self.url = final_url
        url = self.url.split("?")[0]
        json_url = url + ("/" if url[-1] != "/" else "") + ".json"
        print(json_url)
        try:
            response = self.session.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
            # print(response.text)
            response.raise_for_status()
            try:
                data = response.json()
                if len(data) > 0 and "data" in data[0] and "children" in data[0]["data"]:
                    return data[0]["data"]["children"][0]["data"]
                else:
                    console.print(f"[red]Unexpected JSON structure.")
                    return None
            except json.JSONDecodeError:
                console.print(f"[red]Failed to decode JSON response.")
                return None
        except Exception as e:
            console.print(f"[red]An error occurred while fetching data: {e}")
            return None

    def extract_title(self):
        return self.data.get("title", "") if self.data else ""

    def extract_description(self):
        return self.data.get("selftext", "") if self.data else ""

    def extract_images(self):
        images = []
        if self.data:
            if "preview" in self.data and "images" in self.data["preview"]:
                images = [
                    img["source"]["url"] for img in self.data["preview"]["images"]
                ]
            if self.data.get("media_metadata"):
                images.extend(
                    [
                        self.data["media_metadata"][pic]["p"][-1]["u"]
                        for pic in self.data["media_metadata"]
                        if self.data["media_metadata"][pic]["e"] == "Image"
                    ]
                )
        return images

    def extract_videos(self):
        videos = []
        if self.data:
            if self.data.get("secure_media", {}) and self.data.get("secure_media",{}).get("reddit_video"):
                videos.append(
                    self.data["secure_media"]["reddit_video"].get("dash_url", "")
                )
            if self.data.get("media_metadata"):
                videos.extend(
                    [
                        self.data["media_metadata"][video]["dashUrl"]
                        for video in self.data["media_metadata"]
                        if self.data["media_metadata"][video]["e"] == "RedditVideo"
                    ]
                )
        return videos

    def extract_upvotes(self):
        return self.data.get("ups", 0) if self.data else 0

    def extra_user_red_info(self):
        subreddit = self.data.get("subreddit_name_prefixed", "reddit")
        user = self.data.get("author", "")
        created_at = time_ago(self.data.get("created_utc", 0))
        upvotes = self.extract_upvotes()
        return f"{user} posted in {subreddit}\n{created_at} | ⬆️ : {upvotes}\n\n"

    def download_video(self, url, filename):
        command = ["ffmpeg", "-i", url, "-c", "copy", filename, "-loglevel", "quiet"]

        spinner_name = "dots"

        with console.status("[cyan]Downloading...", spinner=spinner_name):
            try:
                process = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                process.wait()

                if process.returncode == 0:
                    console.print(f"[green]Reddit Video Download completed")
                else:
                    console.print(f"[red]An error occurred: Return code {process.returncode}")

            except subprocess.CalledProcessError as e:
                console.print(f"[red]An error occurred: {e}")

        return filename

    def download_media(self, urllist):
        output_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(output_dir, exist_ok=True)
        files = []
        for i, url in enumerate(urllist):
            typeof = "Video" if "v" in url.split(".")[0][-1] else "Photo"
            # print(url)
            local_filename = os.path.join(
                output_dir,
                f"{url.split('?')[0].split('/')[-2]}.mp4" if typeof == 'Video' else f"{url.split('?')[0].split('/')[-1].split('.')[0]}.jpg"
            )
            if os.path.isfile(local_filename):
                files.append(local_filename) if local_filename not in files else None
                continue
            if typeof != "Video":
                url = html.unescape(url)
                try:
                    console.clear()
                    console.print(
                        f"Downloading {typeof} {i + 1}/{len(urllist)}...",
                        style="bold blue",
                    )
                    with self.session.get(url, stream=True) as r:
                        r.raise_for_status()
                        total_size = int(r.headers.get("content-length", 0))
                        with open(local_filename, "wb") as f:
                            with Progress() as progress:
                                task = progress.add_task(
                                    "[cyan]Downloading...", total=total_size
                                )
                                for chunk in r.iter_content(chunk_size=8192):
                                    f.write(chunk)
                                    progress.update(task, advance=len(chunk))
                    console.print(
                        f"{i + 1}/{len(urllist)} {typeof}s downloaded successfully.",
                        style="bold green",
                    )
                    files.append(local_filename)
                except requests.RequestException as e:
                    console.print(f"[red]Download error: {e}")
            else:
                files.append(self.download_video(url, local_filename))
        return files

    def main(self):
        if self.data:
            title = self.extract_title()
            description = self.extract_description()
            images = self.extract_images()
            videos = self.extract_videos()
            all_media = (
                images + videos if not (len(images) == len(videos) == 1) else videos
            )

            post_info = self.extra_user_red_info()
            self.caption = (
                post_info
                + f"<b>{title}</b>\n\n{description[:1700]}{'...' if len(description)>1700 else ''}"
            )
            return 'working', self.caption, self.download_media(all_media)
        else:
            return False, None , []


# test_cases
# Multipe videos
# url = "https://www.reddit.com/r/singedmains/comments/htu0c6/how_to_win_vs_gnar_teemo_quin_kennen_at_level_2/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"

# Single Video
# url = "https://www.reddit.com/r/hotnepalese/comments/1drakqm/_/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"
# url = "https://www.reddit.com/r/dankindianmemes/comments/1dp74u9/ancient_india/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"
# Single Photo
# url = "https://www.reddit.com/r/nepalitiktokbabes/comments/1dqqc3m/dm_for_her/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"

# Multiple Photos
# url = "https://www.reddit.com/r/Pictures/comments/1dqc8bp/im_just_like_taking_pictures_of_the_sunset/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"

# Post with desc
# url = "https://www.reddit.com/r/NepalSocial/comments/1drag2f/are_nepali_men_actually_homophobic/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"

# Comment

# comment in a pic
# url = "https://www.reddit.com/r/Pictures/comments/1dpsfcl/comment/lak85b8/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"


# # # Example usage
# if __name__ == "__main__":
#     # url = "https://www.reddit.com/r/nepalitiktokbabes/comments/1dqqc3m/dm_for_her/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button"
#     reddit = Reddit(url)
#     result = reddit.main()
#     print(result)

# print(Reddit("https://www.reddit.com/r/hotnepalese/s/WOoQi217OX").main())
# print(
#     Reddit(
#         "https://www.reddit.com/r/hotnepalese/comments/1drfrlv/sajisessential_summer/"
#     ).main()
# )
