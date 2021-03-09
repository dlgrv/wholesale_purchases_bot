import emoji
import telebot

menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
menu_keyboard.row(f'{emoji.RAINBOW}Каталог', f'{emoji.DOG_FACE}Личный кабинет')
menu_keyboard.row(f'{emoji.NERD_FACE}Вопрос - Ответ', f'{emoji.SHOPPING_CART}Мои закупки')
menu_keyboard.row(f'{emoji.OK_HAND}Отзывы', f'{emoji.POSTAL_HORN}Гарантии')

# CATALOG DEVICE KEYBOARD
catalog_device_inline_keyboard = telebot.types.InlineKeyboardMarkup()
emoji_for_catalog_device = [emoji.LOVE_YOU_GESTURE,
                     emoji.THUMBS_UP,
                     emoji.INDEX_POINTING_UP,
                     emoji.CALL_ME_HAND,
                     emoji.VULCAN_SALUTE,
                     emoji.LOVE_YOU_GESTURE,
                     emoji.THUMBS_UP,
                     emoji.INDEX_POINTING_UP,
                     emoji.CALL_ME_HAND,
                     emoji.VULCAN_SALUTE]

# КЛАВИАТУРА "ЛИЧНЫЙ КАБИНЕТ"
acc = telebot.types.InlineKeyboardMarkup()
acc_address = telebot.types.InlineKeyboardButton(text=f'{emoji.OPEN_MAILBOX_WITH_RAISED_FLAG}Изменить адрес',
                                                 callback_data='address')
acc_name = telebot.types.InlineKeyboardButton(text=f'{emoji.FILE_CABINET}Изменить ФИО',
                                              callback_data='name')
acc_phone_number = telebot.types.InlineKeyboardButton(text=f'{emoji.MOBILE_PHONE}Изменить номер',
                                                      callback_data='phone_number')
acc_balance = telebot.types.InlineKeyboardButton(text=f'{emoji.CREDIT_CARD}Пополнить баланс',
                                                 callback_data='balance')
acc_support = telebot.types.InlineKeyboardButton(text=f'{emoji.PANDA}Поддержка',
                                                url='https://t.me/lenkablue')
acc.add(acc_phone_number, acc_address)
acc.add(acc_name)
acc.add(acc_support, acc_balance)

# КЛАВИАТУРА "ВОПРОС- ОТВЕТ"
que_answ = telebot.types.InlineKeyboardMarkup()
que_answ.add(telebot.types.InlineKeyboardButton(text=f'{emoji.PANDA}Поддержка',
                                                url='https://t.me/lenkablue'))

# КЛАВИАТУРА "МОИ ЗАКУПКИ"
shopping_cart = telebot.types.InlineKeyboardMarkup()
shopping_cart_order = telebot.types.InlineKeyboardButton(text=f'{emoji.MEMO}Оформить заказ',
                                                         callback_data='order')
shopping_cart.add(shopping_cart_order)

# КЛАВИАТУРА "НЕДОСТАТОЧНО СРЕДСТВ"
insufficient_funds = telebot.types.InlineKeyboardMarkup()
insufficient_funds.add(telebot.types.InlineKeyboardButton(text=f'{emoji.CREDIT_CARD}Пополнить баланс',
                                                          callback_data='balance'))

#КЛАВИАТУРА "ПРОВЕРИТЬ ПОПОЛНЕНИЕ БАЛАНСА"
balance_check = telebot.types.InlineKeyboardMarkup()
balance_check.add(telebot.types.InlineKeyboardButton(text=f'{emoji.FACE_WITH_MONOCLE}Проверить пополнение',
                                                   callback_data='balance_check'))
#КЛАВИАТУРА "ФЭЙЛ В ПОПОЛНЕНИИ БАЛАНСА"
balance_check_fail = telebot.types.InlineKeyboardMarkup()
support = telebot.types.InlineKeyboardButton(text=f'{emoji.PANDA}Поддержка',
                                                    url='https://t.me/lenkablue')
balance_check_inline = telebot.types.InlineKeyboardButton(text=f'{emoji.FACE_WITH_MONOCLE}Проверить пополнение',
                                                   callback_data='balance_check')
balance_check_fail.add(support, balance_check_inline)

# КЛАВИАТУРА ДЛЯ ПОДТВЕРДЕНИЯ ДОБАВЛЕНИЯ ЗАКУПКИ
confirmation_add_lot = telebot.types.InlineKeyboardMarkup()
confirmation_yes = telebot.types.InlineKeyboardButton(text=f'{emoji.CHECK_MARK_BUTTON}Да',
                                              callback_data='yes')
confirmation_no = telebot.types.InlineKeyboardButton(text=f'{emoji.CROSS_MARK}Нет',
                                              callback_data='no')
confirmation_add_lot.add(confirmation_yes, confirmation_no)