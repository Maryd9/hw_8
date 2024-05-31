"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from tests.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_2():
    return Product("apple", 34, "This is a apple", 400)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(quantity=800) is True

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(quantity=20)
        assert product.quantity == 980

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError, match="Нет нужного количества"):
            product.buy(quantity=150000)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product_2):
        cart.add_product(product_2, buy_count=4)
        assert cart.products[product_2] == 4

    def test_add_same_product(self, cart, product):
        cart.add_product(product, 15)
        cart.add_product(product, 15)
        assert cart.products[product] == 30

    def test_add_same_product_no_buycount(self, cart, product):
        cart.add_product(product)
        assert cart.products[product] == 1

    def test_remove_product(self, cart, product):
        cart.add_product(product, 15)
        cart.remove_product(product=product, remove_count=2)
        assert cart.products[product] == 13

    def test_remove_product_no_removecount(self, cart, product, product_2):
        cart.add_product(product, 15)
        cart.add_product(product_2, 2)
        cart.remove_product(product=product)
        assert len(cart.products) == 1 and product_2 in cart.products and cart.products[product_2] == 2

    def test_remove_product_big_removecount(self, cart, product):
        cart.add_product(product, 15)
        cart.remove_product(product=product, remove_count=20000)
        assert not len(cart.products)

    def test_clear(self, cart, product, product_2):
        cart.add_product(product, 15)
        cart.add_product(product_2, 21)
        cart.clear()
        assert not len(cart.products)

    def test_total_price(self, cart, product, product_2):
        cart.add_product(product, 15)  # price = 100
        cart.add_product(product_2, 21)  # price = 34
        assert cart.get_total_price() == 2214

    def test_buy(self, cart, product):
        cart.add_product(product, 3)
        cart.buy()
        assert product.quantity == 997

    def test_buy_more_than_available(self, cart, product):
        cart.add_product(product, 2000)
        with pytest.raises(ValueError, match="Нет нужного количества"):
            cart.buy()
