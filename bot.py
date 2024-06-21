from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler


def start(update: Update, context: CallbackContext):
    # Boshlang'ich 8 ta buttonlarni qo'shamiz
    buttons = [
        [KeyboardButton("Button 1"), KeyboardButton("Button 2"), KeyboardButton("Button 3")],
        [KeyboardButton("Button 4"), KeyboardButton("Button 5"), KeyboardButton("Button 6")],
        [KeyboardButton("Button 7")],
        [KeyboardButton("Button 8")]
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Choose an option:', reply_markup=keyboard)


def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # Inline buttonni ko'rsatamiz
    inline_buttons = [
        [InlineKeyboardButton("Count +", callback_data='count_plus')]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_buttons)
    query.edit_message_text(text=f"Button {query.data} bosildi!", reply_markup=inline_keyboard)


def add_buttons(update: Update, context: CallbackContext):
    # Yangi buttonlarni qo'shamiz
    buttons = [
        [KeyboardButton("New Button 1"), KeyboardButton("New Button 2"), KeyboardButton("New Button 3")],
        [KeyboardButton("New Button 4"), KeyboardButton("New Button 5"), KeyboardButton("New Button 6")],
        [KeyboardButton("New Button 7")],
        [KeyboardButton("New Button 8")]
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('More options added:', reply_markup=keyboard)

    # Inline buttonni ko'rsatamiz
    inline_buttons = [
        [InlineKeyboardButton("Count +", callback_data='count_plus')]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_buttons)
    update.message.reply_text('Inline buttons:', reply_markup=inline_keyboard)


def main():
    # Telegram Bot Token
    token = '6620795518:AAHZKwor6vkorKVpxIQ_Li89BTOSRosPp_A'

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # /start komandasi uchun handler
    dispatcher.add_handler(CommandHandler('start', start))

    # Har qanday text uchun handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, add_buttons))

    # Callback query handler
    dispatcher.add_handler(CallbackQueryHandler(button_handler, pattern='count_plus'))

    # Botni ishga tushiramiz
    updater.start_polling()
    updater.idle()


if name == 'main':
   main()