import unittest
from app import Cart
from test_data import TestData


class TestCartDiscounts(unittest.TestCase):
    def test_chai_apples(self):
        test_chai_apples_cart = Cart()
        test_chai_apples_cart.add_multiple_products_to_cart(['CH1', 'AP1'])
        total = test_chai_apples_cart.display()[1]
        self.assertEqual(total, 9.11)

    def test_chai_apples_milk(self):
        test_chai_apples_milk_cart = Cart()
        test_chai_apples_milk_cart.add_multiple_products_to_cart(['CH1', 'AP1', 'AP1', 'AP1', 'MK1'])
        total = test_chai_apples_milk_cart.display()[1]
        self.assertEqual(total, 16.61)

    def test_chai_apples_coffee_milk(self):
        test_chai_apples_coffee_milk_cart = Cart()
        test_chai_apples_coffee_milk_cart.add_multiple_products_to_cart(['CH1', 'AP1', 'CF1', 'MK1'])
        total = test_chai_apples_coffee_milk_cart.display()[1]
        self.assertEqual(total, 20.34)

    def test_milk_apples(self):
        test_milk_apples_cart = Cart()
        test_milk_apples_cart.add_multiple_products_to_cart(['MK1', 'AP1'])
        total = test_milk_apples_cart.display()[1]
        self.assertEqual(total, 10.75)

    def test_coffee(self):
        test_coffee_cart = Cart()
        test_coffee_cart.add_multiple_products_to_cart(['CF1', 'CF1'])
        total = test_coffee_cart.display()[1]
        self.assertEqual(total, 11.23)

    def test_apples_chai(self):
        test_apples_chai_cart = Cart()
        test_apples_chai_cart.add_multiple_products_to_cart(['AP1', 'AP1', 'CH1', 'AP1'])
        total = test_apples_chai_cart.display()[1]
        self.assertEqual(total, 16.61)

    def test_free_with_limits(self):
        test_free_with_limits_cart = Cart()
        test_free_with_limits_cart.add_multiple_products_to_cart(['CH1', 'MK1', 'CH1', 'MK1'])
        total = test_free_with_limits_cart.display()[1]
        self.assertEqual(total, 10.97)

    def test_oatmeal_apples(self):
        test_oatmeal_apples_cart = Cart()
        test_oatmeal_apples_cart.add_multiple_products_to_cart(['OM1', 'AP1', 'AP1', 'AP1'])
        total = test_oatmeal_apples_cart.display()[1]
        self.assertEqual(total, 14.94)

    def test_big_cart(self):
        test_big_cart_cart = Cart()
        test_big_cart_cart.add_multiple_products_to_cart(TestData.random_items_10k)
        total = test_big_cart_cart.display()[1]
        self.assertEqual(total, 38867.35)


if __name__ == '__main__':
    unittest.main()