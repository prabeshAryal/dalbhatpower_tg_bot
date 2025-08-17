from mytelegrammodules.commandhandlers.commonimports import *
from mytelegrammodules.user_bot import TelethonModuleByME
from downloader.general import FileDownloader

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


async def file_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shutil.rmtree(os.path.join(os.getcwd(), 'downloads'), ignore_errors=True)
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Filedl Command")
    #Filter only URLS
    string = update.message.text
    
    if 'as_media' in string.lower():
        media = True
    else:
        media = False
         
    texter = update.message.from_user.full_name
    print(str(texter)+" sent a Full File download link" + str(string))
    pattern = r'([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
    entries = re.findall(pattern, string)
    try:
        for url in entries:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            check, CAPTION,filename = FileDownloader().download_file(url)
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            if check != False:
                if is_file_size_less_than_50mb(filename):
                    with Loader("Uploading Small File : ","Small File Upload Success"):
                        try:
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_document")
                            if media != True:
                                await update.message.reply_document(document=open(filename, 'rb'), caption=CAPTION, disable_content_type_detection=True, disable_notification=True, parse_mode='MARKDOWN')
                            else:
                                update.message.reply_document(document=open(filename, 'rb'), caption=CAPTION, disable_notification=True, parse_mode='MARKDOWN') 
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                        except Exception as e:
                            print(e)
                else :
                    try:
                        if media != True:
                            resp = await TelethonModuleByME.send_file_to_chat(filename, update, context, CAPTION)
                        else:
                            resp = await TelethonModuleByME.send_video_to_chat(filename, update, context, CAPTION)
                        fromchatid= int(os.environ.get('TG_APP_CHAT_ID'))
                        frommesid = resp.id
                        await update.message.reply_copy(from_chat_id=fromchatid, message_id=frommesid, caption=CAPTION,parse_mode='MARKDOWN')
                    except Exception as e:
                        print(e)
                try:
                    os.remove(filename)
                except Exception as e:
                    print(e)
            shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    except BaseException as e:
        print(e)
        shutil.rmtree(os.path.join(os.getcwd(), 'downloads'),
                      ignore_errors=True)
    print("%50s"%"Done\n")


