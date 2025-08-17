from mytelegrammodules.commandhandlers.commonimports import *

import subprocess
import string,random
import json, os

import os
import subprocess
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import CallbackContext
from telegram.constants import ParseMode

def extract_media_info(media_file_path, media_type):
    command = [
        'ffprobe', '-v', 'error', '-show_entries', f'stream=duration,width,height{",album" if media_type=="audio" else ""}', '-of', 'json', media_file_path
    ]
    try:
        ffprobe_output = subprocess.check_output(command).decode('utf-8')
        media_info = json.loads(ffprobe_output)['streams'][0]
        duration = media_info.get('duration')  # Get the 'duration' value or None
        
        dimensions = {}
        if 'width' in media_info and 'height' in media_info:
            dimensions['width'] = int(media_info['width'])
            dimensions['height'] = int(media_info['height'])
    except (subprocess.CalledProcessError, KeyError, IndexError):
        duration = None
        dimensions = {}
    
    # Cast 'duration' to integer if it's not None, otherwise set a default value of 0
    duration = int(float(duration)) if duration is not None else 0
    
    thumbnail_path = None
    if media_type == 'video':
        thumbnail_path = extract_video_thumbnail(media_file_path)
    
    return duration, dimensions, thumbnail_path



def extract_video_thumbnail(video_url):
# Use ffmpeg to extract video thumbnail
    thumbnail_filename = generate_random_string() + '.jpg'
    THUMBNAIL_DIR = os.path.join(os.getcwd(),'downloads')
    thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_filename)
    command = ['ffmpeg', '-i', video_url, '-ss', '00:00:01', '-vframes', '1', thumbnail_path, '-y']
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return thumbnail_path

def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

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


# Directory where downloaded files are stored
DOWNLOADS_DIR = os.path.join(os.getcwd(),'downloads')

async def handle_files(update: Update, context: CallbackContext) -> None:
    filelist = os.listdir(DOWNLOADS_DIR)
    
    if len(filelist) == 1:
        filename = filelist[0]
        if filename.endswith(('mp4', 'webm', 'mkv')):
            caption = await execute_command_and_get_output(update, context, f"ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 '{filename}'")
            video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
            try:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=open(filename, 'rb'),
                    duration=video_duration,
                    width=video_dimensions['width'],
                    height=video_dimensions['height'],
                    thumbnail=open(video_thumbnail_path, 'rb'),
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    supports_streaming=True
                )
            except Exception as e:
                context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=open(filename, 'rb'),
                    duration=video_duration,
                    width=video_dimensions['width'],
                    height=video_dimensions['height'],
                    thumbnail=open(video_thumbnail_path, 'rb'),
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    supports_streaming=True
                )
            os.remove(filename)
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
        
        elif filename.endswith(('jpg', 'webp', 'heic')):
            caption = await execute_command_and_get_output(update, context, f"identify -format '%wx%h' '{filename}'")
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
            try:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(filename, 'rb'),
                    caption=caption,
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(filename, 'rb'),
                    caption=caption,
                    parse_mode=ParseMode.HTML
                )
            os.remove(filename)
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
    
    else:
        media_group = []
        for filename in filelist:
            if filename.endswith(('mp4', 'webm', 'mkv')):
                media_group.append(InputMediaVideo(open(os.path.join(DOWNLOADS_DIR, filename), 'rb'), parse_mode=ParseMode.HTML))
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                await asyncio.sleep(0.4)
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            
            elif filename.endswith(('jpg', 'jpeg', 'webp', 'heic')):
                media_group.append(InputMediaPhoto(open(os.path.join(DOWNLOADS_DIR, filename), 'rb'), parse_mode=ParseMode.HTML))
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                await asyncio.sleep(0.2)
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
        try:
            await context.bot.send_media_group(
                chat_id=update.effective_chat.id,
                media=media_group
            )
        except Exception as e:
            context.bot.send_media_group(
                chat_id=update.effective_chat.id,
                media=media_group
            )
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")

async def execute_command_and_get_output(update: Update, context: CallbackContext, command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Command execution failed with error:\n{e.stderr}"


# Example usage of the function
# Call handle_files(update, context) where update and context are passed from Telegram bot framework
