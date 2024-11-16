import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Dispatcher
from flask import Flask, request
import os

# Setup basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your own Telegram Bot token
TOKEN = os.getenv('7156757667:AAGveiJjxqSlANKXKaV5rAvZxP78y4_CQiI')
PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)

# Define the start command handler
def start(update: Update, context):
    chat_id = update.message.chat_id
    keyboard = [
        [InlineKeyboardButton("Button 1", callback_data='1'), InlineKeyboardButton("Button 2", callback_data='2')],
        [InlineKeyboardButton("Button 3", callback_data='3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to the bot! Here is your photo:', reply_markup=reply_markup)
    update.message.reply_photo(photo='https://example.com/photo.jpg', caption='Here is a cool photo!')

# Handle button press
def button(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")

# Setup Webhook Handler
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running...'

def main():
    # Create an Updater object with your bot token
    global bot, dispatcher
    bot = Bot(token=TOKEN)
    dispatcher = Dispatcher(bot, None)

    # Add handlers for /start command and callback buttons
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Set webhook
    bot.set_webhook(url=f'https://<your-app-name>.onrender.com/{TOKEN}')

if __name__ == "__main__":
    main()
    app.run(host="0.0.0.0", port=PORT)
