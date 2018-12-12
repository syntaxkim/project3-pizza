# Project 3 - Pizza (Django)

English: [README.md](https://github.com/syntaxkim/project3-pizza/blob/master/README.md)

온라인 피자 주문 및 주문관리 웹 앱입니다. 메뉴를 통해 카트에 담은 뒤 주문을 할 수 있으며, 사진 업로드와 후기 작성을 수 있습니다. 관리자는 관리 페이지에서 주문을 확인하고 상태를 갱신할 수 있습니다.

![menu](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/menu.png?raw=true)
* The menu model comes from an actual [pizza restaurant menu](http://www.pinocchiospizza.net/menu.html) located in Cambridge, MA.


## 문제해결 고려사항
* 같은 항목의 서로 다른 크기와 가격을 어떻게 구현할 것인가?
* 피자의 토핑은 어떻게 구현할 것인가?
* 최종 주문 금액을 어떻게 합산할 것인가?
* 서브메뉴의 추가 옵션은 어떻게 만들 것인가?


## 모델 다이어그램
![model_diagram](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/model_diagram.png?raw=true)


## 기능

### 유저 인증
웹 기능들을 사용하기 위해서는 가입과 로그인이 필요합니다.


### 장바구니
품목별로 다른 옵션을 선택할 수 있습니다.
![item_pizza](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/item_pizza.png?raw=true)
![item_sub](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/item_sub.png?raw=true)
![cartitem_list](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/cartitem_list.png?raw=true)


### 주문
주문 시 특정 정보를 입력해야 합니다. (form validation 필요)
![order](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/order.png?raw=true)
![order_detail](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/order_detail.png?raw=true)


### 주문 관리
관리자만 당일 주문을 확인할 수 있으며, 진행 상황에 따라 주문 상태를 갱신할 수 있습니다.
![manage_order_list](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/manage_order_list.png?raw=true)


### 후기 작성
후기 작성 시 사진 업로드가 가능합니다.
![review_list](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/review_list.png?raw=true)
![review_detail](https://github.com/syntaxkim/project3-pizza/blob/master/screenshots/review_detail.png?raw=true)


### Basic test-cases included
[orders/tests.py](https://github.com/syntaxkim/project3-pizza/blob/master/orders/tests.py)
[reviews/tests.py](https://github.com/syntaxkim/project3-pizza/blob/master/reviews/tests.py)


## Languages and Tools
* Languages: Python 3.7, JavaScript ES6
* Frameworks and Libraries: Django 2.1, Bootstrap, jQuery
