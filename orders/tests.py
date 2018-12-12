from django.test import TestCase, Client
from django.db.models import Max

from .models import Category, Item, CartItem, OrderItem, Order, User

# pylint: disable=no-member

# Create your tests here.
class OrdersTestCase(TestCase):
    
    def setUp(self):

        # Create users.
        user_1 = User.objects.create(username='User_1', password='passw0rd')
        user_2 = User.objects.create(username='User_2', password='passw0rd')

        # Create items.
        pizza = Category.objects.create(name='Pizza')
        topping = Category.objects.create(name='Topping')
        item_1 = Item.objects.create(category=pizza, name='Item_1', price=10000)
        item_2 = Item.objects.create(category=pizza, name='Item_2', price=0)
        item_3 = Item.objects.create(category=pizza, name='Item_3', price=-10000)
        Item.objects.create(category=topping, name='topping_1')

        # Create cartitems.
        CartItem.objects.create(user=user_1, item=item_1, quantity=1, price=item_1.price)
        CartItem.objects.create(user=user_1, item=item_2, quantity=1, price=item_2.price)
        CartItem.objects.create(user=user_1, item=item_3, quantity=1, price=item_3.price)

        # Create orderitems
        orderitem_1 = OrderItem.objects.create(user=user_2, item=item_1, quantity=1, price=item_1.price)
        orderitem_2 = OrderItem.objects.create(user=user_2, item=item_2, quantity=1, price=item_2.price)
        OrderItem.objects.create(user=user_2, item=item_3, quantity=1, price=item_3.price)

        # Create an order
        order_1 = Order.objects.create(
            user = user_2,
            contact = '0l0',
            billing_address = 'somewhere',
            shipping_address = 'anywhere',
            subtotal = orderitem_1.price + orderitem_2.price
        )
        order_1.items.add(orderitem_1)
        order_1.items.add(orderitem_2)

    ### Database-side tests
    # Test item.
    def test_valid_item(self):
        item_1 = Item.objects.get(name='Item_1')
        self.assertTrue(item_1.is_valid_item())

    def test_invalid_item(self):
        item_3 = Item.objects.get(name='Item_3')
        self.assertFalse(item_3.is_valid_item())

    # Test cart_item.
    def test_valid_cartitem(self):
        item_1 = Item.objects.get(name='Item_1')
        cartitem_1 = CartItem.objects.get(item=item_1)
        self.assertTrue(cartitem_1.is_valid_cartitem())

    def test_invalid_cartitem(self):
        item_2 = Item.objects.get(name='Item_2')
        cartitem_2 = CartItem.objects.get(item=item_2)
        self.assertFalse(cartitem_2.is_valid_cartitem())

    def test_cartitem_count(self):
        user_1 = User.objects.get(username='User_1')
        self.assertEqual(user_1.cart.count(), 3)

    # Test order_item.
    def test_valid_orderitem(self):
        item_1 = Item.objects.get(name='Item_1')
        orderitem_1 = OrderItem.objects.get(item=item_1)
        self.assertTrue(orderitem_1.is_valid_orderitem())

    def test_invalid_orderitem(self):
        item_2 = Item.objects.get(name='Item_2')
        orderitem_2 = OrderItem.objects.get(item=item_2)
        self.assertFalse(orderitem_2.is_valid_orderitem())
    
    # Test order.
    def test_valid_order(self):
        user_2 = User.objects.get(username='User_2')
        order = Order.objects.get(user=user_2)
        self.assertTrue(order.is_valid_order())

    def test_invalid_order(self):
        user_2 = User.objects.get(username='User_2')
        orderitem_2 = OrderItem.objects.get(price=0)
        orderitem_3 = OrderItem.objects.get(price=-10000)
        order = Order.objects.create(
            user = user_2,
            contact = '010',
            billing_address = 'somewhere',
            shipping_address = 'anywhere',
            subtotal = orderitem_2.price + orderitem_2.price
        )
        order.items.add(orderitem_2)
        order.items.add(orderitem_3)
        self.assertFalse(order.is_valid_order()) # subtotal is -10000

    def test_order_subtotal(self):
        user_2 = User.objects.get(username='User_2')
        item_1 = Item.objects.get(name='Item_1')
        item_2 = Item.objects.get(name='Item_2')
        order = Order.objects.get(user=user_2)
        self.assertEqual(order.subtotal, item_1.price + item_2.price)

    def test_order_count(self):
        user_2 = User.objects.get(username='User_2')
        order = Order.objects.get(user=user_2)
        self.assertEqual(order.items.count(), 2)

    ### View-side tests
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 302)

    def test_valid_item_page(self):
        item_1 = Item.objects.get(name='Item_1')
        c = Client()
        response = c.get(f"/item/{item_1.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_item_page(self):
        max_id = Item.objects.all().aggregate(Max("id"))["id__max"]
        c = Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)