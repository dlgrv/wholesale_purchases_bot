import telebot
import threading

from config import token

import db
import function
import keyboard
import emoji
import variable
import texts

bot = telebot.TeleBot(token)

def start_update_purchases():
    try:
        function.purchases_calculating_time()
        threading.Timer(20, start_update_purchases).start()
    except Exception:
        print(Exception)
start_update_purchases()

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        check_user = db.check_user(message.from_user.id)
        if check_user:
            # НЕ В ПЕРВЫЙ РАЗ
            bot.send_sticker(message.chat.id,
                            'CAACAgIAAxkBAAK-lGAPa3mA92pHFzD4sEOuGceqKjR8AAJUAAOtZbwUJTaFSf0QNk4eBA')
            bot.send_message(message.chat.id,
                             f'{emoji.GOGGLES}Уже все работает',
                             reply_markup=keyboard.menu_keyboard)
        else:
            # В ПЕРВЫЙ РАЗ
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAK8oGANZIES4aae4B87-c4eI8o0GgeaAAJPAAOtZbwUa5EcjYesr5MeBA')
            bot.send_message(message.chat.id,
                             f'{emoji.SMILING_FACE_WITH_SUNGLASSES}Привет, {message.from_user.username}!\n'
                             f'Главное меню{emoji.BACKHAND_INDEX_POINTING_DOWN}\n'
                             f'(P.S. 1₽=1{emoji.STAR})',
                             reply_markup=keyboard.menu_keyboard)
            db.add_user(message.from_user.id, message.from_user.username)
    except Exception as e:
        print(repr(e))

@bot.message_handler(content_types=['text'])
def send_text(message):
    # ОБРАБОТКА ГЛАВНОЙ КЛАВИАТУРЫ
    try:
        if message.text == f'{emoji.RAINBOW}Каталог':
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAK_cmAQQyuk2IsBvZh4iNv6urt2Vw7vAAI1AAOtZbwU9aVxXMUw5eAeBA')
            bot.send_message(message.chat.id,
                             texts.catalog())
        elif message.text == f'{emoji.DOG_FACE}Личный кабинет':
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAK8s2ANavcla_bu4OBqoWWrFcrfCAbmAAJjAAOtZbwUOe6_ufD-GsYeBA')
            bot.send_message(message.chat.id,
                             texts.acc(message.from_user.id),
                             reply_markup=keyboard.acc,
                             parse_mode='Markdown')
        elif message.text == f'{emoji.NERD_FACE}Вопрос - Ответ':
            bot.send_message(message.chat.id,
                             texts.que_answ(),
                             reply_markup=keyboard.que_answ,
                             parse_mode='Markdown')
        elif message.text == f'{emoji.SHOPPING_CART}Мои закупки':
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAALDRWAUoUHcmpT9A5c97cJ9FKbX9L1AAAJZAAOtZbwU9LtHF4nhLQkeBA')
            bot.send_message(message.chat.id,
                             texts.shopping_cart(message.from_user.id))
                             #reply_markup=keyboard.shopping_cart)
        elif message.text == f'{emoji.OK_HAND}Отзывы':
            return_text = texts.reviews()
            bot.send_message(message.chat.id,
                             return_text,
                             parse_mode='MarkdownV2')
        elif message.text == f'{emoji.POSTAL_HORN}Гарантии':
            return_text = texts.guarantees()
            bot.send_message(message.chat.id,
                             return_text,
                             parse_mode='MarkdownV2')
        # ОБРАБОТКА ДОБАВЛЕНИЯ ЛОТА В "МОИ ЗАКУПКИ" ИЗ "КАТАЛОГА"
        elif '/add_lot_' in message.text:
            add_lot_numb = message.text.replace('/add_lot_', '')
            if add_lot_numb.isdigit():
                add_lot_numb = int(add_lot_numb)
                lot_name = function.get_lot_name(add_lot_numb)
                return_text = texts.confirmation_add_lot(lot_name)
                uid = message.from_user.id
                bot.send_message(message.from_user.id,
                                 return_text,
                                 reply_markup=keyboard.confirmation_add_lot)
                db.update_add_lot_numb(uid, add_lot_numb)
            else:
                bot.send_message(message.from_user.id,
                                 texts.bag_warning())
        elif '/edit_lot_' in message.text:
            edit_lot_numb = message.text.replace('/edit_lot_', '')
            if edit_lot_numb.isdigit():
                edit_lot_numb = int(edit_lot_numb)
                if edit_lot_numb > 0:
                    return_text = function.edit_lot_before(edit_lot_numb, message.from_user.id)
                    msg = bot.send_message(message.from_user.id,
                                           return_text)
                    bot.register_next_step_handler(msg, edit_lot_func)
                else:
                    return_text = texts.bag_warning()
                    bot.send_message(message.from_user.id,
                                     return_text)
            else:
                bot.send_message(message.from_user.id,
                                 texts.bag_warning())

        # ОБРАБОТКА КОМАНД АДМИНА/МОДЕРА
        elif 'balance' in message.text.lower() and message.from_user.id in variable.admin_id:
            balance_command = message.text.lower().split()
            try:
                if balance_command[1] == 'up':
                    user_id = balance_command[2]
                    amount = balance_command[3]
                    if db.check_user(user_id):
                        db.update_balance(user_id, amount)
                        bot.send_message(message.from_user.id,
                                         f'{emoji.CHECK_MARK_BUTTON}Успешное пополнение баланса')
                        bot.send_message(user_id,
                                         f'{emoji.CHECK_MARK_BUTTON}Пополнение баланса на сумму: {amount}{emoji.STAR}')
                    else:
                        bot.send_message(message.from_user.id,
                                         f'Пользователь не найден')
                if balance_command[1] == 'down':
                    user_id = balance_command[2]
                    amount = balance_command[3]
                    if db.check_user(user_id):
                        db.update_balance(user_id, -1*amount)
                        bot.send_message(message.from_user.id,
                                         f'{emoji.CHECK_MARK_BUTTON}Успешное списание баланса')
                    else:
                        bot.send_message(message.from_user.id,
                                         f'Пользователь не найден')
            except Exception as e:
                bot.send_message(message.from_user.id,
                                 f'{emoji.WARNING}Ошибка при выполнении команды\n'
                                 f'{e}')
                print('balance error', e)
        elif 'add' in message.text.lower() and message.from_user.id in variable.moder_id:
            add_command = message.text.lower().split()
            if add_command[1] == 'remind':
                bot.send_message(message.from_user.id,
                                 texts.add_example())
            elif len(add_command) > 2 and add_command[2].isdigit() and add_command[3].isdigit():
                function.add_purchase(add_command, message.from_user.id, message.from_user.username)
            elif add_command[1] == 'clean' and message.from_user.id in variable.admin_id:
                function.purchases_clean()
                bot.send_message(message.from_user.id,
                                 'Все закупки удалены.')
        elif message.text.lower() == 'clean shopping cart':
            function.clean_shopping_cart(message.from_user.id)
            bot.send_message(message.from_user.id,
                             'Корзина очищена.')
        elif message.text.lower() == 'help' and message.from_user.id in variable.moder_id:
            bot.send_message(message.from_user.id,
                             texts.help())
    except Exception as e:
        print(repr(e))

#ОБРАБОТКА ИНЛАЙН КЛАИВИАТУР ИЗ ЛИЧНОГО КАБИНЕТА И ПОПОЛНЕНИЯ БАЛАНСА
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'yes':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                uid = call.message.chat.id
                add_lot_numb = int(db.get_add_lot_numb(uid)[0])
                return_text = function.add_lot(add_lot_numb, uid)
                bot.send_message(uid,
                                 return_text)
            elif call.data == 'no':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_sticker(call.message.chat.id,
                                 'CAACAgIAAxkBAAK_cmAQQyuk2IsBvZh4iNv6urt2Vw7vAAI1AAOtZbwU9aVxXMUw5eAeBA')
                bot.send_message(call.message.chat.id,
                                 texts.catalog())
            elif call.data == 'balance':
                return_text = function.generate_random_number_for_add_balance(call.message.chat.id)
                print(return_text)
                msg = bot.send_message(call.message.chat.id,
                                       return_text,
                                       parse_mode='MarkdownV2',
                                       reply_markup=keyboard.balance_check)
            elif call.data == 'balance_check':
                uid = call.message.chat.id
                bool_balance_check, return_text = function.check_time_before_check(uid)
                if bool_balance_check:
                    bot.send_message(call.message.chat.id,
                                     return_text)
                else:
                    bot.send_message(call.message.chat.id,
                                     return_text,
                                     reply_markup=keyboard.balance_check_fail)
            elif call.data == 'address':
                msg = bot.send_message(call.message.chat.id,
                                       texts.address_example())
                bot.register_next_step_handler(msg, input_address)
            elif call.data == 'name':
                msg = bot.send_message(call.message.chat.id,
                                       texts.name_example())
                bot.register_next_step_handler(msg, input_name)

            elif call.data == 'phone_number':
                msg = bot.send_message(call.message.chat.id,
                                       texts.phone_number_example())
                bot.register_next_step_handler(msg, input_phone_number)
    except Exception as e:
        print(repr(e))

#ОБРАБОТКА ВВЕДЕННОГО АДРЕСА ПОСЛЕ НАЖАТИЯ "ИЗМЕНИТЬ АДРЕСС" В ЛК (ЛИЧНОМ КАБИНЕТЕ)
@bot.callback_query_handler(func=lambda call: True)
def input_address(message):
    try:
        uid = message.from_user.id
        address = message.text
        if len(address) > 15:
            db.add_address(uid, address)
            bot.send_message(message.chat.id,
                             f'{emoji.CHECK_MARK_BUTTON}Адрес изменен',
                             reply_markup=keyboard.menu_keyboard,
                             parse_mode= 'Markdown')
        else:
            bot.send_message(message.chat.id,
                             f'{emoji.PANDA}По-моему что-то не так...',
                             parse_mode='Markdown')
            send_text(message)
    except Exception as e:
        print(repr(e))

#ОБРАБОТКА ВВЕДЕННОГО ИМЕНИ ПОСЛЕ НАЖАТИЯ "ИЗМЕНИТЬ ИМЯ" В ЛК
@bot.callback_query_handler(func=lambda call: True)
def input_name(message):
    try:
        uid = message.from_user.id
        name = message.text
        if len(name) > 15:
            db.add_name(uid, name)
            bot.send_message(message.chat.id,
                             f'{emoji.CHECK_MARK_BUTTON}ФИО изменены',
                             reply_markup=keyboard.menu_keyboard,
                             parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id,
                             f'{emoji.PANDA}По-моему ты что-то неправильно ввел',
                             parse_mode='Markdown')
            send_text(message)
    except Exception as e:
        print(repr(e))

#ОБРАБОТКА ВВЕДЕННОГО ТЕЛЕФОНА ПОСЛЕ НАЖАТИЯ "ИЗМЕНИТЬ НОМЕР" В ЛК
@bot.callback_query_handler(func=lambda call: True)
def input_phone_number(message):
    try:
        uid = message.from_user.id
        phone_number = message.text
        if len(phone_number) >= 11 and phone_number[1:].isdigit():
            db.add_phone_number(uid, phone_number)
            bot.send_message(message.chat.id,
                             f'{emoji.CHECK_MARK_BUTTON}Телефон изменен',
                             reply_markup=keyboard.menu_keyboard,
                             parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id,
                             f'{emoji.PANDA}По-моему ты что-то неправильно ввел',
                             parse_mode='Markdown')
            send_text(message)
    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: True)
def edit_lot_func(message):
    try:
        uid = message.from_user.id
        quantity = message.text
        if quantity.isdigit():
            return_text = function.edit_lot_after(uid, quantity)
            bot.send_message(message.chat.id,
                             return_text,
                             reply_markup=keyboard.menu_keyboard,
                             parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id,
                             f'{emoji.PANDA}По-моему ты что-то неправильно ввел',
                             parse_mode='Markdown')
            send_text(message)
    except Exception as e:
        print(repr(e))

bot.polling()