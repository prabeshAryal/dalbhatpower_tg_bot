from mytelegrammodules.commandhandlers.commonimports import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    # print(update)
    # print(update.message['text']+" - Bot is already running!")
    chatid = update.message.chat_id
    texter = update.message.chat.full_name
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Start Command")
    group = update.message.chat.title
    username = update.message.chat.username
    # print(str(chatid)+ str(texter)+ str(group)+ str(username))
    DBMSSimple.update_data(chatid,texter,username,group)
    await update.message.reply_html(
        rf"Dear {user.mention_html()}, Bot is active, Send /help for any queries regarding how to use bot.", reply_markup=ReplyKeyboardRemove(selective=True))

