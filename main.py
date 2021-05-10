# -*- coding: utf-8 -*-
import telebot
from telebot import types

bot=telebot.TeleBot("1825773865:AAHASjes5aHTKTyt8FegYcGLBDPafO0hfAo")
channel="-1001347996353"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Вітаю, " + message.from_user.first_name + ".\nЦей бот створений для збору Вашої контактної інформації, яка буде передана соціальним службам щоб знайти волонтера для подальшої допомоги.")
    send_choose(message)

def send_choose(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_about = types.KeyboardButton("Про нас")
    button_request = types.KeyboardButton("Відправити заявку")
    keyboard.add(button_about, button_request)
    bot.send_message(message.chat.id, "⬇️ Оберіть потрібну Вам операцію", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == "Про нас":
        bot.send_message(message.chat.id, "❗️*Бот працює в тестовому режимі.*\n\nБот збирає Ваші контактні дані і надсилає запит на залучення волонтерів даним організаціям (список буде поповнюватися):\nУкраїнська волонтерська служба: https://volunteer.country/request\nНаціональний корпус: Волонтери #НКВолонтери\nГрупа активної реабілітації: https://gar.org.ua/\n“Сучасний погляд”: http://www.gssp.org.ua/pro-nas\n\n🧑‍💻*Розробники:*\nАдамчук Іван Іванович\nБехтер Ольга Костянтинівна\nБорецький Іван Володимирович\nВолянюк Богдан Анатолійович\nДаниленко Марія Вадимівна", parse_mode="Markdown", disable_web_page_preview=True)

    if message.text == "Відправити заявку":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_cancel = types.KeyboardButton("Відмінити")
        keyboard.add(button_cancel)
        bot.send_message(message.chat.id, "✍️ Опишіть в двух словах Вашу проблему, або натисність на кнопку нижче для відміни операції", reply_markup=keyboard)
        bot.register_next_step_handler(message, number_step)

    if message.text == "Відмінити":
        bot.send_message(message.chat.id, "👌 Операцію відмінено!")
        send_choose(message)

def number_step(message):
    if message.text == "Відмінити":
        bot.send_message(message.chat.id, "👌 Операцію відмінено!")
        send_choose(message)
    else:
        global problem
        problem = message.text
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Відправити телефон", request_contact=True)
        button_cancel = types.KeyboardButton("Відмінити")
        keyboard.add(button_phone, button_cancel)
        bot.send_message(message.chat.id, '⬇️ Натисність на кнопку нижче для автоматичної відправки номеру телефону або відмініть операцію', reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def contact(message):
    bot.send_message(message.chat.id, "💪 Дякую. Контактна інформація буде передана волонтерським організаціям для подальшої роботи.")
    
    if message.contact is not None:
        bot.send_message(channel, '❗️*Надійшла нова заявка!*\n\nКоментар: ' + problem + '\n\n⬇️ Контакт', parse_mode="Markdown")
        bot.send_contact(channel, first_name=message.contact.first_name, phone_number=message.contact.phone_number, last_name=message.contact.last_name)

    send_choose(message)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()