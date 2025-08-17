from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Function to process links - you will handle the implementation of this
def process_link(link):
    # This function should return a tuple: (status, caption, file_path_list)
    # Example:
    # return ("success", "Here's your file!", ["/path/to/file1", "/path/to/file2"])
    pass

async def send_and_all(update, context, check, caption, filelist, url):
    if check != False:
        cap = convert_html(caption)
        CAPTION = '<a href="'+url+'">'+cap+'</a>'
        if len(filelist) == 1:
            filename = filelist[0]
            if filename.endswith(('mp4','webm','mkv','hevc','avc')):
                video_duration, video_dimensions, video_thumbnail_path = extract_media_info(filename, 'video')
                video_thumbnail_path = video_thumbnail_path if os.path.exists(video_thumbnail_path) else None
                with Loader("Uploading Instagram Video", "Instagram Video Upload Success"):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                    try:
                        await update.message.reply_video(video=open(filename, 'rb'),duration=video_duration, write_timeout=1000, connect_timeout=1000, read_timeout=1000, caption=CAPTION, disable_notification=True, width=video_dimensions['width'], height=video_dimensions['height'], thumbnail=open(video_thumbnail_path,'rb') if video_thumbnail_path else None, parse_mode='HTML', supports_streaming=True)
                    except Exception as e:
                        await context.bot.send_video(chat_id=update.effective_chat.id,
                            video=open(filename, "rb"),
                            duration=video_duration,
                            write_timeout=1000,
                            connect_timeout=1000,
                            read_timeout=1000,
                            caption=CAPTION,
                            disable_notification=True,
                            width=video_dimensions["width"],
                            height=video_dimensions["height"],
                            thumbnail=open(video_thumbnail_path, "rb"),
                            parse_mode="HTML",
                            supports_streaming=True,
                        )
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            if filename.endswith(('jpg','jpeg', 'webp','heic')):
                with Loader("Uploading Instagram Photo", "Instagram Photo Upload Success"):
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
                if filename.endswith(('mp4', 'webm','mkv','hevc','avc')):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_video")
                    media_group.append(InputMediaVideo(open(filename, 'rb'), caption=CAPTION if (len(media_group)%10==0) else '', parse_mode='HTML'))
                    time.sleep(0.4)
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
                if filename.endswith(('jpg', 'jpeg','webp','heic')):
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
                    media_group.append(InputMediaPhoto(open(filename, 'rb'), caption=CAPTION if (len(media_group)%10==0) else '', parse_mode='HTML'))
                    time.sleep(0.2)
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="cancel")
            with Loader("Uploading Instagram Media Group", "Instagram Media Group Upload Success"):
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


# Function to forward photos and videos
async def forward_media(update: Update, context: CallbackContext):
    target_chat_id = 'nepalibeauties'  # Replace with the target chat ID (owner's chat)

    if update.message.photo:
        await context.bot.send_photo(chat_id=target_chat_id, photo=update.message.photo[-1].file_id, caption=update.message.caption)
    
    elif update.message.video:
        await context.bot.send_video(chat_id=target_chat_id, video=update.message.video.file_id, caption=update.message.caption)
    
    elif update.message.text:
        if "http" in update.message.text:
            status, caption, file_path_list = process_link(update.message.text)
            if status == "success":
                for file_path in file_path_list:
                    await context.bot.send_document(chat_id=target_chat_id, document=open(file_path, 'rb'), caption=caption)

# Start command
async def start(update: Update, context: CallbackContext):
    update.message.reply_text("I'm a forwarding bot! Send me photos, videos, or links, and I'll forward them.")

def main():
    token = '6902521433:AAGz26Do-zYaRrfW_yCjGTCTpmOsHw5syQI'  # Replace with your bot's token
    updater = Updater(token, use_context=True)
    
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo | Filters.video | Filters.text, forward_media))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
