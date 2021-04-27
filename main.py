import telebot
import config
import time
from user import User
from med import Med
from aid_kit import AidKit

bot = telebot.TeleBot(config.token)
user_dict = {}
med_dict = {}


#   TODO вынести формирование клавиатуры главного меню в отдельнную функцию.
def main_menu_helper(message):
    add_med_button = telebot.types.InlineKeyboardButton(
        text="Добавить 💊",
        callback_data="new_med")
    list_med_button = telebot.types.InlineKeyboardButton(
        text="Список 💊",
        callback_data="list_of_meds")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(add_med_button, list_med_button)
    bot.send_message(message.from_user.id,
                     "========= М Е Н Ю =========",
                     reply_markup=keyboard)


#   TODO вынести формирование клавиатуры главного меню в отдельнную функцию.
def simple_question_helper(message, callback_yes, callback_not):
    yes_button = telebot.types.InlineKeyboardButton(
        text="Да ✅",
        callback_data=callback_yes)
    not_button = telebot.types.InlineKeyboardButton(
        text="Нет ❌",
        callback_data=callback_not)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(yes_button, not_button)
    bot.send_message(message.from_user.id,
                     "Узнали? Согласны?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda query: query.data == "main_menu")
def main_menu(message):
    main_menu_helper(message)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую тебя, '
                     + message.from_user.first_name)
    new_user = User(message.from_user.first_name)
    new_user.tg_code = message.chat.id
    new_user.register_at = time.time()
    new_user.id = new_user.create_new_user()
    chat_id = message.chat.id
    user_dict[chat_id] = new_user
    main_menu_helper(message)


@bot.callback_query_handler(
    func=lambda query: query.data == "new_med")
def new_med(call):
    bot.answer_callback_query(call.id, call.data)
    back_to_menu_button = telebot.types.InlineKeyboardButton(
        text="Назад",
        callback_data="main_menu")
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(back_to_menu_button)
    bot.send_message(call.from_user.id,
                     "Как называется?", reply_markup=keyboard)
    bot.register_next_step_handler(call.message, get_med_name)


def get_med_name(message):

    med = Med(message.text)
    chat_id = message.chat.id
    med_dict[chat_id] = med
    text = """Итак, %s, верно? Теперь введите количество препарата\
в одной упаковке (шт, мл)""" % med.name
    bot.send_message(message.from_user.id, text)
    bot.register_next_step_handler(message, get_value_in_full)


def get_value_in_full(message):
    try:
        chat_id = message.chat.id
        value_in_full = message.text
        if not value_in_full.isdigit():
            msg = bot.reply_to(message, 'Введите числом, по-братски, а, ну чё ты')
            bot.register_next_step_handler(msg, get_value_in_full)
            return
        med = med_dict[chat_id]
        med.value_in_full = value_in_full
        msg = bot.reply_to(message, 'Pill is: \n %s \n %s' % (med.name, med.value_in_full))
        med_dict[chat_id] = med
        print("chat_id " + str(chat_id))
        bot.register_next_step_handler(message, simple_question_helper(message, 'save_med', 'restart_med'))
    except Exception as e:
        print("я здесь")
        bot.reply_to(message, e)


@bot.callback_query_handler(
    func=lambda query: query.data == 'save_med')
def save_new_med(call):
    try:
        print(call.message.chat.id)
        med = med_dict[call.message.chat.id]
        med_id = med.create_new_med()
        med.id = med_id
        text = "Сколько их у тебя сейчас осталось?"
        bot.send_message(call.from_user.id, text)
        bot.register_next_step_handler(call.message, testttt)
        return
    except Exception as e:
        raise Exception
        #   TODO разгрести завалы
        # add_med_button = telebot.types.InlineKeyboardButton(
        #     text="Добавить 💊",
        #     callback_data="new_med")
        # list_med_button = telebot.types.InlineKeyboardButton(
        #     text="Список 💊",
        #     callback_data="list_of_meds")
        # keyboard = telebot.types.InlineKeyboardMarkup()
        # keyboard.add(add_med_button, list_med_button)
        # bot.reply_to(call.message, 'та всё уже, поздняк. \n\
        # на-ка тут поковыряйся', reply_markup=keyboard)


def testttt(message):
    try:
        chat_id = message.chat.id
        value_fuct = message.text
        if not value_fuct.isdigit():
            msg = bot.reply_to(message, 'Введите числом, по-братски, а, ну чё ты')
            bot.register_next_step_handler(msg, testttt)
            return
        med = med_dict[chat_id]
        user = user_dict[chat_id]
        aid_kit = AidKit(med.id, user.id)
        aid_kit.create_new_aid_kit()
        print("Пиздос")
        # med_dict[chat_id] = med
        # bot.register_next_step_handler(msg, simple_question_helper(message, 'save_med', 'restart_med'))
    except Exception as e:
        print(e)
        bot.reply_to(message, e)


if __name__ == '__main__':
    bot.polling()
