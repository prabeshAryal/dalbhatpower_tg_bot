from mytelegrammodules.commandhandlers.commonimports import *
from mytelegrammodules.user_bot import TelethonModuleByME
from downloader.teraboxdl import terabox_dlp

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


async def short_vid_download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)

    download=theOPDownloader()
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Sent Short Video Link")
    #Filter only URLS
    string = update.message.text
    print(str(string))
    pattern = r'([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    for url in entries:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        CAPTION, filename,check = download.short_vids(url)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")

        if check == True:
            print(filename)
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
            with Loader("Uploading Tiktok/YtShort : ","Tiktok/YtShort Upload Success"):
                video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
                await update.message.reply_video(video=open(filename, 'rb'),duration=video_duration, caption=CAPTION,write_timeout=1000, connect_timeout=1000, read_timeout=1000, disable_notification=True, width=video_dimensions.get('width', 0), height=video_dimensions.get('height', 0),thumbnail=open(video_thumbnail_path,'rb'), parse_mode='HTML', supports_streaming=True)
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            os.remove(filename)
    print("%50s"%"Done\n")


async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)

    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Video Command")
    download=theOPDownloader()
    #Filter only URLS
    string = update.message.text
    texter = update.message.from_user.full_name
    print(str(texter)+" sent a Full video link" + str(string))
    pattern = r'([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    for url in entries:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        CAPTION, filename,check = download.download_video(url)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
        if check == True:
            if is_file_size_less_than_50mb(filename):
                with Loader("Uploading Manual Short Video : ","Manual Short Video Upload Success"):
                    try:
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                        video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
                        # print(video_thumbnail_path)
                        await update.message.reply_video(video=open(filename, 'rb'),duration=video_duration, caption=CAPTION, write_timeout=1000, connect_timeout=1000, read_timeout=1000, disable_notification=True, width=video_dimensions.get('width', 0), height=video_dimensions.get('height', 0),thumbnail=open(video_thumbnail_path,'rb'), parse_mode='HTML', supports_streaming=True)
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                    except Exception as e:
                        print(e)
            else :
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
    print("%50s"%"Done\n")

async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)

    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Audio Command")
    download=theOPDownloader()
    #Filter only URLS
    string = update.message.text
    texter = update.message.from_user.full_name
    print(str(texter)+" sent a Full Audio link" + str(string))
    pattern = r'([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    for url in entries:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        CAPTION, filename,check = download.download_audio(url)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
        # await context.bot.send_video(chat_id=update.message.chat_id, video=open(filename, 'rb'), supports_streaming=True,caption = CAPTION, parse_mode='HTML')
        if check == True:
            if is_file_size_less_than_50mb(filename):
                with Loader("Uploading Short Audio : ","Short Audio Upload Success"):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_audio")
                    audio_duration, _, _ = extract_media_info(filename, 'audio')
                    await update.message.reply_audio(audio=open(filename, 'rb'),duration=audio_duration, caption=CAPTION, write_timeout=1000, connect_timeout=1000, read_timeout=1000, disable_notification=True,parse_mode='HTML')
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            else :
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
    print("%50s"%"Done\n")



async def terabox_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)

    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Terabox Command")
    #Filter only URLS
    string = update.message.text
    texter = update.message.from_user.full_name
    print(str(texter)+" sent a Terabox video link : " + str(string))
    pattern = r'([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    for url in entries:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        check,CAPTION, file_list = terabox_dlp(url)
        # print(file_list)
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
        if check == True:
            for filename in file_list:
                if is_file_size_less_than_50mb(filename):
                    with Loader("Uploading Terabox Short Video : ","Manual Terabox Video Upload Success"):
                        try:
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                            video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
                            # print(video_thumbnail_path)
                            await update.message.reply_video(video=open(filename, 'rb'),duration=video_duration, caption=CAPTION, write_timeout=1000, connect_timeout=1000, read_timeout=1000, disable_notification=True, width=video_dimensions.get('width', 0), height=video_dimensions.get('height', 0),thumbnail=open(video_thumbnail_path,'rb'), parse_mode='HTML', supports_streaming=True)
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                        except Exception as e:
                            print(e)
                else :
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
    print("%50s"%"Done\n")