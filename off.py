import datetime
import sqlite3
#import mysql.connector

conn = sqlite3.connect('ohaloff')
c = conn.cursor()

# ms_db = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='tr@n5cent',
#     database='ohal'
# )
# ms_cursor = ms_db.cursor()

# TABLES0 = {'inventory0': ("""CREATE TABLE IF NOT EXISTS inventory0(
#             category TEXT,
#             brand TEXT,
#             price REAL,
#             in_stock INTEGER,
#             low_value INTEGER,
#             buying_price INTEGER
#             )"""), 
#             'sales0': ("""CREATE TABLE IF NOT EXISTS sales0(
#             r_id INTEGER,
#             brand TEXT,
#             price REAL,
#             quantity REAL,
#             tot_price REAL,
#             da_te TEXT,
#             ti_me TEXT,
#             payment TEXT
#             )""")}  # for local db


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.add()

    def add(self):
        # sqlite3 local db

        vals = (self.username, self.password)

        sqlt1 = ("""CREATE TABLE IF NOT EXISTS inventory0(
            category TEXT,
            brand TEXT,
            price REAL,
            in_stock INTEGER,
            low_value INTEGER,
            buying_price REAL
            )""")
        sqlt2 = ("""CREATE TABLE IF NOT EXISTS sales0(
            r_id INTEGER,
            brand TEXT,
            price REAL,
            quantity REAL,
            tot_price REAL,
            da_te TEXT,
            ti_me TEXT,
            payment TEXT,
            profit INTEGER
            )""")

        tables0 = [sqlt1, sqlt2]
        for table in tables0:
            c.execute(table)

        c.execute("INSERT INTO users VALUES(?, ?)", vals)
        # k = c.fetchall()
        # for i in k:
        #     print(k)
        conn.commit()

    @staticmethod
    def clear_records():
        c.execute('DELETE FROM users')

        class online():
            ...
            # try:
            #     sql = "INSERT INTO userss(id, fst_name, lst_name, contact, email, question," \
            #           "answer, password, invent_table, sale_table) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            #
            #     ms_cursor.execute(sql, vals)
            #
            #     msql = (" CREATE TABLE `{}`("
            #             " `id` int(10) AUTO_INCREMENT,"
            #             " `r_id` int(10) NOT NULL,"
            #             " `category` varchar(100) NOT NULL,"
            #             " `brand` varchar(100) NOT NULL,"
            #             " `price` int(10),"
            #             " `in_stock` int(10),"
            #             " `low_value` int(10),"
            #             " `buying_price` int(1),"
            #             " PRIMARY KEY(`id`)"
            #             ") ENGINE = InnoDB".format(self.invent))
            #     msq = (" CREATE TABLE `{}`("
            #            " `id` int(10) AUTO_INCREMENT,"
            #            " `r_id` int(10),"
            #            " `brand` varchar(100),"
            #            " `price` int(10),"
            #            " `quantity` int(10),"
            #            " `tot_price` int(10),"
            #            " `da_te` varchar(100),"
            #            " `ti_me` varchar(100),"
            #            " `payment` varchar(20),"
            #            " PRIMARY KEY(`id`)"
            #            " ) ENGINE = InnoDB".format(self.sales))
            #
            #     tables = [msql, msq]
            #     for table in tables:
            #         ms_cursor.execute(table)
            #     ms_db.commit()
            #     print("CREATED")
            #
            # except:
            #     print("Try Later")

    @staticmethod
    def details():
        c.execute("SELECT * FROM users")
        dets = c.fetchall()
        return dets
    
    @staticmethod
    def login(tup):
        # tup = (username, password)
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", tup)
        print(details := c.fetchone())
        return details

class Item:

    def __init__(self, category: str, brand: str, price: float, in_stock: int, low_value: int, buying_price: float):

        assert price >= 0
        assert in_stock >= 0
        assert low_value >= 0

        self.category = category
        self.brand = brand
        self.price = price
        self.in_stock = in_stock
        self.low_value = low_value
        self.buying_price = buying_price
        self.add()

    def add(self):
        tup = (self.category, self.brand, self.price, self.in_stock, self.low_value, self.buying_price)
        with conn:
            c.execute('INSERT INTO 	inventory0 VALUES(?,?,?,?,?,?)', tup)

    @staticmethod
    def search(tpl):
        # tpl = (state,  brand/category/price, value)
        if tpl[0] == 1:
            # tpl = (state,0,0)
            with conn:
                c.execute("SELECT rowid, brand, category, price, in_stock, low_value, buying_price FROM inventory0")
                items = c.fetchall()
                return items

        elif tpl[0] == 2:
            # tpl = (state,0,0)
            with conn:
                c.execute("SELECT rowid, brand, in_stock FROM inventory0 WHERE in_stock<=low_value")
                items = c.fetchall()
                return items

        elif tpl[0] == 3:
            # tpl = (state,0,0)
            with conn:
                c.execute("SELECT category FROM inventory0 ORDER BY category ASC")
                items = c.fetchall()
                items = set(items)
                return items

        elif tpl[0] == 4:
            # tpl = (state,0,0)
            with conn:
                c.execute("SELECT brand FROM inventory0")
                items = c.fetchall()
                items = set(items)
                return items

        elif tpl[0] == 0:
            # tpl = (state, brand/category/price/rowid, value)
            with conn:
                c.execute("SELECT rowid, * FROM inventory0 WHERE {} = ?".format(tpl[1]), (tpl[2],))
                items = c.fetchall()
                return items

    @staticmethod
    def update_item(tpl):
        # tpl = (change_data_brand, change_data_price, change_data_in_stock, change_data_low_val, category, brand)
        with conn:
            c.execute("UPDATE inventory0 SET brand = ?, price = ?, in_stock = ?, low_value = ?, buying_price = ? WHERE category = ? AND brand = ?", 
                      (tpl[0], tpl[1], tpl[2], tpl[3], tpl[4], tpl[5], tpl[6]))
            
    @staticmethod
    def update_item_sell(tpl):
        # tpl = (change_data_brand, change_data_price, change_data_in_stock, change_data_low_val, category, brand)
        with conn:        
            c.execute("UPDATE inventory0 SET {} = ? WHERE category = ? AND brand = ?".format(tpl[0]),
                      (tpl[1], tpl[2], tpl[3]))

    @staticmethod
    def remove(tpl):
        # tpl = (instock, price, brand)
        print(f'{tpl[0]}. {tpl[1]}, {tpl[2]} removed?')
        with conn:
            c.execute("DELETE FROM inventory0 WHERE in_stock = ? AND price = ? AND brand = ?", (tpl[0], tpl[1], tpl[2]))
        print(f'{tpl[0]}. {tpl[1]}, {tpl[2]} removed')

    @staticmethod
    def butts_details(state, bno):
        # tpl = (state, cats_index)
        c.execute("SELECT category FROM inventory0")
        cats = c.fetchall()
        butts = []
        for i in cats:
            i = str(i[0])
            if i not in butts:
                butts.append(i)  # considering use of generators
            # print(len(cats))
        if state == 1:
            # generate category buttons
            return butts

        elif state == 2:
            # when you press category buttons and returns all the data associated with each button
            c.execute("SELECT rowid, * FROM inventory0")
            brands = c.fetchall()
            sub_butts = [print([i[2], i[3], i[4]]) for i in brands if i[1] == butts[bno]]
            return sub_butts

    @staticmethod
    def sell(tpl):
        # tpl = old_val, category, brand, quantity
        new_val = float(tpl[0]) - float(tpl[3])
        new_val = str(new_val)
        Item.update_item_sell(('in_stock', new_val, tpl[1], tpl[2]))

    def __repr__(self):
        return f'{self.brand}, {self.price}, {self.low_value}'

    @staticmethod
    def clear_records():
        c.execute('DELETE FROM inventory0')
    

class Sale:

    def __init__(self, r_id, brand, price, quantity, tot_price, payment, buying_price):
        self.r_id = r_id
        self.brand = brand
        self.quantity = quantity
        self.price = price
        self.tot_price = tot_price
        self.payment = payment
        self.buying_price = buying_price
        self.add()

    def add(self):
        date_time = datetime.datetime.now()
        date_time = str(date_time)
        da_te = date_time[:10]
        ti_me = date_time[11:16]
        profit = self.price - self.buying_price
        tup = (self.r_id, self.brand, self.price, self.quantity, self.tot_price, da_te, ti_me, self.payment, profit)
        with conn:
            c.execute('INSERT INTO 	sales0 VALUES(?,?,?,?,?,?,?,?,?)', tup)

    @staticmethod
    def search(tpl):
        # tpl = (state, cat_to_search, val_to_search)
        if tpl[0] == 1:
            with conn:
                c.execute("SELECT rowid, * FROM sales0")
                items = c.fetchall()
                return items

        elif tpl[0] == 2:
            # with conn:
            #    c.execute("SELECT da_te FROM sales0")
            #    dates = c.fetchall()
            #    dates = set(dates)
            #    return dates
            with conn:
                c.execute("SELECT {} FROM sales0 ORDER BY rowid DESC".format(tpl[1]))
                columns = c.fetchall()
                columns = set(columns)
                return columns

        elif tpl[0] == 3:
            with conn:
                c.execute("SELECT brand FROM sales0")
                brands = c.fetchall()
                brands = set(brands)
                return brands

        elif tpl[0] == 4:
            # tpl = (4,0,['pay_method', 'date']
            with conn:
                c.execute("SELECT da_te, ti_me, brand FROM sales0 WHERE payment = ? AND da_te = ?",
                          (tpl[2][0], tpl[2][1]))
                items = c.fetchall()
                return items

        elif tpl[0] == 5:
            with conn:
                c.execute("SELECT * FROM sales0 WHERE {} = ? AND {} = ?".format(tpl[1], tpl[3]), (tpl[2], tpl[4]))
                items = c.fetchall()
                return items

        elif tpl[0] == 0:
            with conn:
                c.execute("SELECT * FROM sales0 WHERE {} = ?".format(tpl[1]), (tpl[2],))
                items = c.fetchall()
                return items

    @staticmethod
    def update_cat(tpl):
        # tpl = (change_data, new_value, edited_brand)
        with conn:
            c.execute("UPDATE sales0 SET {} = ? WHERE brand = ?".format(tpl[0]), (tpl[1], tpl[2]))

    @staticmethod
    def remove(tpl):
        # tpl = (brand, quantity, ti_me)
        with conn:
            c.execute("DELETE FROM sales0 WHERE brand = ? AND quantity = ? AND ti_me = ?", tpl)
            print('cleared')

    @staticmethod
    def clear_records():
        c.execute('DELETE FROM sales0')

def sell(dtls, quantity, total_price, payment):
    Item.sell((dtls[4], dtls[1], dtls[2], quantity))
    Sale(dtls[0], dtls[2], dtls[3], quantity, total_price, payment, dtls[6])


with conn:
    c.execute("""CREATE TABLE IF NOT EXISTS users(
                username TEXT,
                password TEXT
                )""")

# User.clear_records()

# fst = User('levy', '34RAZOR')

# k = User.login(('levy', '34'))

# if k:
#     print(k)
#     print(type(k))
# else:
#     print('kuma bana')



# sell(dets, 2)
# tpl = (change_data, new_value, rowid, brand)
# tpl = old_val, rowid, brand, quantity
# print(Item.search((0, 0, 0))[2])
# Item.remove('hunters') Item.update_item(('in_stock', new_val, tpl[1], tpl[2]))
# lst = [
# ['vodka', 'ciroc', 4500, 23, 12, 4000],
# ['whiskey', 'JD', 3000, 43, 15, 1500],
# ['vodka', 'absolut', 4500, 23, 12, 4000],
# # ['whiskey', 'jw black', 3000, 43, 15, 1500],
# ['beer', 'tusker', 300, 32, 10, 340],
# ['beer', 'hunters', 300, 32, 10, 440]
# ]
# t = User()
# t.add()
# for item in lst:
#     t = Item(item[0], item[1], item[2], item[3], item[4], item[5])