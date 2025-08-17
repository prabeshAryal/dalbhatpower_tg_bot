import math
import re
import requests
import os
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from datetime import datetime, timezone
from dateutil import parser
import humanize
from rich.console import Console
from rich.progress import Progress

# Initialize rich console
console = Console()

def convert_html(string):
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }
    for key, value in replacements.items():
        string = string.replace(key, value)
    return string



# Constants
SYNDICATION_URL = "https://cdn.syndication.twimg.com"
TWEET_ID_PATTERN = re.compile(r"^[0-9]+$")


# Custom Error Class
class TwitterApiError(Exception):
    def __init__(self, message, status, data):
        super().__init__(message)
        self.name = "TwitterApiError"
        self.status = status
        self.data = data


# Twitter Class
class Twitter:
    def __init__(self):
        self.session = requests.Session()

    def get_token(self, id: str) -> str:
        token = (float(id) / 1e15) * math.pi

        def to_base36(number):
            chars = "0123456789abcdefghijklmnopqrstuvwxyz"
            result = []
            integer_part = int(number)
            fractional_part = number - integer_part

            # Convert integer part
            if integer_part == 0:
                result.append("0")
            else:
                while integer_part > 0:
                    integer_part, remainder = divmod(integer_part, 36)
                    result.append(chars[remainder])
                result.reverse()

            # Convert fractional part
            if fractional_part > 0:
                result.append(".")
                while (
                    fractional_part and len(result) < 18
                ):  # Limit to prevent infinite loop
                    fractional_part *= 36
                    digit = int(fractional_part)
                    result.append(chars[digit])
                    fractional_part -= digit

            return "".join(result)

        base36_token = to_base36(token).replace(".", "").lstrip("0")
        return base36_token

    def set_url_params(self, url, params):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params.update(params)
        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query,
                parsed_url.fragment,
            )
        )
        return new_url

    def fetch_tweet(self, id: str, fetch_options=None):
        if len(id) > 40 or not TWEET_ID_PATTERN.match(id):
            raise ValueError(f"Invalid tweet id: {id}")

        url = f"{SYNDICATION_URL}/tweet-result"

        features = [
            "tfw_timeline_list:",
            "tfw_follower_count_sunset:true",
            "tfw_tweet_edit_backend:on",
            "tfw_refsrc_session:on",
            "tfw_fosnr_soft_interventions_enabled:on",
            "tfw_show_birdwatch_pivots_enabled:on",
            "tfw_show_business_verified_badge:on",
            "tfw_duplicate_scribes_to_settings:on",
            "tfw_use_profile_image_shape_enabled:on",
            "tfw_show_blue_verified_badge:on",
            "tfw_legacy_timeline_sunset:true",
            "tfw_show_gov_verified_badge:on",
            "tfw_show_business_affiliate_badge:on",
            "tfw_tweet_edit_frontend:on",
        ]

        params = {
            "id": id,
            "lang": "en",
            "features": ";".join(features),
            "token": self.get_token(id),
        }

        url = self.set_url_params(url, params)
        headers = fetch_options.get("headers") if fetch_options else {}

        res = self.session.get(url, headers=headers)
        is_json = "application/json" in res.headers.get("Content-Type", "")

        data = res.json() if is_json else None

        if res.ok:
            if data and data.get("__typename") == "TweetTombstone":
                return {"tombstone": True}
            return {"data": data}

        if res.status_code == 404:
            return {"notFound": True}

        raise TwitterApiError(
            message=(
                data.get("error")
                if data and "error" in data
                else f"Failed to fetch tweet at '{url}' with status {res.status_code}."
            ),
            status=res.status_code,
            data=data,
        )

    def tweet_data_extractor(self, tweet_data):
        tweet = tweet_data["data"]
        caption1 = tweet["text"]
        # caption1 = convert_html(caption1)
        created_at = humanize.naturaltime(
            datetime.now(timezone.utc) - parser.parse(tweet["created_at"])
        )
        user = tweet["user"]
        user_display_name = user["screen_name"]
        user_name = user["name"]
        media_details = tweet.get("mediaDetails", False)
        quoted_tweet = tweet.get("quoted_tweet", False)

        if quoted_tweet:
            media_details = quoted_tweet.get("mediaDetails", False)
            tweet = quoted_tweet
            caption2 = tweet["text"]
            user2 = tweet["user"]
            user_display_name2 = user2["screen_name"]
            user_name2 = user2["name"]

        # video_url = (
        #     [
        #         max(
        #             media_details[0]["video_info"]["variants"],
        #             key=lambda v: v.get("bitrate", 0),
        #         )["url"]
        #     ]
        #     if media_details
        #     and "video_info" in media_details[0]
        #     and "variants" in media_details[0]["video_info"]
        #     else []
        # )
        
        video_url = []
        for media_detail in tweet_data['data'].get('mediaDetails', []):
            if 'video_info' in media_detail and 'variants' in media_detail['video_info']:
                highest_bitrate_variant = max(media_detail['video_info']['variants'], key=lambda v: v.get('bitrate', 0))
                video_url.append(highest_bitrate_variant['url'])

        # Ensure only unique URLs are kept (if needed)
        video_url = list(set(video_url))
        photos_url = [photo["url"] for photo in tweet.get("photos", [])]

        all_medias = video_url + photos_url

        if quoted_tweet:
            caption = (
                f"{user_name} quoted {user_name2}'s Tweet:\n"
                f"{created_at}\n\n"
                f"{caption1}\n\n<i>{user_name2} X'ed | {created_at}\n\n{caption2}</i>"
            )
        else:
            caption = f"{user_name} X'ed | {created_at}\n\n{caption1}"

        return caption, all_medias

    def download_media(self, urllist):
        output_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        files = []
        for i, url in enumerate(urllist):
            local_filename = os.path.join(
                output_dir,
                url.split("?")[0].split("/")[-1],
            )
            typeof = "Video" if local_filename.endswith("mp4") else "Photo"
            try:
                console.clear()
                console.print(
                    f"Downloading {typeof} {i+1}/{len(urllist)}...", style="bold blue"
                )
                with self.session.get(url, stream=True) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get("content-length", 0))
                    with open(local_filename, "wb") as f:
                        console.clear()
                        with Progress() as progress:
                            task = progress.add_task(
                                "[cyan]Downloading...", total=total_size
                            )
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                                progress.update(task, advance=len(chunk))
                console.print(
                    f"{i+1}/{len(urllist)} {typeof}s downloaded successfully.",
                    style="bold green",
                )
                files.append(local_filename)
            except requests.RequestException as e:
                console.print(f"Download error: {e}", style="bold red")
        return files

    def get_tweet(self, url):
        tweet_id = [
            part
            for part in url.split("?")[0].split("/")
            if TWEET_ID_PATTERN.match(part)
        ][0]
        try:
            tweet_data = self.fetch_tweet(tweet_id)
        except TwitterApiError as e:
            console.print(
                f"TwitterApiError: Tweet Doesn't Exist (status: {e.status})",
                style="bold red",
            )
            return "error", None, []

        try:
            caption, url_of_medias = self.tweet_data_extractor(tweet_data)
            # print(url_of_medias)
            try:
                downloaded_files = self.download_media(url_of_medias)
                # print(url_of_medias)
                return "success", caption, downloaded_files
            except Exception as e:
                console.print(f"Media Download Error: {e}", style="bold red")
                return "error", None, []
        except Exception as e:
            console.print(f"Tweet Data Extract Error: {e}", style="bold red")
            return "error", None, []


# Example usage
# if __name__ == "__main__":
#     twitter = Twitter()
#     urls = [
#         "https://x.com/spectatorindex/status/1803144871563415602",
#         "https://x.com/creepydotorg/status/1803022231590556063?t=PYWBz3jxEKHt8lfpiOU3bA&s=19",
#         "https://x.com/atifzia/status/1803153128419659778",
#         "https://x.com/atifzia/status/1803153128419659778/photo/1",
#         "https://x.com/MahuaMoitraFans/status/1806640973386060285",
#         "https://x.com/Pagal_aurat/status/1806264464922349752",
#         "https://x.com/RoshanKrRaii/status/1806556620048175416",
#     ]
#     i = 1
#     for url in urls:
#         print(i)
#         i+=1
#         status, caption, downloaded_files = twitter.get_tweet(url)
#         print(f"Status: {status}")
#         print(f"Caption: {caption}")
#         print(f"Downloaded Files: {downloaded_files}")
