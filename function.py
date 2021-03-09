import random
import telebot
import requests
import json
import random
import time


import db
import texts
import config
import variable

from config import token
bot = telebot.TeleBot(token)

last_request_time = {}

def add_purchase(new_purchase, seller_id, seller_username):
    purchases = db.get_purchases()[0]
    text = ' ' + str(int(random.random()*10000)) + ' ' + new_purchase[1] + ' ' + str(int(int(new_purchase[2]) * 1.3)) + \
           ' ' + '0' + ' ' + new_purchase[3] + ' ' + str(seller_id) + ' ' + str(seller_username) + ' ' + \
           str(int(time.time())) + ' ' + 'open' + ' |'
    purchases += text
    db.update_purchases(purchases)

def get_lot_name(lot_number):
    purchases = get_parsing_purchases_list()
    lot_name = purchases[lot_number-1][1].replace('_', ' ').title()
    return lot_name

def calculating_discount(orders_array):
    discount, orders = 0, 0
    for i in orders_array:
        orders += int(i)
    if orders <= 500: discount = 3
    elif orders <= 1500: discount = 5
    elif orders <= 5000: discount = 7
    elif orders <= 10000: discount = 9
    elif orders <= 20000: discount = 10
    else: discount = 12
    return discount

def purchases_clean():
    db.update_purchases('')
    return texts.clean_shopping_cart()

def parsing_purchases_list(purchases_list):
    purchases_list = purchases_list.split(' |')
    for i in range(len(purchases_list)):
        purchases_list[i] = purchases_list.split()
    return purchases_list

def get_parsing_purchases_list():
    purchases_list = db.get_purchases()
    purchases_list = purchases_list[0][1:-2].split(' | ')
    for i in range(len(purchases_list)):
        purchases_list[i] = purchases_list[i].split(' ')
    return purchases_list

def add_lot(add_lot_numb, uid):
    shopping_cart = db.get_shopping_cart(uid)[0]
    purchases_list = get_parsing_purchases_list()
    return_text = ''
    if purchases_list != [[]]:
        lot_id = purchases_list[add_lot_numb-1][0]
        condition = purchases_list[add_lot_numb-1][8]
        if lot_id not in shopping_cart and condition == 'open':
            lot_price = int(purchases_list[add_lot_numb-1][2])
            balance = db.get_balance(uid)[0]
            if balance == '':
                balance = 0
            else:
                balance = int(balance)
            if lot_price <= balance:
                check_availability = True
                shopping_cart += f'{lot_id} 1 '
                print(shopping_cart)
                db.update_shopping_cart(uid, shopping_cart)
                update_balance(uid)
                lot_name = purchases_list[add_lot_numb - 1][1]
                return_text = texts.add_lot(lot_id, lot_name, check_availability)
            else:
                return_text = texts.insufficient_funds()
        elif lot_id in shopping_cart:
            lot_name = purchases_list[add_lot_numb - 1][1]
            check_availability = False
            return_text = texts.add_lot(lot_id, lot_name, check_availability)
        elif condition == 'close':
            return_text = texts.lot_close()
        return return_text
    #db.update_check_shopping_cart(uid, 'false')

def edit_lot_before(edit_lot_numb, uid):
    shopping_cart = db.get_shopping_cart(uid)[0].split()
    purchases = get_parsing_purchases_list()
    return_text = '.'
    edit_lot_numb_in_array_shopping_cart = edit_lot_numb * 2 - 2
    for i in range(len(purchases)):
        if purchases[i][0] == shopping_cart[edit_lot_numb_in_array_shopping_cart]:
            lot_id = purchases[i][0]
            lot_name = purchases[i][1].replace('_', ' ')
            db.update_edit_lot_id(uid, lot_id)
            return_text = texts.edit_lot_before(lot_name)
            break
    return return_text

def edit_lot_after(uid, quantity):
    quantity = int(quantity)
    purchases = get_parsing_purchases_list()
    shopping_cart = db.get_shopping_cart(uid)[0].split()
    edit_lot_id = db.get_edit_lot_id(uid)[0]
    balance = int(db.get_balance(uid)[0])
    frozen_balance = int(db.get_frozen_balance(uid)[0])
    for i in range(0, len(shopping_cart), 2):
        if edit_lot_id == shopping_cart[i]:
            quantity_in_shopping_cart = int(shopping_cart[i+1])
            break
    return_text = texts.bag_warning()
    for i in range(len(purchases)):
        if purchases[i][0] == edit_lot_id:
            if quantity == 0:
                for j in range(0, len(shopping_cart), 2):
                    if shopping_cart[j] == edit_lot_id:
                        lot_name = purchases[i][1].replace('_', ' ').title()
                        shopping_cart.pop(i)
                        shopping_cart.pop(i)
                        new_shopping_cart = ' '.join(shopping_cart) + ' '
                        db.update_shopping_cart(uid, new_shopping_cart)
                        update_balance(uid)
                        return_text = texts.edit_lot_deleted(lot_name)
                        break
            elif int(purchases[i][4]) < quantity:
                return_text = texts.lack_lot()
                break
            elif balance < quantity * int(purchases[i][2]):
                return_text = texts.insufficient_funds()
                break
            else:
                lot_name = purchases[i][1].replace('_', ' ').title()
                print(shopping_cart)
                shopping_cart[shopping_cart.index(edit_lot_id)+1] = str(quantity)
                purchases[i][3] = str(int(purchases[i][3])+quantity)
                new_shopping_cart = ' '.join(shopping_cart) + ' '
                db.update_shopping_cart(uid, new_shopping_cart)
                new_purchases = ''
                for j in range(len(purchases)):
                    for g in range(len(purchases[j])):
                        new_purchases += ' ' + purchases[j][g]
                    new_purchases += ' |'
                db.update_purchases(new_purchases)
                return_text = texts.edit_lot_after(lot_name, quantity)
                update_balance(uid)
                print(db.get_purchases()[0])
                print(new_purchases)
                break
    #db.update_check_shopping_cart(uid, 'false')
    return return_text

# ПЕРЕПИСАТЬ!
def purchases_calculating_time():
    all_shopping_carts = db.get_all_users_for_update_purchases()
    purchases = db.get_purchases()[0]
    if purchases != '':
        purchases = purchases[1:-2].split(' | ')
        for i in range(len(purchases)):
            purchases[i] = purchases[i].split(' ')
        for i in range(len(purchases)):
            purchases[i][3] = '0'
        for i in range(len(all_shopping_carts)):
            all_shopping_carts[i] = list(all_shopping_carts[i])
            all_shopping_carts[i][1] = all_shopping_carts[i][1].split()
        for i in range(len(all_shopping_carts)):
            if all_shopping_carts[i][1] != []:
                #and all_shopping_carts[i][2] == 'false':
                for j in range(0, len(all_shopping_carts[i][1]), 2):
                    for g in range(len(purchases)):
                        if all_shopping_carts[i][1][j] == purchases[g][0]:
                            purchases[g][3] = str(int(purchases[g][3]) + int(all_shopping_carts[i][1][j+1]))
        new_purchases = ''
        for j in range(len(purchases)):
            for g in range(len(purchases[j])):
                new_purchases += ' ' + purchases[j][g]
            new_purchases += ' |'
        for i in range(len(purchases)):
            if int(purchases[i][3]) >= int(purchases[i][4]):
                print('!!!', purchases)
                # ЗАКРЫВАЕМ ЗАКУПКУ
                purchases[i][8] = 'close'
                purchases[i][8] = 'close'
                purchase_id = purchases[i][0]
                creator_id = purchases[i][5]
                lot_name = purchases[i][1].replace('_', ' ').title()
                for j in range(len(all_shopping_carts)):
                    try:
                        index_in_shopping_cart = str(all_shopping_carts[i][1].index(purchase_id))
                        #if all_shopping_carts[i][1][g] == purchase_id:
                    except Exception:
                        index_in_shopping_cart = 'not_found'
                    if index_in_shopping_cart.isdigit():
                        index_in_shopping_cart = int(index_in_shopping_cart)
                        quantity = int(all_shopping_carts[i][1][index_in_shopping_cart + 1])
                        amount = int(int(purchases[i][2]) * 0.7 * quantity)
                        return_text = texts.close_purchase_for_users(lot_name)
                        user_id = all_shopping_carts[j][0]
                        balance = int(db.get_balance(user_id)[0])
                        discount = calculating_discount(db.get_orders(user_id)[0])
                        new_balance = balance - int(int(purchases[i][2]) * (1 - discount / 100) * quantity +
                                                                                                  variable.delivery)
                        db.update_amount(user_id, new_balance)
                        bot.send_message(user_id, return_text)
                        return_text = texts.close_purchase_for_creator(user_id, lot_name, quantity, amount)
                        bot.send_message(creator_id, return_text)
                        delete_purchase_from_shopping_cart(user_id, purchase_id)
                delete_purchase_from_catalog(purchase_id)

def delete_purchase_from_shopping_cart(uid, purchase_id):
    shopping_cart = db.get_shopping_cart(uid)[0].split()
    pur_index = shopping_cart.index(purchase_id)
    shopping_cart.pop(pur_index)
    shopping_cart.pop(pur_index)
    amount = 0
    for i in range(1, len(shopping_cart), 2):
        amount += int(shopping_cart[i])
    new_shopping_cart = ' '.join(shopping_cart) + ' '
    db.update_shopping_cart(uid, new_shopping_cart)
    db.update_amount(uid, amount)

def delete_purchase_from_catalog(purchase_id):
    purchases = db.get_purchases()
    purchases = purchases[0][1:-2].split(' | ')
    for i in range(len(purchases)):
        purchases[i] = purchases[i].split(' ')
    for i in range(len(purchases)):
        if purchases[i][0] == purchase_id:
            purchases.pop(i)
            break
    new_purchases = ''
    for j in range(len(purchases)):
        for g in range(len(purchases[j])):
            new_purchases += ' ' + purchases[j][g]
        new_purchases += ' |'
    db.update_purchases(new_purchases)

def generate_random_number_for_add_balance(uid):
    return_text = texts.close_add_balance()
    '''random_number = random.randint(1000000, 9999999999)
    return_text = texts.add_balance(random_number)
    db.update_random_number_for_add_balance(uid, random_number)'''
    return return_text

def update_balance(uid):
    shopping_cart = db.get_shopping_cart(uid)[0].split()
    purchases = db.get_purchases()[0][1:-2].split(' | ')
    orders_array = db.get_orders(uid)[0].split()
    discount = calculating_discount(orders_array)
    balance, frozen_balance = int(db.get_balance(uid)[0]), int(db.get_frozen_balance(uid)[0])
    amount, amount_balance = 0, 0
    for i in range(len(purchases)):
        purchases[i] = purchases[i].split(' ')
    for i in range(0, len(shopping_cart), 2):
        for j in range(len(purchases)):
            if purchases[j][0] == shopping_cart[i]:
                amount += int(purchases[j][2]) * int(shopping_cart[i+1])
    if amount == 0:
        delivery = 0
    else:
        delivery = variable.delivery
    #discount = calculating_discount(orders_array)
    frozen_balance = amount + delivery
    db.update_frozen_balance(uid, frozen_balance)
    db.update_amount(uid, amount)
    return amount, discount

def check_time_before_check(uid):
    bool_balance_check = False
    time_now = int(time.time())
    if uid in last_request_time:
        if time_now - last_request_time[uid] < variable.waiting_time:
            return_text = texts.warning_about_frequent_check()
        else:
            last_request_time[uid] = time_now
            bool_balance_check, return_text = add_balance_check(uid)
    else:
        last_request_time[uid] = time_now
        bool_balance_check, return_text = add_balance_check(uid)
    return bool_balance_check, return_text

def add_balance_check(uid):
    random_number_user = db.get_random_number_for_add_balance(uid)[0][1]
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + config.qiwi_token
    parameters = {'rows': '50'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + config.qiwi_account + '/payments', params=parameters)
    req = json.loads(h.text)
    bool_balance_check = False
    amount = 0
    for i in range(len(req['data'])):
        if req['data'][i]['comment'] == random_number_user:
            amount = int(req['data'][i]['sum']['amount'])
            amount = amount + int(db.get_balance(uid)[0])
            db.update_balance(uid, amount)
            db.update_random_number_for_add_balance(uid, '.')
            bool_balance_check = True
            break
    if bool_balance_check:
        return_text = texts.add_balance_success(amount)
    else:
        return_text = texts.add_balance_fail()
    return bool_balance_check, return_text

def clean_shopping_cart(uid):
    db.update_shopping_cart(uid, '')
    db.update_amount(uid, '0')