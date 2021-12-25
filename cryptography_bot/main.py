from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import random
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
    text = "Hi there " + update.message.from_user.username + "!\nI'm the Codereptile cryptography bot v1.0.0\n" \
           + "I can encrypt your messages using Elgamal crypto-system over group G=(Z_p\\{0}, *)\n" \
           + "Use /help to list all available commands\n"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def help(update: Update, context: CallbackContext):
    text = "/encrypt {p} {g} {g^a} {message}\n" \
           + "Encrypts the {message} using {p} and {g} as settings for the crypto-system and {g^a} as a public key.\n"
    text += "/decrypt {p} {a} {encrypted-message}\n" \
            + "Decrypts the {encrypted-message} using {p} as a setting for the crypto-system and {a} as a private key\n"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def fast_pow(x, y, p):
    if y == 0:
        return 1
    if y % 2 == 0:
        tmp = fast_pow(x, y / 2, p)
        return (tmp * tmp) % p
    else:
        return (x * fast_pow(x, y - 1, p)) % p


def encrypt(update: Update, context: CallbackContext):
    data = update.message.text.split()
    if len(data) < 4:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Not enough fields")
    p = int(data[1])
    g = int(data[2])
    g_a = int(data[3])
    message = ""
    for part in data[4:]:
        message += part + " "

    text = "Your encrypted message:\n"

    for i in range(len(message) - 1):
        character = ord(message[i])
        b = random.randint(1, p)
        g_b = fast_pow(g, b, p)
        g_ab = fast_pow(g_a, b, p)
        encrypted_character = (character * g_ab) % p

        text += str(g_b) + " " + str(encrypted_character) + "\n"

    text += "-1"

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def decrypt(update: Update, context: CallbackContext):
    data = update.message.text.split()
    if len(data) < 3:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Not enough fields")
    p = int(data[1])
    a = int(data[2])

    text = "Your decrypted message:\n"

    i = 3
    while True:
        g_b = int(data[i])
        if g_b == -1:
            break
        encrypted_character = int(data[i + 1])

        character = (encrypted_character * fast_pow(g_b, p - 1 - a, p)) % p

        text += chr(character)

        i += 2

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")




if not TEST_MODE:
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('encrypt', encrypt))
    dispatcher.add_handler(CommandHandler('decrypt', decrypt))
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
