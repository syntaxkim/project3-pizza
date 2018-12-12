# Project 3 - Pizza (Django)

한국어: [README_KOR.md](https://github.com/syntaxkim/project3-pizza/blob/master/README_KOR.md)

A web application for handling a pizza restaurant's online orders. Users can browse the retaurant's menu, add items to their cart, and submit their orders. They also can post reviews with photos. Meanwhile, the restaurant owners can view orders that havve been placed and update order status as needed.

![menu]()
* The menu model comes from an actual [pizza restaurant menu](http://www.pinocchiospizza.net/menu.html) located in Cambridge, MA.


## Problems to consider
* How should you represent the different prices for large and small versions of the same dish?
* Where do toppings fit into your model for pizzas?
* How do you calculate the ultimate price of a pizza?
* How will you make the custom add-ons for the subs work?


## Model diagram
![model_diagram]()


## Features

### User authentication
User registration is required in order to use web features.


### Add items into user's cart
Different options are displayed for particular items.
![item_pizza]()
![item_sub]()
![cartitem_list]()


### Order items
Users are asked to submit particular information for orders.
![order]()
![order_detail]()


### Manage orders
Restaurant managers(admin users) can view today's recently placed orders and update the status accordingly.
![manage_order_list]()


### Post reviews
Users can post reviews with their own photos.
![review_list]()
![review_detail]()


### Basic test-cases included
[orders/tests.py]()
[reviews/tests.py]()


## Languages and Tools
* Languages: Python 3.7, JavaScript ES6
* Frameworks and Libraries: Django 2.1, Bootstrap, jQuery
