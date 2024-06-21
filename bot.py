import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, CallbackContext
import requests

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define conversation states
NAME, AGE = range(2)

# Define start command handler
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton("Button 1"), KeyboardButton("Button 2"), KeyboardButton("Button 3")],
        [KeyboardButton("Button 4"), KeyboardButton("Button 5"), KeyboardButton("Button 6")],
        [KeyboardButton("Button 7")],
        [KeyboardButton("Button 8")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)
    update.message.reply_text('Please enter your name:')
    return NAME

# Define handler for collecting name
def get_name(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    context.user_data['name'] = update.message.text
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! Now, please enter your age:')
    return AGE

# Define handler for collecting age
def get_age(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    context.user_data['age'] = update.message.text
    logger.info("Age of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! You can now interact with the bot using the buttons.')
    return ConversationHandler.END

# Define handler for default button clicks
def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    keyboard = [
        [KeyboardButton("Button 9"), KeyboardButton("Button 10"), KeyboardButton("Button 11")],
        [KeyboardButton("Button 12"), KeyboardButton("Button 13"), KeyboardButton("Button 14")],
        [KeyboardButton("Button 15")],
        [KeyboardButton("Button 16")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('New buttons added:', reply_markup=reply_markup)

    inline_keyboard = [
        [InlineKeyboardButton(f'Count + {i}', callback_data=f'count_{i}') for i in range(1, 5)]
    ]
    inline_reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text('Inline buttons:', reply_markup=inline_reply_markup)

# Define handler for inline button clicks
def inline_button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")

# Define handler for /pic command
def send_picture(update: Update, context: CallbackContext) -> None:
    url = 'https://example.com/joker.jpg'  # Replace with actual URL of the Joker image
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("6620795518:AAHZKwor6vkorKVpxIQ_Li89BTOSRosPp_A")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states NAME and AGE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, get_age)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add handlers
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, button_click))
    dispatcher.add_handler(CallbackQueryHandler(inline_button_click))
    dispatcher.add_handler(CommandHandler('pic', data:image/jpeg;base64,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))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
