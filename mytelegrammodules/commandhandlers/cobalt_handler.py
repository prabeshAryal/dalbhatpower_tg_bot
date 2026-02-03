import os, re, requests, html
import time

from downloader.cobalt import cobalt
import shutil

from mytelegrammodules.commandhandlers.commonimports import *
from mytelegrammodules.user_bot import TelethonModuleByME


# Set the chat ID to forward messages to
# update.effective_chat.id = -1001735655334
# update.effective_chat.id= '@nepalibeauties'

API_HASH = "6902521433:AAGz26Do-zYaRrfW_yCjGTCTpmOsHw5syQI"

MEDIA_GROUP_TYPES = {
    "audio": InputMediaAudio,
    "document": InputMediaDocument,
    "photo": InputMediaPhoto,
    "video": InputMediaVideo,
}


class MsgDict(TypedDict):
    media_type: Literal["video", "photo"]
    media_id: str
    caption: str
    post_id: int

import re

def convert_html(string):
    string = string.replace("<", "&lt")
    string = string.replace(">", "&gt")
    return string

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

def contains_phrase(text, phrase):
    # Normalize the text and phrase
    normalized_text = re.sub(r'\s+', ' ', text.strip().lower())
    normalized_phrase = re.sub(r'\s+', ' ', phrase.strip().lower())
    
    # Check if the normalized phrase is in the normalized text
    return normalized_phrase in normalized_text

def escape_markdown_v2(text):
    return re.sub(r'([*_{}\[\]()~`>#+\-=|.!])', r'\\\1', text)

async def send_and_all(update, context, check, caption, filelist, url):
    if check != False:
        cap = convert_html(caption)
        CAPTION = '<a href="' + url + '">' + cap + "</a>"
        if len(filelist) == 1:
            filename = filelist[0]
            if not is_file_size_less_than_50mb(filename) and filename.endswith(("mp3", "wav", "opus", "ogg", "m4a")):
                try:
                    resp = await TelethonModuleByME.send_audio_to_chat(filename, update, context, CAPTION)
                    fromchatid= int(os.environ.get('TG_APP_CHAT_ID'))
                    frommesid = resp.id
                    try:
                        await update.message.reply_copy(from_chat_id=fromchatid, message_id=frommesid, caption=CAPTION,parse_mode='HTML')  
                    except Exception as e:
                        await context.bot.copy_message(chat_id=update.message.chat_id, from_chat_id=fromchatid, message_id=frommesid, caption=CAPTION,parse_mode='HTML')
                except Exception as e:
                    print (e)
                os.remove(filename)
                return True
            elif not is_file_size_less_than_50mb(filename) and filename.endswith(("mp4", "webm", "mkv", "hevc", "avc", "mov")):
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
                os.remove(filename)
                return True
            
            if filename.endswith(("mp4", "webm", "mkv", "hevc", "avc", "mov")):
                video_duration, video_dimensions, video_thumbnail_path = (
                    extract_media_info(filename, "video")
                )
                video_thumbnail_path = (
                    video_thumbnail_path
                    if os.path.exists(video_thumbnail_path)
                    else None
                )
                with Loader(
                    "Uploading Video", "Video Upload Success"
                ):
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="upload_video"
                    )
                    try:
                        await update.message.reply_video(video=open(filename, 'rb'),duration=video_duration, write_timeout=1000, connect_timeout=1000, read_timeout=1000, caption=CAPTION, disable_notification=True, width=video_dimensions.get('width',0), height=video_dimensions.get('height',0), thumbnail=open(video_thumbnail_path,'rb') if video_thumbnail_path else None, parse_mode='HTML', supports_streaming=True)
                    except Exception as e:
                        await context.bot.send_video(
                            chat_id=update.effective_chat.id,
                            video=open(filename, "rb"),
                            duration=video_duration,
                            write_timeout=1000,
                            connect_timeout=1000,
                            read_timeout=1000,
                            caption=CAPTION,
                            disable_notification=True,
                            width=video_dimensions.get("width",0),
                            height=video_dimensions.get("height",0),
                            thumbnail=open(video_thumbnail_path, "rb"),
                            parse_mode="HTML",
                            supports_streaming=True,
                        )
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="cancel"
                    )
            elif filename.endswith(("jpg", "jpeg", "webp", "heic", "png")):
                with Loader(
                    "Uploading Photo", "Photo Upload Success"
                ):
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="upload_photo"
                    )
                    try:
                        await update.message.reply_photo(photo=open(filename, 'rb'),caption=CAPTION, write_timeout=1000, connect_timeout=1000, read_timeout=1000,disable_notification=True, parse_mode='HTML')
                    except Exception as e:
                    
                        await context.bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=open(filename, "rb"),
                            caption=CAPTION,
                            write_timeout=1000,
                            connect_timeout=1000,
                            read_timeout=1000,
                            disable_notification=True,
                            parse_mode="HTML",
                        )
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="cancel"
                    )
                
            elif filename.endswith(("mp3", "wav", "opus", "ogg", "m4a")):
                with Loader(
                    "Uploading Music", "Music Upload Success"
                ):
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="upload_audio"
                    )
                    try:
                        await update.message.reply_audio(audio=open(filename, 'rb'),caption=CAPTION, write_timeout=1000, connect_timeout=1000, read_timeout=1000,disable_notification=True, parse_mode='HTML')
                    except Exception as e:
                    
                        await context.bot.send_audio(
                            chat_id=update.effective_chat.id,
                            photo=open(filename, "rb"),
                            caption=CAPTION,
                            write_timeout=1000,
                            connect_timeout=1000,
                            read_timeout=1000,
                            disable_notification=True,
                            parse_mode="HTML",
                        )
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="cancel"
                    )
            os.remove(filename)
        else:
            media_group = []
            for filename in filelist:
                if filename.endswith(("mp4", "webm", "mkv", "hevc", "avc", "mov")):
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="upload_video"
                    )
                    media_group.append(
                        InputMediaVideo(
                            open(filename, "rb"),
                            caption=CAPTION if (len(media_group) % 10 == 0) else "",
                            parse_mode="HTML",
                        )
                    )
                    time.sleep(0.4)
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="cancel"
                    )
                if filename.endswith(("jpg", "jpeg", "webp", "heic", "png")):
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="upload_photo"
                    )
                    media_group.append(
                        InputMediaPhoto(
                            open(filename, "rb"),
                            caption=CAPTION if (len(media_group) % 10 == 0) else "",
                            parse_mode="HTML",
                        )
                    )
                    time.sleep(0.2)
                    await context.bot.send_chat_action(
                        chat_id=update.effective_chat.id, action="cancel"
                    )
            with Loader(
                "Uploading Media Group",
                "Media Group Upload Success",
            ):
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
            for filename in filelist:
                os.remove(filename)

async def cobalt_dlp(update: Update, context: ContextTypes.DEFAULT_TYPE, audio=False) -> None:
    message = update.message

    # Handle media groups (photos or videos)
    splitted = message.text.split(' ')
    if len(splitted)>1:
        lol_msg = splitted[1]
    else:
        lol_msg =message.text
    # Implement your direct forwarding logic here
    if re.match(r"([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})",lol_msg):
        instagram = r"(https:\/\/)?((www|m).)?((instagram\.)([\w]+))[\S]*"
        tiktok= r"((https:\/\/)?(((www.)?tiktok\.com\/@[-a-z\.A-Z0-9_]+\/(video|photo)\/\d+)|(vt\.tiktok\.com\/[-a-zA-Z0-9]+)))"
        reddit = r"(https\:\/\/)?([w]+\.)?reddit\.com\/[A-Za-z_/0-9]+"
        facebook = r"(https\:\/\/)?([w]+\.)?(facebook|fb)\.(com|watch)\/[A-Za-z_/0-9]+(.php\?(id|v)=[\d]+)?"
        twitter = r"https?://(?:(?:www|m(?:obile)?)\.)?(?:(?:twitter|x)\.com|twitter3e4tixl4xyajtrzo62zg5vztmjuricljdp2c5kshju4avyoid\.onion)/"
        youtube = r"(?:https?://)?(?:(?:www|m)\.)?youtube\.com/shorts/[-a-zA-Z0-9]+"
        insta3rdparty = r'https:\/\/www\.picuki\.com\/media\/(\d+)'
        
        urls = re.findall(r"([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})",lol_msg)
        for a_url in urls:
            check, caption, files = cobalt(a_url,audio=audio).download()
            if check == False or check==None or len(files)<1:
                caption = f"""Your link couldn't be downloaded to \n\n Unsupported link Format or couldn't download😢 \n{update.message.text}\n\n You can still try to other methods"""
                await update.message.reply_markdown(
                    caption, reply_markup=ReplyKeyboardRemove(selective=True)
                )
                shutil.rmtree(os.path.join(os.getcwd(),'downloads'), ignore_errors=True)
                try:
                    await update.message.set_reaction(reaction="😭")
                except Exception as e:
                    # Handle message not found or other errors silently
                    print(f"Failed to set reaction: {e}")
            else:
                await send_and_all(update,context,check,caption,files,a_url)
                shutil.rmtree(os.path.join(os.getcwd(),'downloads'), ignore_errors=True)
                try:
                    await update.message.set_reaction(reaction="❤️‍🔥")
                except Exception as e:
                    print(f"Failed to set reaction: {e}")
    else:
        caption = f"""Not a Link \n\n Unsupported Format or Couldn't download😢 \n{update.message.text}\n\n You can still try to other methods"""
        await update.message.reply_markdown(
                    caption, reply_markup=ReplyKeyboardRemove(selective=True)
                )
        shutil.rmtree(os.path.join(os.getcwd(),'downloads'),ignore_errors=True)
        try:
            await update.message.set_reaction(reaction="😭")
        except Exception as e:
            print(f"Failed to set reaction: {e}")
    # You can implement link handling here
