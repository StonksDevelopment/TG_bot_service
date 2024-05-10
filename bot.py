import telebot
from telebot import types
import os.path

print("Нажмите любую кнопку чтобы начать")
n = input()
if os.path.isfile('spisok.txt') == False:
    joinedFile1 = open("spisok.txt", "w")

print("Введите токен:")
botoken = input()
print("Введите id оператора:")
oper = int(input())
print("успешно")
bot = telebot.TeleBot(botoken)

@bot.message_handler(commands=['start'])
def formasters(message):
    bot.send_message(message.chat.id, "Здравствуйте! Введите команду /add (фамилия имя без скобок) для дальнейшей работы с ботом.")

@bot.message_handler(commands=['add'])
def formasters(message):
    joinedFile2 = open("spisok.txt", "a")
    joinedFile2.write(str(message.chat.id) + " " + message.text[message.text.find(' '):] + "\n")
    bot.send_message(message.chat.id, "Вы добавлены в базу")

@bot.message_handler(commands=['id'])
def id(message):
    if message.chat.id == oper:
        global master
        master = message.text[message.text.find(' '):]
        master = master.strip()
        bot.send_message(message.chat.id, "Принято")

@bot.message_handler(commands=['send'])
def otpravlaem(message):
    if message.chat.id == oper:
        markup = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton("Принимаю заказ", callback_data="question1")
        markup.add(button)
        bot.send_message(master, message.text[message.text.find(' '):], reply_markup=markup)
        bot.send_message(message.chat.id, "Отправлено")

@bot.message_handler(commands=['sum'])
def otpravlaemopy(message):
    bot.send_message(oper, "Мастер id:" + str(message.chat.id) + ", сумма работ составила" + message.text[message.text.find(' '):] + "р.")
    bot.send_message(message.chat.id, "Информация отправлена оператору")

@bot.message_handler(commands=['deny'])
def formasters(message):
    bot.send_message(oper, "Мастер id:" + str(message.chat.id) + ", отменил заказ по причине: " + message.text[message.text.find(' '):])
    bot.send_message(message.chat.id, "Информация отправлена оператору")

@bot.message_handler(commands=['time'])
def formasters(message):
    bot.send_message(oper, "Мастер id:" + str(message.chat.id) + ", перенёс заказ на " + message.text[message.text.find(' '):])
    bot.send_message(message.chat.id, "Информация отправлена оператору")

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == "question1":
            bot.send_message(oper,  "Мастер id:" + str(call.message.chat.id) + ", взял заказ.")
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton("Прибыл на адрес", callback_data="question2")
            markup.add(button1)
            bot.send_message(call.message.chat.id, "По прибытии нажмите кнопку <Прибыл на адрес>, информация будет отправлена оператору.", reply_markup=markup)
        elif call.data == "question2":
            bot.send_message(oper, "Мастер id:" + str(call.message.chat.id) + ", прибыл на место.")
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton("Приступаю к работе", callback_data="question3")
            button2 = types.InlineKeyboardButton("Перенести заказ", callback_data="question5")
            button3 = types.InlineKeyboardButton("Отменить заказ", callback_data="questionend")
            markup.add(button1, button2, button3)
            bot.send_message(call.message.chat.id, "Готовы приступить к работе?", reply_markup=markup)
        elif call.data == "question3":
            bot.send_message(oper, "Мастер id:" + str(call.message.chat.id) + ", приступил к работе.")
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton("Закрыть заказ", callback_data="question4")
            markup.add(button1)
            bot.send_message(call.message.chat.id, "Хорошо, после выполнения всех работ нажмите <Закрыть заказ>.", reply_markup=markup)
        elif call.data == "question4":
            bot.send_message(call.message.chat.id, "Пропишите команду /sum и после неё сумму, например: /sum 1000. ")
        elif call.data == "questionend":
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton("Да", callback_data="yes")
            button2 = types.InlineKeyboardButton("Нет", callback_data="questionend1")
            markup.add(button1, button2)
            bot.send_message(call.message.chat.id, "Вы уверены?", reply_markup=markup)
        elif call.data == "questionend1":
            bot.send_message(call.message.chat.id, "Бывает,просто вернитесь к предыдущему шагу и выберите нужный ответ.")
        elif call.data == "yes":
            bot.send_message(call.message.chat.id, "Укажите причину отмены заказа, написав команду /deny (Причина отмены).")
        elif call.data == "question5":
            bot.send_message(call.message.chat.id, "Укажите дату и время, на которые переносится заказ, введя команду /time (Дата и время).")

bot.polling(none_stop = True)