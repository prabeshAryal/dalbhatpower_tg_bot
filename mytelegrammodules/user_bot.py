from telethon import TelegramClient
from utils.loader import Loader
from mytelegrammodules.commandhandlers.commonimports import *
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
import os 

api_id = int(os.environ.get('TG_APP_API_ID'))
api_hash = os.environ.get('TG_APP_API_HASH')
session = os.environ.get('TG_APP_SHORT_NAME')
chat_id=int(os.environ.get('TG_APP_CHAT_ID'))

class TelethonModuleByME():
    # def callback(current, total):
    #     # print('Uploaded', current, 'out of', total,
    #     #       'bytes: {:.2%}'.format(current / total))
    #     print('  {:.2f}/{:.2f} MB ({:.2%}) '.format((current/1000000),(total/1000000),(current/total)),end='',flush=True)
  
        # Function to send video to chat
    # Function to send audio to chat
    last_edit_time = 0  # Initialize the last edit time as 0
    past_size = 0
    
    

    async def send_audio_to_chat(audio_file_path, update, context, title):
        with Loader("Uploading Long Video : ", "Uploaded Successfully"):
            async with TelegramClient(session, api_id, api_hash) as client:
                audio_duration, _, _ = extract_media_info(audio_file_path, 'audio')
                attributes = [
                    DocumentAttributeAudio(
                        voice=False,  # Set to False to make audio streamable
                        duration=audio_duration,  # Set the duration in seconds (adjust as needed)
                    )
                ]
                message = await update.message.reply_text(f"🚀 Uploading: {title}\nSize: {TelethonModuleByME.get_readable_file_size(audio_file_path)}", parse_mode='HTML',disable_web_page_preview=True)
                a = await client.send_file(chat_id, audio_file_path,attributes=attributes, supports_streaming=True, progress_callback=lambda current, total: TelethonModuleByME.callback(current, total, context, message, title, audio_file_path, typee='Audio'))
                return a
    
    async def send_file_to_chat(file_path, update, context, title):
        with Loader("Uploading File: ", "Uploaded Successfully"):
            async with TelegramClient(session, api_id, api_hash) as client:
                # Prepare the message text with dynamic information
                message_text = (
                    f"🚀 Uploading...\n\n"
                    f"{title}"
                )
                # Send the initial message and upload the file
                message = await update.message.reply_text(message_text, parse_mode='MARKDOWN', disable_web_page_preview=True)
                a = await client.send_file(
                    chat_id,
                    file_path,
                    force_document=True,
                    progress_callback=lambda current, total: TelethonModuleByME.callback(current, total, context, message, title, file_path, message_text, typee='File')
                )
                return a
        
    async def send_video_to_chat(video_file_path, update, context, title):
        with Loader("Uploading Large Video : ", "Uploaded Successfully"):
            async with TelegramClient(session, api_id, api_hash) as client:
                video_duration, video_dimensions, video_thumbnail_path = extract_media_info(video_file_path, 'video')
                # extra_metadata = {
                #     'title': title,
                #     'duration': video_duration,
                #     'dimensions': f"{video_dimensions['width']}x{video_dimensions['height']}",
                #     'thumbnail': video_thumbnail_path
                # }
                attributes = [
                    DocumentAttributeVideo(
                        duration=video_duration,
                        w=video_dimensions['width'],
                        h=video_dimensions['height'],
                        supports_streaming=True
                    )
                ]
                
                # Prepare the message text with dynamic information
                message_text = (
                    f"🚀 Uploading Video: {title}\n"
                    f"Size: {TelethonModuleByME.get_readable_file_size(video_file_path)}\n"
                    f"Duration: {TelethonModuleByME.format_time(video_duration)}\n"
                    f"Dimensions: {video_dimensions['width']}x{video_dimensions['height']}"
                )
                
                # Send the initial message and embed metadata with the video
                message = await update.message.reply_text(message_text, parse_mode='HTML', disable_web_page_preview=True)
                a = await client.send_file(
                    chat_id,
                    video_file_path,
                    attributes=attributes,
                    supports_streaming=True,
                    thumb=video_thumbnail_path,
                    # extra=extra_metadata,
                    progress_callback=lambda current, total: TelethonModuleByME.callback(current, total, context, message, title, video_file_path,message_text, typee='Video')
                )
                return a

    @staticmethod
    def get_readable_file_size(file_path):
        size_in_bytes = os.path.getsize(file_path)
        size_units = ['B', 'KB', 'MB', 'GB', 'TB']
        size_index = 0
        while size_in_bytes >= 1024 and size_index < len(size_units) - 1:
            size_in_bytes /= 1024
            size_index += 1
        return f"{size_in_bytes:.2f} {size_units[size_index]}"
    
    @staticmethod
    # def format_time(seconds):
    #     """Convert seconds into a human-readable format of hours, minutes, and seconds."""
    #     if seconds < 60:
    #         return f"{seconds:.2f} seconds"
    #     elif seconds < 3600:
    #         minutes = seconds // 60
    #         seconds = seconds % 60
    #         return f"{minutes:.0f} minutes and {seconds:.2f} seconds"
    #     else:
    #         hours = seconds // 3600
    #         minutes = (seconds % 3600) // 60
    #         seconds = (seconds % 3600) % 60
    #         return f"{hours:.0f} hours, {minutes:.0f} minutes, and {seconds:.2f} seconds"
    def format_time(seconds):
        """Convert seconds into a concise human-readable format of hours, minutes, and seconds."""
        if seconds < 60:
            return f"{int(seconds)} Seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes:.0f} Min {int(seconds)} Sec"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.2f} Hrs {minutes:.0f} Mins"
    @staticmethod
    async def callback(current, total, context, message, title, file_path,extra_cap='', typee='File'):
        print('  {:.2f}/{:.2f} MB ({:.2%}) '.format((current/1000000),(total/1000000),(current/total)),end='',flush=True)
        percentage = (current / total)
        progress_bar_length = 15  # Length of the progress bar
        completed_blocks = int(percentage * progress_bar_length)
        remaining_blocks = progress_bar_length - completed_blocks
        
        # Construct the progress bar using Unicode characters (■ for completed, □ for remaining)
        progress_bar = "■" * completed_blocks + "□" * remaining_blocks
        extra_cap = '\n'.join(extra_cap.split('\n')[2:]) if typee == 'Video' else ''
        # if percentage == 1.0:
        #     progress_message =(
        #         f"🎉 Here is your file: {title}"
        #         f"Size: {TelethonModuleByME.get_readable_file_size(file_path)}\n"
        #         f"{extra_cap}\n") if typee!='File' else title
        # else:

        
        try:
            current_time = time.time()  # Get the current time
            time_since_last_edit = current_time - TelethonModuleByME.last_edit_time            
            if time_since_last_edit < 10 and percentage<1.0:
                pass
            elif percentage==1.0:
                await message.delete()
            else:
                past_size = TelethonModuleByME.past_size if hasattr(TelethonModuleByME, 'past_size') else 0
                # Calculate the size of the data transferred since the last measurement
                current_size = current - past_size
                # Update past_size to be the current amount of data transferred
                TelethonModuleByME.past_size = current
                # Calculate the speed in MB/s, assuming the time interval is 10 seconds
                speed = current_size / (1024 * 1024 * 10)  # size in MB divided by 10 seconds
                
                total_size = total  # Replace with the total size of the data to be transferred
                remaining_size = total_size - current
                
                if speed > 0:
                    time_remaining = (remaining_size / (1024 * 1024)) / speed  # remaining size in MB divided by speed in MB/s
                else:
                    time_remaining = float('inf')  # If speed is 0, set time remaining to infinity
        
                # Format the estimated time remaining
                formatted_time_remaining = TelethonModuleByME.format_time(time_remaining)
                
                progress_message = (
                    f"🚀 Uploading {typee}: {title}\n\n"
                    f"Size: {TelethonModuleByME.get_readable_file_size(file_path)}\n"
                    f"Progress: {percentage:.2%}\n"
                    f"Speed: {speed:.2f} MB/s\n"
                    f"ETA: {formatted_time_remaining}\n"
                    f"{extra_cap if extra_cap != title else ''}\n"  # Adjusted for correct conditional output
                    f"[{progress_bar}]"
                ) if typee != 'File' else (
                    f"🚀 Uploading...\n\n"
                    f"{title}\n"  # Added newline after title for proper formatting
                    f"Progress: {percentage:.2%}\n"
                    f"Speed: {speed:.2f} MB/s\n"  # Corrected float formatting
                    f"ETA: {formatted_time_remaining}\n"
                    f"[{progress_bar}]"
                )

                await message.edit_text(progress_message, parse_mode='HTML' if typee!='File' else 'MARKDOWN', disable_web_page_preview=True)
                TelethonModuleByME.last_edit_time = current_time  # Update the last edit time

        except Exception as e:
            print(e)



# async def main():
#     # Call the functions from telegram_utils with await
#     response = await TelethonModuleByME.send_video_to_chat(chat_id,'')
#     print(response)
#     # await send_audio_to_chat(chat_id, audio_file_path)

# # Create an event loop and run the main coroutine
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())


# response = await TelethonModuleByME.send_video_to_chat(chat_id,'')

#Upto 
#Here 
# Is
# Correct
