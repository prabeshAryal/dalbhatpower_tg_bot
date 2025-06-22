from mytelegrammodules.commandhandlers.commonimports import *
from downloader.facebook import Facebook
from downloader.twitter import Twitter
from downloader.reddit import Reddit
from downloader.tiktokk import tt_dlp
from mytelegrammodules.user_bot import TelethonModuleByME

from utils.loader import Loader

from bs4 import BeautifulSoup

def sanitize_html_bs4(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    # Keep only supported tags
    for tag in soup.find_all(True):  # True matches all tags
        if tag.name not in ['b', 'i', 'u', 's', 'code', 'pre']:
            tag.unwrap()  # Remove unsupported tags, but keep the content
    return str(soup)

# html_string = '<div class="example">Hello <b>Bold</b> <script>alert("XSS")</script></div>'
# sanitized_html = sanitize_html_bs4(html_string)
# print(sanitized_html)

def convert_html(string):
    replacements = {
        # '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        # '"': '&quot;',
        # "'": '&#39;'
    }
    for key, value in replacements.items():
        string = string.replace(key, value)
    return string



def media_group_splitter(input_list):
    if len(input_list) <= 10:
        return [input_list]

    num_parts = len(input_list) // 10
    remainder = len(input_list) % 10

    parts = []
    start = 0
    for _ in range(num_parts):
        end = start + 10
        parts.append(input_list[start:end])
        start = end

    if remainder > 0:
        parts.append(input_list[-remainder:])

    return parts

def is_file_size_less_than_50mb(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False

    # Get the file size in bytes
    file_size_bytes = os.path.getsize(file_path)

    # Convert to megabytes
    file_size_mb = file_size_bytes / (1024 * 1024)

    # Check if the file size is less than 50 MB
    if file_size_mb < 50:
        return True
    else:
        return False




async def send_and_all(update, context, check, caption, filelist, url, site):
    if check != False:
        cap = convert_html(caption)
        CAPTION = '<a href="'+url+'">'+cap+'</a>'
        CAPTION = sanitize_html_bs4(CAPTION) if site.lower()=='x' and len(filelist)>0 else CAPTION
        if len(filelist)==0:
            await update.message.reply_html(CAPTION, reply_markup=ReplyKeyboardRemove(selective=True))
        elif len(filelist) == 1:
            filename = filelist[0]
            if filename.endswith(('mp4', 'webm','mkv')):
                video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
                with Loader("Uploading MultiSocial Video", "MultiSocial Video Upload Success"):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                    if is_file_size_less_than_50mb(filename):
                        try:
                            await update.message.reply_video(video=open(filename, 'rb'),duration=video_duration, write_timeout=1000, connect_timeout=1000, read_timeout=1000, caption=CAPTION, disable_notification=True, width=video_dimensions['width'], height=video_dimensions['height'], thumbnail=open(video_thumbnail_path,'rb'), parse_mode='HTML', supports_streaming=True)
                        except Exception as e:
                            await context.bot.send_video(chat_id=update.effective_chat.id,
                                video=open(filename, "rb"),
                                duration=video_duration,
                                write_timeout=1000,
                                connect_timeout=1000,
                                read_timeout=1000,
                                caption=CAPTION,
                                disable_notification=True,
                                width=video_dimensions.get("width", 1080),
                                height=video_dimensions.get("height", 1920),
                                thumbnail=open(video_thumbnail_path, "rb"),
                                parse_mode="HTML",
                                supports_streaming=True,
                            )
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                    else:
                        try:
                            resp = await TelethonModuleByME.send_video_to_chat(filename, update, context, CAPTION)
                            fromchatid= int(os.environ.get('TG_APP_CHAT_ID'))
                            frommesid = resp.id
                            try:
                                await update.message.reply_copy(from_chat_id=fromchatid, message_id=frommesid, caption=CAPTION,parse_mode='HTML')  
                            except Exception as e:
                                await context.bot.copy_message(chat_id=update.message.chat_id, from_chat_id=fromchatid, message_id=frommesid, caption=CAPTION,parse_mode='HTML')
                        except Exception as e:
                            print(e)
            if filename.endswith(('jpg', 'webp','heic')):
                with Loader("Uploading MultiSocial Photo", "MultiSocial Photo Upload Success"):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                    try:
                        await update.message.reply_photo(photo=open(filename, 'rb'),caption=CAPTION, write_timeout=1000, connect_timeout=1000, read_timeout=1000,disable_notification=True, parse_mode='HTML')
                    except Exception as e:
                        context.bot.send_photo(chat_id=update.effective_chat.id,
                            photo=open(filename, "rb"),
                            caption=CAPTION,
                            write_timeout=1000,
                            connect_timeout=1000,
                            read_timeout=1000,
                            disable_notification=True,
                            parse_mode="HTML",
                        )
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            os.remove(filename)
        else:
            media_group = []
            for filename in filelist:
                if filename.endswith(('mp4', 'webm')):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                    media_group.append(InputMediaVideo(open(filename, 'rb'), caption=CAPTION if (len(media_group)%10==0) else '', parse_mode='HTML'))
                    time.sleep(0.4)
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                if filename.endswith(('jpg', 'jpeg','webp','heic')):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                    media_group.append(InputMediaPhoto(open(filename, 'rb'), caption=CAPTION if (len(media_group)%10==0) else '', parse_mode='HTML'))
                    time.sleep(0.2)
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            with Loader("Uploading Multisocial Media Group", "Multisocial Media Group Upload Success"):
                for index, media_chunks in enumerate(media_group_splitter(media_group)):
                    if index == 0:
                        try:
                            await update.message.reply_media_group(media=media_chunks, write_timeout=1000, connect_timeout=1000, read_timeout=1000)
                        except Exception as e:
                            await context.bot.send_media_group(
                                chat_id=update.effective_chat.id,
                                media=media_chunks,
                                write_timeout=1000,
                                connect_timeout=1000,
                                read_timeout=1000,
                            )
                    else:
                        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_chunks, write_timeout=1000, connect_timeout=1000, read_timeout=1000)
                    time.sleep(2)

async def multi_social_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     # fullurlregex = r'(https?:\/\/(?:(www|m)\.)?MultiSocial\.com\/(p|reel)\/([^/?#&\s]+))'
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) + ' ' + str(json['last_name'])+' : ' +
          str(json['id']))+" - Sent MultiSocial Link : " + update.message.text)
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    try:
        
        reddit_regex = r'(https\:\/\/)?([w]+\.)?reddit\.com\/[A-Za-z_/0-9]+'
        facebook_regex = r'(https\:\/\/)?([w]+\.)?(facebook|fb)\.(com|watch)\/[A-Za-z_/0-9]+(.php\?(id|v)=[\d]+)?'   
        twitter_regex = r'https?://(?:(?:www|m(?:obile)?)\.)?(?:(?:twitter|x)\.com|twitter3e4tixl4xyajtrzo62zg5vztmjuricljdp2c5kshju4avyoid\.onion)/'
        tiktok_regex= r"((https:\/\/)?(((www.)?tiktok\.com\/@[-a-z\.A-Z0-9_]+\/(video|photo)\/\d+)|(vt\.tiktok\.com\/[-a-zA-Z0-9]+)))"

        only_necesssary_regex = r'([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
        links = re.findall(only_necesssary_regex, update.message.text)
        if len(links) == 0:
            toreply = 'Please send a Proper Social Post Link\n\tNote : Profiles and Highlights are not yet Supported_'
            await update.message.reply_markdown(toreply, reply_markup=ReplyKeyboardRemove(selective=True))
            return 'Done'
        else:
            for link in links:
                # print(url)
                url = link
                check = False
                if re.match(reddit_regex,link):
                    site ="reddit"
                    check, caption, filelist = Reddit(url).main()
                elif re.match(facebook_regex,link):
                    site ="facebook"
                    check, caption, filelist = Facebook.downloader(url)
                elif re.match(twitter_regex,link):
                    site="x"
                    check, caption, filelist = Twitter().get_tweet(url)
                elif re.match(tiktok_regex,link):
                    site="tiktok"
                    check, caption, filelist = tt_dlp(url).download()
                else:
                    continue
                # check, caption, filelist = ig_dlp(url).download()
                if check!= False:
                    await send_and_all(update, context, check, caption, filelist, url,site)
                # time.sleep(2)
                # os.remove(s for s in filelist)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    except Exception as e:
        print(e)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    print('%50s' % "Done")