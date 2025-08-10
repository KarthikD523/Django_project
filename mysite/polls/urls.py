from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/register/", views.registerView, name="register"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("home/", views.Product_home, name="home"),
    path("protected/", views.ProtectedView.as_view(), name="protected"),


    path("products/",views.view_products, name="products"),
    path("cart/", views.view_cart, name="cart"),

    path("product_description/<int:product_id>/", views.view_product_description, name="product_description"),
    path("addtocart/<int:product_id>/",views.add_to_cart,name="add_to_cart"),

    path("add_product/",views.add_product,name='add_product'),
     path("my_products/",views.my_products,name='my_products')
    
]