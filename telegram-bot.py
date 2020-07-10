#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import ParseMode

import torrent_search


TELEGRAM_TOKEN = 'aaaaaaaaaaaaaaaaaaaaaaaaa'
# TELEGRAM_TARGET = os.environ['TELEGRAM_TARGET']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_SEARCH, TYPING_GET_TARGET = range(3)


def start(update, context):
    update.message.reply_text(
        "품번을 입력하세요")

    return TYPING_SEARCH

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("bye bye")

    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def regular_search(update, context):

    text = update.message.text

    context.user_data['torrent_info'] = []

    update.message.reply_text('[%s] :: 검색합니다. '%(text))

    torrent_search_results = torrent_search.torrent_search(text)

    if len(torrent_search_results) <= 0 :
        update.message.reply_text('[%s] :: 검색결과없습니다. 다시입력하세요. '%(text))
        return TYPING_SEARCH

    idx = 0

    update.message.reply_text('--- 검색결과 [%d 개] ---- '%(len(torrent_search_results)))

    for torrent_search_result in torrent_search_results :
        result_str = '[%d] ::: [%s] (seed: %s) (%s)'%(idx, torrent_search_result['size'], torrent_search_result['title'], torrent_search_result['seed'] )
        update.message.reply_text(result_str)
        idx = idx + 1

    context.user_data['torrent_infos'] = torrent_search_results

    update.message.reply_text(' --> 다운로드할 번호를 입력하세요. ')

    return TYPING_GET_TARGET

def regular_get_target(update, context):
    torrent_search_results = context.user_data['torrent_infos']

    text = update.message.text
    context.user_data['choice'] = text

    update.message.reply_text('입력한 순번은 [%s] 의 마그넷 주소를 찾습니다.'%(text))

    torrent_search_result = torrent_search_results[int(text)]
    magnet_url = torrent_search.get_magnet_addr(torrent_search_result['link'])

    if magnet_url is not None :
        update.message.reply_text('마그넷 주소를 찾았습니다!.. 마그넷을 추가합니다.')
        ####################################################################
        # todo magnet add proc........
        ####################################################################
        # 마그넷 주소를 얻어왔으니 추가할부분
        update.message.reply_text('다운로드 시작합니다... bye bye~ ')

    del context.user_data['torrent_infos']

    # restart search
    update.message.reply_text("품번을 입력하세요")

    return TYPING_SEARCH


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            TYPING_SEARCH: [MessageHandler(Filters.text,
                                           regular_search)
                            ],
            TYPING_GET_TARGET: [MessageHandler(Filters.text,
                                           regular_get_target)
                            ],
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
