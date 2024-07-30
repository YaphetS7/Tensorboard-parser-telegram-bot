import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from config import token, path2runs, MINE
from utils import draw, parse_tfevent, get_all_paths
import os


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['get_logs'])
def start_message(message):
    if message.chat.id != MINE:
        return
    bot.send_message(message.chat.id, '\n'.join(get_all_paths(path2runs)))


@bot.message_handler(commands=['get_logs_keyboard'])
def start_message(message):
    if message.chat.id != MINE:
        return
    log_paths = get_all_paths(path2runs)
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 1
    for log_path in log_paths:
        button = InlineKeyboardButton(text=log_path, callback_data=log_path)
        keyboard.add(button)
    
    bot.send_message(message.chat.id, 'Choose path', reply_markup=keyboard)



@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.chat.id != MINE:
        return
    path = message.text
    d = parse_tfevent(os.path.join(path2runs, path))
    chart_buffer = draw('epoch',d)

    bot.send_photo(message.chat.id, chart_buffer)


@bot.callback_query_handler(func=lambda call: True)
def log_paths_button_callback(call):
    if call.message.chat.id != MINE:
        return
    path = call.data
    d = parse_tfevent(os.path.join(path2runs, path))
    chart_buffer = draw('epoch', d)
    bot.send_photo(
        call.message.chat.id,
        chart_buffer,
        caption=f'График для {path}'
    )
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)



if __name__ == '__main__':
    commands_list = [
        BotCommand('get_logs', 'Вывод путей сообщением'),
        BotCommand('get_logs_keyboard', 'Вывод путей кнопками')
    ]
    bot.set_my_commands(commands=commands_list)
    bot.polling()