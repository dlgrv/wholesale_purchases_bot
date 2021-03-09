from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
import variable

table_name = variable.table_name
save_acc = variable.save_acc

#переписать весь код на dictionary=True

# CHECK - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_user(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT *  ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (check_user)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (check_user)')
        pass
    finally:
        cursor.close()
        conn.close()

# ADD - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def add_user(uid, username):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f"INSERT INTO {table_name} (uid, username, address, phone_number, name, balance, frozen_balance) " \
            f"VALUES ('{uid}', '{username}', '_', '_', '_', '0', '0')"
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (add_user)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (add_user)')
        pass
    finally:
        cursor.close()
        conn.close()


def add_address(uid, address):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET address = "{address}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_address)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_address)')
        pass
    finally:
        cursor.close()
        conn.close()


def add_name(uid, name):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET name = "{name}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (add_name)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (add_name)')
        pass
    finally:
        cursor.close()
        conn.close()


def add_phone_number(uid, phone_number):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET phone_number = "{phone_number}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (add_phone_number)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (add_phone_number)')
        pass
    finally:
        cursor.close()
        conn.close()

# UPDATE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def update_balance(uid, balance):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET balance = {balance} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_balance)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_balance)')
        pass
    finally:
        cursor.close()
        conn.close()

def update_add_lot_numb(uid, add_lot_numb):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET add_lot_numb = "{add_lot_numb}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_add_lot_numb)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_add_lot_numb)')
        pass
    finally:
        cursor.close()
        conn.close()

def update_frozen_balance(uid, frozen_balance):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET frozen_balance = {frozen_balance} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_frozen_balance)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_frozen_balance)')
        pass
    finally:
        cursor.close()
        conn.close()

def update_purchases(purchases):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET purchases = "{purchases}" ' \
            f'WHERE uid = "{save_acc}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_purchases)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_purchases)')
        pass
    finally:
        cursor.close()
        conn.close()


def update_amount(uid, amount):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET amount = {amount} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_amount)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_amount)')
        pass
    finally:
        cursor.close()
        conn.close()


def update_shopping_cart(uid, shopping_cart):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET shopping_cart = "{shopping_cart}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_shopping_cart)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_shopping_cart)')
        pass
    finally:
        cursor.close()
        conn.close()

def update_edit_lot_id(uid, lot_id):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET edit_lot_id = "{lot_id}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_edit_lot_id)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_edit_lot_id)')
        pass
    finally:
        cursor.close()
        conn.close()

def update_check_shopping_cart(uid, check):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET check_shopping_cart = "{check}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_check_shopping_cart)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_update_shopping_cart)')
        pass
    finally:
        cursor.close()
        conn.close()

def update_random_number_for_add_balance(uid, number):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET random_number_for_add_balance = {number} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_random_number_for_add_balance)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_random_number_for_add_balance)')
        pass
    finally:
        cursor.close()
        conn.close()
# GET - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_purchases():
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT purchases ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{save_acc}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_purchases)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_purchases)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_amount(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT amount ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_amount)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_amount)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_person_info(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT address, name, phone_number, orders, balance, frozen_balance, username ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_person_info)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_person_info)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_balance(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT balance ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_balance)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_balance)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_all_users_for_update_purchases():
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor(buffered=True)

    query = f'SELECT uid, shopping_cart, check_shopping_cart ' \
            f'FROM {table_name} '
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f'[DataBase] --> {rows} (get_all_users)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_all_users)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_add_lot_numb(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT add_lot_numb ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_add_lot_numb)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_add_lot_numb)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_frozen_balance(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT frozen_balance ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_frozen_balance)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_frozen_balance)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_edit_lot_id(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT edit_lot_id ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_edit_lot_id)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_edit_lot_id)')
        pass
    finally:
        cursor.close()
        conn.close()


def get_orders(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT orders ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_orders)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_orders)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_shopping_cart(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT shopping_cart ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_shopping_cart)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_shopping_cart)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_info_for_update_balance(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT balance, frozen_balance, shopping_cart, purchases ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_info_for_update_balance)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_info_for_update_balance)')
        pass
    finally:
        cursor.close()
        conn.close()

def get_random_number_for_add_balance(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT uid, random_number_for_add_balance ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f'[DataBase] --> {rows} (get_users_with_random_numbers_for_add_balance)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_users_with_random_numbers_for_add_balance)')
        pass
    finally:
        cursor.close()
        conn.close()


