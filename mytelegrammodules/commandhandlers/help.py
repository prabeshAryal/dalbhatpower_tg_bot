from mytelegrammodules.commandhandlers.commonimports import *


# sample_text = '''
# **A lot of help commands available.**\n \n
#     \t`/start` - _Check whether bot is working or not._ 
#     \t`/help` - _This menu is displayed._
#     \t`/clean` - _Resets the bot server to the deployment time._\n \n 
# **Any Sort of Public Video Links** 
#     \t- _Sends you video upto 50MB using that link._\n
#     \t`/ytaudio` your\_youtube\_link - _Sends audio from link._ \n\n 
# **Some OpenAI tools :**\n 
#     \t•`/dalle` Write Something to generate Image from. - _Sends pictures from text._
#     \t•`/gpt` Write Something to generate Text from. - _Completes Your Text._ \n\n
# **Isn't this help enough ???**'''


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Help Command")
    
    helptext = ''' ‎ ‎ ‎ ‎ ‎ ‎ ‎***@DalBhatPowerBot*** \n‎ ‎ ‎ ‎ ‎ ‎ ‎__(v2.0 with Beta release)__
***Few help commands available.***

`/start` - _Check whether bot is working or not._  
`/help` - _This menu is displayed._

`/echo something` - _Copies message sent with or replied to_  
`/info something` - _General information of you_  
`/pin` - _Pins the message replied to_  
`/unpin` - _Unpins the message replied to_  
`/delete` - _Deletes the message replied to_

`any message with Tiktok / Facebook / Reddit / Twitter / Instagram / Terabox` - _Sends you videos/photos._  
`Only Youtube Shorts Link` - _Sends you videos._  
`@dalbhatpowerbot nepaliword` - _Can be Used to Search Nepali word._

`/ad 2072-10-18` - _Convert BS To AD (Beta)._  
`/bs 2000/10/08` - _Convert BS To AD._  
`/now` - _Displays current Nepali Time and Date._  
`/today` - _Displays today's Nepali Date_  
`/patro` - _Displays this Nepali Month_

`/rashi` - _Displays All Rashifal._  
`/rashi something` - _Displays only that horoscope_  
`/rashi makar` - _Displays only makar horoscope_  
`/rashi capricorn` - _Displays only makar horoscope_  
`something` can be name, horoscope or beginning letter in English, Nepali and Roman Versions

`/sahagotri gotra` - _Gives surnames with same gotras_  
`/mygotra surname` - _Gives your possible gotras_  
`/gotra surname` - _Gives your possible gotras_  
`/findgotra surname/gotra` - _Gives possible detailed gotra info_

`/video link` - _Downloads and sends videos (1080p) up to 2 GB_  
`/audio link` - _Downloads and sends audios (mp3) up to 2 GB_
*Use `/cobalt` if above fails !*
`/cobalt link` - _Downloads and sends videos (1080p) up to 2 GB_
`/caudio link` - _Downloads and sends audios (mp3) up to 2 GB_

`/ig link` - _Downloads and sends Instagram posts/reels/stories_  
`/X link` - _Downloads and sends tweets and videos_  
`/fb link` - _Downloads and sends Facebook videos_  
`/r link` - _Downloads and sends Reddit posts_  
`/tt link` - _Downloads and sends TikTok videos_
`/yt link` - _Downloads and sends Youtube videos_
`/yta link` - _Downloads and sends Youtube audios_

**👶BETA MODE**

`/nepse` - _Gives overall information about NEPSE_
`/nepse radhi` - _Gives stock price of RADHI scrip_

`/download link` - _Downloads and sends some directly downloadable files_
`/file`, `dwld`,`dwnld`,`dl`,`direct_dl`, does same too.
`/terabox` - _Downloads and sends Terabox Content_

**Isn't this help enough ???**
'''
# Downloads and send Facebook posts/videos (alpha)


    # await context.bot.send_message(chat_id=update.message.chat.id, text=helptext,parse_mode='MARKDOWN')
    await update.message.reply_markdown(
    helptext, reply_markup=ReplyKeyboardRemove(selective=True))
    # print("Help Module 1 completed successfully")



async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /info is issued."""
    message = update.message

    # Check if it's a personal chat
    if message.chat.type == 'private':
        user = message.from_user
        if user.username:
            infotext = f"Username: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
        else:
            infotext = f"First Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"

    # Check if it's a group chat
    elif message.chat.type == 'group':
        chat = message.chat
        infotext = f"Group Name: {chat.title}\nID: `-100{chat.id}`"

    # Check if the command mentions a user
    elif context.args:
        username = context.args[0]

        # Try to retrieve the user's information
        try:
            user = await context.bot.get_chat(username)
            if user:
                if user.username:
                    infotext = f"Username: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
                else:
                    infotext = f"First Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
        except Exception as e:
            infotext = f"User not found: {e}"

    # If none of the above, default to group info in groups, user info in private messages
    else:
        if message.chat.type == 'group':
            chat = message.chat
            infotext = f"Group Name: {chat.title}\nID: `{chat.id}`"
        else:
            user = message.from_user
            if user.username:
                infotext = f"Username: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
            else:
                infotext = f"First Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"

    await message.reply_markdown(infotext, reply_markup=ReplyKeyboardRemove(selective=True))
