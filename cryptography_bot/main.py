from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import os
import logging

token = os.environ['CRYPTOGRAPHY_BOT_TOKEN']

TEST_MODE = False
if token == "None":
    TEST_MODE = True

if not TEST_MODE:
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

LOGGING = True

if LOGGING:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi there " + update.message.from_user.username +
                                  "!\nI'm the Codereptile cryptography bot v0.1.0\n" +
                                  "Use /help to list all available commands\n")


def help(update: Update, context: CallbackContext):
    message = "command will be listed here"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message)


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if not TEST_MODE:
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

if __name__ == '__main__':
    if TEST_MODE:
        print("Test mode: docker launch success")
    else:
        updater.start_polling()
        debug_mode = True
        while debug_mode:
            command = ""
            try:
                command = input("Enter server-side command:\n")
                if command == "stop":
                    print("Shutting server down")
                    updater.stop()
                    exit(0)
                else:
                    print("Unknown command")
            except EOFError as e:
                print("Server in production mode:", e)
                debug_mode = False
