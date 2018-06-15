import copy

PRODUCTS_DATA = [['CH1', 'Chai', 3.11],
                 ['AP1', 'Apples', 6.00],
                 ['CF1', 'Coffee', 11.23],
                 ['MK1', 'Milk', 4.75],
                 ['OM1', 'Oatmeal', 3.69]]


class Products:
    def __init__(self):
        self.products = {}
        self.init_products()

    def add_product(self, product_code, name, price):
        self.products[product_code] = Product(product_code, name, price)

    def get_product_by_product_code(self, product_code):
        product_code = product_code.upper()
        return self.products[product_code] if product_code in self.products else None

    def init_products(self):
        for product in PRODUCTS_DATA:
            self.add_product(*product)


class Product:
    def __init__(self, product_code, name, price):
        self.product_code = product_code
        self.name = name
        self.price = price


class Discount:
    def __init__(self, discount_code, limit, trigger_product, action_product, count=0):
        self.discount_code = discount_code
        self.limit = limit
        self.trigger_product = trigger_product
        self.action_product = action_product
        self.count = count


class DiscountMeta:
    def __init__(self, name='Discount', discount_price=0):
        self.name = name
        self.discount_price = discount_price


class BuyOneGetOneFreeDiscount(Discount):
    def __init__(self, discount_code, limit, trigger_product, action_product, count=0):
        Discount.__init__(self, discount_code, limit, trigger_product, action_product, count)

    def apply_discount(self, trigger_product_qty, action_product_qty, price):
        discount = 0.0
        if self.count % 2:
            discount = -price
        self.count += 1
        return DiscountMeta(self.discount_code, discount) if discount < 0 else None


class BulkApplesDiscount(Discount):
    def __init__(self, discount_code, limit, trigger_product, action_product, count=0):
        Discount.__init__(self, discount_code, limit, trigger_product, action_product, count)

    def apply_discount(self, trigger_product_qty, action_product_qty, price):
        discount = 0.0
        if trigger_product_qty >= 3:
            discount = 4.50 - price
        return DiscountMeta(self.discount_code, discount) if discount < 0 else None


class BuyChaiGetFreeMilkDiscount(Discount):
    def __init__(self, discount_code, limit, trigger_product, action_product, count=0):
        Discount.__init__(self, discount_code, limit, trigger_product, action_product, count)

    def apply_discount(self, trigger_product_qty, action_product_qty, price):
        discount = 0.0
        if trigger_product_qty >= 1 and action_product_qty >= 1:
            self.count += 1
            discount = -price
        return DiscountMeta(self.discount_code, discount) if discount < 0 else None


class BuyOatmealGetApplesDiscount(Discount):
    def __init__(self, discount_code, limit, trigger_product, action_product, count=0):
        Discount.__init__(self, discount_code, limit, trigger_product, action_product, count)

    def apply_discount(self, trigger_product_qty, action_product_qty, price):
        discount = 0.0
        if (trigger_product_qty > self.count) and (action_product_qty > self.count):
            self.count += 1
            discount = -(price * 0.5)
        return DiscountMeta(self.discount_code, discount) if discount < 0 else None


class CartItem:
    def __init__(self, product_code, name, price, discount_meta=[]):
        self.product_code = product_code
        self.name = name
        self.price = price
        self.discount_meta = discount_meta


class Cart:
    def __init__(self):
        self.cart = []
        self.total_item_qty = {}
        self.discounts = []
        self.init_discounts()

    def add_item(self, cart_item):
        self.cart.append(copy.deepcopy(cart_item))
        if cart_item.product_code in self.total_item_qty:
            self.total_item_qty[cart_item.product_code] += 1
        else:
            self.total_item_qty[cart_item.product_code] = 1

    def calculate_discounts(self):
        for discount in self.discounts:
            for cart_item in self.cart:
                if discount.action_product == cart_item.product_code and \
                        (discount.limit == 0 or discount.count < discount.limit) and \
                        discount.trigger_product in self.total_item_qty and \
                        discount.action_product in self.total_item_qty:
                    # Update price for stacked discounts
                    price = cart_item.price
                    for applied_discount in cart_item.discount_meta:
                        price += applied_discount.discount_price

                    discount_meta = discount.apply_discount(self.total_item_qty[discount.trigger_product],
                                                            self.total_item_qty[discount.action_product],
                                                            price)
                    if discount_meta is not None:
                        cart_item.discount_meta.append(discount_meta)

    def display(self):
        self.calculate_discounts()
        # Display header
        cart_display = ('{:<18}{:>17}\n{:<18}{:>17}\n'.format('Item', 'Price', '----', '-----'))
        cart_total: float = 0.0
        if not self.cart:
            cart_display += '{:*^35}\n'.format(' EMPTY CART ')
        for cart_item in self.cart:
            # Display cart item
            cart_display += ('{:<18}{:17.2f}\n'.format(cart_item.product_code, cart_item.price))
            cart_total += cart_item.price
            for discount_meta in cart_item.discount_meta:
                # Display applied discounts
                cart_display += ('{: >12}{:<6}{:17.2f}\n'.format('', discount_meta.name,
                                                                 discount_meta.discount_price))
                cart_total += discount_meta.discount_price
        cart_total = round(cart_total, 2)
        cart_display += ('{:->36}{:>35.2f}\n\n'.format('\n', cart_total))
        return cart_display, cart_total

    def add_to_cart(self, product_code):
        item = products.get_product_by_product_code(product_code)
        if item is not None:
            self.add_item(CartItem(item.product_code, item.name, item.price))

    def add_multiple_products_to_cart(self, product_codes):
        for product_code in product_codes:
            self.add_to_cart(product_code)

    def init_discounts(self):
        self.discounts.append(BuyOneGetOneFreeDiscount('BOGO', 0, 'CF1', 'CF1'))
        self.discounts.append(BulkApplesDiscount('APPL', 0, 'AP1', 'AP1'))
        self.discounts.append(BuyChaiGetFreeMilkDiscount('CHMK', 1, 'CH1', 'MK1'))
        self.discounts.append(BuyOatmealGetApplesDiscount('APOM', 0, 'OM1', 'AP1'))


class App:
    def __init__(self):
        self.cart = Cart()
        self.menu_items = ['1. Add to Cart',
                           '2. Display Cart',
                           '3. Exit']
        self.menu_options = {1: self.add_to_cart,
                             2: self.display_cart,
                             3: self.exit_app}
        self.menu_loop()

    def menu_input(self):
        # Display menu items and input selection
        [print(m) for m in self.menu_items]
        return input('Please select a menu item: ')

    def menu_loop(self):
        while True:
            # Loop until user exits
            menu_item = self.menu_input()
            # Get menu item number or loop back around
            try:
                menu_item = int(menu_item)
            except ValueError:
                pass
            # Exit
            if menu_item == len(self.menu_items):
                break
            # Valid menu item
            if menu_item in range(1, len(self.menu_items)):
                self.menu_options[menu_item]()

    def display_products(self):
        # Display available products
        border = '+{:-^14}|{:-^14}|{:-^9}+'.format('', '', '')
        header = '|{: ^14}|{: ^14}|{: ^9}|'.format('Product Code', 'Name', 'Price')
        print('{}\n{}\n{}'.format(border, header, border))
        [print('|{: ^14}|   {: <11}|{: >7}  |'.format(*product)) for product in PRODUCTS_DATA]
        print(border)

    def add_to_cart(self):
        self.display_products()
        # Input product code(s)
        print('Enter one or more product codes (comma separated)')
        product_codes = input('Product code(s): ')
        # Add product(s) to cart
        self.cart.add_multiple_products_to_cart([product_code.strip() for product_code in product_codes.split(',')])

    def display_cart(self):
        print(self.cart.display()[0])

    def exit_app(self): return None


products = Products()
