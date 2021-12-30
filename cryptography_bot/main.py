from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import random
import os
import logging
import sympy

token = os.environ['CRYPTOGRAPHY_BOT_TOKEN']
ENCRYPTION_BASE = 1114112

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
    text = "Hi there " + update.message.from_user.username + "!\nI'm the Codereptile cryptography bot v1.2.0\n" \
           + "I can encrypt your messages using Elgamal crypto-system over group G=(Z_p\\{0}, *)\n" \
           + "Use /help to list all available commands\n"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def help(update: Update, context: CallbackContext):
    text = "/encrypt {p} {g} {g^a} {message}\n" \
           + "Encrypts the {message} using {p} and {g} as settings for the crypto-system and {g^a} as a public key.\n"
    text += "-------\n"
    text += "/decrypt {p} {a} {encrypted-message}\n" \
            + "Decrypts the {encrypted-message} using {p} as a setting for the crypto-system and {a} as a private key\n"
    text += "-------\n"
    text += "/encrypt_simple {p} {g} {g^a} {message}\n" \
            + "Same as /encrypt, but prints numbers in base10 and encodes every symbol independently\n"
    text += "-------\n"
    text += "/decrypt_simple {p} {a} {encrypted-message}\n" \
            + "Used for deciphering messages, encrypted with /encrypt_simple\n"
    text += "-------\n"
    text += "/gen_keys {min_p}\n" \
            + "Creates a crypto-system G (with p >= min_p) and pair of private and corresponding private keys\n"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def encrypt_simple(update: Update, context: CallbackContext):
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
        g_b = pow(g, b, p)
        g_ab = pow(g_a, b, p)
        encrypted_character = (character * g_ab) % p

        text += str(g_b) + " " + str(encrypted_character) + "\n"

    text += "-1"

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def decrypt_simple(update: Update, context: CallbackContext):
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

        character = (encrypted_character * pow(g_b, p - 1 - a, p)) % p

        text += chr(character)

        i += 2

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def base62_encode(value: int) -> str:
    ans_str = ""
    while value > 0:
        digit = value % 62
        if digit <= 9:
            ans_str += chr(ord('0') + digit)
        elif digit <= 9 + 26:
            ans_str += chr(ord('a') + digit - 10)
        else:
            ans_str += chr(ord('A') + digit - 10 - 26)
        value //= 62
    return ans_str[::-1]


def base62_decode(string: str) -> int:
    number = 0
    for digit in string:
        number *= 62
        if digit.isupper():
            number += ord(digit) - ord('A') + 10 + 26
        elif digit.islower():
            number += ord(digit) - ord('a') + 10
        else:
            number += ord(digit) - ord('0')
    return number


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

    message_number = 0
    for i in range(len(message) - 1):
        message_number *= ENCRYPTION_BASE
        message_number += ord(message[i])

    message_list = list()
    while message_number > 0:
        message_list.append(int(message_number % p))
        message_number //= p
    message_list.reverse()

    text = "Your encrypted message:\n"

    for message_digit in message_list:
        b = random.randint(1, p)
        g_b = pow(g, b, p)
        g_ab = pow(g_a, b, p)
        encrypted_character = (message_digit * g_ab) % p

        text += base62_encode(g_b) + " " + base62_encode(encrypted_character) + "\n"

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

    message_list = list()

    i = 3
    while True:
        g_b = data[i]
        if g_b == '-1':
            break
        g_b = base62_decode(g_b)
        encrypted_digit = base62_decode(data[i + 1])

        decrypted_digit = (encrypted_digit * pow(g_b, p - 1 - a, p)) % p

        message_list.append(decrypted_digit)

        i += 2

    message_number = 0
    for message_digit in message_list:
        message_number *= p
        message_number += message_digit

    message = ""
    while message_number > 0:
        message += chr(int(message_number % ENCRYPTION_BASE))
        message_number //= ENCRYPTION_BASE
    text += message[::-1]

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def gen_keys(update: Update, context: CallbackContext):
    min_p = 1000
    data = update.message.text.split()
    print(len(data))
    if len(data) > 3:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Too many fields")
    elif len(data) == 2:
        min_p = int(data[1])

    text = "Your key set:\n"

    p = sympy.randprime(min_p, min_p * 2)
    text += "P = " + str(p) + "\n"
    g = sympy.randprime(p, 2 * p) % p
    text += "G = " + str(g) + "\n"
    a = random.randint(int(p / 2), p)
    text += "A(private key) = " + str(a) + " KEEP THIS NUMBER SECRET!!!\n"
    g_a = pow(g, a, p)
    text += "G^A(public key) = " + str(g_a) + "\n"

    text += "\nNow your friend can make a secure message using:\n"
    text += "/encrypt " + str(p) + " " + str(g) + " " + str(g_a) + " {some message}\n"
    text += "Which could be decrypted using only:\n"
    text += "/decrypt " + str(p) + " " + str(a) + " {encrypted message}\n"

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if not TEST_MODE:
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('encrypt', encrypt))
    dispatcher.add_handler(CommandHandler('decrypt', decrypt))
    dispatcher.add_handler(CommandHandler('encrypt_simple', encrypt_simple))
    dispatcher.add_handler(CommandHandler('decrypt_simple', decrypt_simple))
    dispatcher.add_handler(CommandHandler('gen_keys', gen_keys))
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
