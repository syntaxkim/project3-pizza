# Project 3 - Pizza (Django)

한국어: [README_KOR.md](https://github.com/syntaxkim/project3-pizza/blob/master/README_KOR.md)

A web application for handling a pizza restaurant's online orders. Users can browse the retaurant's menu, add items to their cart, and submit their orders. They also can post reviews with photos. Meanwhile, the restaurant owners can view orders that havve been placed and update order status as needed.

![menu](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/menu.png?raw=true)
* The menu model comes from [Pinocchio's Pizza & Subs](http://www.pinocchiospizza.net/menu.html) located in Cambridge, MA.


## Problems to consider
* How should you represent the different prices for large and small versions of the same dish?
* Where do toppings fit into your model for pizzas?
* How do you calculate the ultimate price of a pizza?
* How will you make the custom add-ons for the subs work?


## Model diagram
![model_diagram](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/model_diagram.png?raw=true)


## Features

### User authentication
User registration is required in order to use web features.


### Add items into user's cart
Different options are displayed for particular items.
![item_pizza](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/item_pizza.png?raw=true)
![item_sub](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/item_sub.png?raw=true)
![cartitem_list](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/cartitem_list.png?raw=true)


### Order items
Users are asked to submit particular information for orders.
![order](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/order.png?raw=true)
![order_detail](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/order_detail.png?raw=true)


### Manage orders
Restaurant managers(admin users) can view today's recently placed orders and update the status accordingly.
![manage_order_list](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/manage_order_list.png?raw=true)


### Post reviews
Users can post reviews with their own photos.
![review_list](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/review_list.png?raw=true)
![review_detail](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/review_detail.png?raw=true)


### Basic test-cases included
[orders/tests.py](https://github.com/syntaxkim/project3-pizza/blob/master/orders/tests.py)
[reviews/tests.py](https://github.com/syntaxkim/project3-pizza/blob/master/reviews/tests.py)


## Languages and Tools
* Languages: Python 3.7, JavaScript ES6
* Frameworks and Libraries: Django 2.1, Bootstrap, jQuery
