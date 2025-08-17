from mytelegrammodules.commandhandlers.start import *
from mytelegrammodules.commandhandlers.help import *
from mytelegrammodules.commandhandlers.inlinedict import *
from mytelegrammodules.commandhandlers.nepcal import *
from mytelegrammodules.commandhandlers.vidauddl import *
from mytelegrammodules.commandhandlers.insta_igdlp import *
from mytelegrammodules.commandhandlers.ttok_dlp import *
from mytelegrammodules.commandhandlers.others import *
from mytelegrammodules.commandhandlers.gotra_handler import *
from mytelegrammodules.commandhandlers.ffmpeg_man import *
from mytelegrammodules.commandhandlers.multisocialdl import multi_social_dl
from mytelegrammodules.commandhandlers.general_downloader import *
from mytelegrammodules.commandhandlers.cobalt_handler import cobalt_dlp
from mytelegrammodules.commandhandlers.nepse import *


API_HASH = TG_BOT = os.getenv('TG_BOT_TOKEN')



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_HASH).read_timeout(500).write_timeout(1000).get_updates_read_timeout(200).connect_timeout(1000).build()
    print("Application is running!")
    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("send", send))
    application.add_handler(CommandHandler("echo", send))
    application.add_handler(CommandHandler("pin", pin))
    application.add_handler(CommandHandler("unpin", unpin))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("update", boradcast_all))
    application.add_handler(CommandHandler("broadcast", boradcast_all))
    application.add_handler(CommandHandler("sendall", boradcast_all))

    # application.add_handler(MessageHandler(filters.Regex(r'^\/send ') & ~filters.COMMAND, send, block=False))

    #Calendar variants
    application.add_handler(CommandHandler("ad", ad))
    application.add_handler(CommandHandler("toad", ad))
    application.add_handler(CommandHandler("bs", bs))
    application.add_handler(CommandHandler("tobs", bs))
    application.add_handler(CommandHandler("now", now))
    application.add_handler(CommandHandler("time", now))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("date", today))
    application.add_handler(CommandHandler("patro", patro))
    application.add_handler(CommandHandler("calendar", patro))
    application.add_handler(CommandHandler("calender", patro))
    application.add_handler(CommandHandler("month", patro))

    
    #rasifal variants
    application.add_handler(CommandHandler("rasifal", rasifal))
    application.add_handler(CommandHandler("rashi", rasifal))
    application.add_handler(CommandHandler("rasi", rasifal))
    application.add_handler(CommandHandler("rasifal", rasifal))
    application.add_handler(CommandHandler("rasiphal", rasifal))
    application.add_handler(CommandHandler("horoscope", rasifal))
    application.add_handler(CommandHandler("zodiac", rasifal))
    
    application.add_handler(CommandHandler("mygotra", my_gotra))
    application.add_handler(CommandHandler("gotra", my_gotra))
    application.add_handler(CommandHandler("sahagotri", sahagotri))
    application.add_handler(CommandHandler("findgotra", gotra))
    
    application.add_handler(CommandHandler("nepse", nepse, block=False))
    application.add_handler(CommandHandler("stock", nepse,block=False))
    application.add_handler(CommandHandler("scrip", nepse, block=False))


    #YTDLP
    application.add_handler(CommandHandler("video", video, block=True))
    application.add_handler(CommandHandler("audio", audio, block=True))
    
    #cobalt
    application.add_handler(CommandHandler("ig", instagram_dl, block=False))
    application.add_handler(CommandHandler("instagram", instagram_dl, block=False))
    
    #rapid_api
    application.add_handler(CommandHandler("igstory", rapid_ig_dl, block=False))
    application.add_handler(CommandHandler("ig2", rapid_ig_dl, block=False))
    application.add_handler(CommandHandler("igbackup", rapid_ig_dl, block=False))
    application.add_handler(CommandHandler("rapidapi", rapid_ig_dl, block=False))
    application.add_handler(CommandHandler("rapidig", rapid_ig_dl, block=False))
    
    application.add_handler(CommandHandler("terabox", terabox_dl, block=False))
    application.add_handler(CommandHandler("tera", terabox_dl, block=False))
    application.add_handler(CommandHandler("facebook", multi_social_dl, block=False))
    application.add_handler(CommandHandler("snapsave", multi_social_dl, block=False))
    application.add_handler(CommandHandler("x", multi_social_dl, block=False))
    application.add_handler(CommandHandler("twitter", multi_social_dl, block=False))
    application.add_handler(CommandHandler("tweet", multi_social_dl, block=False))
    application.add_handler(CommandHandler("fb", multi_social_dl, block=False))
    application.add_handler(CommandHandler("reddit", multi_social_dl, block=False))
    application.add_handler(CommandHandler("r", multi_social_dl, block=False))
    application.add_handler(CommandHandler("tiktok", short_vid_download, block=False))
    application.add_handler(CommandHandler("tt", cobalt_dlp, block=False))
    application.add_handler(CommandHandler("yt", cobalt_dlp, block=False))
    application.add_handler(CommandHandler("ytv", cobalt_dlp, block=False))
    application.add_handler(CommandHandler("cobalt", cobalt_dlp, block=False))
    application.add_handler(CommandHandler("cvideo", cobalt_dlp, block=False))

    application.add_handler(CommandHandler("ytm", partial(cobalt_dlp, audio=True), block=False))
    application.add_handler(CommandHandler("yta", partial(cobalt_dlp, audio=True), block=False))
    application.add_handler(CommandHandler("caudio", partial(cobalt_dlp, audio=True), block=False))
    application.add_handler(CommandHandler("ytaudio", partial(cobalt_dlp, audio=True), block=False))

    
    #Downloader
    application.add_handler(CommandHandler("download", file_dl, block=False))
    application.add_handler(CommandHandler("dwnld", file_dl, block=False))
    application.add_handler(CommandHandler("dwld", file_dl, block=False))
    application.add_handler(CommandHandler("file", file_dl, block=False))
    application.add_handler(CommandHandler("fdm", file_dl, block=False))
    application.add_handler(CommandHandler("dl", file_dl, block=False))
    application.add_handler(CommandHandler("direct_dl", file_dl, block=False))

    
    application.add_handler(InlineQueryHandler(inline_query))
        
    #For Short Video Links in Messages
    # application.add_handler(MessageHandler(filters.Regex('(?:https?://)?(?:(?:www|m)\.)?youtube\.com/shorts/[-a-zA-Z0-9]+|tiktok\.com/@[-a-zA-Z0-9_]+/video/\d+|vt\.tiktok\.com/[-a-zA-Z0-9]+') & ~filters.COMMAND, short_vid_download, block=False))
    # application.add_handler(MessageHandler(filters.Regex(r'(?:https?:\/\/)?(?:(?:www|m)\.)?(?:instagram\.com\/reel(s)?\/[-a-zA-Z0-9_]+|youtu(?:be\.com\/shorts\/|\.be\/)|tiktok\.com\/@[-a-zA-Z0-9_]+\/video\/\d+)') & ~filters.COMMAND, short_vid_download, block=True))
    # application.add_handler(MessageHandler(filters.Regex(r'(https?:\/\/(?:(www|m)\.)?instagram\.com\/p\/([^/?#&\s]+))') & ~filters.COMMAND, instagram_dl, block=True))
    # application.add_handler(MessageHandler(filters.Regex(r'((https:\/\/)?(((www.)?tiktok\.com\/@[-a-z\.A-Z0-9_]+\/photo\/\d+)|(vt\.tiktok\.com\/[-a-zA-Z0-9]+)))') & ~filters.COMMAND, tiktok_dl, block=True))
    # application.add_handler(MessageHandler(filters.Regex('(facebook\.com)\/((photo\/[\S]+)|(groups\/([\w\.]+\/permalink\/[\d]+))|([\w\.]+)\/(posts)\/[\w]+)') & ~filters.COMMAND, facebook_dl, block=False))

# (https?:\/\/(?:(www|m)\.)?instagram\.com\/(p|reel(s)?)\/([^/?#&\s]+))
    application.add_handler(MessageHandler(filters.Regex(r'(?:https?://)?(?:(?:www|m)\.)?youtube\.com/shorts/[-a-zA-Z0-9]+') & ~filters.COMMAND, cobalt_dlp, block=False))
    # application.add_handler(MessageHandler(filters.Regex(r'((http(s)?:\/\/)?(?:(www|m)\.)?instagram\.[\w]+([^?#&%\s]+)?)') & ~filters.COMMAND, instagram_dl, block=True))
    application.add_handler(MessageHandler(filters.Regex(r'(https:\/\/)?((www|m).)?((instagram\.)([\w]+))[\S]*') & ~filters.COMMAND, instagram_dl, block=True))    
    application.add_handler(MessageHandler(filters.Regex(r'((https:\/\/)?(((www.)?tiktok\.com\/@[-a-z\.A-Z0-9_]+\/(video|photo)\/\d+)|(vt\.tiktok\.com\/[-a-zA-Z0-9]+)))') & ~filters.COMMAND, multi_social_dl, block=True))
    application.add_handler(MessageHandler(filters.Regex(r'(?:terabox(?:app|link|share)?\.com|terabox\.app|nephobox\.com|4funbox\.com|mirrobox\.com|momerybox\.com|gibibox\.com|goaibox\.com|terasharelink\.com|freeterabox\.com|1024(?:tera|terabox)\.com|.*(?:tera|box).*)') & ~filters.COMMAND, terabox_dl, block=True))
    application.add_handler(MessageHandler(filters.Regex(r'(https\:\/\/)?([w]+\.)?reddit\.com\/[A-Za-z_/0-9]+') & ~filters.COMMAND, multi_social_dl, block=True))
    application.add_handler(MessageHandler(filters.Regex(r'(https\:\/\/)?([w]+\.)?(facebook|fb)\.(com|watch)\/[A-Za-z_/0-9]+(.php\?(id|v)=[\d]+)?') & ~filters.COMMAND, multi_social_dl, block=True))
    application.add_handler(MessageHandler(filters.Regex(r'https?://(?:(?:www|m(?:obile)?)\.)?(?:(?:twitter|x)\.com|twitter3e4tixl4xyajtrzo62zg5vztmjuricljdp2c5kshju4avyoid\.onion)/') & ~filters.COMMAND, multi_social_dl, block=True))
    application.add_handler(MessageHandler(filters.Regex(r'https:\/\/www\.picuki\.com\/media\/(\d+)') & ~filters.COMMAND, instagram_dl, block=True))    



#  insta+yt+tiktok = (?:https?://)?(?:(?:www|m)\.)?(?:instagram\.com/reel(s)?/[-a-zA-Z0-9_]+|youtu(?:be\.com/shorts/|\.be/)|tiktok\.com/@[-a-zA-Z0-9_]+/video/\d+|vt\.tiktok\.com/[-a-zA-Z0-9]+)'

    #For other links
    # application.add_handler(MessageHandler(filters.Regex('([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})') & ~filters.COMMAND, main_url_dl))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
