
# Importing Secrets
import dotenv
dotenv.load_dotenv()
import mytelegrammodules.bot as bot




def startbot():
    print("Starting bot... ")
    bot.main()
    

if __name__ == "__main__":
    startbot()