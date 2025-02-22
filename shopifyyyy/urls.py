from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('home',views.home,name="home"),
    path('categories',views.categories,name="category"),
    path('productdetails/<str:name>',views.productdetails,name="productdetails"),
    path('single_productdetails/<str:cname>/<str:spname>',views.single_productdetails,name="single_productdetails"),
    path('negotiate/<str:product_name>/', views.negotiate, name='negotiate'),
    path('register',views.register,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path("blog", views.blog, name="blog"),
    path("about", views.about, name="about"),
    path('search/', views.search_view, name='search_view'),
    path('logout/', views.logout, name='logout'),
    path('fav/', views.fav_page, name='fav'),
    path('favviewpage/', views.fav_view_page, name='favviewpage'),
        path('remove_fav/<str:cid>', views.remove_fav, name='remove_fav'),
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('cart', views.cart_page, name='cart'),
    path('remove_cart/<str:cid>', views.remove_cart, name='remove_cart'),




]
