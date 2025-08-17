import requests
import re
import os
from rich.console import Console
from rich.progress import Progress

# Initialize rich console
console = Console()


class Facebook:

    @staticmethod
    def SnapSave(facebook_video_url):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "content-length": "184",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "_ga=GA1.1.80793777.1718523979; _ga_WNPZGVDWE9=GS1.1.1718523979.1.1.1718523992.47.0.0",
            "origin": "https://snapsave.app",
            "referer": "https://snapsave.app/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "iframe",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }

        snapsave_url = "https://snapsave.app/action.php"
        console.print("Fetching video URL...", style="bold blue")

        try:
            resp = requests.post(
                snapsave_url, data={"url": facebook_video_url}, headers=headers
            )
            resp.raise_for_status()
            if resp.status_code == 200:
                try:
                    the_js_result = re.search(
                        r"javascript\">(.*?)<\/script>", resp.text
                    ).group(1)
                except:
                    the_js_result = resp.text

                try:
                    translated_js = Facebook.JSRunner(the_js_result)
                    url_result = re.search(
                        r"href=\\\\\\\"(http.*?)\\\\\\\"", translated_js
                    ).group(1)
                    console.print("Video URL obtained from API.", style="bold green")
                    return url_result
                except:
                    console.print(
                        "Failed to parse video URL from API response.", style="bold red"
                    )
                    return None
            else:
                console.print("Failed to fetch video URL from API.", style="bold red")
                return None
        except requests.RequestException as e:
            console.print(f"Request error: {e}", style="bold red")
            return None

    @staticmethod
    def JSRunner(js_string):
        token = requests.get("https://onecompiler.com/api/getIdAndToken").json()
        TOKEN_TITLE = token["id"]
        TOKEN = token["token"]
        JS_CONTENT = js_string.replace('"', '"') + ";"
        js_translate_data = {
            "name": "JavaScript",
            "title": TOKEN_TITLE,
            "version": "ES6",
            "mode": "javascript",
            "description": None,
            "extension": "js",
            "languageType": "programming",
            "active": True,
            "properties": {
                "language": "javascript",
                "docs": True,
                "tutorials": True,
                "cheatsheets": True,
                "filesEditable": True,
                "filesDeletable": True,
                "files": [{"name": "index.js", "content": JS_CONTENT}],
                "newFileOptions": [
                    {
                        "helpText": "New JS file",
                        "name": "script${i}.js",
                        "content": "/**\n *  In main file\n *  let script${i} = require('./script${i}');\n *  console.log(script${i}.sum(1, 2));\n */\n\nfunction sum(a, b) {\n    return a + b;\n}\n\nmodule.exports = { sum };",
                    },
                    {
                        "helpText": "Add Dependencies",
                        "name": "package.json",
                        "content": '{\n  "name": "main_app",\n  "version": "1.0.0",\n  "description": "",\n  "main": "HelloWorld.js",\n  "dependencies": {\n    "lodash": "^4.17.21"\n  }\n}',
                    },
                ],
            },
            "_id": TOKEN_TITLE,
            "user": None,
            "idToken": TOKEN,
            "visibility": "public",
        }

        translated_js_from_js_runner = requests.post(
            "https://onecompiler.com/api/code/exec", json=js_translate_data
        ).text
        return translated_js_from_js_runner

    @staticmethod
    def get_page_title(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            start_index = response.text.find("<title>")
            end_index = response.text.find("</title>")

            if start_index != -1 and end_index != -1:
                start_index += len("<title>")
                return response.text[start_index:end_index]
            else:
                return "✨"
        except requests.exceptions.RequestException:
            return "✨"

    @staticmethod
    def download_video(video_url):
        output_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        local_filename = os.path.join(
            output_dir,
            video_url.split("/")[-1].split("?")[1].split("=")[1].split(".")[0] + ".mp4",
        )

        try:
            console.clear()
            console.print("Downloading video...", style="bold blue")
            with requests.get(video_url, stream=True) as r:
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
                f"Video downloaded successfully to {local_filename}", style="bold green"
            )
            return local_filename
        except requests.RequestException as e:
            console.print(f"Download error: {e}", style="bold red")
            return None

    @staticmethod
    def downloader(facebook_video_url):
        try:
            console.print("Starting the download process...", style="bold blue")

            # Fetch video URL
            video_url = Facebook.SnapSave(facebook_video_url)
            if video_url:
                # Clear the console line
                console.clear()
                console.print("Initiating download process...", style="bold blue")
                # Download the video
                local_filename = Facebook.download_video(video_url)
                if local_filename:
                    status = "Success"
                    caption = Facebook.get_page_title(facebook_video_url)
                    file_list = [local_filename]
                else:
                    status = "Failed"
                    caption = None
                    file_list = []
                    console.print("Failed to download video.", style="bold red")
            else:
                return False, None, []
                # status = "Failed"
                # caption = None
                # file_list = []
                # console.print("Failed to fetch video URL.", style="bold red")

            # Print final result
            if status == "Success":
                console.clear()
                console.print(
                    f"Facebook Video Downloaded. {file_list[0]}", style="bold green"
                )
                return status, caption, file_list
                # console.print(f"Page Title: {caption}", style="bold green")
            else:
                # console.clear()
                console.print("Error occurred. Check the logs above.", style="bold red")
                return False, None, []

        except Exception as e:
            # console.clear()
            console.print(f"An unexpected error occurred: {e}", style="bold red")
            return False, None, []


# Example usage
# if __name__ == "__main__":
#     # url = "https://www.facebook.com/share/r/asdsawda/"
#     url = "https://www.facebook.com/share/r/3rUVhtPzeDBWwRMs/"
#     status, caption, file_list = Facebook.downloader(url)
