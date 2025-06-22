from mytelegrammodules.commandhandlers.commonimports import *

async def rasifal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Rasifal Command")
    receivedstring = update.message.text
    splitted = receivedstring.split(' ')
    if len(splitted) == 1:
        rashi=NepaliRashiFal.get_all_horoscope()
        await update.message.reply_sticker(sticker='CAACAgUAAxkBAAJ7-WXWLtcptK6ejCT7wtM8XpVE8XlXAAK3DQACMyCxVlaEjzU0X1irNAQ')
        await context.bot.send_message(chat_id=update.message.chat_id, text=rashi, parse_mode="MARKDOWN")
    else:
        rashi,which_rashi=NepaliRashiFal.get_horoscope(splitted[1])
        stickers = ['CAACAgUAAxkBAAJ74WXWKWOVywjGrjc9iz7YUIxnGNh0AAKeDwACtWuxVssBRvxLCox_NAQ','CAACAgUAAxkBAAJ742XWKWhOlMB8m-OTkXR5OP-v6m95AALtEAACE46xVuvFXw7YBgYJNAQ', 'CAACAgUAAxkBAAJ75WXWKWxMQeaIDwsW2YJi8Vj2UP8bAAKaDQAC2NmxVlj2VYEDp4W0NAQ', 'CAACAgUAAxkBAAJ752XWKXCE083Zn3Kt9wu9iK8RWRi2AAKrDQACM4C4Vk290tsPyqcdNAQ', 'CAACAgUAAxkBAAJ76WXWKXWs4YPL_euiyfdLb-7yfTkfAAKuDQACPXmxVidbu3IWF3MGNAQ', 'CAACAgUAAxkBAAJ762XWKXlmI5DuiZdUozNcoG_UrVQSAAIKDQAC68OxVhPxyJHgufnzNAQ', 'CAACAgUAAxkBAAJ77WXWKX2st3eXnLWdbaPsu6dcNL7nAAL3DgACqUm5VoxgyitRWEJrNAQ', 'CAACAgUAAxkBAAJ772XWKYAxGexGUmiD6cnR0SA5P4H6AAI5DwACjJuwVnNLLoVNlbLdNAQ','CAACAgUAAxkBAAJ78WXWKYXaegfmbdQooLicbtH9T8qrAAJKDgACxCmxVo2-1j7flB7lNAQ', 'CAACAgUAAxkBAAJ782XWKYnotppVQgKggw2os5fSjb-BAALDDwACpBKwVnDN-DU80cD2NAQ','CAACAgUAAxkBAAJ79WXWKZKdc8v_0MZBlG3EqBroZ2_YAAK_DgACBdGwViMLCU3hJk8tNAQ','CAACAgUAAxkBAAJ792XWKZYQx8id9r8nagnYNWQ_o6S4AAInDgACPtixVl5KXpz40gyJNAQ']
        if which_rashi ==8000:
            await update.message.reply_markdown("Timi paillai bhagaymani xau💖, rashi hernu pardaina.🥰", reply_markup=ReplyKeyboardRemove(selective=True))
        elif which_rashi != 69:    
            await update.message.reply_sticker(sticker=stickers[which_rashi])
            await context.bot.send_message(chat_id=update.message.chat_id, text=rashi, parse_mode="MARKDOWN")
        else:
            await update.message.reply_markdown(rashi, reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")
    
async def ad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued AD Command")
    string = ' '.join(update.message.text.split()[1:])
    await update.message.reply_markdown(nepalSpecialTimes.convert_to_ad(string), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")

async def bs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued BS Command")
    string = ' '.join(update.message.text.split()[1:])
    await update.message.reply_markdown(nepalSpecialTimes.convert_to_bs(string), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued NOW Command")
    await update.message.reply_markdown(nepalSpecialTimes.nepali_now(), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")



async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Today Command")
    await update.message.reply_markdown(nepalSpecialTimes.nepali_today(), reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")



async def patro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued Patro Command")
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    the_patro = str(nepalSpecialTimes.patro())
    cleaned_patro = ansi_escape.sub('___', the_patro)    
    await update.message.reply_markdown(cleaned_patro, reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")


