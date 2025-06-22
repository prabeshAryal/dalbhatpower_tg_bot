
# ---------------------------------------------------------------- #
#                    Import System modules
# ---------------------------------------------------------------- #

import os, re, sys,json,ast,shutil
import requests
import time, datetime,nepali_datetime
import html

# ---------------------------------------------------------------- #
# **************************************************************** #
# ---------------------------------------------------------------- #


# ---------------------------------------------------------------- #
#                   Import official packages
# ---------------------------------------------------------------- #

#Import Telegram Features
from telegram import InputMediaAudio, InputMediaVideo, InputMediaPhoto, Update, ReplyKeyboardRemove,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, Updater, InlineQueryHandler
from telegram.constants import ParseMode


# import loader
import contextlib
from utils.loader import Loader

# Multiprocess
# ---------------------------------------------------------------- #
# **************************************************************** #
# ---------------------------------------------------------------- #




# ---------------------------------------------------------------- #
#                    Import self made modules
# ---------------------------------------------------------------- #

from NEPAL.dict.nepali_dict import NepaliDictionary
from NEPAL.calendar.rasifal import NepaliRashiFal
from NEPAL.calendar.nepali_calendar import nepalSpecialTimes
from mytelegrammodules.database.databasemanager import DBMSSimple

from downloader.audio_video_downloader import theOPDownloader
from downloader.instagram import *


from utils.vid_aud_metadata import *


# ---------------------------------------------------------------- #
# **************************************************************** #
# ---------------------------------------------------------------- #


# ---------------------------------------------------------------- #
#                    Import Telegarm Command Functions
# ---------------------------------------------------------------- #
# Defined in Bot.py

# ---------------------------------------------------------------- #
# **************************************************************** #
# ---------------------------------------------------------------- #

from typing import TypedDict, List, Literal, cast
from telegram.ext import JobQueue
from telegram import (
    Update,
    InputMediaVideo,
    InputMediaPhoto,
    InputMediaDocument,
    InputMediaAudio,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    MessageHandler,
    filters,
    CommandHandler,
    ContextTypes,
    Application,
)
from utils.loader import Loader
from utils.vid_aud_metadata import *
from telegram.helpers import effective_message_type
from functools import partial
