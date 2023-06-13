from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.Home,name='home-page'),
    path('products/',views.Products,name='products-page'),
    path('products/<int:id>',views.Categories,name='categories-page'),
    path('about/',views.About,name='about-page'),
    path('orders/',views.Orders_list,name='orders-page'),
    path('orders/details/<int:order_id>/',views.Order_details_request,name='orders-details-page'),
    path('login/',views.Login_request,name='login-page'),
    path('register/',views.Register_request,name='register-page'),
    path('logout/',views.Logout_req,name='logout-page'),
    path('piece/<int:pk>',views.Piece,name='piece-page'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart_anonymous/<int:product_id>/', views.add_to_cart_anonymous, name='add_to_cart_anonymous'),
    path('order_creation/<int:cart_id>/',views.order_creation,name='order_creation'),
    path('cart',views.Cart_page,name='cart-page'),
    path('cart_deleting/<int:product_id>',views.item_remove,name='cart-item-remove'),
    path('cancel-order/<int:order_id>/',views.order_cancel,name='order_cancel-mth')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)