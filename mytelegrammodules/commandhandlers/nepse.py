from mytelegrammodules.commandhandlers.commonimports import *
from NEPAL.NEPSE.nepse import NepalStock

async def nepse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
# {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued NEPSE Command ")
    # print(str(texter)+" issued a NEPSE command.")
    receivedstring = update.message.text
    print(str(receivedstring))
    splitted = receivedstring.split(' ')

    if len(splitted) == 1:
        with contextlib.redirect_stdout(None):
            NEPSE=NepalStock.nepse_indexes()
    else:
        with contextlib.redirect_stdout(None):
            NEPSE=NepalStock.nepse_single_stock(splitted[1])   
    await update.message.reply_markdown(NEPSE, reply_markup=ReplyKeyboardRemove(selective=True))
    print("%50s"%"Done\n")

    