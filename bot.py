import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from main import main
from main import main_indiv
import os
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 8443))

telegram_bot_token = "YOUR_TOKEN_HERE"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    chat_id = update.effective_chat.id
    message = "Hello! Welcome to Cryptotracker Telegram Bot! To begin, please press top5 to show the Top 5 coin prices!"   
    context.bot.send_message(chat_id=chat_id, text=message)

def top5(update, context):
    chat_id = update.effective_chat.id
    message = ""
    crypto_data, coin_types = main()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        message += f"Coin: {coin}\nPrice: USD{price}\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)

def choosecoin(update, context):
    update.message.reply_text(text='Which coin do you want to track?🔎')

def get_coininfo(update, context):
    coin_name = update.message.text
    coin_name = str.lower(coin_name)
    # TODO: do what you want with book name
    res = main_indiv(coin_name)

    if res is None:
        crypto_data, coin_types = main()
        types = ''
        for i in coin_types[0:5]:
            types += i + ', '
        answer = f'Sorry! That is not a valid coin! Here are some of the coins that you can try: {types}\n please try again.'

    else:
        coin = res["coin"]
        price = res["price"]
        answer = f'The latest price for {coin} is {price}'
    update.message.reply_text(answer)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("top5", top5))
dispatcher.add_handler(CommandHandler("choosecoin", choosecoin))
dispatcher.add_handler(MessageHandler(Filters.text, get_coininfo))
# updater.start_polling()
updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=telegram_bot_token,
                          webhook_url = 'https://YOUR-HEROKU-NAME-HERE.herokuapp.com/' + telegram_bot_token)
updater.idle()