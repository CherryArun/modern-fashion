from django.urls import path
from . import views

urlpatterns = [
	path('', views.home,name="home"),
	path('product_list/', views.product_list,name="product_list"),
	path('login/', views.user_login,name="user_login"),
	path('register/', views.register,name="register"),
	path('dashboard/', views.dashboard,name="dashboard"),
	path('logout/', views.logout,name="logout"),
	path('add_to_cart/<int:pk>/', views.add_to_cart,name="add_to_cart"),
	path('view_items_cart_product/',views.view_items_cart_product,name="view_items_cart_product"),
	path('remove_item/<int:pk>/',views.remove_item,name="remove_item"),
	path('purchase/',views.purchase,name="purchase"),
	path('purchased_item/<str:pk>/<str:status>/',views.purchased_item,name="purchased_item"),
	path('order_item_user/',views.order_item_user,name="order_item_user"),
	path('try_now/',views.try_now,name="try_now"),
	path('all_category/',views.all_category,name="all_category"),
	path('category_list/<int:pk>/',views.category_list,name="category_list"),
]
