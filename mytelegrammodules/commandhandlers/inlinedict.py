from mytelegrammodules.commandhandlers.commonimports import *

from telegram.constants import ParseMode
from html import escape
from uuid import uuid4

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    if not query:  # empty query should not be handled
        return

    # results = [
    #     InlineQueryResultArticle(
    #         id=str(uuid4()),
    #         title="Caps",
    #         input_message_content=InputTextMessageContent(query.upper()),
    #     ),
    #     InlineQueryResultArticle(
    #         id=str(uuid4()),
    #         title="Bold",
    #         input_message_content=InputTextMessageContent(
    #             f"<b>{escape(query)}</b>", parse_mode=ParseMode.HTML
    #         ),
    #     ),
    #     InlineQueryResultArticle(
    #         id=str(uuid4()),
    #         title="Italic",
    #         input_message_content=InputTextMessageContent(
    #             f"<i>{escape(query)}</i>", parse_mode=ParseMode.HTML
    #         ),
    #     ),
    # ]
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=rf"{query}",
            description=rf"{NepaliDictionary.nepali_dictionary(query)}",
            input_message_content=InputTextMessageContent(NepaliDictionary.nepali_dictionary(query),parse_mode=ParseMode.MARKDOWN),
        )]

    await update.inline_query.answer(results)