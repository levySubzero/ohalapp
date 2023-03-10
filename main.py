import kivy
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty, StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.list import OneLineListItem, ThreeLineListItem
from kivymd.theming import ThemeManager
import datetime

import off

__version__ = '1.0'

Window.size = (700, 600)

Builder.load_file('./ui/user_data.kv')
Builder.load_file('./ui/sell_main.kv')
Builder.load_file('./ui/sell_brands.kv')
Builder.load_file('./ui/view_cart.kv')
Builder.load_file('./ui/sales_main.kv')
Builder.load_file('./ui/sales_item.kv')
Builder.load_file('./ui/stock_main.kv')
Builder.load_file('./ui/view_inventory.kv')
Builder.load_file('./ui/add_to_inventory.kv')
Builder.load_file('./ui/update_item.kv')
Builder.load_file('./ui/sales_date_select.kv')
Builder.load_file('./ui/bottom_navigator.kv')
Builder.load_file('./ui/sales_item_select.kv')
Builder.load_file('./ui/view_stock.kv')
Builder.load_file('./ui/confirm_dialog.kv')
Builder.load_file('./ui/add_cart_dialog_contents.kv')
Builder.load_file('./ui/date_dialog_contents.kv')
Builder.load_file('./ui/stock_update.kv')
Builder.load_file('./ui/update_stock_contents.kv')
Builder.load_file('./ui/brand_grid_item.kv')
# Builder.load_file('delete_dialog_contents.kv')


class WindowManager(Factory.ScreenManager):
    ...


class RegisterScreen(Screen):
    ...


class LoginScreen(Screen):
    ...


class HomeScreen(Screen):
    ...


class SellMScreen(Screen):
    ...


class MD3Card(MDCard):
    text = StringProperty()


class SellBrandsScreen(Screen):
    cart = StringProperty()
    cart = 'CART'


class BrandsListItem(ThreeLineListItem):
    info = ListProperty()
    item_name = StringProperty()
    item_price = StringProperty()
    item_instock = StringProperty()


class AddCartDialog(MDBoxLayout):
    quantity = StringProperty()
    info = ListProperty()


class DeleteDialog(MDBoxLayout):
    info = ListProperty()


class ConfirmDialog(MDBoxLayout):
    ...


class UpdateStockContents(MDFloatLayout):
    new_stock = StringProperty()
    buying_price = StringProperty()


class MCard(MDCard, CommonElevationBehavior):
    ...


class ViewCartScreen(Screen):
    ...


class SalesMScreen(Screen):
    ...


class SalesItemScreen(Screen):
    title = StringProperty()


class StockMScreen(Screen):
    ...


class StockNewScreen(Screen):
    ...
    

class ViewInventoryScreen(Screen):
    ...


class AddInventoryScreen(Screen):
    ...


class UpdateItemContents(Screen):
    ...


class ColumnListItem(OneLineListItem):
    ...


class ThreeLiners(ThreeLineListItem):
    ...



class SalesItemSelectScreen(Screen):
    ...


class SalesDateSelectScreen(Screen):
    ...


class CategoryListItem(OneLineListItem):
    category = StringProperty()

    
class ViewStockScreen(Screen):        
    ...


class StockUpdateScreen(Screen):
    ...


class OhalApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory_table = None
        self.data_dialog2 = None
        self.item_remove_dialog = None
        self.updated_dialog = None
        self.item_update_dialog = None
        self.add_invent_dialog = None
        self.data_table = None
        self.search_data = ''
        self.item_quantity = 0
        self.date_dialog = None
        self.lower_amount_dialog = None
        self.sell_dialog2 = None
        self.clear_dialog = None
        self.sold_dialog = None
        self.sell_dialog = None
        self.cart_table = None
        self.dialog = None
        self.selection_cart = []
        self.selection_sales = []
        self.selection_stock = []
        self.update_items = []

    def build(self):
        # setting theme properties
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Light"
        self.nav_color =  [0, 0.9, 0.9, 1]
        self.text_color = [1, 0, 0, 1]
        self.theme_cls.accent_hue = '400'
        self.title = 'Ohal'
        self.win_man = WindowManager(transition=FadeTransition())

        self.cart_list = []
        self.direct_sell_list = []
        self.inventory_table_row = []
        self.cart_text = f'CART {len(self.cart_list)}'
        self.data_item_title = ''

        self.screens = [
            HomeScreen(name='home'), #0
            SellMScreen(name='sell_main'), 
            SellBrandsScreen(name='sell_brands'), #2
            ViewCartScreen(name='view_cart'),
            SalesMScreen(name='sales_main'),   #4
            SalesItemScreen(name='sales_item'),
            StockMScreen(name='stock_main'),    #6
            ViewInventoryScreen(name='inventory_screen'),
            AddInventoryScreen(name='add_invent'),    #8
            SalesItemSelectScreen(name='sales_item'),
            SalesDateSelectScreen(name='sales_date'),   #10
            RegisterScreen(name='register_data'),
            LoginScreen(name='login'),    #12
            StockNewScreen(name='stock_new'),
            UpdateItemContents(name='item_update'),  #14
            ViewStockScreen(name='stock_screen'),
            StockUpdateScreen(name='stock_update')   #16
        ]

        print(off.User.details())
        # if off.User.details() == []:
        #     self.win_man.switch_to(self.screens[11])

        # else:
        #     self.win_man.switch_to(self.screens[0])

        self.sell_press()
        return self.win_man

    def home(self):
        self.change_screen(self.screens[0])

    def sell_press(self):
        self.sold_dialog = MDDialog(  # opens when item is sold and database updates successfully
            title='SOLD',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda s=self: self.sold_dialog.dismiss(s)
                ),
            ],
        )

        self.lower_amount_dialog = MDDialog(  # opens when item instock quantity is less than input
            title='ENTER LOWER AMOUNT',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda s=self: self.lower_amount_dialog.dismiss()
                ),
            ],
        )
        self.win_man.switch_to(self.screens[1])
        self.category_list_builder()

    # creating the categories, page
    def category_list_builder(self, text='', search=False):
        # fetch all categories
        category_list = off.Item.search((3, 0, 0))
        self.screens[1].ids['_cat_list'].clear_widgets()

        def add_category_item(category_item):
            cart_button = MDRaisedButton(text=category_item, md_bg_color=(0, 0.6, 0.9, 1), text_color=(0, 0, 0, 1), font_size="27sp", size_hint=(.3, .2), _elevation_raised=2)
            cart_button.on_release = lambda x=category_item: self.category_select(x)
            self.screens[1].ids['_cat_list'].add_widget(cart_button)
            # self.screens[1].ids['_cat_list'].data.append(
            #     {
            #         "viewclass": "CategoryListItem",
            #         "text": category_item,
            #         "on_release": lambda x=category_item: self.category_select(x),
            #     }
            # )

        self.screens[1].ids['_cat_list'].data = []
        for cat in category_list:
            if search:
                if text in cat[0]:
                    add_category_item(cat[0].capitalize())
            else:
                add_category_item(cat[0].capitalize())

    # when a category is selected for selling
    def category_select(self, category, text='', search=False):
        category = category.lower()
        items = off.Item.search((0, 'category', category))
        self.sell_item = SellBrandsScreen()
        self.win_man.switch_to(self.screens[2])
        self.screens[2].ids['_brands_list'].clear_widgets()

        def add_brand_item(item):
            txt = f"""
                {item[2].capitalize()} \n
                Price: {item[3]} \n
                In-stock: {item[4]} \n
            """
            cart_button = MD3Card(
                line_color=(0.2, 0.2, 0.2, 0.8),
                style='outlined',
                text=txt,
            )
            
            # cart_button = MDRaisedButton(text=txt, halign="center", size_hint=(.3, .2), _elevation_raised=2)
            cart_button.on_release = lambda x=item: self.item_select(x, func1='sell')
            self.screens[2].ids['_brands_list'].add_widget(cart_button)
            
        item_names = []
        for item in items:
            if search:
                if text in item[2]:
                    add_brand_item(list(item))
            else:
                add_brand_item(list(item))
            
    # selection of a specific product for selling and updating
    def item_select(self, info, func1):
        print(info)

        if func1 == 'sell':
            self.info = info
            self.dialog = MDDialog(  # input quantity and sell item or add to cart
                title=f'{info[2]}',
                type="custom",
                content_cls=AddCartDialog(),
                buttons=[
                    MDFlatButton(
                        text='CANCEL',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda d=self: self.dialog.dismiss(d)
                    ),
                    MDFlatButton(
                        text='ADD TO CART',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        # action = lambda instance, d=info: self.add_to_cart(instance, d),
                        on_release=lambda instance, d=info: self.add_to_cart(instance, d)
                    ),
                ],
            )
            self.dialog.open()

        if func1 == 'stock':
            self.item_update(info)

        if func1 == 'stock_item':
            self.item_update(info)

    def view_inventory(self, cat, func3):
        if cat == 'all':
            items = off.Item.search((1, 0, 0))
        else:
            items = off.Item.search((0, 'category', cat))
        self.win_man.switch_to(self.screens[2])
        # self.screens[7].ids['_inventory_items'].clear_widgets()
        self.screens[2].ids['_brands_list'].clear_widgets()
        
        def add_brand_item(item):
            if cat == 'all':
                print(item)
                txt = f"""
                    {item[1].capitalize()} \n
                    Price: {item[3]} \n
                    In-stock: {item[4]} \n
                """
            else:
                print(item)
                txt = f"""
                    {item[2].capitalize()} \n
                    Price: {item[3]} \n
                    In-stock: {item[4]} \n
                """
            cart_button = MD3Card(
                line_color=(0.2, 0.2, 0.2, 0.8),
                style='outlined',
                text=txt,
            )
            # cart_button = MDRaisedButton(text=txt, size_hint=(.3, .2), _elevation_raised=2)
            cart_button.on_release = lambda x=item: self.item_select(x, func3)
            self.screens[2].ids['_brands_list'].add_widget(cart_button)
            # self.screens[7].ids['_inventory_items'].add_widget(cart_button)
            
        item_names = []
        for item in items:
            add_brand_item(list(item))

    def add_to_cart(self, obj, info):
        self.qtty = AddCartDialog()
        # self.brands = SellBrandsScreen()
        input_quantity = self.dialog.content_cls.ids._quantity.text
        try:
            float(input_quantity)
        except:
            return
        if float(input_quantity) > float(info[4]):
            self.lower_amount_dialog.open()
        else:
            self.quantity = input_quantity
            self.total_price = float(self.quantity) * float(info[3])
            info = [info, [self.quantity, self.total_price]]
            self.cart_list.append(info)
            print(self.cart_list)
            self.screens[2].ids['_cart_butt'].text = f'CART {len(self.cart_list)}'
            self.close_dialog(obj, self.dialog)

    def sell_direct(self, info):
        # sell one item without adding to cart
        self.sell_dialog2 = MDDialog(  # select payment method and confirm transaction o direct sales
            title='Confirm',
            type="custom",
            content_cls=ConfirmDialog(),
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.sell_dialog2.dismiss(d)
                ),
                MDFlatButton(
                    text='SELL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda obj: self.direct_sell_confirm(obj)
                ),
            ]
        )
        input_quantity = self.dialog.content_cls.ids._quantity.text
        if float(input_quantity) > float(info[4]):
            self.lower_amount_dialog.open()
        else:
            self.quantity = input_quantity
            self.total_price = float(self.quantity) * float(info[3])

            # list sharing properties with item in def_sell_car:
            self.direct_sell_list = [info, [self.quantity, self.total_price]]
            self.dialog.dismiss()
            self.sell_dialog2.open()
        # self.dialog.content_cls.ids['_add_contents'].add_widget(self.confirm)

    def direct_sell_confirm(self, obj):
        row = self.direct_sell_list
        print(row, 'row')
        off.sell(row[0], row[1][0], row[1][1], self.payment)
        self.sell_dialog2.dismiss()
        self.sold_dialog.open()
        self.close_dialog(obj, self.dialog)
        self.win_man.switch_to(self.win_man.screens[1])

    def sell_cart(self, instance):
        self.sell_dialog.dismiss()

        #  def sell(dtls, quantity, total_price, payment):
        for item in self.cart_list:
            off.sell(item[0], item[1][0], item[1][1], self.payment)
        
        if self.cash == 0.0:
            self.cash = self.total_due

        self.print_stuff(self.cart_list)
        self.cart_list.clear()
        self.dialog.dismiss()
        self.view_cart(instance)
        self.win_man.switch_to(self.screens[1])
        self.sold_dialog.open()

    def view_cart(self, obj):
        self.rows_cart = []
        self.date = ''
        self.time = ''
        self.serviced_by = 'vYLe'
        self.sub_total = 0.0
        self.discount = 0
        self.total_due = 0.0
        self.cash = 0.0
        self.balance = 0.0
        self.no_items = 0
        self.rate = 16
        self.vat_amt = 0.0
        self.vat = 0.0
        # self.screens[3].ids['_cart_float'].clear_widgets()
        
        self.detail_area_string = """
        """
        self.cart_table = MDDataTable(pos_hint={'top': 1, 'x': 0},
                                      size_hint=(1, 1),
                                      check=True,
                                      elevation=0,
                                      background_color_header=(0.3, 0.3, 1, 1),
                                      use_pagination=True,
                                      column_data=[
                                          ("Item", dp(30)),
                                          ("Price", dp(20)),
                                          ("Quantity", dp(15)),
                                          ("Total", dp(25))
                                      ],
                                      row_data=[]
                                      )
        self.cart_table.row_data = []
        self.cart_table.bind(on_check_press=self.check_press_cart)
        self.screens[3].ids['_cart_float'].add_widget(self.cart_table)
        for index, column in enumerate(self.cart_list, start=1):
            self.cart_table_column = (str(column[0][2]), str(column[0][3]), str(column[1][0]), str(column[1][1]))
            if (index % 2) == 0:
                self.cart_table.background_color_cell=(0.3, 0.3, 1, 0.4)
            self.cart_table.row_data.append(self.cart_table_column)
            self.sub_total += float(column[1][1])
            self.no_items += 1

        self.rows_cart = self.cart_table.row_data
        self.vat_amt = self.sub_total
        self.screens[3].ids['_total'].text = f'Total: {str(self.sub_total)}'
        self.detail_area()
        self.win_man.switch_to(self.screens[3])

    def check_press_cart(self, instance_table, current_row):
        self.selection_cart.append(current_row)

    def remove_cart(self, obj):
        for selection in self.selection_cart:
            try:
                indx = self.rows_cart.index(tuple(selection))
                self.cart_list.remove(self.cart_list[indx])
                # self.view_cart()
            except ValueError:
                break
        self.selection_cart = []
        self.view_cart(obj)

    def clear_cart(self, instance):
        self.clear_dialog.dismiss()
        self.cart_list.clear()
        self.view_cart(instance)

    def sell_cart_dialog(self):
        self.sell_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
            title='Confirm',
            type="custom",
            content_cls=ConfirmDialog(),
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.sell_dialog.dismiss(d)
                ),
                MDFlatButton(
                    text='SELL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda obj: self.sell_cart(obj)
                ),
            ]
        )
        self.sell_dialog.open()

    def sold(self, instance):
        self.close_dialog.dismiss()
        self.win_man.switch_to(self.screens[1])

    def clear_cart_dialog(self):
        self.clear_dialog = MDDialog(  # for removing all items from cart
            title='Sure to remove all items?',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.clear_dialog.dismiss(d)
                ),
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda instance: self.clear_cart(instance)
                ),
            ]
        )
        self.clear_dialog.open()

    def get_balance(self):
        self.cash = self.screens[3].ids['_cash_amount'].text
        self.balance = int(self.cash) - self.sub_total
        self.screens[3].ids['_balance'].text = f'Balance: {str(self.balance)}'
        self.detail_area()

    def detail_area(self):
        self.vat = 0.16 * self.sub_total
        self.vat_amt = float(self.sub_total) - float(self.vat)
        self.total_due = self.sub_total
        date_time = datetime.datetime.now()
        date_time = str(date_time)
        self.date = date_time[:10]
        self.time = date_time[11:16]
        self.receipt_string = f"""
        ----------------------------
        TOTAL:  {self.total_due}
        ----------------------------
        NO. OF ITEMS: {self.no_items}
        ----------------------------
        CASH: {self.cash}
        ----------------------------
        BALANCE: {self.balance}
        -------------------------------
        """
        self.detail_area_string = """
        """
        self.screens[3].ids['_sale_details_text'].text = self.receipt_string

    def print_stuff(self, stuff):
        width1 = 35
        width2 = 15
        items = []
        total_price = 0.0
        
        for item in stuff:
            print(item[0][2], item[1][0], item[0][3])
            total = str(float(item[1][0]) * float(item[0][3]))
            total_price += float(total)
            p = f'{item[0][3]}'.ljust(width2 - len(total), ' ') + total
            msg = f'{item[0][2]}( X {item[1][0]})'.ljust(width1 - len(p), ' ')
            msg += total
            items.append(msg)

        total_price = str(total_price)
        items.append('\nTOTAL'.ljust(width1-len(total_price), ' ')+total_price)
        items = '\n'.join(items) 
        print(items)
        return items
    
    def sales_data(self, obj, data):

        if data == 'da_te':
            self.win_man.switch_to(self.screens[9])
            self.sales_date_item_list_builder(obj)

        else:
            self.win_man.switch_to(self.screens[9])
            self.sales_item_list_builder(obj)
            # self.data_dialog_title = 'Item Search'
            # self.search_data = 'Enter Item'
            # title = 'Enter Item Name'

        # self.data_dialog = MDDialog(  # enter date or item to search
        #     title=self.data_dialog_title,
        #     type="custom",
        #     content_cls=DateDialogContents(),
        #     buttons=[
        #         MDFlatButton(
        #             text='CANCEL',
        #             theme_text_color="Custom",
        #             text_color=self.theme_cls.primary_color,
        #             on_release=lambda instance, d=self.date_dialog: self.close_dialog(instance, d)
        #         ),
        #         MDFlatButton(
        #             text='SEARCH',
        #             theme_text_color="Custom",
        #             text_color=self.theme_cls.primary_color,
        #             on_release=lambda obj, d=data: self.sale_results(obj, d)
        #         ),
        #     ]
        # )

        #self.data_dialog.open()

    def sales_date_item_list_builder(self, instance, text='', search=False):
        # fetch all available dates
        self.screens[9].ids['_title'].text = 'Records by Date'
        sales_date_list = off.Sale.search((2, 'da_te', 0))

        def add_sales_date(date_item):
            self.screens[9].ids['_sales_list'].data.append(
                {
                    "viewclass": "CategoryListItem",
                    "text": date_item,
                    "on_release": lambda x='da_te', y=date_item: self.sale_results(instance, x, y)
                }
            )

        self.screens[9].ids['_sales_list'].data = []
        print(sales_date_list)
        for date in sales_date_list:
            date=date[0]
            if search:
                if text in date:
                    add_sales_date(date)
            else:
                add_sales_date(date)

    def sales_item_list_builder(self, instance, text='', search=False):
        # fetch each brand from sales
        self.screens[9].ids['_title'].text = 'Records by Products'
        sales_item_list = off.Sale.search((3, 0, 0))

        def add_sales_item(sales_item):
            self.screens[9].ids['_sales_list'].data.append(
                {
                    "viewclass": "CategoryListItem",
                    "text": sales_item.capitalize(),
                    "on_release": lambda x='brand', y=sales_item : self.sale_results(instance, x, y)
                }
            )

        self.screens[9].ids['_sales_list'].data = []
        print(sales_item_list)
        for cat in sales_item_list:
            print(cat[0])
            if search:
                if text in cat[0]:
                    add_sales_item(cat[0])
            else:
                add_sales_item(cat[0])

    def sales_payment(self, instance, data):
        self.data_dialog2_title = 'Select Payment Method'
        self.data_dialog2 = MDDialog(  
            title=self.data_dialog2_title,
            type="custom",
            content_cls=ConfirmDialog(),
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.data_dialog2.dismiss()
                ),
                MDFlatButton(
                    text='SEARCH',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda i=instance, d=data, q='q': self.sale_results(i, d, q)
                ),
            ]
        )

        # self.data_dialog3 = MDDialog(  # enter date to search
        #     title='',
        #     type="custom",
        #     content_cls=DateDialogContents(),
        #     buttons=[
        #         MDFlatButton(
        #             text='CANCEL',
        #             theme_text_color="Custom",
        #             text_color=self.theme_cls.primary_color,
        #             on_release=lambda instance, d=self.date_dialog: self.close_dialog(instance, d)
        #         ),
        #         MDFlatButton(
        #             text='SEARCH',
        #             theme_text_color="Custom",
        #             text_color=self.theme_cls.primary_color,
        #             on_release=lambda: self.sale_results1()
        #         ),
        #     ]
        # )

        self.data_dialog4 = MDDialog(  # enter date to search
            title=self.data_dialog2_title,
            type="custom",
            content_cls=ConfirmDialog(),
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda instance, d=self.date_dialog: self.close_dialog(instance, d)
                ),
                MDFlatButton(
                    text='SEARCH',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda: self.sale_results1()
                ),
            ]
        )
        self.data_dialog2.open()

    def sale_results(self, instance, data, query):
        self.data_row = []
        if data == 'payment':
            self.data = data
            self.query = self.payment
            self.data_dialog2.dismiss()
            self.screens[5].ids['_back_button'].on_release = lambda x=self.screens[4] : self.win_man.switch_to(x)

        else:
            self.data = data
            self.query = query
            self.screens[5].ids['_back_button'].on_release = lambda x=self.screens[9] : self.win_man.switch_to(x)
        self.screens[5].ids['_sales_item_title'].text = f'{self.query} results'
        self.win_man.switch_to(self.screens[5])
        self.screens[5].ids['_table'].data = []
        
        rows = off.Sale.search((0, self.data, self.query))
        # datatab = MDDataTable(pos_hint={'top': 1, 'x': 0},
        #                       size_hint=(1, 1),
        #                       rows_num=10,
        #                       elevation=0,
        #                       background_color_header=(0.3, 0.3, 1, 1),
        #                       use_pagination=True,
        #                       check=True,
        #                       column_data=[
        #                           ("Item", dp(30)),
        #                           ("Date", dp(25)),
        #                           ("Price", dp(20)),
        #                           ("quantity", dp(15)),
        #                           ("Total", dp(25)),
        #                           ("Profit", dp(20)),
        #                           ("Paid via", dp(20)),
        #                           ("Time", dp(20)),
        #                       ],
        #                       row_data=[]
        #                       )

        # self.screens[5].ids['_table'].add_widget(datatab)

        for index, row in enumerate(rows, start=1):
            table_row = [row[1], row[5], row[2], row[3], row[4], row[8], row[7], row[6]]
            # print(table_row)
            self.screens[5].ids['_table'].data.append(
                {
                    "viewclass": "ThreeLiners",
                    "text": f"{row[1]} ( X {row[3]})",
                    "secondary_text": f"{row[2]} ( total {row[4]})",
                    "tertiary_text": f"{row[5]} at {row[6]}",
                    "on_release": lambda x=row: self.records_on_click(x),
                }
            )
        # datatab.bind(on_check_press=self.sales_check_press)

    #immediate function when a sale record is clicked
    def records_on_click(self, info):
        self.delete_record_dialog = MDDialog( 
            title='Sure to delete this record?',
            type="custom",
            # content_cls=AddCartDialog(),
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.delete_record_dialog.dismiss(d)
                ),
                MDFlatButton(
                    text='Delete',
                    theme_text_color="Error",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda instance, d=info: self.records_delete(info)
                ),
            ],
        )
        self.delete_record_dialog.open()

    #sales record delete function
    def records_delete(self, info):
        self.delete_record_dialog.dismiss()
        self.record_deleted_dialog = MDDialog( 
            title=f'Record deleted successfully?',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.record_deleted_dialog.dismiss(d)
                ),
            ],
        )
        try:
            off.Sale.remove((info[1], info[3], info[6]))
            self.record_deleted_dialog.open()
        except:
            ...
        self.win_man.switch_to(self.screens[4])

    def stock_press(self):
        self.win_man.switch_to(self.screens[6])
        # self.stock_main()

    def stock_main(self, func2, text='', search=False):
        category_list = off.Item.search((3, 0, 0))
        self.screens[1].ids['_cat_list'].clear_widgets()
        self.win_man.switch_to(self.screens[1])

        def add_category_item(category_item):
            cart_button = MDRaisedButton(text=category_item, md_bg_color=(0, 0.6, 0.9, 1), text_color=(0, 0, 0, 1), font_size="27sp", size_hint=(.3, .2), _elevation_raised=2)
            if func2 == 'new_stock_item':
                cart_button.on_release = lambda c=category_item : self.new_item_form(c)
            if func2 == 'stock_item':
                cart_button.on_release = lambda x=category_item.lower(), func3=func2 : self.view_inventory(x, func3)
            if func2 == 'stock':
                cart_button.on_release = lambda x=category_item.lower() : self.update_stock_table(x)
            if func2 == 'view_stock':
                cart_button.on_release = lambda x=category_item.lower() : self.view_stock(x)
            self.screens[1].ids['_cat_list'].add_widget(cart_button)
        
        self.screens[1].ids['_cat_list'].data = []

        if func2 == 'view_stock':
            all_button = MDRaisedButton(text='All Items', md_bg_color=(0, 0.6, 0.9, 1), text_color=(0, 0, 0, 1), font_size="27sp", size_hint=(.3, .2), _elevation_raised=2)
            all_button.on_release = lambda x='all' : self.view_stock(x)
            self.screens[1].ids['_cat_list'].add_widget(all_button)
        # for updating stock item
        elif func2 == 'stock_item':
            all_button = MDRaisedButton(text='All Items', md_bg_color=(0, 0.6, 0.9, 1), text_color=(0, 0, 0, 1), font_size="27sp", size_hint=(.3, .2), _elevation_raised=2)
            all_button.on_release = lambda x='all', func3=func2 : self.view_inventory(x, func3)
            self.screens[1].ids['_cat_list'].add_widget(all_button)
        elif func2 == 'new_stock_item':
            new_button = MDRaisedButton(text='+ New Category', md_bg_color=(0, 0.6, 0.9, 1), text_color=(0, 0, 0, 1), font_size="27sp", size_hint=(.3, .2), _elevation_raised=2)
            new_button.on_release = lambda x='new' : self.new_item_form(x)
            self.screens[1].ids['_cat_list'].add_widget(new_button)
        else:
            all_button = MDRaisedButton(text='All Items', md_bg_color=(0, 0.6, 0.9, 1), text_color=(0, 0, 0, 1), font_size="27sp", size_hint=(.3, .2), _elevation_raised=2)
            all_button.on_release = lambda x='all' : self.update_stock_table(x)
            self.screens[1].ids['_cat_list'].add_widget(all_button)

        for cat in category_list:
            if search:
                if text in cat[0]:
                    add_category_item(cat[0].capitalize())
            else:
                add_category_item(cat[0].capitalize())

    def add_stock(self, instance, text='', search=False):
        category_list = off.Item.search((3, 0, 0))
        self.screens[1].ids['_cat_list'].clear_widgets()
        self.win_man.switch_to(self.screens[1])

        def add_category_item(category_item):
            cart_button = MDRaisedButton(text=category_item, md_bg_color=(0, 0.6, 0.9, 1), text_color=(0, 0, 0, 1), font_size="27sp", size_hint=(.3, .2), _elevation_raised=2)
            cart_button.on_release = lambda x=category_item.lower() : self.update_stock_table(instance, x)
            self.screens[1].ids['_cat_list'].add_widget(cart_button)

        all_button = MDRaisedButton(text='All Items', size_hint=(.3, .2), _elevation_raised=2)
        all_button.on_release = lambda x='all' : self.update_stock_table(x)
        self.screens[1].ids['_cat_list'].add_widget(all_button)

        for cat in category_list:
            if search:
                if text in cat[0]:
                    add_category_item(cat[0].capitalize())
            else:
                add_category_item(cat[0].capitalize())

    def view_stock(self, cat):
        self.win_man.switch_to(self.screens[15])
        row_info = []
        self.screens[15].ids['_fl'].data = []
        items_list = []
        if cat == 'all':
            items_list = off.Item.search((1, ))
        else:
            items_list = off.Item.search((0, 'category', cat))

        # data_tables = MDDataTable(
        #     size_hint=(1, 0.87),
        #     pos_hint={'top': 1,'x': 0},
        #     rows_num=10,
        #     elevation=0,
        #     background_color_header=(0.3, 0.3, 1, 1),
        #     use_pagination=True,
        #     check=True,
        #     column_data=[
        #         ("Category", dp(30)),
        #         ("Item", dp(30)),
        #         ("Price", dp(25)),
        #         ("In stock", dp(20)),
        #         ("Low stock", dp(20)),
        #         ("Buying price", dp(25)),
        #     ],
        #     row_data=[]
        # )
            
        for index, item in enumerate(items_list, start=1):
            print(item)
            self.screens[15].ids['_fl'].data.append(
                {
                    "viewclass": "ThreeLiners",
                    "text": f"{item[2]}",
                    "secondary_text": f"{item[4]} available in stock",
                    "tertiary_text": f"Selling at: {item[3]}",
                    "on_release": lambda x=item: self.items_on_click(x),
                }
            )
        # datatab.bind(on_check_press=self.sales_check_press)

    #immediate function when a items is clicked
    def items_on_click(self, info):
        self.delete_item_dialog = MDDialog( 
            title=f'Sure to delete {info[1].capitalize()} from stock?',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.delete_item_dialog.dismiss(d)
                ),
                MDFlatButton(
                    text='Delete',
                    theme_text_color="Error",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda instance, d=info: self.items_delete(info)
                ),
            ],
        )
        self.delete_item_dialog.open()

    #items delete function
    def items_delete(self, info):
        self.delete_item_dialog.dismiss()
        self.record_deleted_dialog = MDDialog( 
            title=f'Record deleted successfully?',
            type="custom",
            content_cls=AddCartDialog(),
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.record_deleted_dialog.dismiss(d)
                ),
            ],
        )
        try:
            off.Item.remove((info[3], info[2], info[1]))
            self.record_deleted_dialog.open()
        except:
            ...
        self.win_man.switch_to(self.screens[4])

    #bring item delete options
    def stock_check_press(self, instance_table, current_row):
        self.selection_stock.append(current_row)

    #communicates with db to actually delete
    def item_delete_stock(self):
        for selection in self.selection_stock:
            print(selection)
            try:
                off.Item.remove((selection[3], selection[2], selection[1]))
            except:
                break
        self.selection_stock = []
        self.stock_main('view_stock')

    def remove_item(self, specify, info):
        self.item_remove_dialog.dismiss()
        self.removed_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
            title='Product removed',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.removed_dialog.dismiss()
                ),
            ]
        )
        if specify == 'stock':
            print('removing stock')
            # off.Item.remove((self.stock_selected[4], self.stock_selected[0]))
        else:
            print('removing sales')
            # off.Sale.remove((, , ))
        self.removed_dialog.open()

    def clear_records_dialogs(self, table):
        self.items_clear_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
            title=f"This will delete all {table} records?",
            type="custom",
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.item_remove_dialog.dismiss()
                ),
                MDFlatButton(
                    text='CLEAR',
                    theme_text_color="Error",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x=self, d=table : self.clear_records(d)
                ),
            ]
        )
        self.items_clear_dialog.open()

    def clear_records(self, table):
        self.items_clear_dialog.dismiss()
        self.cleared_dialog = MDDialog(  
            title='Records cleared',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.cleared_dialog.dismiss()
                ),
            ]
        )
        if table == 'sales':
            off.Sale.clear_records()
            print('clear sales')
        else:
            off.Item.clear_records()
            print('clear stock')
        self.win_man.switch_to(self.screens[4])
        self.cleared_dialog.open()

    def update_stock_table(self, instance, query):
        self.win_man.switch_to(self.screens[16])
        self.screens[16].ids['_sales_item_title'].text = f'Select items to update'
        self.screens[16].ids['_table'].clear_widgets()
        rows = off.Item.search((0, 'category', query))
        update_items = []
        
        datatab = MDDataTable(pos_hint={'top': 1, 'x': 0},
                              size_hint=(1, 1),
                              rows_num=10,
                              elevation=0,
                              background_color_header=(0.3, 0.3, 1, 1),
                              check=True,
                              column_data=[
                                  ("Item", dp(40)),
                                  ("Price", dp(25)),
                                  ("In Stock", dp(18)),
                                  ("Low value", dp(18)),
                                  ("Buying Price", dp(25)),
                              ],
                              row_data=[]
                              )

        self.screens[16].ids['_table'].add_widget(datatab)
        for row in rows:
            table_row = [row[2], row[3], row[4], row[5], row[6]]
            datatab.row_data.append(table_row)

        def add_update_list(instance, row_data):
            update_items.append(row_data)
            print(update_items)

        # datatab.on_check_press = lambda : add_update_list(instance)

    def item_update(self, info):
        self.update_info = info
        self.win_man.switch_to(self.screens[14])
        self.screens[14].ids['_item_name'].text = f'{info[2]}'
        self.screens[14].ids['_selling_price'].text = f'{info[3]}'
        self.screens[14].ids['_instock'].text = f'{info[4]}'
        self.screens[14].ids['_lowstock'].text = f'{info[5]}'
        self.screens[14].ids['_buying_price'].text = f'{info[6]}'

    def update_item(self):
        # self.item_update_dialog.dismiss()
        # (change_data_brand, change_data_price, change_data_in_stock, change_data_low_val, category, brand)
        # self.u_value = self.input_update_dialog.content_cls.ids['_new_value'].text
        # self.input_update_dialog.dismiss()

        try:
            float(self.screens[14].ids['_selling_price'].text)
            float(self.screens[14].ids['_instock'].text)
            float(self.screens[14].ids['_lowstock'].text)
            float(self.screens[14].ids['_buying_price'].text)
        except:
            return
        
        brand = self.screens[14].ids['_item_name'].text
        price = float(self.screens[14].ids['_selling_price'].text)
        instock = float(self.screens[14].ids['_instock'].text)
        lowstock = float(self.screens[14].ids['_lowstock'].text)
        buying_price = float(self.screens[14].ids['_buying_price'].text)

        off.Item.update_item((brand, price, instock, lowstock, buying_price, self.update_info[1], self.update_info[2]))

        def update_succesful(instance):
            self.updated_dialog.dismiss()
            self.win_man.switch_to(self.screens[6])


        self.updated_dialog = MDDialog(  
            title=f'{brand} updated successfully',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self : update_succesful(d)
                ),
            ]
        )

        self.updated_dialog.open()

    def update_setter(self, col):
        print(col)
        if col == 'Category':
            self.colum = col.lower()
            self.input_update_dialog.content_cls.ids._cat.text_color = [1, 0, 0, 1]
            self.input_update_dialog.content_cls.ids._price.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._name.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._in_st.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._low.text_color = self.theme_cls.primary_color

        elif col == 'Name':
            self.colum = 'brand'
            self.input_update_dialog.content_cls.ids._cat.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._price.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._name.text_color = [1, 0, 0, 1]
            self.input_update_dialog.content_cls.ids._in_st.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._low.text_color = self.theme_cls.primary_color

        elif col == 'Low-value':
            self.colum = 'low_value'
            self.input_update_dialog.content_cls.ids._cat.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._price.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._name.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._in_st.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._low.text_color = [1, 0, 0, 1]

        elif col == 'In-stock':
            self.colum = 'in_stock'
            self.input_update_dialog.content_cls.ids._cat.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._price.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._name.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._in_st.text_color = [1, 0, 0, 1]
            self.input_update_dialog.content_cls.ids._low.text_color = self.theme_cls.primary_color

        else:
            self.colum = 'price'
            self.input_update_dialog.content_cls.ids._cat.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._price.text_color = [1, 0, 0, 1]
            self.input_update_dialog.content_cls.ids._name.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._in_st.text_color = self.theme_cls.primary_color
            self.input_update_dialog.content_cls.ids._low.text_color = self.theme_cls.primary_color

    def expand_stock(self):
        try:
            self.new_category = self.screens[8].ids['_category'].text.lower()
            self.new_item = self.screens[8].ids['_item_name'].text.lower()
            float(self.screens[8].ids['_price'].text)
            float(self.screens[8].ids['_instock'].text)
            float(self.screens[8].ids['_lowstock'].text)
            float(self.screens[8].ids['_buying_price'].text)
        except:
            return

        self.new_category = self.screens[8].ids['_category'].text
        self.new_item = self.screens[8].ids['_item_name'].text
        self.new_price = self.screens[8].ids['_price'].text
        self.new_instock = self.screens[8].ids['_instock'].text
        self.new_low_value = self.screens[8].ids['_lowstock'].text
        self.new_buying_price = self.screens[8].ids['_buying_price'].text
        self.add_invent_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
            title=f'Confirm {self.new_item} at {self.new_price} to {self.new_category}',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.add_invent_dialog.dismiss()
                ),
                MDFlatButton(
                    text='ADD',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.add_to_inventory
                ),
            ]
        )
        self.add_invent_dialog.open()

    def new_item_form(self, cat):
        self.win_man.switch_to(self.screens[8])
        if cat != 'new':
            self.screens[8].ids['_category'].text = cat

    def add_to_inventory(self, obj):
        self.add_invent_dialog.dismiss()

        def add_successful(instance):
            self.added_dialog.dismiss()
            self.win_man.switch_to(self.screens[6])

        self.added_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
            title=f'{self.new_item.capitalize()} added successfully',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: add_successful(d)
                ),
            ]
        )
        off.Item(self.new_category.lower(), self.new_item.lower(), float(self.new_price), int(self.new_instock),
                 int(self.new_low_value), float(self.new_buying_price))
        self.added_dialog.open()

    def change_screen(self, screen):
        # function for switching screen views using window manager
        #  self.win_man.remove_widget(self.win_man.current_screen)
        self.win_man.switch_to(screen)

    def close_dialog(self, obj, dialog):
        dialog.dismiss()

    def payment_setter(self, c):

        # function to set payment mode via dialog and change button color

        if c == 'mpesa':
            if self.sell_dialog is not None:
                self.sell_dialog.content_cls.ids['_mpesa_button'].text_color = [1, 0, 0, 1]
                self.sell_dialog.content_cls.ids['_cash_button'].text_color = self.theme_cls.primary_color
                self.sell_dialog.content_cls.ids['_other_button'].text_color = self.theme_cls.primary_color

            if self.sell_dialog2 is not None:
                self.sell_dialog2.content_cls.ids['_mpesa_button'].text_color = [1, 0, 0, 1]
                self.sell_dialog2.content_cls.ids['_cash_button'].text_color = self.theme_cls.primary_color
                self.sell_dialog2.content_cls.ids['_other_button'].text_color = self.theme_cls.primary_color

            if self.data_dialog2 is not None:
                self.data_dialog2.content_cls.ids['_mpesa_button'].text_color = [1, 0, 0, 1]
                self.data_dialog2.content_cls.ids['_cash_button'].text_color = self.theme_cls.primary_color
                self.data_dialog2.content_cls.ids['_other_button'].text_color = self.theme_cls.primary_color

        elif c == 'cash':
            if self.sell_dialog is not None:
                self.sell_dialog.content_cls.ids['_cash_button'].text_color = [1, 0, 0, 1]
                self.sell_dialog.content_cls.ids['_mpesa_button'].text_color = self.theme_cls.primary_color
                self.sell_dialog.content_cls.ids['_other_button'].text_color = self.theme_cls.primary_color

            if self.sell_dialog2 is not None:
                self.sell_dialog2.content_cls.ids['_cash_button'].text_color = [1, 0, 0, 1]
                self.sell_dialog2.content_cls.ids['_mpesa_button'].text_color = self.theme_cls.primary_color
                self.sell_dialog2.content_cls.ids['_other_button'].text_color = self.theme_cls.primary_color

            if self.data_dialog2 is not None:
                self.data_dialog2.content_cls.ids['_cash_button'].text_color = [1, 0, 0, 1]
                self.data_dialog2.content_cls.ids['_mpesa_button'].text_color = self.theme_cls.primary_color
                self.data_dialog2.content_cls.ids['_other_button'].text_color = self.theme_cls.primary_color
        else:
            if self.sell_dialog is not None:
                self.sell_dialog.content_cls.ids['_other_button'].text_color = [1, 0, 0, 1]
                self.sell_dialog.content_cls.ids['_cash_button'].text_color = self.theme_cls.primary_color
                self.sell_dialog.content_cls.ids['_mpesa_button'].text_color = self.theme_cls.primary_color

            if self.sell_dialog2 is not None:
                self.sell_dialog2.content_cls.ids['_other_button'].text_color = [1, 0, 0, 1]
                self.sell_dialog2.content_cls.ids['_cash_button'].text_color = self.theme_cls.primary_color
                self.sell_dialog2.content_cls.ids['_mpesa_button'].text_color = self.theme_cls.primary_color

            if self.data_dialog2 is not None:
                self.data_dialog2.content_cls.ids['_other_button'].text_color = [1, 0, 0, 1]
                self.data_dialog2.content_cls.ids['_cash_button'].text_color = self.theme_cls.primary_color
                self.data_dialog2.content_cls.ids['_mpesa_button'].text_color = self.theme_cls.primary_color

        self.payment = c

    def details_account(self):

        self.biz_id = self.screens[11].ids['_biz_id'].text
        self.user_name = self.screens[11].ids['_user_name'].text
        self.phone_no = self.screens[11].ids['_phone_no'].text
        self.email = self.screens[11].ids['_email'].text
        self.password = self.screens[11].ids['_password'].text
        self.con_password = self.screens[11].ids['_con_password'].text

        details = [self.biz_id, self.user_name, self.phone_no, self.phone_no, self.email, self.password,
                   self.con_password]

        empty_fields = []

        for j in details:
            if j == '':
                empty_fields.append(j)

            else:
                pass

        if len(empty_fields) > 0:
            self.all_fields_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
                title='Fill all fields',
                type="custom",
                buttons=[
                    MDFlatButton(
                        text='OK',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda d=self: self.all_fields_dialog.dismiss()
                    )
                ]
            )

            self.all_fields_dialog.open()

        elif self.password != self.con_password:

            self.pass_match_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
                title="Passwords don't match",
                type="custom",
                buttons=[
                    MDFlatButton(
                        text='Retype',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda d=self: self.pass_match_dialog.dismiss()
                    )
                ]
            )

            self.pass_match_dialog.open()

        else:
            self.create_account_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
                title=f'{self.user_name} Create account for {self.biz_id}',
                type="custom",
                buttons=[
                    MDFlatButton(
                        text='CANCEL',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda d=self: self.create_account_dialog.dismiss()
                    ),
                    MDFlatButton(
                        text='CREATE',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda instance: self.create_account(instance)
                    ),
                ]
            )
            self.create_account_dialog.open()

    def create_account(self, instance_table):
        self.create_account_dialog.dismiss()
        off.User(self.biz_id, self.user_name, self.phone_no, self.email, self.password)
        self.account_created_dialog = MDDialog(  # select payment method and confirm transaction o direct sales
            title=f'Account created successfully',
            type="custom",
            buttons=[
                MDFlatButton(
                    text='OK',
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda d=self: self.account_created_dialog.dismiss()
                )]
        )
        self.account_created_dialog.open()

        self.win_man.switch_to(self.screens[0])


if __name__ == "__main__":
    OhalApp().run()
