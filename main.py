import telebot
from telebot import types

bot = telebot.TeleBot("1825773865:AAHASjes5aHTKTyt8FegYcGLBDPafO0hfAo")
owner="-1001347996353"

@bot.message_handler(commands=['start'])
def send_choose(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Про нас')
    itembtn2 = types.KeyboardButton('Відправити заявку')
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, "Вітаю, " + message.from_user.first_name + ".\nВас вітає бот Соціального працівника. Бот створений для збору Вашої контактної інформації, яка буде передана соціальним службам щоб знайти волонтера для подальшої допомоги.", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == "Про нас":
        bot.send_message(message.chat.id, "Бот працює в тестовому режимі.\n\nБот збирає Ваші контактні дані і надсилає запит на залучення волонтерів даним організаціям (список буде поповнюватися):\nУкраїнська волонтерська служба https://volunteer.country/request\nНаціональний корпус: Волонтери #НКВолонтери\nГрупа активної реабілітації https://gar.org.ua/\n“Сучасний погляд” http://www.gssp.org.ua/pro-nas\n\nРозробники:\nАдачук Іван Іванович\nБехтер Ольга Костянтинівна\nБорецький Іван Володимирович\nВолянюк Богдан Анатолійович\nДаниленко Марія Вадимівна", disable_web_page_preview=True)

    if message.text == "Відправити заявку":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Відправити телефон", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, 'Натисність на кнопку нижче для автоматичної відправки номеру телефону.', reply_markup=keyboard)

@bot.message_handler(content_types=['contact'])
def contact(message):
    bot.send_message(message.chat.id, 'Дякую.\nКонтактна інформація буде передана волонтерським організаціям для подальшої роботи.\nУ разі необхідності отримання повторної допомоги - відправте контакти ще раз.\nВсього найкращого!')
    if message.contact is not None:
        bot.send_contact(owner, first_name=message.contact.first_name, phone_number=message.contact.phone_number, last_name=message.contact.last_name)

if __name__ == '__main__':
    bot.polling(none_stop = True)