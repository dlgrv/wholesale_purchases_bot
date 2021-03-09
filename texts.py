import emoji
import db
import function
import variable

#₽

def que_answ():
    return_text = f'{emoji.QUESTION_MARK}Ответы на часто задаваемые вопросы:\n\n' \
           'В: Как можно получить свой заказ?\n' \
           'О: В "Личном Кабинете" укажите адрес куда нужно доставить товар. Доставка также может осуществляться ' \
                  'первым классом Почты России, по этому вопросу обращатсья в поддержку. Обычно приходит в любой ' \
                  'город в течении 1-4 дней.\n\n' \
           'В: Как оплатить товар?\n' \
           'О: В главном меню бота нужно нажать кнопку «Личный кабинет», «Пополнить баланс». Мы принимаем к оплате ' \
                  'карту. После пополнения баланса, нажмите кнопку «Каталог», и выберете интересующий вас товар.\n\n' \
           'В: От чего зависит персональная скидка?\n' \
           'О: Персональная скидка зависит от суммы ваших заказов:\n' \
           'До 500₽ 3%\n' \
           'От 501₽ до 1500₽ 5%\n' \
           'От 1501₽ до 5000₽ 7%\n' \
           'От 5001₽ до 10 000₽ 9%\n' \
           'От 10 001₽ до 20 000₽ 10%\n' \
           'От 20 001₽ 12%\n\n' \
           'В: Оригинал или подделка?\n' \
           'О: Мы продаем исключительно оригинальную продукцию.\n\n'\
           f'Если у Вас остались какие-то вопросы, то пишите в поддержку{emoji.BACKHAND_INDEX_POINTING_DOWN}\n' \
           f'Мы обязательно решим Вашу проблему{emoji.PANDA}'
    # 'В: Вы продадите, если мне менее 18 лет?\n' \
    # 'О: Да, мы не требуем от Вас никакого подтверждения личности, ведь наша целевая аудитория - люди до 18 лет. ' \
    #       'На почте паспорт тоже не требуют, забрать можно по трек-коду.\n\n' \
    return return_text


def catalog():
    return_text = f'{emoji.UNICORN}Выбери закупку, в которой хочешь участвовать{emoji.BACKHAND_INDEX_POINTING_DOWN}\n\n'
    purchases = db.get_purchases()[0]
    if purchases != '':
        purchases = purchases[1:-2].split(' | ')
        # если добавлять закупки, то это " name name name name|". В начале- пробел, в конце- |.
        for i in range(len(purchases)):
            purchases[i] = purchases[i].split(' ')
        for i in range(len(purchases)):
            purchase_id = purchases[i][0]
            name = purchases[i][1].replace('_', ' ').title()
            price = purchases[i][2]
            numb_pieces = purchases[i][3]
            max_numb_pieces = purchases[i][4]
            #seller_id = purchases[i][5]
            #seller_token = purchases[i][6]
            end_time = purchases[i][7]
            return_text += f'{variable.emoji_for_name[i%3]}{name}\n' \
                           f'{variable.emoji_for_lot_id}Лотов занято: {numb_pieces}/{max_numb_pieces}\n' \
                           f'{variable.emoji_for_price}Цена: {price}{emoji.STAR}\n' \
                           f'{variable.emoji_for_add_lot[i%5]}Участвовать: /add_lot_{i + 1}\n\n'
    else:
        return_text += f'{emoji.WOMAN_SHRUGGING}На данный момент каталог пуст.\n' \
                       f'Вся информация о новых поступлениях у нас в канале!'
    return return_text

def acc(uid):
    function.update_balance(uid)
    person_info = db.get_person_info(uid)
    if person_info != None:
        if person_info[0] == '_':
            address = f'{emoji.CROSS_MARK}'
        else:
            address = person_info[0]
        if person_info[1] == '_':
            name = f'{emoji.CROSS_MARK}'
        else:
            name = person_info[1]
        if person_info[2] == '_':
            phone_number = f'{emoji.CROSS_MARK}'
        else:
            phone_number = person_info[2]
        orders = person_info[3]
        balance = person_info[4]
        frozen_balance = person_info[5]
        discount = function.calculating_discount(orders.split())
        return_text = f'{emoji.DOG_FACE}*Личный кабинет*{emoji.BACKHAND_INDEX_POINTING_DOWN}\n\n' \
                      f'{emoji.JOYSTICK}ID профиля: {uid}\n' \
                      f'{emoji.MONEY_MOUTH_FACE}Персональная скидка: {discount}%\n' \
                      f'{emoji.MONEY_BAG}Свободный баланс: {int(balance)-int(frozen_balance)}{emoji.STAR} ' \
                      f'({balance}- {emoji.SNOWFLAKE}{frozen_balance})\n' \
                      f'{emoji.SNOWFLAKE}В ожидании закупки: {frozen_balance}{emoji.STAR}\n\n' \
                      f'{emoji.HOUSE}Адрес доставки: {address}\n' \
                      f'{emoji.FILE_CABINET}ФИО: {name}\n' \
                      f'{emoji.MOBILE_PHONE}Номер: {phone_number}'
    else:
        return_text = f'{emoji.WOMAN_SHRUGGING}Мы не нашли вашего аккаунта.\n' \
                      f'Советуем обратится в поддержку'
    return return_text

def shopping_cart(uid):
    shopping_cart = db.get_shopping_cart(uid)[0].split()
    purchases = db.get_purchases()[0][1:-2].split(' | ')
    # если добавлять закупки, то это " name name name name|". В начале- пробел, в конце- |.
    for i in range(len(purchases)):
        purchases[i] = purchases[i].split(' ')
    return_text = f'{emoji.SHOPPING_CART}Закупки в которых ты участвуешь{emoji.BACKHAND_INDEX_POINTING_DOWN} \n\n'
    for i in range(0, len(shopping_cart), 2):
        for j in range(len(purchases)):
            print(shopping_cart[i], purchases[j][0])
            if purchases[j][0] == shopping_cart[i]:
                return_text += f'{variable.emoji_for_shopping_cart[i%3]}{purchases[j][1].replace("_", " ").title()}\n' \
                               f'{emoji.KEY}Закупка: {purchases[j][3]}/{purchases[j][4]}\n' \
                               f'{emoji.RAISED_HAND}Кол-во: {shopping_cart[i+1]} шт.\n' \
                               f'{emoji.LABEL}Сумма: {int(purchases[j][2])*int(shopping_cart[i+1])}{emoji.STAR}\n'\
                               f'{emoji.GEAR}Редактировать: /edit_lot_{int(i / 2 + 1)}\n\n'
    if shopping_cart == []:
        return_text += f'{emoji.WOMAN_SHRUGGING}Пусто! Совсем ни-че-го!\n\n'
    print('----------->', shopping_cart)
    orders_array = db.get_orders(uid)[0].split()
    amount, discount = int(db.get_amount(uid)[0]), function.calculating_discount(orders_array)
    return_text += f'{emoji.ABACUS}Сумма: {amount}{emoji.STAR} - {discount}% = ' \
            f'{amount - int(amount * discount / 100)}{emoji.STAR}\n' \
            f'{emoji.DELIVERY_TRUCK}Доставка: {variable.delivery}{emoji.STAR}\n'
    if shopping_cart != []:
        return_text += f'{emoji.WOMAN_TIPPING_HAND}Итог: {amount - int(amount * discount / 100) + variable.delivery}{emoji.STAR}'
    else:
        return_text += f'{emoji.WOMAN_TIPPING_HAND}Итог:{emoji.STAR}'
    return return_text

def add_example():
    return_text = 'Пример: \n'
    return_text += 'Название_закупки стоимость_1_шт максимальное_число_лотов'
    return return_text

def name_example():
    return_text = f'{emoji.WRITING_HAND}Введи ФИО\n\n' \
           f'{emoji.WARNING}Правильность ввода в ваших интересах{emoji.WARNING}\n\n' \
           f'Пример ввода:\n' \
           f'Наумов Николай Алексеевич'
    return return_text

def address_example():
    return_text = f'{emoji.WRITING_HAND}Введи адрес доставки\n\n' \
           f'{emoji.WARNING}Правильность ввода в ваших интересах{emoji.WARNING}\n\n' \
           f'Пример ввода:\n'\
           f'Россия, Радужный Край, город Стрыкало, улица Пушкина, дом 12А, квартира 69, индекс 424007'
    return return_text

def phone_number_example():
    return_text = f'{emoji.WRITING_HAND}Введи свой мобильный телефон\n\n' \
           f'{emoji.WARNING}Правильность ввода в ваших интересах{emoji.WARNING}\n\n' \
           f'Пример ввода:\n' \
           f'89996098787'
    return  return_text

def add_lot(lot_id, lot_name, check_availability):
    if check_availability:
        return_text = f'{emoji.CHECK_MARK_BUTTON}Отлично, ты участвуешь в закупке\n' \
               f'{lot_name.replace("_", " ").title()}\n' \
               f'{emoji.BACKHAND_INDEX_POINTING_RIGHT}Изменить количество лотов или удалить можно в своих закупках'
    else:
        return_text = f'{emoji.WOMAN_SHRUGGING}Данный лот уже есть у тебя в корзине\n' \
                      f'{emoji.BACKHAND_INDEX_POINTING_RIGHT}Именить количество лотов или удалить закупку можно там же'
    return return_text

def insufficient_funds():
    return_text = f'{emoji.WOMAN_SHRUGGING}У тебя недостаочно средств'
    return return_text

def clean_shopping_cart():
    return_text = f'{emoji.CHECK_MARK_BUTTON}Корзина очищена.'
    return return_text

def lot_close():
    return_text = f'{emoji.WOMAN_SHRUGGING}Данный лот уже закрыт'
    return return_text

def help():
    return_text = f'Команды:\n\n' \
                  f'balance up (uid) (amount)\n' \
                  f'К сущетсвующему балансу юзера с (uid) прибавляет (amount)\n\n' \
                  f'balance down (uid) (amount)\n' \
                  f'Из существующего баланса юзера с (uid) вычиатет (amount)\n\n' \
                  f'clean shopping cart\n' \
                  f'Очищает корзину польвотелю, который ввел команду\n\n' \
                  f'add название_закупки стоимость_1_шт максимальное_число_лотов\n' \
                  f'Добавляет закупку в каталог\n' \
                  f'Примечания*\n' \
                  f'-Названание закупки указывать через (_)\n' \
                  f'-Стоимость вашего товара указывается в рублях, без копеек. ' \
                  f'В каталоге закупок стоимость будет указана с учетом процента бота. ' \
                  f'Те если вы укажите цену лота 100 рублей, то в общем каталоге цена будет 130 рублей.\n' \
                  f'-Максимальное число лотов- это необходимое количество штук товара для совершения закупки. ' \
                  f'По достижению данного количества, бот прекращает возможность участвовать в данной закупке,' \
                  f'создателю закупки и медераторам высылается информация с итогами (имена, адреса, ' \
                  f'номера телефонов покупателей, а так же количество приобретенного товара)\n' \
                  f'Пример: add HQD_Rosy_ice_banana 129 50\n\n'\
                  f'add clean\n' \
                  f'Удаляет все закупки'
    return return_text

def add_balance(random_number):
    return_text = f'{emoji.CREDIT_CARD}Пополнение баланса осуществляется через перевод на QIWI кошелек по ' \
                  f'{emoji.BACKHAND_INDEX_POINTING_RIGHT}[этой ссылке](qiwi.com/p/79951180741) \n' \
                  f'Вы "дарите" средства, которые переводите, мы предоставляем товар. 1₽=1{emoji.STAR}\n' \
                  f'Если понимаете о чем речь{emoji.WINKING_FACE}\n' \
                  f'{emoji.WARNING}*В комментарии к переводу обязательно должен быть указан временный ключ:* ' \
                  f'{random_number}'
    return return_text

def add_balance_success(amount):
    return_text = f'{emoji.CHECK_MARK_BUTTON}Ваш баланс успешно пополнен на {amount}{emoji.STAR}!'
    return return_text

def add_balance_fail():
    return_text = f'{emoji.WOMAN_SHRUGGING}Мы пока ничего не нашли\n' \
                  f'Либо вы не осуществляли перевод, либо деньги еще не успели перевеститсь (не больше 5 минут)\n' \
                  f'В противном случае обратитесь в поддержку'
    return return_text

def warning_about_frequent_check():
    return_text = f'{emoji.WARNING}Проверка пополения баланса не чаще 1 раза в {variable.waiting_time} секунд!'
    return return_text

def bag_warning():
    return_text = f'{emoji.UPSIDE_DOWN_FACE}Что-то пошло не так\n' \
                  f'Но это не точно*'
    return return_text

def edit_lot_before(lot_name):
    return_text = f'{emoji.BACKHAND_INDEX_POINTING_RIGHT}Вы редактируете {lot_name.replace("_", " ").title()}\n' \
                  f'{emoji.WOMAN_TIPPING_HAND}Просто напиши желаемое количество лотов данной закупки'
    return return_text

def edit_lot_after(lot_name, quantity):
    return_text = f'{emoji.CHECK_MARK_BUTTON}Отлично! Теперь {lot_name} в ваших закупках в количестве {quantity} шт.'
    return return_text

def edit_lot_deleted(lot_name):
    return_text = f'{emoji.WASTEBASKET}Ты удалил {lot_name} из своих закупок'
    return return_text

def lack_lot():
    return_text = f'{emoji.WOMAN_SHRUGGING}Не хватает свободных лотов закупки'
    return return_text

def close_purchase_for_users(lot_name):
    return_text = f'{emoji.CHECK_MARK_BUTTON}Закупка {lot_name} завершилась!\n' \
                  f'{emoji.WOMAN_BOWING}Ожидайте доставки или сообщения от продовца;)'
    return return_text

def close_purchase_for_creator(uid, lot_name, quantity, amount):
    person_info = db.get_person_info(uid)
    if person_info[0] == '':
        address = f'{emoji.CROSS_MARK}'
    else:
        address = person_info[0]
    if person_info[1] == '':
        name = f'{emoji.CROSS_MARK}'
    else:
        name = person_info[1]
    if person_info[2] == '':
        phone_number = f'{emoji.CROSS_MARK}'
    else:
        phone_number = person_info[2]
    orders = person_info[3]
    username = person_info[6]
    return_text = f'{emoji.DOG_FACE}' \
                  f'{emoji.JOYSTICK}ID профиля: {uid}\n' \
                  f'Username: @{username}' \
                  f'{emoji.HOUSE}Адрес доставки: {address}\n' \
                  f'{emoji.FILE_CABINET}ФИО: {name}\n' \
                  f'{emoji.MOBILE_PHONE}Номер: {phone_number}\n'\
                  f'Заказал: {lot_name}\n' \
                  f'Кол-во: {quantity}шт.\n' \
                  f'На сумму: {amount}{emoji.STAR}\n'
    return return_text

def confirmation_add_lot(lot_name):
    return_text = f'{emoji.WOMAN_BOWING}Подтверждение добавления {lot_name} в закупки\n' \
                  f'{emoji.BACKHAND_INDEX_POINTING_RIGHT}Как только закупка завершится, деньги сразу спишутся с баланса'
    return return_text

def reviews():
    return_text = f'[Ссылочка](https://t.me/HQDpuppyShopOtzivi) на наш канал с отзывами{emoji.SMILING_FACE}\n' \
                  f'Будет очень круто, если ты подпишишься' \
                  f'В обмен переодически мы будем кидать промокоды{emoji.WINKING_FACE}'
    return return_text

def guarantees():
    return_text = f'[Ссылочка](https://t.me/SurveyHQDpuppyShop) на наш опросник{emoji.SMILING_FACE}\n' \
                  f'Там мы решаем, какие закупки будем делать{emoji.WINKING_FACE}'
    return return_text

def close_add_balance():
    return_text = 'На данный момент пополнение баланса отключено.'
    return return_text