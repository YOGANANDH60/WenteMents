from django.urls import path
from . import views


urlpatterns = [
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
]
