import os
import random
import sys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

import strings as st


# Поиск токена
def getToken():
    token = ''
    if os.path.isfile(st.BOT_TOKEN_FILENAME):
        f = open(st.BOT_TOKEN_FILENAME, "r")
        token = f.read()
        f.close()
    else:
        print("Пожалуйста, создайте в папке проекта файл 'token.txt' и поместите туда токен для работы телеграм бота  и запустите скрипт заново")
        sys.exit()  
    return token


# проверка на выигрыш
def isWin(arr, who):
    if (((arr[0] == who) and (arr[4] == who) and (arr[8] == who)) or
            ((arr[2] == who) and (arr[4] == who) and (arr[6] == who)) or
            ((arr[0] == who) and (arr[1] == who) and (arr[2] == who)) or
            ((arr[3] == who) and (arr[4] == who) and (arr[5] == who)) or
            ((arr[6] == who) and (arr[7] == who) and (arr[8] == who)) or
            ((arr[0] == who) and (arr[3] == who) and (arr[6] == who)) or
            ((arr[1] == who) and (arr[4] == who) and (arr[7] == who)) or
            ((arr[2] == who) and (arr[5] == who) and (arr[8] == who))):
        return True
    return False


# возвращает количество неопределенных ячеек
def countUndefinedCells(cellArray):
    counter = 0
    for i in cellArray:
        if i == st.SYMBOL_UNDEF:
            counter += 1
    return counter


# callBackData - данные для формирования callBack данных обновленного игрового поля
def game(callBackData):
    message = st.ANSW_YOUR_TURN 
    alert = None

    buttonNumber = int(callBackData[0])  
    if not buttonNumber == 9:  
        charList = list(callBackData)  
        charList.pop(0)  
        if charList[buttonNumber] == st.SYMBOL_UNDEF: 
            charList[buttonNumber] = st.SYMBOL_X  
            if isWin(charList, st.SYMBOL_X):  
                message = st.ANSW_YOU_WIN
            else:  
                if countUndefinedCells(charList) != 0:  
                    isCycleContinue = True
                    while (isCycleContinue):
                        rand = random.randint(0, 8) 
                        if charList[rand] == st.SYMBOL_UNDEF:  
                            charList[rand] = st.SYMBOL_O
                            isCycleContinue = False  
                            if isWin(charList, st.SYMBOL_O):  
                                message = st.ANSW_BOT_WIN
        else:
            alert = st.ALERT_CANNOT_MOVE_TO_THIS_CELL
        if countUndefinedCells(charList) == 0 and message == st.ANSW_YOUR_TURN:
            message = st.ANSW_DRAW

        # формирование новой строчки callBackData на основе сделанного хода
        callBackData = ''
        for c in charList:
            callBackData += c


    # проверка, что игра закончилась (message равно одному из трех вариантов: победил Х, 0 или ничья):
    if message == st.ANSW_YOU_WIN or message == st.ANSW_BOT_WIN or message == st.ANSW_DRAW:
        message += '\n'
        for i in range(0, 3):
            message += '\n | '
            for j in range(0, 3):
                message += callBackData[j + i * 3] + ' | '
        callBackData = None  # обнуление callBackData
    return message, callBackData, alert


# на вход получает callBackData - данные с callBack-кнопки
def getKeyboard(callBackData):
    keyboard = [[], [], []]

    if callBackData != None:  
        for i in range(0, 3):
            for j in range(0, 3):
                keyboard[i].append(InlineKeyboardButton(callBackData[j + i * 3], callback_data=str(j + i * 3) + callBackData))
    return keyboard


def newGame(update, _):
    # сформировать callBack данные для первой игры, то есть строку, состояющую из 9 неопределенных символов
    data = ''
    for i in range(0, 9):
        data += st.SYMBOL_UNDEF

    # отправить сообщение для начала игры
    update.message.reply_text(st.ANSW_YOUR_TURN, reply_markup=InlineKeyboardMarkup(getKeyboard(data)))


def button(update, _):
    query = update.callback_query
    callbackData = query.data 

    message, callbackData, alert = game(callbackData) 
    if alert is None:  
        query.answer()  
        query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(getKeyboard(callbackData)))
    else: 
        query.answer(text=alert, show_alert=True)


def help_command(update, _):
    update.message.reply_text(st.ANSW_HELP)


if __name__ == '__main__':
    updater = Updater(getToken())  # получения токена из файла 'token.txt' и инициализация updater

    # добавление обработчиков
    updater.dispatcher.add_handler(CommandHandler('start', newGame))
    updater.dispatcher.add_handler(CommandHandler('new_game', newGame))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, help_command))  # обработчик на любое текстовое сообщение
    updater.dispatcher.add_handler(CallbackQueryHandler(button))  # добавление обработчика на CallBack кнопки

    # Запуск бота
    updater.start_polling()
    updater.idle()