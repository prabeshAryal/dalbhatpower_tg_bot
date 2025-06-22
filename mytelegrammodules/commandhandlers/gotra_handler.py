from mytelegrammodules.commandhandlers.commonimports import *
from NEPAL.gotra.gotra import *


async def sahagotri(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued sahagotris Command")
    receivedstring = update.message.text
    splitted = receivedstring.split(' ')
    try:
        if len(splitted)==2:
            thequery = splitted[1]
            result = GOTRA().search_for_gotra(thequery)
            if result:
                sahagotriss = "\n-".join(result)
            else:
                return None
            messageeee = f"तपाइले दिएको गोत्र({thequery})मा पर्ने सहगोत्री थरहरु यस प्रकार छन् : \n\n-"+sahagotriss
            await update.message.reply_markdown(messageeee, reply_markup=ReplyKeyboardRemove(selective=True))
    except Exception as e:
        print(e)
    print("%50s"%"Done\n")
    
async def my_gotra(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued mygotra Command")
    receivedstring = update.message.text
    splitted = receivedstring.split(' ')
    try:
        if len(splitted)==2:
            thequery = splitted[1]
            result = GOTRA().search_for_thar(thequery)
            if result:
                tharssss = "\n-".join(result)
            else:
                return None
            messageeee = f"तपाइले थरको({thequery}) गोत्र यि मध्य कुनैपनि हुन सक्छ : \n\n-"+tharssss
            await update.message.reply_markdown(messageeee, reply_markup=ReplyKeyboardRemove(selective=True))
    except Exception as e:
        print(e)
    print("%50s"%"Done\n")

async def gotra(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    json = update.message.from_user
    # {'is_bot': False, 'username': 'sads', 'first_name': 'assad', 'last_name': 'asd', 'id': 23423234, 'language_code': 'en'}
    print((str(json['first_name']) +' ' +str(json['last_name'])+' : ' +str(json['id']))+" - Issued gotra Command")
    receivedstring = update.message.text
    splitted = receivedstring.split(' ')
    try:
        if len(splitted)==2:
            thequery = splitted[1]
            result = GOTRA().retrieve_all_sahagotris(thequery)
            if result:
                formatted_result = []
                for gotra, surnames in result.items():
                    formatted_result.append(f"{gotra}:\n\t" + "\n\t".join(surnames))
                sabgotrasss = "\n\n".join(formatted_result)
            else:
                return None
            messageeee = f"तपाइ‍ॅको ({thequery}) मिल्न सक्ने गोत्र वा थर हरु यस प्रकार छन् : \n\n"+ sabgotrasss
            await update.message.reply_markdown(messageeee, reply_markup=ReplyKeyboardRemove(selective=True))
    except Exception as e:
        print(e)
    print("%50s"%"Done\n")


