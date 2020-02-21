from django.urls import path

from .views import ContactView, IndexView, MenuView, SignInView, SignUpView, logout, ItemView
from .views import ShoppingCartView, OrderView


urlpatterns = [
    path("", IndexView.as_view()),
    path("contact", ContactView.as_view(), name="contact"),
    path("menu", MenuView.as_view(), name="menu"),
    path("menu/<int:pk>/item", ItemView.as_view(), name="item"),
    path("shoppingcart", ShoppingCartView.as_view(), name="shoppingcart"),
    path("order", OrderView.as_view(), name="order"),
    path("login", SignInView.as_view(), name="login"),
    path("logout", logout, name="logout"),
    path("signup", SignUpView.as_view(), name="signup")
]

